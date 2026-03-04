from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Debt(SQLModel, table=True):
    __tablename__ = "debts"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field()
    type: str = Field()  # credit_card | loan | other
    principal: Decimal = Field()
    interest_rate_apr: Decimal = Field()
    emi_monthly: Decimal = Field()
    start_date: date = Field()
    tenure_months: int = Field()
    remaining_balance: Decimal = Field(index=True)
    minimum_payment: Decimal | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
