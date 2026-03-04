from pydantic import BaseModel
from typing import Optional


class AIInsightResponse(BaseModel):
    summary: str
    cached_at: Optional[str] = None
