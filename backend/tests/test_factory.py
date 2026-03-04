from sai_backend.adapters.factory import get_adapter
from sai_backend.adapters.mock import MockAdapter
from sai_backend.adapters.llamacpp import LlamaCppAdapter


def test_factory_returns_mock_by_default(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND", raising=False)
    adapter = get_adapter()
    assert isinstance(adapter, MockAdapter)


def test_factory_returns_mock_for_mock_setting(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "mock")
    adapter = get_adapter()
    assert isinstance(adapter, MockAdapter)


def test_factory_returns_llamacpp_when_requested(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "llamacpp")
    adapter = get_adapter()
    assert isinstance(adapter, LlamaCppAdapter)


def test_factory_falls_back_to_mock_for_unknown_backend(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "something-else")
    adapter = get_adapter()
    assert isinstance(adapter, MockAdapter)