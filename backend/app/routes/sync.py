import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.sync_log import SyncLog
from app.config import get_settings
from app.schemas.sync import SyncUploadRequest, SyncStatusResponse
from app.security.deps import get_current_user
from app.services.encryption_service import encrypt, decrypt, ciphertext_sha256
from app.services.drive_sync_service import upload_backup, list_backups, download_backup
from app.utils.files import temporary_copy

router = APIRouter(prefix="/sync", tags=["sync"])

DEVICE_ID_HEADER = "X-Device-ID"


def _device_id() -> str:
    return str(uuid.uuid4())


@router.get("/status", response_model=dict)
def sync_status(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    last = session.exec(
        select(SyncLog).where(SyncLog.user_id == current_user.id, SyncLog.status == "success").order_by(SyncLog.timestamp.desc()).limit(1)
    ).first()
    backups = list_backups(get_settings().astra_sync_folder_name)
    return {"success": True, "data": {"last_sync": last.timestamp.isoformat() if last else None, "device_id": _device_id(), "backup_count": len(backups), "drive_connected": bool(get_settings().astra_google_client_id)}}


@router.get("/oauth/start", response_model=dict)
def oauth_start():
    settings = get_settings()
    if not settings.astra_google_client_id:
        return {"success": True, "data": {"auth_url": None, "message": "Drive not configured"}}
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.astra_google_client_id}&redirect_uri={settings.astra_google_redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/drive.file"
    return {"success": True, "data": {"auth_url": auth_url}}


@router.get("/oauth/callback")
def oauth_callback(code: str | None = None, state: str | None = None):
    return {"success": True, "data": {"message": "TODO: exchange code for tokens and store"}}


@router.post("/backup/upload", response_model=dict)
def backup_upload(
    body: SyncUploadRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()
    if settings.astra_offline_mode:
        raise HTTPException(503, "Offline mode enabled")
    db_path = settings.database_url.replace("sqlite:///", "")
    if not os.path.exists(db_path):
        raise HTTPException(500, "Database file not found")
    tmp = temporary_copy(db_path)
    try:
        with open(tmp, "rb") as f:
            plaintext = f.read()
        salt, nonce, ciphertext = encrypt(plaintext, body.passphrase, kdf=settings.astra_encryption_kdf)
        sha = ciphertext_sha256(ciphertext)
        device_id = _device_id()
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        backup_id = f"backup_{ts}_{device_id[:8]}"
        manifest = {"schema_version": 1, "app_version": "0.1", "created_at_utc": ts, "device_id": device_id, "backup_filename": backup_id + ".enc", "cipher": "aes-256-gcm", "kdf": settings.astra_encryption_kdf, "salt_b64": __import__("base64").b64encode(salt).decode(), "nonce_b64": __import__("base64").b64encode(nonce).decode(), "ciphertext_sha256": sha}
        result = upload_backup(ciphertext, manifest, settings.astra_sync_folder_name)
        if result.get("error"):
            session.add(SyncLog(user_id=current_user.id, direction="upload", status="fail", backup_id=backup_id, device_id=device_id, message=result.get("error")))
            session.commit()
            raise HTTPException(502, result["error"])
        session.add(SyncLog(user_id=current_user.id, direction="upload", status="success", backup_id=backup_id, device_id=device_id))
        session.commit()
        return {"success": True, "data": {"status": "uploaded", "backup_id": backup_id, "drive_file_id": result.get("drive_file_id"), "created_at_utc": ts}}
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


@router.get("/backup/list", response_model=dict)
def backup_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    backups = list_backups(get_settings().astra_sync_folder_name)
    return {"success": True, "data": [{"backup_id": b.get("backup_id"), "created_at_utc": b.get("created_at_utc"), "device_id": b.get("device_id")} for b in backups]}


@router.post("/backup/download", response_model=dict)
def backup_download(backup_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    ciphertext, manifest = download_backup(backup_id, get_settings().astra_sync_folder_name)
    if ciphertext is None:
        raise HTTPException(404, "Backup not found")
    return {"success": True, "data": {"ciphertext_b64": __import__("base64").b64encode(ciphertext).decode(), "manifest": manifest}}


@router.post("/backup/restore", response_model=dict)
def backup_restore(backup_id: str, passphrase: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    raise HTTPException(501, "Restore: download backup then replace DB and restart backend (manual flow)")
