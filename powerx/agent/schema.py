from typing import Any, Literal
from pydantic import BaseModel, Field

Capability = Literal["chat","code","research","vision","image_generate","video_generate","speech_to_text","text_to_speech","file_analyze","github"]

class Attachment(BaseModel):
    name: str
    mime_type: str
    url: str | None = None
    text: str | None = None

class AgentRequest(BaseModel):
    messages: list[dict[str, Any]]
    capability: Capability | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    max_tokens: int = Field(default=2048, ge=1, le=16384)
    allow_tools: bool = True

class AgentResponse(BaseModel):
    ok: bool
    capability: str
    model_id: str | None = None
    runtime_id: str | None = None
    output: Any = None
    tool_events: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None
