from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    date: date = Field(index=True)
    amount: Decimal = Field()
    currency: str = Field(default="INR")
    type: str = Field(index=True)  # income | expense | transfer
    account_id: int = Field(foreign_key="accounts.id")
    to_account_id: int | None = Field(default=None, foreign_key="accounts.id")
    category_id: int = Field(foreign_key="categories.id", index=True)
    description: str = Field(default="")
    merchant: str | None = Field(default=None)
    notes: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
