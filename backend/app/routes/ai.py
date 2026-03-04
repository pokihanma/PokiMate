from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.transaction import Transaction
from app.models.debt import Debt
from app.models.holding import Holding
from app.models.goal import Goal
from app.security.deps import get_current_user
from app.config import get_settings
from app.services.ai_client import call_ai_summarize

router = APIRouter(prefix="/ai", tags=["ai"])


def _sanitized_payload(session: Session, user_id: int, month: str) -> dict:
    from app.utils.time import parse_month, month_end
    start = parse_month(month)
    end = month_end(start) if start else None
    tx_list = []
    if start and end:
        tx_list = session.exec(select(Transaction).where(Transaction.user_id == user_id, Transaction.date >= start, Transaction.date <= end)).all()
    income = sum(float(t.amount) for t in tx_list if t.type == "income")
    expense = sum(float(t.amount) for t in tx_list if t.type == "expense")
    debts = session.exec(select(Debt).where(Debt.user_id == user_id)).all()
    debt_total = sum(float(d.remaining_balance) for d in debts)
    holdings = session.exec(select(Holding).where(Holding.user_id == user_id)).all()
    portfolio_value = sum(float(h.units) * float(h.current_price) for h in holdings)
    goals = session.exec(select(Goal).where(Goal.user_id == user_id, Goal.status == "active")).all()
    return {
        "month": month,
        "income_total": income,
        "expense_total": expense,
        "savings": income - expense,
        "debt_total": debt_total,
        "portfolio_value": portfolio_value,
        "goals_count": len(goals),
    }


@router.post("/weekly-summary", response_model=dict)
def weekly_summary(
    month: str | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()
    if settings.astra_ai_mode == "OFF":
        return {"success": True, "data": {"summary": "AI is disabled.", "cached_at": None}}
    month = month or date.today().strftime("%Y-%m")
    payload = _sanitized_payload(session, current_user.id, month)
    result = call_ai_summarize(payload)
    if result:
        return {"success": True, "data": {"summary": result.get("summary", "No summary."), "cached_at": result.get("cached_at")}}
    return {"success": True, "data": {"summary": "AI unavailable.", "cached_at": None}}


@router.post("/spending-insights", response_model=dict)
def spending_insights(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    settings = get_settings()
    if settings.astra_ai_mode == "OFF":
        return {"success": True, "data": {"summary": "AI is disabled.", "cached_at": None}}
    month = date.today().strftime("%Y-%m")
    payload = _sanitized_payload(session, current_user.id, month)
    result = call_ai_summarize(payload)
    if result:
        return {"success": True, "data": {"summary": result.get("summary", "No insights."), "cached_at": result.get("cached_at")}}
    return {"success": True, "data": {"summary": "AI unavailable.", "cached_at": None}}


@router.post("/debt-coach", response_model=dict)
def debt_coach(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    settings = get_settings()
    if settings.astra_ai_mode == "OFF":
        return {"success": True, "data": {"summary": "AI is disabled.", "cached_at": None}}
    payload = _sanitized_payload(session, current_user.id, date.today().strftime("%Y-%m"))
    payload["focus"] = "debt"
    result = call_ai_summarize(payload)
    if result:
        return {"success": True, "data": {"summary": result.get("summary", "No commentary."), "cached_at": result.get("cached_at")}}
    return {"success": True, "data": {"summary": "AI unavailable.", "cached_at": None}}


@router.post("/portfolio-commentary", response_model=dict)
def portfolio_commentary(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    settings = get_settings()
    if settings.astra_ai_mode == "OFF":
        return {"success": True, "data": {"summary": "AI is disabled.", "cached_at": None}}
    payload = _sanitized_payload(session, current_user.id, date.today().strftime("%Y-%m"))
    payload["focus"] = "portfolio"
    result = call_ai_summarize(payload)
    if result:
        return {"success": True, "data": {"summary": result.get("summary", "No commentary."), "cached_at": result.get("cached_at")}}
    return {"success": True, "data": {"summary": "AI unavailable.", "cached_at": None}}
