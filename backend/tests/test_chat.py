from fastapi.testclient import TestClient
from sai_backend.main import app

client = TestClient(app)


def test_chat_completions_contract():
    payload = {
        "model": "apertus-8b",
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.2,
        "max_tokens": 32,
        "stream": False,
    }

    r = client.post("/v1/chat/completions", json=payload)

    assert r.status_code == 200

    data = r.json()

    assert data["object"] == "chat.completion"
    assert "id" in data
    assert "created" in data
    assert data["model"] == "apertus-8b"

    assert "choices" in data
    assert isinstance(data["choices"], list)
    assert len(data["choices"]) == 1

    choice = data["choices"][0]
    assert choice["index"] == 0
    assert choice["message"]["role"] == "assistant"
    assert isinstance(choice["message"]["content"], str)
    assert choice["message"]["content"].strip() != ""
    assert choice["finish_reason"] == "stop"

    assert "usage" in data

    # latency header should exist
    assert "x-backend-latency-ms" in r.headers