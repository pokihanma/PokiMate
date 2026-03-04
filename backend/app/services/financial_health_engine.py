"""
Financial health score 0-100 from ruleset_v1.json.
Factors: savings rate, debt ratio, emergency fund, budget adherence, income stability (optional).
"""
import json
import os
from pathlib import Path


def _load_ruleset() -> dict:
    path = Path(__file__).parent / "ruleset_v1.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def _score_component(value: float, thresholds: dict) -> float:
    """Map value to 0-1 score using excellent/good/fair/poor thresholds."""
    if value >= thresholds.get("excellent", 1):
        return 1.0
    if value >= thresholds.get("good", 0.5):
        return 0.75
    if value >= thresholds.get("fair", 0.25):
        return 0.5
    if value >= thresholds.get("poor", 0):
        return 0.25
    return 0.0


def financial_health_score(
    savings_rate: float,
    dti_ratio: float,
    emergency_fund_months: float | None = None,
    budget_overspend_pct: float = 0.0,
    income_stability_proxy: float = 1.0,
) -> float:
    """
    Returns 0-100 score.
    emergency_fund_months: months of expenses covered. If None, use 0 for that component.
    budget_overspend_pct: fraction of budgets overspent (0 = perfect).
    """
    rules = _load_ruleset()
    weights = rules.get("weights", {
        "savings_rate": 0.25,
        "debt_ratio": 0.25,
        "emergency_fund": 0.20,
        "budget_adherence": 0.20,
        "income_stability": 0.10,
    })
    ranges = rules.get("ranges", {})

    sr_th = ranges.get("savings_rate", {"excellent": 0.25, "good": 0.15, "fair": 0.05, "poor": 0})
    s1 = _score_component(savings_rate, sr_th)

    dti_th = ranges.get("debt_ratio_dti", {"excellent": 0.1, "good": 0.2, "fair": 0.35, "poor": 1.0})
    s2 = 1.0 - _score_component(dti_ratio, {"excellent": dti_th["poor"], "good": dti_th["fair"], "fair": dti_th["good"], "poor": dti_th["excellent"]})

    em_months = emergency_fund_months if emergency_fund_months is not None else 0
    em_th = ranges.get("emergency_months", {"excellent": 6, "good": 3, "fair": 1, "poor": 0})
    s3 = _score_component(em_months, em_th)

    bo_th = ranges.get("budget_overspend_pct", {"excellent": 0, "good": 0.05, "fair": 0.15, "poor": 1.0})
    s4 = 1.0 - _score_component(budget_overspend_pct, bo_th)

    s5 = min(1.0, income_stability_proxy)

    w = weights
    score = (
        w.get("savings_rate", 0.25) * s1
        + w.get("debt_ratio", 0.25) * s2
        + w.get("emergency_fund", 0.20) * s3
        + w.get("budget_adherence", 0.20) * s4
        + w.get("income_stability", 0.10) * s5
    )
    return round(score * 100, 1)
