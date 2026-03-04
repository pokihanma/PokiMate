from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget
from app.models.recurring import RecurringRule
from app.schemas.finance import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    CategoryCreate,
    CategoryResponse,
    BudgetCreate,
    BudgetResponse,
    RecurringCreate,
    RecurringResponse,
)
from app.security.deps import get_current_user
from app.services.finance_engine import spending_by_category, budget_utilization
from app.services.audit_service import log_event
from app.services.csv_import_service import import_csv
from app.utils.time import parse_month, month_end
from app.utils.validation import transaction_type_valid

router = APIRouter(prefix="/finance", tags=["finance"])


def _tx_to_dict(t: Transaction) -> dict:
    return {
        "id": t.id,
        "user_id": t.user_id,
        "date": t.date.isoformat(),
        "amount": float(t.amount),
        "currency": t.currency,
        "type": t.type,
        "account_id": t.account_id,
        "to_account_id": t.to_account_id,
        "category_id": t.category_id,
        "description": t.description or "",
        "merchant": t.merchant,
        "notes": t.notes,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
    }


@router.get("/transactions", response_model=dict)
def list_transactions(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    type_: str | None = Query(None, alias="type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    q = select(Transaction).where(Transaction.user_id == current_user.id)
    if from_date:
        q = q.where(Transaction.date >= from_date)
    if to_date:
        q = q.where(Transaction.date <= to_date)
    if type_ and transaction_type_valid(type_):
        q = q.where(Transaction.type == type_)
    q = q.order_by(Transaction.date.desc())
    rows = session.exec(q).all()
    return {"success": True, "data": [_tx_to_dict(r) for r in rows]}


@router.post("/transactions", status_code=201, response_model=dict)
def create_transaction(
    body: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if not transaction_type_valid(body.type):
        raise HTTPException(400, "Invalid type")
    t = Transaction(
        user_id=current_user.id,
        date=body.date,
        amount=body.amount,
        currency=body.currency,
        type=body.type,
        account_id=body.account_id,
        to_account_id=body.to_account_id,
        category_id=body.category_id,
        description=body.description,
        merchant=body.merchant,
        notes=body.notes,
    )
    session.add(t)
    session.commit()
    session.refresh(t)
    log_event(session, current_user.id, current_user.id, None, "create", "transaction", t.id, None, _tx_to_dict(t))
    return {"success": True, "data": _tx_to_dict(t)}


@router.put("/transactions/{tx_id}", response_model=dict)
def update_transaction(
    tx_id: int,
    body: TransactionUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    t = session.get(Transaction, tx_id)
    if not t or t.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    old = _tx_to_dict(t)
    if body.date is not None:
        t.date = body.date
    if body.amount is not None:
        t.amount = body.amount
    if body.type is not None:
        t.type = body.type
    if body.account_id is not None:
        t.account_id = body.account_id
    if body.category_id is not None:
        t.category_id = body.category_id
    if body.description is not None:
        t.description = body.description
    session.add(t)
    session.commit()
    session.refresh(t)
    log_event(session, current_user.id, current_user.id, None, "update", "transaction", t.id, old, _tx_to_dict(t))
    return {"success": True, "data": _tx_to_dict(t)}


@router.delete("/transactions/{tx_id}", status_code=204)
def delete_transaction(
    tx_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    t = session.get(Transaction, tx_id)
    if not t or t.user_id != current_user.id:
        raise HTTPException(404, "Not found")
    old = _tx_to_dict(t)
    session.delete(t)
    session.commit()
    log_event(session, current_user.id, current_user.id, None, "delete", "transaction", tx_id, old, None)
    return None


@router.get("/categories", response_model=dict)
def list_categories(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(Category).where(Category.user_id == current_user.id)).all()
    return {"success": True, "data": [{"id": r.id, "user_id": r.user_id, "name": r.name, "kind": r.kind, "color": r.color, "created_at": r.created_at.isoformat()} for r in rows]}


@router.post("/categories", status_code=201, response_model=dict)
def create_category(
    body: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    c = Category(user_id=current_user.id, name=body.name, kind=body.kind, color=body.color, keywords=body.keywords)
    session.add(c)
    session.commit()
    session.refresh(c)
    return {"success": True, "data": {"id": c.id, "user_id": c.user_id, "name": c.name, "kind": c.kind, "color": c.color, "created_at": c.created_at.isoformat()}}


@router.get("/budgets", response_model=dict)
def list_budgets(
    month: str = Query(..., description="YYYY-MM"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    budgets = session.exec(select(Budget).where(Budget.user_id == current_user.id, Budget.month == month)).all()
    tx_list = session.exec(select(Transaction).where(Transaction.user_id == current_user.id)).all()
    tx_dicts = [{"date": t.date, "type": t.type, "category_id": t.category_id, "amount": t.amount} for t in tx_list]
    spending = spending_by_category(tx_dicts, month)
    cat_ids = {b.category_id for b in budgets}
    categories = {}
    if cat_ids:
        for c in session.exec(select(Category).where(Category.user_id == current_user.id)).all():
            if c.id in cat_ids:
                categories[c.id] = c.name
    bud_list = [{"category_id": b.category_id, "limit_amount": b.limit_amount, "category_name": categories.get(b.category_id)} for b in budgets]
    util = budget_utilization(spending, bud_list)
    return {"success": True, "data": [{"id": b.id, "user_id": b.user_id, "category_id": b.category_id, "month": b.month, "limit_amount": float(b.limit_amount), "utilization": next((u for u in util if u["category_id"] == b.category_id), {})} for b in budgets]}


@router.post("/budgets", status_code=201, response_model=dict)
def create_budget(
    body: BudgetCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    b = Budget(user_id=current_user.id, category_id=body.category_id, month=body.month, limit_amount=body.limit_amount)
    session.add(b)
    session.commit()
    session.refresh(b)
    return {"success": True, "data": {"id": b.id, "user_id": b.user_id, "category_id": b.category_id, "month": b.month, "limit_amount": float(b.limit_amount), "created_at": b.created_at.isoformat()}}


@router.get("/recurring", response_model=dict)
def list_recurring(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    rows = session.exec(select(RecurringRule).where(RecurringRule.user_id == current_user.id)).all()
    return {"success": True, "data": [{"id": r.id, "user_id": r.user_id, "title": r.title, "amount": float(r.amount), "currency": r.currency, "category_id": r.category_id, "account_id": r.account_id, "frequency": r.frequency, "next_due_date": r.next_due_date.isoformat(), "is_active": r.is_active, "created_at": r.created_at.isoformat()} for r in rows]}


@router.post("/recurring", status_code=201, response_model=dict)
def create_recurring(
    body: RecurringCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    r = RecurringRule(
        user_id=current_user.id,
        title=body.title,
        amount=body.amount,
        currency=body.currency,
        category_id=body.category_id,
        account_id=body.account_id,
        frequency=body.frequency,
        day_of_month=body.day_of_month,
        next_due_date=body.next_due_date,
    )
    session.add(r)
    session.commit()
    session.refresh(r)
    return {"success": True, "data": {"id": r.id, "user_id": r.user_id, "title": r.title, "amount": float(r.amount), "currency": r.currency, "category_id": r.category_id, "account_id": r.account_id, "frequency": r.frequency, "next_due_date": r.next_due_date.isoformat(), "is_active": r.is_active, "created_at": r.created_at.isoformat()}}


@router.post("/import/csv", response_model=dict)
def import_csv_route(
    file: UploadFile = File(...),
    account_id: int = Query(...),
    category_id: int = Query(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    content = file.file.read()
    count, errors = import_csv(session, current_user.id, content, account_id, category_id)
    return {"success": True, "data": {"imported": count, "errors": errors}}


@router.get("/summary", response_model=dict)
def finance_summary(
    month: str = Query(..., description="YYYY-MM"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    start = parse_month(month)
    if not start:
        raise HTTPException(400, "Invalid month")
    end = month_end(start)
    tx_list = session.exec(select(Transaction).where(Transaction.user_id == current_user.id, Transaction.date >= start, Transaction.date <= end)).all()
    income_total = sum(float(t.amount) for t in tx_list if t.type == "income")
    expense_total = sum(float(t.amount) for t in tx_list if t.type == "expense")
    savings_rate = (income_total - expense_total) / income_total if income_total else 0.0
    tx_dicts = [{"date": t.date, "type": t.type, "category_id": t.category_id, "amount": t.amount} for t in tx_list]
    spending = spending_by_category(tx_dicts, month)
    categories = {c.id: c.name for c in session.exec(select(Category)).all()}
    top_categories = [{"category": categories.get(cid, str(cid)), "amount": float(amt)} for cid, amt in sorted(spending.items(), key=lambda x: -float(x[1]))[:10]]
    budgets = session.exec(select(Budget).where(Budget.user_id == current_user.id, Budget.month == month)).all()
    bud_list = [{"category_id": b.category_id, "limit_amount": b.limit_amount, "category_name": categories.get(b.category_id)} for b in budgets]
    budget_util = budget_utilization(spending, bud_list)
    return {"success": True, "data": {"month": month, "income_total": income_total, "expense_total": expense_total, "savings_rate": round(savings_rate, 4), "top_categories": top_categories, "budget_utilization": [{"category": u.get("category"), "limit": u.get("limit"), "used": u.get("used"), "pct": u.get("pct")} for u in budget_util]}}
