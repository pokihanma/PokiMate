from datetime import date
from app.services.investment_engine import xirr, xirr_newton_raphson


def test_xirr_known_case():
    # Cashflows: -100000 at start, -10000 mid, +135000 at end (~1.5 years)
    cashflows = [
        (date(2024, 1, 1), -100000.0),
        (date(2024, 6, 1), -10000.0),
        (date(2026, 3, 1), 135000.0),
    ]
    r, method, it = xirr(cashflows)
    assert -0.99 <= r <= 2.0
    assert method in ("newton-raphson", "fallback")
    assert it >= 0


def test_xirr_insufficient():
    cashflows = [(date(2024, 1, 1), -100.0)]
    r, method, it = xirr(cashflows)
    assert r == 0.0
    assert method == "insufficient"
