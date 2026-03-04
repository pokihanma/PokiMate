from datetime import date
from decimal import Decimal
from app.services.debt_engine import (
    debt_to_income_ratio,
    debt_stress_index,
    payoff_schedule_avalanche,
    payoff_schedule_snowball,
)


def test_dti():
    assert debt_to_income_ratio(Decimal("20000"), Decimal("100000")) == 0.2
    assert debt_to_income_ratio(Decimal("0"), Decimal("100000")) == 0.0


def test_stress_index():
    s = debt_stress_index(0.2, 2, 0.0)
    assert 0 <= s <= 1.0


def test_payoff_schedule():
    debts = [
        {"remaining_balance": Decimal("100000"), "interest_rate_apr": Decimal("12"), "emi_monthly": Decimal("5000")},
        {"remaining_balance": Decimal("50000"), "interest_rate_apr": Decimal("24"), "emi_monthly": Decimal("3000")},
    ]
    d1, ti, saved, schedule = payoff_schedule_avalanche(debts, Decimal("2000"), date(2026, 3, 1))
    assert d1 >= date(2026, 3, 1)
    assert ti >= 0
    assert len(schedule) >= 1
