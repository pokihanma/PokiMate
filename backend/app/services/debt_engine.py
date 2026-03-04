"""
Deterministic debt engine.
- DTI = total_monthly_emi / monthly_income
- Debt stress index = weighted mix of DTI, number_of_debts, utilization proxy.
- Payoff simulator: snowball (smallest balance first) or avalanche (highest APR first).
"""
from datetime import date
from decimal import Decimal
from app.utils.money import round2


def debt_to_income_ratio(total_emi: Decimal, monthly_income: Decimal) -> float:
    if not monthly_income or monthly_income <= 0:
        return 0.0
    return float(round2(total_emi / monthly_income))


def debt_stress_index(
    dti: float,
    number_of_debts: int,
    utilization_proxy: float = 0.0,
) -> float:
    """Simple 0-1 stress index. Weights: DTI ~0.5, count ~0.3, utilization ~0.2."""
    dti_score = min(1.0, dti / 0.5)  # 50% DTI = 1.0
    count_score = min(1.0, number_of_debts / 10.0)
    util_score = min(1.0, utilization_proxy)
    return round(0.5 * dti_score + 0.3 * count_score + 0.2 * util_score, 2)


def _monthly_interest(balance: Decimal, apr: Decimal) -> Decimal:
    return round2(balance * (apr / 100) / 12)


def payoff_schedule_snowball(
    debts: list[dict],
    extra_payment: Decimal,
    as_of_date: date,
) -> tuple[date, Decimal, Decimal, list[dict]]:
    """Sort by remaining_balance ascending; pay minimums, apply extra to smallest."""
    from copy import deepcopy
    debts = sorted(deepcopy(debts), key=lambda d: float(d["remaining_balance"]))
    return _payoff_schedule_impl(debts, extra_payment, as_of_date, "snowball")


def payoff_schedule_avalanche(
    debts: list[dict],
    extra_payment: Decimal,
    as_of_date: date,
) -> tuple[date, Decimal, Decimal, list[dict]]:
    """Sort by interest_rate_apr descending; pay minimums, apply extra to highest APR."""
    from copy import deepcopy
    debts = sorted(
        deepcopy(debts),
        key=lambda d: -float(d.get("interest_rate_apr", 0)),
    )
    return _payoff_schedule_impl(debts, extra_payment, as_of_date, "avalanche")


def _payoff_schedule_impl(
    debts: list[dict],
    extra_payment: Decimal,
    as_of_date: date,
    strategy: str,
) -> tuple[date, Decimal, Decimal, list[dict]]:
    from datetime import date as dt_date
    from calendar import monthrange
    total_interest = Decimal(0)
    monthly_schedule: list[dict] = []
    month = as_of_date
    extra_remaining = extra_payment
    while any(float(d.get("remaining_balance", 0)) > 0 for d in debts):
        month_total_payment = Decimal(0)
        month_total_interest = Decimal(0)
        for d in debts:
            bal = Decimal(str(d.get("remaining_balance", 0)))
            if bal <= 0:
                continue
            apr = Decimal(str(d.get("interest_rate_apr", 0)))
            emi = Decimal(str(d.get("emi_monthly", 0)))
            interest = _monthly_interest(bal, apr)
            month_total_interest += interest
            principal = emi - interest
            if principal > bal:
                principal = bal
            payment = interest + principal
            month_total_payment += payment
            bal -= principal
            if extra_remaining > 0 and bal > 0:
                ex = min(extra_remaining, bal)
                principal += ex
                payment += ex
                bal -= ex
                extra_remaining -= ex
            d["remaining_balance"] = max(Decimal(0), bal)
        total_interest += month_total_interest
        monthly_schedule.append({
            "month": f"{month.year}-{month.month:02d}",
            "payment": float(month_total_payment),
            "interest": float(month_total_interest),
            "principal": float(month_total_payment - month_total_interest),
            "balance": float(sum(Decimal(str(d.get("remaining_balance", 0))) for d in debts)),
        })
        extra_remaining = extra_payment
        # next month
        if month.month == 12:
            month = dt_date(month.year + 1, 1, 1)
        else:
            month = dt_date(month.year, month.month + 1, 1)
        if len(monthly_schedule) > 600:
            break
    debt_free_date = month
    interest_saved = Decimal(0)
    return debt_free_date, total_interest, interest_saved, monthly_schedule
