import os

from .base import LLMAdapter
from .mock import MockAdapter


def get_adapter() -> LLMAdapter:
    backend = os.getenv("LLM_BACKEND", "mock").lower()
    if backend == "mock":
        return MockAdapter()
    # placeholder for real runtime later
    return MockAdapter()
