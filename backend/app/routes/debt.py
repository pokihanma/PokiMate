from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.debt import Debt
from app.models.debt_payment import DebtPayment
from app.schemas.debt import DebtCreate, DebtUpdate, DebtPaymentCreate, DebtSimulateRequest
from app.security.deps import get_current_user
from app.services.debt_engine import (
    debt_to_income_ratio,
    debt_stress_index,
    payoff_schedule_snowball,
    payoff_schedule_avalanche,
)

router = APIRouter(prefix="/debt", tags=["debt"])


def _debt_to_dict(d: Debt) -> dict:
    return {
        "id": d.id,
        "user_id": d.user_id,
        "name": d.name,
        "type": d.type,
        "principal": float(d.principal),
        "interest_rate_apr": float(d.interest_rate_apr),
        "emi_monthly": float(d.emi_monthly),
        "start_date": d.start_date.isoformat(),
        "tenure_months": d.tenure_months,
        "remaining_balance": float(d.remaining_balance),
        "minimum_payment": float(d.minimum_payment) if d.minimum_payment else None,
        "created_at": d.created_at.isoformat(),
    }


@router.get("/list", response_model=dict)
def list_debts(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Debt).where(Debt.user_id == current_user.id)).all()
    return {"success": True, "data": [_debt_to_dict(r) for r in rows]}


@router.post("", status_code=201, response_model=dict)
def create_debt(
    body: DebtCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    d = Debt(
        user_id=current_user.id,
        name=body.name,
        type=body.type,
        principal=body.principal,
        interest_rate_apr=body.interest_rate_apr,
        emi_monthly=body.emi_monthly,
        start_date=body.start_date,
        tenure_months=body.tenure_months,
        remaining_balance=body.remaining_balance,
        minimum_payment=body.minimum_payment,
    )
    session.add(d)
    session.commit()
    session.refresh(d)
    return {"success": True, "data": _debt_to_dict(d)}


@router.put("/{debt_id}", response_model=dict)
def update_debt(
    debt_id: int,
    body: DebtUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    d = session.get(Debt, debt_id)
    if not d or d.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    if body.name is not None:
        d.name = body.name
    if body.remaining_balance is not None:
        d.remaining_balance = body.remaining_balance
    if body.minimum_payment is not None:
        d.minimum_payment = body.minimum_payment
    session.add(d)
    session.commit()
    session.refresh(d)
    return {"success": True, "data": _debt_to_dict(d)}


@router.delete("/{debt_id}", status_code=204)
def delete_debt(
    debt_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    d = session.get(Debt, debt_id)
    if not d or d.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    session.delete(d)
    session.commit()
    return None


@router.post("/payment", status_code=201, response_model=dict)
def create_payment(
    body: DebtPaymentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    debt = session.get(Debt, body.debt_id)
    if not debt or debt.user_id != current_user.id:
        raise HTTPException(404, "Debt not found")
    p = DebtPayment(user_id=current_user.id, debt_id=body.debt_id, date=body.date, amount=body.amount, notes=body.notes)
    session.add(p)
    debt.remaining_balance = debt.remaining_balance - body.amount
    if debt.remaining_balance < 0:
        debt.remaining_balance = Decimal(0)
    session.add(debt)
    session.commit()
    session.refresh(p)
    return {"success": True, "data": {"id": p.id, "debt_id": p.debt_id, "date": p.date.isoformat(), "amount": float(p.amount)}}


@router.get("/summary", response_model=dict)
def debt_summary(
    monthly_income: float | None = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    debts = session.exec(select(Debt).where(Debt.user_id == current_user.id)).all()
    total_emi = sum(float(d.emi_monthly) for d in debts)
    total_balance = sum(float(d.remaining_balance) for d in debts)
    income = Decimal(str(monthly_income)) if monthly_income else Decimal(0)
    dti = debt_to_income_ratio(Decimal(str(total_emi)), income) if income else 0.0
    stress = debt_stress_index(dti, len(debts), 0.0)
    return {"success": True, "data": {"total_balance": total_balance, "total_emi": total_emi, "dti_ratio": dti, "debt_stress_index": stress}}


@router.post("/simulate", response_model=dict)
def simulate(
    body: DebtSimulateRequest,
    strategy: str = Query("avalanche", alias="s"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    debts = session.exec(select(Debt).where(Debt.user_id == current_user.id)).all()
    debt_list = [_debt_to_dict(d) for d in debts]
    for d in debt_list:
        d["remaining_balance"] = Decimal(str(d["remaining_balance"]))
        d["interest_rate_apr"] = Decimal(str(d["interest_rate_apr"]))
        d["emi_monthly"] = Decimal(str(d["emi_monthly"]))
    extra = Decimal(str(body.extra_payment_monthly))
    if strategy == "snowball":
        debt_free_date, total_interest, interest_saved, schedule = payoff_schedule_snowball(debt_list, extra, body.as_of_date)
    else:
        debt_free_date, total_interest, interest_saved, schedule = payoff_schedule_avalanche(debt_list, extra, body.as_of_date)
    return {"success": True, "data": {"strategy": strategy, "as_of_date": body.as_of_date.isoformat(), "extra_payment_monthly": float(extra), "debt_free_date": debt_free_date.isoformat(), "total_interest": float(total_interest), "interest_saved_vs_minimum": float(interest_saved), "monthly_schedule": schedule}}
