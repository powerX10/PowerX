from __future__ import annotations
from typing import Any

def normalize_messages(body: dict[str, Any]) -> list[dict[str, str]]:
    raw = body.get("messages")
    if isinstance(raw, list) and raw:
        out: list[dict[str, str]] = []
        for item in raw:
            if isinstance(item, dict):
                role = str(item.get("role") or "user")
                content = item.get("content")
                if isinstance(content, str) and content.strip():
                    out.append({"role": role, "content": content})
        if out:
            return out

    for key in ("message", "prompt", "text", "input"):
        value = body.get(key)
        if isinstance(value, str) and value.strip():
            return [{"role": "user", "content": value}]

    raise ValueError("messages/message/prompt/text/input required")


def chat_payload(body: dict[str, Any]) -> dict[str, Any]:
    return {
        "messages": normalize_messages(body),
        "max_tokens": int(body.get("max_tokens", 512)),
        "temperature": float(body.get("temperature", 0.2)),
    }


def mobile_prompt(job: dict[str, Any]) -> str:
    payload = job.get("payload") if isinstance(job, dict) else None
    if not isinstance(payload, dict):
        payload = job if isinstance(job, dict) else {}

    messages = payload.get("messages")
    if isinstance(messages, list) and messages:
        parts: list[str] = []
        for m in messages:
            if isinstance(m, dict):
                role = str(m.get("role") or "user").upper()
                content = m.get("content")
                if isinstance(content, str) and content.strip():
                    parts.append(f"{role}: {content}")
        if parts:
            parts.append("ASSISTANT:")
            return "\n".join(parts)

    for key in ("prompt", "text", "message", "input"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value

    raise ValueError("mobile inference payload contains no text")
