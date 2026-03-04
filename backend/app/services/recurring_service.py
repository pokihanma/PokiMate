"""Compute upcoming recurring bills (on demand)."""
from datetime import date, timedelta
from sqlmodel import Session, select
from app.models.recurring import RecurringRule


def upcoming(session: Session, user_id: int, days: int = 30) -> list[dict]:
    """Return recurring rules with next_due_date in [today, today+days]."""
    end = date.today() + timedelta(days=days)
    rules = session.exec(
        select(RecurringRule).where(
            RecurringRule.user_id == user_id,
            RecurringRule.is_active == True,
            RecurringRule.next_due_date <= end,
        )
    ).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "amount": float(r.amount),
            "next_due_date": r.next_due_date.isoformat(),
            "frequency": r.frequency,
        }
        for r in rules
    ]
