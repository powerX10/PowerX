from dataclasses import dataclass
from powerx.router.task_types import TaskType


@dataclass(frozen=True)
class RouteDecision:
    task: TaskType
    model_id: str
    runtime: str
    reason: str


PHASE1_ROUTES: dict[TaskType, tuple[str, str]] = {
    TaskType.SIMPLE_CHAT: ("qwen-8b", "gpu16"),
    TaskType.FAST_REASONING: ("qwen-8b", "gpu16"),
    TaskType.DEEP_REASONING: ("gpt-oss-20b", "gpu16"),
    TaskType.VISION_ANALYSIS: ("vision-4b", "gpu16"),
    TaskType.CODING: ("qwen-8b", "gpu16"),
}


def route_task(task: TaskType) -> RouteDecision:
    if task not in PHASE1_ROUTES:
        raise RuntimeError(
            f"Task '{task.value}' belongs to a later runtime phase and is not active in Phase 1."
        )

    model_id, runtime = PHASE1_ROUTES[task]
    return RouteDecision(
        task=task,
        model_id=model_id,
        runtime=runtime,
        reason=f"PowerX automatically selected {model_id} for {task.value}.",
    )
