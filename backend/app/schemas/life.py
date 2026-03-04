from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class LifeMetricCreate(BaseModel):
    date: date
    sleep_hours: Optional[float] = None
    work_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    mood_score: Optional[int] = None  # 1-5
    notes: Optional[str] = None


class LifeMetricUpdate(BaseModel):
    sleep_hours: Optional[float] = None
    work_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    mood_score: Optional[int] = None
    notes: Optional[str] = None


class LifeMetricResponse(BaseModel):
    id: int
    date: date
    sleep_hours: Optional[float] = None
    work_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    mood_score: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str  # daily | weekly


class HabitResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    frequency: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class HabitCheckinRequest(BaseModel):
    date: date
    completed: bool = True
