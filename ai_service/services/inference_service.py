"""
Inference: stub when no LLM key; otherwise call OpenAI/OpenAI-compatible API.
No math; supportive tone only.
"""
import os


def generate(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("AI_API_KEY")
    if not api_key:
        return "AI insights are not configured. Set OPENAI_API_KEY to enable narrative summaries."
    try:
        import httpx
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": 300},
            timeout=30,
        )
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return "Unable to generate insight at this time. Please try again later."
