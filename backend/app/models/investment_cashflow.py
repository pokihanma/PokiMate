from datetime import date
from decimal import Decimal
from sqlmodel import Field, SQLModel


class InvestmentCashflow(SQLModel, table=True):
    __tablename__ = "investment_cashflows"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    holding_id: int | None = Field(default=None, foreign_key="investments_holdings.id")
    date: date = Field(index=True)
    amount: Decimal = Field()
    currency: str = Field(default="INR")
    label: str = Field(default="")
