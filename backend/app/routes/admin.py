from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.security.deps import require_admin
from app.models.user import User
from app.utils.seed import run_seed

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed-demo", response_model=dict)
def seed_demo(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin),
):
    run_seed(session, current_user.id)
    return {"success": True, "data": {"message": "Demo data seeded"}}
