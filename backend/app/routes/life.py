from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.life_metric import LifeMetric
from app.models.habit import Habit
from app.models.habit_entry import HabitEntry
from app.schemas.life import LifeMetricCreate, LifeMetricUpdate, HabitCreate, HabitCheckinRequest
from app.security.deps import get_current_user
from app.services.life_score_engine import weekly_averages

router = APIRouter(prefix="/life", tags=["life"])


@router.get("/metrics", response_model=dict)
def list_metrics(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    q = select(LifeMetric).where(LifeMetric.user_id == current_user.id)
    if from_date:
        q = q.where(LifeMetric.date >= from_date)
    if to_date:
        q = q.where(LifeMetric.date <= to_date)
    q = q.order_by(LifeMetric.date.desc())
    rows = session.exec(q).all()
    return {"success": True, "data": [{"id": r.id, "date": r.date.isoformat(), "sleep_hours": float(r.sleep_hours) if r.sleep_hours else None, "work_hours": float(r.work_hours) if r.work_hours else None, "exercise_minutes": r.exercise_minutes, "mood_score": r.mood_score, "notes": r.notes} for r in rows]}


@router.post("/metrics", status_code=201, response_model=dict)
def create_metric(
    body: LifeMetricCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    from decimal import Decimal
    m = LifeMetric(
        user_id=current_user.id,
        date=body.date,
        sleep_hours=Decimal(str(body.sleep_hours)) if body.sleep_hours is not None else None,
        work_hours=Decimal(str(body.work_hours)) if body.work_hours is not None else None,
        exercise_minutes=body.exercise_minutes,
        mood_score=body.mood_score,
        notes=body.notes,
    )
    session.add(m)
    session.commit()
    session.refresh(m)
    return {"success": True, "data": {"id": m.id, "date": m.date.isoformat(), "sleep_hours": float(m.sleep_hours) if m.sleep_hours else None, "work_hours": float(m.work_hours) if m.work_hours else None, "exercise_minutes": m.exercise_minutes, "mood_score": m.mood_score}}


@router.put("/metrics/{metric_id}", response_model=dict)
def update_metric(
    metric_id: int,
    body: LifeMetricUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    from decimal import Decimal
    m = session.get(LifeMetric, metric_id)
    if not m or m.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    if body.sleep_hours is not None:
        m.sleep_hours = Decimal(str(body.sleep_hours))
    if body.work_hours is not None:
        m.work_hours = Decimal(str(body.work_hours))
    if body.exercise_minutes is not None:
        m.exercise_minutes = body.exercise_minutes
    if body.mood_score is not None:
        m.mood_score = body.mood_score
    if body.notes is not None:
        m.notes = body.notes
    session.add(m)
    session.commit()
    session.refresh(m)
    return {"success": True, "data": {"id": m.id, "date": m.date.isoformat(), "sleep_hours": float(m.sleep_hours) if m.sleep_hours else None, "work_hours": float(m.work_hours) if m.work_hours else None, "exercise_minutes": m.exercise_minutes, "mood_score": m.mood_score}}


@router.get("/habits", response_model=dict)
def list_habits(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Habit).where(Habit.user_id == current_user.id)).all()
    return {"success": True, "data": [{"id": r.id, "user_id": r.user_id, "title": r.title, "description": r.description, "frequency": r.frequency, "is_active": r.is_active, "created_at": r.created_at.isoformat()} for r in rows]}


@router.post("/habits", status_code=201, response_model=dict)
def create_habit(
    body: HabitCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    h = Habit(user_id=current_user.id, title=body.title, description=body.description, frequency=body.frequency)
    session.add(h)
    session.commit()
    session.refresh(h)
    return {"success": True, "data": {"id": h.id, "user_id": h.user_id, "title": h.title, "description": h.description, "frequency": h.frequency, "is_active": h.is_active, "created_at": h.created_at.isoformat()}}


@router.post("/habits/{habit_id}/checkin", response_model=dict)
def habit_checkin(
    habit_id: int,
    body: HabitCheckinRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    habit = session.get(Habit, habit_id)
    if not habit or habit.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    existing = session.exec(select(HabitEntry).where(HabitEntry.habit_id == habit_id, HabitEntry.date == body.date)).first()
    if existing:
        existing.completed = body.completed
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return {"success": True, "data": {"habit_id": habit_id, "date": body.date.isoformat(), "completed": existing.completed}}
    e = HabitEntry(user_id=current_user.id, habit_id=habit_id, date=body.date, completed=body.completed)
    session.add(e)
    session.commit()
    session.refresh(e)
    return {"success": True, "data": {"habit_id": habit_id, "date": body.date.isoformat(), "completed": e.completed}}


@router.get("/summary", response_model=dict)
def life_summary(
    week: str = Query(..., description="YYYY-WW"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        y, w = int(week[:4]), int(week[5:7])
        from datetime import datetime
        week_start = datetime.strptime(f"{y}-W{w}-1", "%G-W%V-%u").date()
    except (ValueError, IndexError):
        week_start = date.today()
    metrics = session.exec(select(LifeMetric).where(LifeMetric.user_id == current_user.id)).all()
    metrics_list = [{"date": m.date, "sleep_hours": float(m.sleep_hours) if m.sleep_hours else None, "work_hours": float(m.work_hours) if m.work_hours else None, "exercise_minutes": m.exercise_minutes, "mood_score": m.mood_score} for m in metrics]
    avgs = weekly_averages(metrics_list, week_start)
    return {"success": True, "data": {"week": week, **avgs}}
