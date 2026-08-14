from typing import Any


MAX_MESSAGES = 128
MAX_TEXT_CHARS = 1_000_000


def validate_messages(messages: list[dict[str, Any]]) -> None:
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a non-empty list")

    if len(messages) > MAX_MESSAGES:
        raise ValueError(f"too many messages; maximum is {MAX_MESSAGES}")

    total = 0
    for message in messages:
        role = message.get("role")
        if role not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"invalid message role: {role}")

        content = message.get("content", "")
        if isinstance(content, str):
            total += len(content)

    if total > MAX_TEXT_CHARS:
        raise ValueError("request text is too large")
