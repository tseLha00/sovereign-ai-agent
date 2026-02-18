import time

from .base import LLMAdapter

class MockAdapter(LLMAdapter):
    def chat(self, *, model: str, messages: list[dict], temperature: float | None, max_tokens: int | None, stream: bool) -> dict:
        user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return {
            "id": f"chatcmpl-{int(time.time()*1000)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": f"Mock response. You said: {user_text}"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": None, "completion_tokens": None, "total_tokens": None},
        }
