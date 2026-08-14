from typing import Any
from powerx.core.provider_factory import build_phase1_providers
from powerx.router.router import route_task
from powerx.router.task_types import TaskType


class PowerXOrchestrator:
    def __init__(self):
        self.providers = build_phase1_providers()

    async def execute_chat(
        self,
        *,
        task: TaskType,
        messages: list[dict[str, Any]],
        max_tokens: int = 1024,
    ) -> dict[str, Any]:
        decision = route_task(task)

        if decision.model_id not in self.providers:
            return {
                "ok": False,
                "route": decision.__dict__,
                "error": (
                    f"Model endpoint '{decision.model_id}' is not configured yet. "
                    "Configure its OpenAI-compatible base URL in .env."
                ),
            }

        provider, actual_model_name = self.providers[decision.model_id]
        output = await provider.chat(
            model=actual_model_name,
            messages=messages,
            max_tokens=max_tokens,
        )

        return {
            "ok": True,
            "route": decision.__dict__,
            "output": output,
        }
