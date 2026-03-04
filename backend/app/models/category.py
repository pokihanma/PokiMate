from datetime import datetime
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field()
    kind: str = Field(index=True)  # income | expense | transfer
    color: str | None = Field(default=None)
    keywords: str | None = Field(default=None)  # JSON array
    created_at: datetime = Field(default_factory=datetime.utcnow)
