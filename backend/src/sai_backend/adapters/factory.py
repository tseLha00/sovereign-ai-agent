import logging
import os

from .base import LLMAdapter
from .llamacpp import LlamaCppAdapter
from .mock import MockAdapter

log = logging.getLogger("sai_backend.adapters")


def get_adapter() -> LLMAdapter:
    backend = os.getenv("LLM_BACKEND", "mock").lower().strip()

    if backend in ("", "mock"):
        return MockAdapter()

    if backend in ("llamacpp", "llama.cpp", "llama_cpp"):
        model_path = os.getenv(
            "LLAMA_CPP_MODEL_PATH",
            "models/Apertus-8B-Instruct-2509-Q4_K_M.gguf",
        )
        cli_bin = os.getenv("LLAMA_CPP_BIN", "llama-cli")
        return LlamaCppAdapter(model_path=model_path, cli_bin=cli_bin)

    log.warning("Unsupported LLM_BACKEND=%r. Falling back to mock adapter.", backend)
    return MockAdapter()