from sai_backend.adapters.llamacpp import LlamaCppAdapter


def test_extract_assistant_text_from_cli_output():
    raw_output = """
Loading model...

build      : b8070-cc45f2ada
model      : Apertus-8B-Instruct-2509-Q4_K_M.gguf
modalities : text

> USER: Say hello in one sentence.
ASSISTANT:

Hello!

[ Prompt: 105.6 t/s | Generation: 20.2 t/s ]

Exiting...
"""

    content = LlamaCppAdapter._extract_assistant_text(raw_output)

    assert content == "Hello!"


def test_normalize_content_removes_assistant_prefix():
    content = LlamaCppAdapter._normalize_content("ASSISTANT: Hello!")
    assert content == "Hello!"


def test_remove_repeated_history_strips_old_prefix():
    messages = [
        {"role": "assistant", "content": "Hello!"},
    ]

    content = "Hello!\nHow can I help you today?"
    cleaned = LlamaCppAdapter._remove_repeated_history(content, messages)

    assert cleaned == "How can I help you today?"


def test_remove_repeated_history_returns_empty_if_exact_repeat():
    messages = [
        {"role": "assistant", "content": "Hello!"},
    ]

    content = "Hello!"
    cleaned = LlamaCppAdapter._remove_repeated_history(content, messages)

    assert cleaned == ""