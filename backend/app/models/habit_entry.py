from datetime import date
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class HabitEntry(SQLModel, table=True):
    __tablename__ = "habit_entries"
    __table_args__ = (UniqueConstraint("habit_id", "date"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    habit_id: int = Field(foreign_key="habits.id", index=True)
    date: date = Field(index=True)
    completed: bool = Field(default=False)
