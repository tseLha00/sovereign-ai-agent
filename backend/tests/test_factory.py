from sai_backend.adapters.factory import get_adapter
from sai_backend.adapters.mock import MockAdapter
from sai_backend.adapters.llamacpp import LlamaCppAdapter


def test_factory_returns_mock_by_default(monkeypatch):
    monkeypatch.delenv("LLM_BACKEND", raising=False)

    adapter = get_adapter()

    assert isinstance(adapter, MockAdapter)


def test_factory_returns_mock_for_unknown_backend(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "something-else")

    adapter = get_adapter()

    assert isinstance(adapter, MockAdapter)


def test_factory_returns_llamacpp_when_requested(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "llamacpp")
    monkeypatch.setenv("LLAMA_CPP_MODEL_PATH", "models/Apertus-8B-Instruct-2509-Q4_K_M.gguf")
    monkeypatch.setenv("LLAMA_CPP_BIN", "llama-cli")

    adapter = get_adapter()

    assert isinstance(adapter, LlamaCppAdapter)
    assert adapter.model_path == "models/Apertus-8B-Instruct-2509-Q4_K_M.gguf"
    assert adapter.cli_bin == "llama-cli"