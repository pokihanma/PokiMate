from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Goal(SQLModel, table=True):
    __tablename__ = "goals"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    type: str = Field()  # savings | fitness | habit | other
    title: str = Field()
    description: str | None = Field(default=None)
    target_date: date = Field(index=True)
    target_value: Decimal | None = Field(default=None)
    progress_value: Decimal | None = Field(default=None)
    status: str = Field(default="active", index=True)  # active | paused | done
    created_at: datetime = Field(default_factory=datetime.utcnow)
