"""
Input sanitization: no PII, no raw DB dumps, no prompts injection.
"""
from typing import Any


def sanitize_input(payload: dict[str, Any]) -> None:
    """Mutate payload to remove or cap any risky fields. Allow only expected aggregates."""
    allowed_keys = {"month", "income_total", "expense_total", "savings", "debt_total", "portfolio_value", "goals_count", "focus"}
    for k in list(payload.keys()):
        if k not in allowed_keys:
            payload.pop(k, None)
    for k in payload:
        if isinstance(payload[k], str) and len(payload[k]) > 500:
            payload[k] = (payload[k][:500] + "...")
        if isinstance(payload[k], (int, float)) and (payload[k] > 1e15 or payload[k] < -1e15):
            payload[k] = 0
