from dataclasses import dataclass
from typing import Optional, Dict

from powerx.models.registry import get_model


@dataclass
class RouteDecision:
    model_id: str
    provider: str
    compute: str
    reason: str
    fallback_provider: Optional[str] = None


TASK_ROUTES: Dict[str, str] = {
    "chief_reasoning": "gpt-oss-120b",
    "deep_research": "gpt-oss-120b",
    "financial_research": "fingpt",
    "institutional_research": "finrobot",
    "forecast": "timesfm",
    "multivariate_forecast": "chronos-2",
    "probabilistic_forecast": "moirai",
    "long_horizon_forecast": "time-moe",
    "chart_analysis": "qwen3-vl",
    "strategy_code": "qwen3-coder",
    "rl_trading": "finrl",
    "technical_analysis": "technical-analysis-agent",
    "market_structure": "market-structure-agent",
    "risk_management": "risk-portfolio-agent",
    "fundamental_macro": "fundamental-macro-agent",
    "sentiment_event": "sentiment-event-agent",
    "orderbook_liquidity": "orderbook-liquidity-agent",
    "strategy_creation": "strategy-architect-agent",
    "opportunity_detection": "opportunity-consensus-agent",
    "trade_execution": "execution-agent",
}


def route_task(
    task_type: str,
    *,
    prefer_device: bool = False,
    gpu_available: bool = True,
    beam_available: bool = True,
    modal_available: bool = True,
) -> RouteDecision:
    if task_type not in TASK_ROUTES:
        task_type = "chief_reasoning"

    model_id = TASK_ROUTES[task_type]
    model = get_model(model_id)

    provider = model.preferred_provider
    fallback = model.fallback_providers[0] if model.fallback_providers else None

    if prefer_device and model.device_capable:
        return RouteDecision(
            model_id=model.id,
            provider="device",
            compute="device",
            reason="Device-capable model selected for local execution.",
            fallback_provider=provider,
        )

    if provider == "beam" and not beam_available:
        provider = fallback or "modal"

    if provider == "modal" and not modal_available:
        provider = fallback or "beam"

    if model.preferred_compute in {"gpu", "16gb_gpu", "80gb_gpu", "multi_gpu"} and not gpu_available:
        for candidate in model.fallback_providers:
            if candidate == "cpu":
                provider = "cpu"
                break

    return RouteDecision(
        model_id=model.id,
        provider=provider,
        compute=model.preferred_compute,
        reason=f"Task '{task_type}' routed to {model.name}.",
        fallback_provider=fallback,
    )
