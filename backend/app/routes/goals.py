from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.goal import Goal
from app.schemas.goals import GoalCreate, GoalUpdate, GoalProgressRequest
from app.security.deps import get_current_user

router = APIRouter(prefix="/goals", tags=["goals"])


def _goal_to_dict(g: Goal) -> dict:
    return {
        "id": g.id,
        "user_id": g.user_id,
        "type": g.type,
        "title": g.title,
        "description": g.description,
        "target_date": g.target_date.isoformat(),
        "target_value": float(g.target_value) if g.target_value else None,
        "progress_value": float(g.progress_value) if g.progress_value else None,
        "status": g.status,
        "created_at": g.created_at.isoformat(),
    }


@router.get("", response_model=dict)
def list_goals(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Goal).where(Goal.user_id == current_user.id)).all()
    return {"success": True, "data": [_goal_to_dict(r) for r in rows]}


@router.post("", status_code=201, response_model=dict)
def create_goal(
    body: GoalCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    g = Goal(
        user_id=current_user.id,
        type=body.type,
        title=body.title,
        description=body.description,
        target_date=body.target_date,
        target_value=body.target_value,
        progress_value=body.progress_value,
    )
    session.add(g)
    session.commit()
    session.refresh(g)
    return {"success": True, "data": _goal_to_dict(g)}


@router.put("/{goal_id}", response_model=dict)
def update_goal(
    goal_id: int,
    body: GoalUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    g = session.get(Goal, goal_id)
    if not g or g.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    if body.title is not None:
        g.title = body.title
    if body.description is not None:
        g.description = body.description
    if body.target_date is not None:
        g.target_date = body.target_date
    if body.target_value is not None:
        g.target_value = body.target_value
    if body.progress_value is not None:
        g.progress_value = body.progress_value
    if body.status is not None:
        g.status = body.status
    session.add(g)
    session.commit()
    session.refresh(g)
    return {"success": True, "data": _goal_to_dict(g)}


@router.post("/{goal_id}/progress", response_model=dict)
def update_progress(
    goal_id: int,
    body: GoalProgressRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    g = session.get(Goal, goal_id)
    if not g or g.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    g.progress_value = body.progress_value
    session.add(g)
    session.commit()
    session.refresh(g)
    return {"success": True, "data": _goal_to_dict(g)}


@router.delete("/{goal_id}", status_code=204)
def delete_goal(
    goal_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    g = session.get(Goal, goal_id)
    if not g or g.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    session.delete(g)
    session.commit()
    return None
