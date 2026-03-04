from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    date: date
    amount: Decimal
    currency: str = "INR"
    type: str  # income | expense | transfer
    account_id: int
    to_account_id: Optional[int] = None
    category_id: int
    description: str = ""
    merchant: Optional[str] = None
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    date: date
    amount: Decimal
    currency: str
    type: str
    account_id: int
    to_account_id: Optional[int] = None
    category_id: int
    description: str
    merchant: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    kind: str  # income | expense | transfer
    color: Optional[str] = None
    keywords: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    kind: str
    color: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category_id: int
    month: str  # YYYY-MM
    limit_amount: Decimal


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    month: str
    limit_amount: Decimal
    created_at: str

    class Config:
        from_attributes = True


class RecurringCreate(BaseModel):
    title: str
    amount: Decimal
    currency: str = "INR"
    category_id: int
    account_id: int
    frequency: str  # weekly | monthly | yearly
    day_of_month: Optional[int] = None
    next_due_date: date


class RecurringResponse(BaseModel):
    id: int
    user_id: int
    title: str
    amount: Decimal
    currency: str
    category_id: int
    account_id: int
    frequency: str
    next_due_date: date
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class FinanceSummaryResponse(BaseModel):
    month: str
    income_total: float
    expense_total: float
    savings_rate: float
    top_categories: list[dict]
    budget_utilization: list[dict]
