from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class DebtCreate(BaseModel):
    name: str
    type: str  # credit_card | loan | other
    principal: Decimal
    interest_rate_apr: Decimal
    emi_monthly: Decimal
    start_date: date
    tenure_months: int
    remaining_balance: Decimal
    minimum_payment: Optional[Decimal] = None


class DebtUpdate(BaseModel):
    name: Optional[str] = None
    remaining_balance: Optional[Decimal] = None
    minimum_payment: Optional[Decimal] = None


class DebtResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    principal: Decimal
    interest_rate_apr: Decimal
    emi_monthly: Decimal
    start_date: date
    tenure_months: int
    remaining_balance: Decimal
    minimum_payment: Optional[Decimal] = None
    created_at: str

    class Config:
        from_attributes = True


class DebtPaymentCreate(BaseModel):
    debt_id: int
    date: date
    amount: Decimal
    notes: Optional[str] = None


class DebtSimulateRequest(BaseModel):
    as_of_date: date
    extra_payment_monthly: Decimal = 0


class DebtSimulateResponse(BaseModel):
    strategy: str
    as_of_date: str
    extra_payment_monthly: float
    debt_free_date: str
    total_interest: float
    interest_saved_vs_minimum: float
    monthly_schedule: list[dict]
