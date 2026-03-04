"""Call ai_service when AI_MODE != OFF. Graceful fallback when unreachable."""
import httpx
from app.config import get_settings
from app.services.ai_cache import get as cache_get, set as cache_set


def call_ai_summarize(payload: dict, prompt_version: str = "v1") -> dict | None:
    settings = get_settings()
    if settings.astra_ai_mode == "OFF":
        return None
    cached = cache_get(payload, prompt_version, settings.astra_ai_mode)
    if cached is not None:
        return cached
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(
                f"{settings.astra_ai_service_url}/ai/summarize",
                json=payload,
            )
            if r.status_code == 200:
                data = r.json()
                cache_set(payload, prompt_version, settings.astra_ai_mode, data)
                return data
    except Exception:
        pass
    return None
