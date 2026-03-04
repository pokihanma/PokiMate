"""
Deterministic budgeting engine. Period: monthly.
Inputs: transactions, budgets, date range.
Outputs: spending_by_category, budget_utilization, overspend flags.
"""
from datetime import date
from decimal import Decimal
from app.utils.time import parse_month, month_start, month_end
from app.utils.money import round2


def spending_by_category(
    transactions: list[dict],
    month: str,
) -> dict[int, Decimal]:
    """Aggregate expense amount per category_id for the given month (YYYY-MM)."""
    out: dict[int, Decimal] = {}
    start = parse_month(month)
    if not start:
        return out
    end = month_end(start)
    for t in transactions:
        if t.get("type") != "expense":
            continue
        d = t.get("date")
        if isinstance(d, str):
            d = date.fromisoformat(d)
        if start <= d <= end:
            cid = t.get("category_id")
            if cid is not None:
                amt = Decimal(str(t.get("amount", 0)))
                out[cid] = out.get(cid, Decimal(0)) + amt
    return {k: round2(v) for k, v in out.items()}


def budget_utilization(
    spending_by_cat: dict[int, Decimal],
    budgets: list[dict],
) -> list[dict]:
    """For each budget, compute used amount and pct (used/limit)."""
    result = []
    for b in budgets:
        cid = b.get("category_id")
        limit = Decimal(str(b.get("limit_amount", 0)))
        used = spending_by_cat.get(cid, Decimal(0))
        pct = float(used / limit) if limit else 0.0
        result.append({
            "category_id": cid,
            "category": b.get("category_name"),
            "limit": float(limit),
            "used": float(used),
            "pct": round(pct, 2),
            "overspend": used > limit,
        })
    return result


def overspend_flags(budget_utilization: list[dict]) -> list[dict]:
    """Return only entries where used > limit."""
    return [u for u in budget_utilization if u.get("overspend")]
