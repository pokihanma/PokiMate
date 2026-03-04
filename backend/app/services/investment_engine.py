"""
Deterministic investment engine.
- Allocation % by asset class.
- XIRR via Newton-Raphson with fallback.
- MMF/rebalancing: rules-based text only (no advisory).
"""
from datetime import date
from decimal import Decimal
from app.utils.money import round2


def allocation_percentages(holdings: list[dict]) -> list[dict]:
    """Compute allocation by type (asset class)."""
    total = sum(
        float(h.get("units", 0)) * float(h.get("current_price", 0))
        for h in holdings
    )
    by_type: dict[str, float] = {}
    for h in holdings:
        t = h.get("type", "other")
        val = float(h.get("units", 0)) * float(h.get("current_price", 0))
        by_type[t] = by_type.get(t, 0) + val
    return [
        {"asset_class": k, "value": v, "pct": round(v / total * 100, 2) if total else 0}
        for k, v in by_type.items()
    ]


def xirr_newton_raphson(cashflows: list[tuple[date, float]], guess: float = 0.1) -> tuple[float, str, int]:
    """
    cashflows: list of (date, amount). Negative = outflow, positive = inflow.
    Returns (xirr, method, iterations).
    """
    if len(cashflows) < 2:
        return 0.0, "insufficient", 0
    base_date = min(d for d, _ in cashflows)
    days_and_amounts = [
        ((d - base_date).days, amt) for d, amt in cashflows
    ]
    rate = guess
    for i in range(100):
        npv = 0.0
        dnpv = 0.0
        for days, amt in days_and_amounts:
            factor = (1 + rate) ** (days / 365.0)
            npv += amt / factor
            dnpv -= amt * (days / 365.0) / (factor * (1 + rate))
        if abs(npv) < 1e-7:
            return rate, "newton-raphson", i + 1
        if abs(dnpv) < 1e-10:
            break
        rate = rate - npv / dnpv
        if rate < -0.99:
            rate = -0.99
    return rate, "newton-raphson", 100


def xirr(cashflows: list[tuple[date, float]]) -> tuple[float, str, int]:
    """Compute XIRR. Tries Newton-Raphson; fallback to simple guess."""
    try:
        r, method, it = xirr_newton_raphson(cashflows)
        if -0.99 <= r <= 10.0:
            return round(r, 4), method, it
    except (ZeroDivisionError, OverflowError):
        pass
    return 0.0, "fallback", 0


def rebalancing_suggestions(
    allocation: list[dict],
    bands: dict[str, tuple[float, float]],
) -> list[str]:
    """If any asset class outside [min_pct, max_pct], add informational suggestion."""
    suggestions = []
    for a in allocation:
        ac = a.get("asset_class", "")
        pct = a.get("pct", 0)
        if ac in bands:
            lo, hi = bands[ac]
            if pct < lo:
                suggestions.append(f"{ac} is below target range ({pct}% < {lo}%). Consider adding.")
            elif pct > hi:
                suggestions.append(f"{ac} is above target range ({pct}% > {hi}%). Consider rebalancing.")
    return suggestions
