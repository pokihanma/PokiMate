from datetime import datetime
from sqlmodel import Field, SQLModel


class SyncLog(SQLModel, table=True):
    __tablename__ = "sync_logs"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    direction: str = Field()  # upload | download | restore
    status: str = Field()  # success | fail
    backup_id: str | None = Field(default=None)
    device_id: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    message: str | None = Field(default=None)
