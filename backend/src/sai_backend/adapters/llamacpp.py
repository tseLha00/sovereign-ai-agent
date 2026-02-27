import subprocess
import time
from pathlib import Path

from .base import LLMAdapter


class LlamaCppAdapter(LLMAdapter):
    def __init__(
        self,
        model_path: str = "models/Apertus-8B-Instruct-2509-Q4_K_M.gguf",
        cli_bin: str = "llama-cli",
    ) -> None:
        self.model_path = model_path
        self.cli_bin = cli_bin
        self.repo_root = Path(__file__).resolve().parents[4]

    def _build_prompt(self, messages: list[dict]) -> str:
        parts: list[str] = []

        latest_system: str | None = None
        non_system_messages: list[dict] = []

        for msg in messages:
            role = str(msg.get("role", "user")).strip().lower()
            content = str(msg.get("content", "")).strip()
            if not content:
                continue

            if role == "system":
                latest_system = content
            else:
                non_system_messages.append({"role": role, "content": content})

        if latest_system:
            parts.append(f"SYSTEM: {latest_system}")

        # Keep only recent turns to reduce prompt echo / repeated history.
        trimmed = non_system_messages[-6:]

        for msg in trimmed:
            role = msg["role"]
            content = msg["content"]

            if role == "user":
                parts.append(f"USER: {content}")
            elif role == "assistant":
                parts.append(f"ASSISTANT: {content}")

        parts.append("ASSISTANT:")
        return "\n".join(parts)

    def _resolve_model_path(self) -> Path:
        model = Path(self.model_path)
        if model.is_absolute():
            return model
        return self.repo_root / model

    def chat(
        self,
        *,
        model: str,
        messages: list[dict],
        temperature: float | None,
        max_tokens: int | None,
        stream: bool,
    ) -> dict:
        if stream:
            raise RuntimeError(
                "Streaming is not supported by LlamaCppAdapter in the current implementation."
            )

        resolved_model = self._resolve_model_path()
        if not resolved_model.exists():
            raise FileNotFoundError(f"Model file not found: {resolved_model}")

        prompt = self._build_prompt(messages)
        temp = 0.7 if temperature is None else float(temperature)
        n_predict = 256 if max_tokens is None else int(max_tokens)

        cmd = [
            self.cli_bin,
            "-m",
            str(resolved_model),
            "-p",
            prompt,
            "-n",
            str(n_predict),
            "--temp",
            str(temp),
            "--single-turn",
            "--no-display-prompt",
            "--simple-io",
        ]

        started = time.time()

        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.repo_root),
                check=False,
                timeout=180,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("llama.cpp request timed out after 180 seconds") from exc

        created = int(time.time())

        if completed.returncode != 0:
            err = (
                completed.stderr.strip()
                or completed.stdout.strip()
                or "llama.cpp execution failed"
            )
            raise RuntimeError(err)

        raw_output = "\n".join(
            part for part in [completed.stdout, completed.stderr] if part
        ).strip()

        extracted = self._extract_assistant_text(raw_output)
        normalized = self._normalize_content(extracted)
        deduped = self._remove_repeated_history(normalized, messages)

        # Most important stability rule:
        # prefer deduped if it still contains something,
        # otherwise fall back to normalized, and only then to a safe message.
        final_content = deduped or normalized
        if not final_content:
            final_content = (
                "I'm sorry, I couldn't produce a clean response for that request. "
                "Please try rephrasing your question."
            )

        return {
            "id": f"chatcmpl-{int(started * 1000)}",
            "object": "chat.completion",
            "created": created,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": final_content,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,
            },
        }

    @staticmethod
    def _extract_assistant_text(raw_output: str) -> str:
        text = raw_output.replace("\r\n", "\n").replace("\r", "\n")

        skip_prefixes = (
            "ggml_",
            "build",
            "model",
            "modalities",
            "available commands:",
            "Loading model...",
            "llama_memory_breakdown_print:",
            "llama_",
            "common_",
            "srv    ",
        )

        skip_exact = {
            "/exit or Ctrl+C     stop or exit",
            "/regen              regenerate the last response",
            "/clear              clear the chat history",
            "/read               add a text file",
            "Exiting...",
            ">",
        }

        cleaned_lines: list[str] = []

        for line in text.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            # Skip banner / ASCII art
            if "▄▄" in stripped or "██" in stripped or "▀▀" in stripped:
                continue

            if stripped in skip_exact:
                continue

            if any(stripped.startswith(prefix) for prefix in skip_prefixes):
                continue

            cleaned_lines.append(stripped)

        cleaned_text = "\n".join(cleaned_lines).strip()

        # If llama echoed prompt roles, keep only the text after the LAST ASSISTANT marker.
        if "ASSISTANT:" in cleaned_text:
            cleaned_text = cleaned_text.rsplit("ASSISTANT:", 1)[-1].strip()

        final_lines: list[str] = []

        for line in cleaned_text.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            # stop at timing footer if it appears
            if stripped.startswith("[ Prompt:"):
                break

            # remove any echoed prompt lines after split
            if stripped.startswith(">"):
                continue
            if stripped.startswith("USER:"):
                continue
            if stripped.startswith("SYSTEM:"):
                continue
            if stripped == "ASSISTANT:":
                continue
            if stripped == "Exiting...":
                continue

            final_lines.append(stripped)

        return "\n".join(final_lines).strip()

    @staticmethod
    def _normalize_content(content: str) -> str:
        if not content:
            return ""

        cleaned = content.strip()

        for prefix in ("ASSISTANT:", "Assistant:"):
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()

        while "\n\n\n" in cleaned:
            cleaned = cleaned.replace("\n\n\n", "\n\n")

        return cleaned.strip()

    @staticmethod
    def _remove_repeated_history(content: str, messages: list[dict]) -> str:
        if not content:
            return ""

        cleaned = content.strip()

        previous_assistant_messages = [
            str(m.get("content", "")).strip()
            for m in messages
            if str(m.get("role", "")).lower() == "assistant"
            and str(m.get("content", "")).strip()
        ]

        for old in reversed(previous_assistant_messages):
            old_clean = old.strip()
            if not old_clean:
                continue

            # If the new answer starts with an older assistant reply,
            # remove that prefix only if something remains afterwards.
            if cleaned.startswith(old_clean):
                candidate = cleaned[len(old_clean):].lstrip(" \n:-")
                if candidate:
                    cleaned = candidate

        return cleaned.strip()