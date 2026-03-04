from datetime import datetime
from sqlmodel import Field, SQLModel


class AuditEvent(SQLModel, table=True):
    __tablename__ = "audit_events"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    actor_user_id: int | None = Field(default=None)
    device_id: str | None = Field(default=None)
    event_type: str = Field()  # create | update | delete | restore | import
    entity: str = Field(index=True)
    entity_id: int | None = Field(default=None, index=True)
    old_json: str | None = Field(default=None)
    new_json: str | None = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
