from datetime import date
from decimal import Decimal
from sqlmodel import Field, SQLModel


class DebtPayment(SQLModel, table=True):
    __tablename__ = "debt_payments"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    debt_id: int = Field(foreign_key="debts.id", index=True)
    date: date = Field(index=True)
    amount: Decimal = Field()
    notes: str | None = Field(default=None)
