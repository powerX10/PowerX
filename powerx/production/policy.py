from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionPolicy:
    runtime_order: tuple[str, ...] = ("gpu16", "cpu", "mobile")
    allow_mobile_fallback: bool = True
    allow_cpu_fallback: bool = True
    max_attempts: int = 3


TASK_MODEL_CANDIDATES: dict[str, tuple[str, ...]] = {
    "deep_reasoning": ("gpt-oss-20b", "qwen-8b", "qwen-4b-local", "phi-mini-local"),
    "simple_chat": ("qwen-8b", "qwen-4b-local", "phi-mini-local", "gemma-1b-local"),
    "fast_reasoning": ("qwen-8b", "qwen-4b-local", "phi-mini-local"),
    "coding": ("qwen-8b", "qwen-4b-local"),
    "vision_analysis": ("vision-4b",),
    "embedding": ("embedding-small",),
    "reranking": ("reranker-small",),
    "forecasting": ("forecast-primary", "forecast-secondary"),
    "safety_check": ("guard-small",),
}


def candidate_models(task: str) -> tuple[str, ...]:
    if task not in TASK_MODEL_CANDIDATES:
        raise KeyError(f"Unsupported PowerX task: {task}")
    return TASK_MODEL_CANDIDATES[task]
