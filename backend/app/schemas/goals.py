from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class GoalCreate(BaseModel):
    type: str  # savings | fitness | habit | other
    title: str
    description: Optional[str] = None
    target_date: date
    target_value: Optional[Decimal] = None
    progress_value: Optional[Decimal] = None


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    target_value: Optional[Decimal] = None
    progress_value: Optional[Decimal] = None
    status: Optional[str] = None  # active | paused | done


class GoalProgressRequest(BaseModel):
    progress_value: Decimal


class GoalResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    description: Optional[str] = None
    target_date: date
    target_value: Optional[Decimal] = None
    progress_value: Optional[Decimal] = None
    status: str
    created_at: str

    class Config:
        from_attributes = True
