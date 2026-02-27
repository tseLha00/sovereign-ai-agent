from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def chat(
        self,
        *,
        model: str,
        messages: list[dict],
        temperature: float | None,
        max_tokens: int | None,
        stream: bool,
    ) -> dict:
        raise NotImplementedError