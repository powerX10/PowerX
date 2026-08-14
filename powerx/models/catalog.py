from dataclasses import dataclass
from typing import Literal

RuntimeClass = Literal["gpu16", "cpu", "mobile", "future_gpu80"]
Capability = Literal[
    "general_reasoning",
    "fast_reasoning",
    "vision",
    "embedding",
    "reranking",
    "forecasting",
    "guard",
    "coding",
]


@dataclass(frozen=True)
class ModelSpec:
    id: str
    display_name: str
    capability: Capability
    preferred_runtime: RuntimeClass
    model_ref: str | None
    enabled_in_phase1: bool
    notes: str


MODELS: dict[str, ModelSpec] = {
    "gpt-oss-20b": ModelSpec(
        "gpt-oss-20b",
        "gpt-oss-20b",
        "general_reasoning",
        "gpu16",
        "openai/gpt-oss-20b",
        True,
        "Primary 16GB-class reasoning model endpoint."
    ),
    "qwen-8b": ModelSpec(
        "qwen-8b",
        "Qwen 8B",
        "fast_reasoning",
        "gpu16",
        None,
        True,
        "Fast reasoning and tool-oriented secondary model."
    ),
    "vision-4b": ModelSpec(
        "vision-4b",
        "4B Vision Model",
        "vision",
        "gpu16",
        None,
        True,
        "Chart/image/document understanding slot."
    ),
    "phi-mini": ModelSpec(
        "phi-mini",
        "Phi Mini",
        "fast_reasoning",
        "mobile",
        None,
        False,
        "Activated in the later mobile-runtime phase."
    ),
    "embedding-small": ModelSpec(
        "embedding-small",
        "Small Embedding Model",
        "embedding",
        "cpu",
        None,
        False,
        "Activated in the CPU-runtime phase."
    ),
    "reranker-small": ModelSpec(
        "reranker-small",
        "Small Reranker",
        "reranking",
        "cpu",
        None,
        False,
        "Activated in the CPU-runtime phase."
    ),
    "forecast-primary": ModelSpec(
        "forecast-primary",
        "Time-Series Forecast Model",
        "forecasting",
        "cpu",
        None,
        False,
        "Activated in the CPU-runtime phase."
    ),
    "guard-small": ModelSpec(
        "guard-small",
        "Small Guard Model",
        "guard",
        "cpu",
        None,
        False,
        "Activated in the CPU-runtime phase."
    ),
    "gpt-oss-120b": ModelSpec(
        "gpt-oss-120b",
        "gpt-oss-120b",
        "general_reasoning",
        "future_gpu80",
        "openai/gpt-oss-120b",
        False,
        "Future heavy reasoning endpoint; not required for Phase 1."
    ),
}


def get_model(model_id: str) -> ModelSpec:
    try:
        return MODELS[model_id]
    except KeyError as exc:
        raise KeyError(f"Unknown PowerX model: {model_id}") from exc


def list_models() -> list[ModelSpec]:
    return list(MODELS.values())
