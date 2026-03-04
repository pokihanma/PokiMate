from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class RecurringRule(SQLModel, table=True):
    __tablename__ = "recurring_rules"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field()
    amount: Decimal = Field()
    currency: str = Field(default="INR")
    category_id: int = Field(foreign_key="categories.id")
    account_id: int = Field(foreign_key="accounts.id")
    frequency: str = Field()  # weekly | monthly | yearly
    day_of_month: int | None = Field(default=None)
    next_due_date: date = Field(index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
