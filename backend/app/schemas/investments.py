from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class HoldingCreate(BaseModel):
    type: str  # stock | mf | sip | gold | fd | mmf
    asset_name: str
    units: Decimal
    avg_cost: Decimal
    current_price: Decimal
    currency: str = "INR"
    as_of_date: date


class HoldingUpdate(BaseModel):
    units: Optional[Decimal] = None
    avg_cost: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    as_of_date: Optional[date] = None


class HoldingResponse(BaseModel):
    id: int
    user_id: int
    type: str
    asset_name: str
    units: Decimal
    avg_cost: Decimal
    current_price: Decimal
    currency: str
    as_of_date: date
    created_at: str

    class Config:
        from_attributes = True


class CashflowCreate(BaseModel):
    holding_id: Optional[int] = None
    date: date
    amount: Decimal
    currency: str = "INR"
    label: str = ""


class CashflowEntry(BaseModel):
    date: str  # YYYY-MM-DD
    amount: float


class XIRRRequest(BaseModel):
    cashflows: list[CashflowEntry]


class XIRRResponse(BaseModel):
    xirr: float
    method: str
    iterations: int
