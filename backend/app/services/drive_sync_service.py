"""
Google Drive sync: upload/download/list. OAuth stubbed when credentials not set.
"""
import os
from datetime import datetime
from app.config import get_settings

# TODO: integrate google-api-python-client when ASTRA_GOOGLE_CLIENT_ID is set


def upload_backup(encrypted_bytes: bytes, manifest: dict, folder_name: str) -> dict:
    """Upload encrypted backup and manifest to Drive. Returns {id, webViewLink} or error."""
    settings = get_settings()
    if not settings.astra_drive_enabled or not settings.astra_google_client_id:
        return {"error": "Drive not configured", "drive_file_id": None}
    # Stub: would use Drive API v3 to create file in folder Pokimate_Backups
    return {"drive_file_id": None, "error": "Drive integration stub"}


def list_backups(folder_name: str) -> list[dict]:
    """List backup manifests in folder. Returns [{backup_id, created_at_utc, device_id}]."""
    settings = get_settings()
    if not settings.astra_drive_enabled:
        return []
    return []


def download_backup(backup_id: str, folder_name: str) -> tuple[bytes | None, dict | None]:
    """Download encrypted file and manifest. Returns (ciphertext_bytes, manifest_dict) or (None, None)."""
    settings = get_settings()
    if not settings.astra_drive_enabled:
        return None, None
    return None, None
