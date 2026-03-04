"""In-memory cache. Key = hash; TTL in days."""
from datetime import datetime, timedelta
from typing import Any

_store: dict[str, tuple[Any, datetime]] = {}


def get_cached(key: str) -> Any | None:
    if key not in _store:
        return None
    val, expires = _store[key]
    if datetime.utcnow() > expires:
        del _store[key]
        return None
    return val


def set_cached(key: str, value: Any, ttl_days: float = 7) -> None:
    _store[key] = (value, datetime.utcnow() + timedelta(days=ttl_days))
