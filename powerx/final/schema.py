from dataclasses import dataclass, field
from typing import Any, Literal

Role = Literal["system","user","assistant","tool"]

@dataclass(frozen=True)
class Message:
    role: Role
    content: Any

@dataclass
class UnifiedInferenceRequest:
    task: str
    messages: list[Message]
    max_tokens: int = 1024
    stream: bool = False
    attachments: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class UnifiedInferenceResponse:
    ok: bool
    request_id: str
    model_id: str | None = None
    runtime: str | None = None
    text: str | None = None
    raw: dict[str, Any] | None = None
    error: str | None = None
