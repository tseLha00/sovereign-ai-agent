import os
import logging

from .base import LLMAdapter
from .mock import MockAdapter

log = logging.getLogger("sai_backend.adapters")


def get_adapter() -> LLMAdapter:
    backend = os.getenv("LLM_BACKEND", "mock").lower().strip()

    if backend in ("", "mock"):
        return MockAdapter()

    # Sprint 1: keep behavior predictable, but do not crash the whole app silently.
    log.warning("Unsupported LLM_BACKEND=%r. Falling back to mock adapter.", backend)
    return MockAdapter()
