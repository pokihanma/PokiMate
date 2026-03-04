from datetime import datetime
from sqlmodel import Field, SQLModel


class Habit(SQLModel, table=True):
    __tablename__ = "habits"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field()
    description: str | None = Field(default=None)
    frequency: str = Field()  # daily | weekly
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
