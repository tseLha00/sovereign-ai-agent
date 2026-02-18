from fastapi.testclient import TestClient
from sai_backend.main import app

client = TestClient(app)

def test_chat_completions_contract():
    payload = {"model": "apertus-8b", "messages": [{"role": "user", "content": "Hello"}]}
    r = client.post("/v1/chat/completions", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["object"] == "chat.completion"
    assert "id" in data
    assert "created" in data
    assert "model" in data
    assert isinstance(data["choices"][0]["message"]["content"], str)
