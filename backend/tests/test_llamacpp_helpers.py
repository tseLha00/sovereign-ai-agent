from sai_backend.adapters.llamacpp import LlamaCppAdapter


def test_normalize_content_removes_assistant_prefix():
    raw = "ASSISTANT: Hello!"
    cleaned = LlamaCppAdapter._normalize_content(raw)
    assert cleaned == "Hello!"


def test_remove_repeated_history_strips_previous_assistant_reply_prefix():
    content = "Hello! How can I help you?"
    messages = [
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "Tell me more"},
    ]
    cleaned = LlamaCppAdapter._remove_repeated_history(content, messages)
    assert cleaned == "How can I help you?"


def test_extract_assistant_text_keeps_only_last_assistant_block():
    raw_output = """
Loading model...

USER: Hi
ASSISTANT:
Hello there!
[ Prompt: 100.0 t/s | Generation: 10.0 t/s ]
Exiting...
"""
    cleaned = LlamaCppAdapter._extract_assistant_text(raw_output)
    assert "Hello there!" in cleaned
    assert "USER:" not in cleaned
    assert "[ Prompt:" not in cleaned