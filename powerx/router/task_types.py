from enum import StrEnum


class TaskType(StrEnum):
    SIMPLE_CHAT = "simple_chat"
    DEEP_REASONING = "deep_reasoning"
    FAST_REASONING = "fast_reasoning"
    VISION_ANALYSIS = "vision_analysis"
    CODING = "coding"
    EMBEDDING = "embedding"
    RERANKING = "reranking"
    FORECASTING = "forecasting"
    SAFETY_CHECK = "safety_check"
