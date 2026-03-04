"""
Aggregate life metrics for dashboard (e.g. weekly averages).
"""
from datetime import date, timedelta
from statistics import mean


def weekly_averages(
    metrics: list[dict],
    week_start: date,
) -> dict[str, float]:
    """Compute average sleep, work, exercise, mood for the 7-day window."""
    week_end = week_start + timedelta(days=6)
    in_week = [
        m for m in metrics
        if week_start <= (m.get("date") or date.min) <= week_end
    ]
    if not in_week:
        return {"sleep_hours": 0, "work_hours": 0, "exercise_minutes": 0, "mood_score": 0}
    sleep = [m["sleep_hours"] for m in in_week if m.get("sleep_hours") is not None]
    work = [m["work_hours"] for m in in_week if m.get("work_hours") is not None]
    ex = [m["exercise_minutes"] for m in in_week if m.get("exercise_minutes") is not None]
    mood = [m["mood_score"] for m in in_week if m.get("mood_score") is not None]
    return {
        "sleep_hours": round(mean(sleep), 1) if sleep else 0,
        "work_hours": round(mean(work), 1) if work else 0,
        "exercise_minutes": int(mean(ex)) if ex else 0,
        "mood_score": round(mean(mood), 1) if mood else 0,
    }
