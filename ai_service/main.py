"""
Pokimate AI service. Accepts sanitized payloads only; returns narrative (no math).
POST /ai/summarize, /ai/insights. Cache by hash(payload + prompt_version + mode).
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import hashlib
import json
import os
from datetime import datetime, timedelta

from services.prompts import get_weekly_prompt, get_insight_prompt
from services.safety import sanitize_input
from services.cache_service import get_cached, set_cached
from services.inference_service import generate

app = FastAPI(title="Pokimate AI Service", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class SummarizeRequest(BaseModel):
    month: str | None = None
    income_total: float = 0
    expense_total: float = 0
    savings: float = 0
    debt_total: float = 0
    portfolio_value: float = 0
    goals_count: int = 0
    focus: str | None = None


@app.post("/ai/summarize")
def ai_summarize(body: SummarizeRequest):
    payload = body.model_dump()
    sanitize_input(payload)
    prompt_version = "v1"
    mode = os.environ.get("AI_MODE", "LIGHT")
    cache_key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode() + prompt_version.encode() + mode.encode()).hexdigest()
    cached = get_cached(cache_key)
    if cached is not None:
        return {"summary": cached, "cached_at": None}
    prompt = get_weekly_prompt(payload) if body.focus != "debt" and body.focus != "portfolio" else get_insight_prompt(payload, body.focus or "summary")
    summary = generate(prompt)
    set_cached(cache_key, summary, ttl_days=7)
    return {"summary": summary, "cached_at": datetime.utcnow().isoformat() + "Z"}


@app.post("/ai/insights")
def ai_insights(body: SummarizeRequest):
    return ai_summarize(body)


@app.get("/health")
def health():
    return {"status": "ok"}
