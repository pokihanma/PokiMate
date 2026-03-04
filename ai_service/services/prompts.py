"""
Safe prompt templates. No PII; no raw DB dumps. Narrative only, no math.
"""
from typing import Any


def get_weekly_prompt(payload: dict[str, Any]) -> str:
    return f"""You are a supportive financial coach. Summarize the following aggregated financial snapshot in 2-3 short, encouraging sentences. Do not perform any calculations or give specific investment advice. Do not use the user's name or any PII.

Month: {payload.get('month', 'N/A')}
Income (total): {payload.get('income_total', 0)}
Expenses (total): {payload.get('expense_total', 0)}
Savings: {payload.get('savings', 0)}
Debt (total): {payload.get('debt_total', 0)}
Portfolio value: {payload.get('portfolio_value', 0)}
Active goals count: {payload.get('goals_count', 0)}

Provide a brief, supportive summary only."""


def get_insight_prompt(payload: dict[str, Any], focus: str) -> str:
    if focus == "debt":
        return f"""You are a supportive debt coach. In 2-3 sentences, comment on the user's debt situation based only on this aggregated data. Do not perform calculations or give specific payoff orders. Be encouraging.

Debt total: {payload.get('debt_total', 0)}
Savings: {payload.get('savings', 0)}

Brief supportive commentary only."""
    if focus == "portfolio":
        return f"""You are a supportive coach. In 2-3 sentences, comment on the user's portfolio and goals based only on this aggregated data. Do not give specific investment advice or perform calculations.

Portfolio value: {payload.get('portfolio_value', 0)}
Goals count: {payload.get('goals_count', 0)}

Brief supportive commentary only."""
    return get_weekly_prompt(payload)
