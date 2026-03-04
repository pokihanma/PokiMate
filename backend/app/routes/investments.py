from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.holding import Holding
from app.models.investment_cashflow import InvestmentCashflow
from app.schemas.investments import HoldingCreate, HoldingUpdate, XIRRRequest, CashflowCreate
from app.security.deps import get_current_user
from app.services.investment_engine import allocation_percentages, xirr

router = APIRouter(prefix="/investments", tags=["investments"])


def _holding_to_dict(h: Holding) -> dict:
    return {
        "id": h.id,
        "user_id": h.user_id,
        "type": h.type,
        "asset_name": h.asset_name,
        "units": float(h.units),
        "avg_cost": float(h.avg_cost),
        "current_price": float(h.current_price),
        "currency": h.currency,
        "as_of_date": h.as_of_date.isoformat(),
        "created_at": h.created_at.isoformat(),
    }


@router.get("/holdings", response_model=dict)
def list_holdings(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Holding).where(Holding.user_id == current_user.id)).all()
    return {"success": True, "data": [_holding_to_dict(r) for r in rows]}


@router.post("/holdings", status_code=201, response_model=dict)
def create_holding(
    body: HoldingCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    h = Holding(
        user_id=current_user.id,
        type=body.type,
        asset_name=body.asset_name,
        units=body.units,
        avg_cost=body.avg_cost,
        current_price=body.current_price,
        currency=body.currency,
        as_of_date=body.as_of_date,
    )
    session.add(h)
    session.commit()
    session.refresh(h)
    return {"success": True, "data": _holding_to_dict(h)}


@router.put("/holdings/{holding_id}", response_model=dict)
def update_holding(
    holding_id: int,
    body: HoldingUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    h = session.get(Holding, holding_id)
    if not h or h.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    if body.units is not None:
        h.units = body.units
    if body.avg_cost is not None:
        h.avg_cost = body.avg_cost
    if body.current_price is not None:
        h.current_price = body.current_price
    if body.as_of_date is not None:
        h.as_of_date = body.as_of_date
    session.add(h)
    session.commit()
    session.refresh(h)
    return {"success": True, "data": _holding_to_dict(h)}


@router.delete("/holdings/{holding_id}", status_code=204)
def delete_holding(
    holding_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    h = session.get(Holding, holding_id)
    if not h or h.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    session.delete(h)
    session.commit()
    return None


@router.post("/cashflow", status_code=201, response_model=dict)
def create_cashflow(
    body: CashflowCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    c = InvestmentCashflow(user_id=current_user.id, holding_id=body.holding_id, date=body.date, amount=body.amount, currency=body.currency, label=body.label)
    session.add(c)
    session.commit()
    session.refresh(c)
    return {"success": True, "data": {"id": c.id, "holding_id": c.holding_id, "date": c.date.isoformat(), "amount": float(c.amount)}}


@router.get("/summary", response_model=dict)
def investments_summary(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Holding).where(Holding.user_id == current_user.id)).all()
    total_value = sum(float(r.units) * float(r.current_price) for r in rows)
    total_cost = sum(float(r.units) * float(r.avg_cost) for r in rows)
    return {"success": True, "data": {"total_value": total_value, "total_cost": total_cost}}


@router.get("/allocation", response_model=dict)
def allocation(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Holding).where(Holding.user_id == current_user.id)).all()
    hold_list = [{"type": r.type, "units": float(r.units), "current_price": float(r.current_price)} for r in rows]
    alloc = allocation_percentages(hold_list)
    return {"success": True, "data": alloc}


@router.post("/xirr", response_model=dict)
def compute_xirr(
    body: XIRRRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    cashflows = [(date.fromisoformat(c.date), c.amount) for c in body.cashflows]
    xirr_val, method, iterations = xirr(cashflows)
    return {"success": True, "data": {"xirr": xirr_val, "method": method, "iterations": iterations}}
