import logging
import time
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from .adapters.factory import get_adapter
from .errors import openai_error

log = logging.getLogger("sai_backend")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="Sovereign AI Agent Backend")
adapter = get_adapter()

REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_DIR = REPO_ROOT / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="ui")

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/ui/")


@app.exception_handler(RequestValidationError)
async def validation_handler(_: Request, exc: RequestValidationError):
    log.warning("Validation error: %s", exc)
    return openai_error(
        "Invalid request body (schema validation failed).",
        status_code=422,
    )


@app.exception_handler(HTTPException)
async def http_handler(_: Request, exc: HTTPException):
    return openai_error(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(Exception)
async def unhandled_handler(_: Request, exc: Exception):
    log.exception("Unhandled server error: %s", exc)
    return openai_error(
        "Internal server error.",
        status_code=500,
        type_="server_error",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    model: str = Field(default="apertus-8b", min_length=1)
    messages: list[ChatMessage] = Field(min_length=1)
    temperature: float | None = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=256, ge=1, le=4096)
    stream: bool | None = False

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, msgs: list[ChatMessage]):
        if not msgs:
            raise ValueError("messages must not be empty")

        if not any(m.role == "user" for m in msgs):
            raise ValueError("messages must contain at least one user message")

        return msgs


@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest, response: Response):
    if req.stream:
        raise HTTPException(
            status_code=400,
            detail="stream=true is not supported in the current implementation.",
        )

    started = time.perf_counter()

    result = adapter.chat(
        model=req.model,
        messages=[m.model_dump() for m in req.messages],
        temperature=req.temperature,
        max_tokens=req.max_tokens,
        stream=False,
    )

    latency_ms = int((time.perf_counter() - started) * 1000)
    response.headers["x-backend-latency-ms"] = str(latency_ms)

    return result