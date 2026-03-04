from decimal import Decimal
from app.services.finance_engine import spending_by_category, budget_utilization


def test_spending_by_category():
    tx = [
        {"date": "2026-03-05", "type": "expense", "category_id": 1, "amount": 100},
        {"date": "2026-03-10", "type": "expense", "category_id": 1, "amount": 50},
        {"date": "2026-03-15", "type": "income", "category_id": 2, "amount": 200},
    ]
    out = spending_by_category(tx, "2026-03")
    assert 1 in out
    assert out[1] == Decimal("150")
    assert 2 not in out  # income excluded


def test_budget_utilization():
    spending = {1: Decimal("80"), 2: Decimal("200")}
    budgets = [
        {"category_id": 1, "limit_amount": Decimal("100"), "category_name": "A"},
        {"category_id": 2, "limit_amount": Decimal("150"), "category_name": "B"},
    ]
    util = budget_utilization(spending, budgets)
    assert len(util) == 2
    overspend = [u for u in util if u.get("overspend")]
    assert any(u["category_id"] == 2 for u in overspend)
