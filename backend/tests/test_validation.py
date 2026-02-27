from fastapi.testclient import TestClient
from sai_backend.main import app

client = TestClient(app)


def test_chat_rejects_empty_messages():
    payload = {
        "model": "apertus-8b",
        "messages": [],
        "stream": False,
    }

    r = client.post("/v1/chat/completions", json=payload)

    assert r.status_code == 422
    data = r.json()
    assert "error" in data
    assert data["error"]["type"] == "invalid_request_error"


def test_chat_requires_at_least_one_user_message():
    payload = {
        "model": "apertus-8b",
        "messages": [
            {"role": "system", "content": "You are helpful."},
            {"role": "assistant", "content": "Hello"},
        ],
        "stream": False,
    }

    r = client.post("/v1/chat/completions", json=payload)

    assert r.status_code == 422
    data = r.json()
    assert "error" in data
    assert data["error"]["type"] == "invalid_request_error"


def test_chat_rejects_stream_true():
    payload = {
        "model": "apertus-8b",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": True,
    }

    r = client.post("/v1/chat/completions", json=payload)

    assert r.status_code == 400
    data = r.json()
    assert "error" in data
    assert data["error"]["type"] == "invalid_request_error"
    assert "not supported" in data["error"]["message"]