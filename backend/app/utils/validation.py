def transaction_type_valid(t: str) -> bool:
    return t in ("income", "expense", "transfer")


def mood_score_valid(s: int | None) -> bool:
    return s is None or (1 <= s <= 5)
