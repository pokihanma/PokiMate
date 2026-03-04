from pydantic import BaseModel
from typing import Optional


class SyncUploadRequest(BaseModel):
    passphrase: str
    keep_versions: int = 10


class SyncUploadResponse(BaseModel):
    status: str
    backup_id: str
    drive_file_id: Optional[str] = None
    created_at_utc: str


class BackupItem(BaseModel):
    backup_id: str
    created_at_utc: str
    device_id: Optional[str] = None


class SyncStatusResponse(BaseModel):
    last_sync: Optional[str] = None
    device_id: Optional[str] = None
    backup_count: int = 0
    drive_connected: bool = False
