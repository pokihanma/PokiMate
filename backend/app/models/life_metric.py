from datetime import date
from decimal import Decimal
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class LifeMetric(SQLModel, table=True):
    __tablename__ = "life_metrics"
    __table_args__ = (UniqueConstraint("user_id", "date"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    date: date = Field(index=True)
    sleep_hours: Decimal | None = Field(default=None)
    work_hours: Decimal | None = Field(default=None)
    exercise_minutes: int | None = Field(default=None)
    mood_score: int | None = Field(default=None)  # 1-5
    notes: str | None = Field(default=None)
