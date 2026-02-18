import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

from .adapters.factory import get_adapter

app = FastAPI(title="Sovereign AI Agent Backend")
adapter = get_adapter()

@app.get("/health")
def health():
    return {"status": "ok"}

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    model: str = "apertus-8b"
    messages: list[ChatMessage]
    temperature: float | None = 0.7
    max_tokens: int | None = 256
    stream: bool | None = False

@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    started = time.time()
    result = adapter.chat(
        model=req.model,
        messages=[m.model_dump() for m in req.messages],
        temperature=req.temperature,
        max_tokens=req.max_tokens,
        stream=bool(req.stream),
    )
    result.setdefault("meta", {})
    result["meta"]["latency_ms"] = int((time.time() - started) * 1000)
    return result
