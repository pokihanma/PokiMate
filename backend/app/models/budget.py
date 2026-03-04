from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    category_id: int = Field(foreign_key="categories.id")
    period: str = Field(default="monthly")
    month: str = Field(index=True)  # YYYY-MM
    limit_amount: Decimal = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
