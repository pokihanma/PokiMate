from datetime import date, datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Holding(SQLModel, table=True):
    __tablename__ = "investments_holdings"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    type: str = Field(index=True)  # stock | mf | sip | gold | fd | mmf
    asset_name: str = Field(index=True)
    units: Decimal = Field()
    avg_cost: Decimal = Field()
    current_price: Decimal = Field()
    currency: str = Field(default="INR")
    as_of_date: date = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
