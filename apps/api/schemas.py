from pydantic import BaseModel, Field
from powerx.router.task_types import TaskType


class ChatRequest(BaseModel):
    task: TaskType
    messages: list[dict]
    max_tokens: int = Field(default=1024, ge=1, le=8192)
