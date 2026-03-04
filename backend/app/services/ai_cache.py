"""In-memory cache for AI responses. Key = hash(payload + prompt_version + mode)."""
import hashlib
import json
from datetime import datetime, timedelta
from typing import Any

_cache: dict[str, tuple[Any, datetime]] = {}
TTL_DAYS = 7
TTL_DAILY = 1


def _hash_key(payload: dict, prompt_version: str, mode: str) -> str:
    blob = json.dumps(payload, sort_keys=True) + prompt_version + mode
    return hashlib.sha256(blob.encode()).hexdigest()


def get(payload: dict, prompt_version: str, mode: str) -> Any | None:
    k = _hash_key(payload, prompt_version, mode)
    if k not in _cache:
        return None
    val, expires = _cache[k]
    if datetime.utcnow() > expires:
        del _cache[k]
        return None
    return val


def set(payload: dict, prompt_version: str, mode: str, value: Any, ttl_days: float = TTL_DAYS) -> None:
    k = _hash_key(payload, prompt_version, mode)
    _cache[k] = (value, datetime.utcnow() + timedelta(days=ttl_days))
