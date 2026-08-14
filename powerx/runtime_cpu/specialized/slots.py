from dataclasses import dataclass


@dataclass(frozen=True)
class SpecializedSlot:
    id: str
    role: str
    endpoint_env: str
    token_env: str | None = None


SPECIALIZED_SLOTS = {
    "forecast-primary": SpecializedSlot(
        "forecast-primary",
        "time-series forecasting",
        "POWERX_FORECAST_PRIMARY_URL",
    ),
    "forecast-secondary": SpecializedSlot(
        "forecast-secondary",
        "forecast cross-check",
        "POWERX_FORECAST_SECONDARY_URL",
    ),
    "embedding-small": SpecializedSlot(
        "embedding-small",
        "semantic embeddings",
        "POWERX_EMBEDDING_URL",
    ),
    "reranker-small": SpecializedSlot(
        "reranker-small",
        "retrieval reranking",
        "POWERX_RERANKER_URL",
    ),
    "guard-small": SpecializedSlot(
        "guard-small",
        "safety/guard classification",
        "POWERX_GUARD_URL",
    ),
}
