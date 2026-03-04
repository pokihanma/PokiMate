from app.services.financial_health_engine import financial_health_score


def test_financial_health_score():
    s = financial_health_score(
        savings_rate=0.20,
        dti_ratio=0.15,
        emergency_fund_months=4.0,
        budget_overspend_pct=0.0,
        income_stability_proxy=1.0,
    )
    assert 0 <= s <= 100
    assert s > 50  # good inputs => decent score


def test_financial_health_score_poor():
    s = financial_health_score(
        savings_rate=0.0,
        dti_ratio=0.5,
        emergency_fund_months=0,
        budget_overspend_pct=0.2,
    )
    assert 0 <= s <= 100
