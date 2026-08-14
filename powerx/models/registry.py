from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class ModelSpec:
    id: str
    name: str
    role: str
    category: str
    kind: str
    parameters: Optional[str]
    preferred_compute: str
    preferred_provider: str
    fallback_providers: List[str] = field(default_factory=list)
    min_vram_gb: Optional[int] = None
    min_ram_gb: Optional[int] = None
    device_capable: bool = False
    always_on: bool = False
    production_enabled: bool = True
    notes: str = ""


MODELS = {
    # 1
    "gpt-oss-120b": ModelSpec(
        id="gpt-oss-120b",
        name="OpenAI gpt-oss-120b",
        role="chief_reasoning",
        category="reasoning",
        kind="foundation_model",
        parameters="120B",
        preferred_compute="80gb_gpu",
        preferred_provider="modal",
        fallback_providers=["beam"],
        min_vram_gb=80,
        notes="Chief Zerion/PowerX reasoning brain; final consensus, complex research and tool orchestration."
    ),

    # 2
    "qwen3-235b-a22b": ModelSpec(
        id="qwen3-235b-a22b",
        name="Qwen3 235B-A22B",
        role="second_heavy_reasoner",
        category="reasoning",
        kind="foundation_model",
        parameters="235B MoE / 22B active",
        preferred_compute="multi_gpu",
        preferred_provider="beam",
        fallback_providers=["modal"],
        notes="Independent heavy second opinion for difficult reasoning and agentic tasks."
    ),

    # 3
    "fingpt": ModelSpec(
        id="fingpt",
        name="FinGPT",
        role="financial_language_intelligence",
        category="finance",
        kind="financial_model_family",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="beam",
        fallback_providers=["modal", "cpu"],
        notes="Financial NLP, sentiment, reports, news and finance-domain analysis."
    ),

    # 4
    "finrobot": ModelSpec(
        id="finrobot",
        name="FinRobot",
        role="institutional_financial_research",
        category="finance_agents",
        kind="agent_framework",
        parameters=None,
        preferred_compute="cpu_plus_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Financial multi-agent research, valuation and analyst-style workflows."
    ),

    # 5
    "timesfm": ModelSpec(
        id="timesfm",
        name="TimesFM",
        role="time_series_forecasting",
        category="forecasting",
        kind="time_series_foundation_model",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Forecasts price, volume, volatility and other market time series."
    ),

    # 6
    "chronos-2": ModelSpec(
        id="chronos-2",
        name="Chronos-2",
        role="multivariate_forecasting",
        category="forecasting",
        kind="time_series_foundation_model",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Independent multivariate/covariate forecasting and confirmation."
    ),

    # 7
    "moirai": ModelSpec(
        id="moirai",
        name="Moirai",
        role="probabilistic_forecasting",
        category="forecasting",
        kind="time_series_foundation_model",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Probabilistic time-series forecasts and uncertainty estimation."
    ),

    # 8
    "time-moe": ModelSpec(
        id="time-moe",
        name="Time-MoE",
        role="long_horizon_market_forecasting",
        category="forecasting",
        kind="time_series_model",
        parameters="up to ~2.4B",
        preferred_compute="16gb_gpu",
        preferred_provider="beam",
        fallback_providers=["modal", "cpu"],
        notes="Additional large time-series specialist for long-sequence forecasting."
    ),

    # 9
    "qwen3-vl": ModelSpec(
        id="qwen3-vl",
        name="Qwen3-VL",
        role="chart_and_visual_analysis",
        category="vision",
        kind="vision_language_model",
        parameters=None,
        preferred_compute="gpu",
        preferred_provider="beam",
        fallback_providers=["modal"],
        notes="Charts, screenshots, dashboards and visual market-structure understanding."
    ),

    # 10
    "qwen3-coder": ModelSpec(
        id="qwen3-coder",
        name="Qwen3-Coder",
        role="strategy_and_code_generation",
        category="coding",
        kind="coding_model",
        parameters=None,
        preferred_compute="gpu",
        preferred_provider="beam",
        fallback_providers=["modal"],
        notes="Creates indicators, trading strategies, backtest logic, tools and integration code."
    ),

    # 11
    "finrl": ModelSpec(
        id="finrl",
        name="FinRL",
        role="reinforcement_learning_trading",
        category="quant_trading",
        kind="rl_framework",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        notes="RL trading policies, portfolio allocation and adaptive strategy research."
    ),

    # 12
    "technical-analysis-agent": ModelSpec(
        id="technical-analysis-agent",
        name="PowerX Technical Analysis Agent",
        role="technical_analysis",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Indicators, momentum, trend, volatility, support/resistance and deterministic TA calculations."
    ),

    # 13
    "market-structure-agent": ModelSpec(
        id="market-structure-agent",
        name="PowerX Market Structure Agent",
        role="price_action_and_liquidity",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Price action, BOS/CHoCH, liquidity sweeps, structure, breakout/retest and regime analysis."
    ),

    # 14
    "risk-portfolio-agent": ModelSpec(
        id="risk-portfolio-agent",
        name="PowerX Risk & Portfolio Agent",
        role="risk_management",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Position sizing, leverage, drawdown, exposure, stop-loss, take-profit and liquidation risk."
    ),

    # 15
    "fundamental-macro-agent": ModelSpec(
        id="fundamental-macro-agent",
        name="PowerX Fundamental & Macro Agent",
        role="fundamental_and_macro_analysis",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_finance_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Macro events, fundamentals, rates, inflation, earnings and cross-asset context."
    ),

    # 16
    "sentiment-event-agent": ModelSpec(
        id="sentiment-event-agent",
        name="PowerX Sentiment & Event Agent",
        role="market_sentiment_and_events",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_finance_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="News/event sentiment, narrative shifts, event risk and market reaction analysis."
    ),

    # 17
    "orderbook-liquidity-agent": ModelSpec(
        id="orderbook-liquidity-agent",
        name="PowerX Order Book & Liquidity Agent",
        role="orderbook_and_microstructure",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_or_gpu",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Bid/ask depth, imbalance, spreads, liquidity, slippage and market microstructure."
    ),

    # 18
    "strategy-architect-agent": ModelSpec(
        id="strategy-architect-agent",
        name="PowerX Strategy Architect",
        role="strategy_creation",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="gpu",
        preferred_provider="beam",
        fallback_providers=["modal"],
        notes="Turns natural-language requests into strategy rules, backtests, revisions and deployable templates."
    ),

    # 19
    "opportunity-consensus-agent": ModelSpec(
        id="opportunity-consensus-agent",
        name="PowerX Opportunity & Consensus Agent",
        role="opportunity_detection",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu_plus_llm",
        preferred_provider="cpu",
        fallback_providers=["beam", "modal"],
        always_on=True,
        notes="Combines scanner outputs, triggers deeper analysis and creates candidate trade opportunities."
    ),

    # 20
    "execution-agent": ModelSpec(
        id="execution-agent",
        name="PowerX Execution Agent",
        role="validated_trade_execution",
        category="zerion_agent",
        kind="custom_agent",
        parameters=None,
        preferred_compute="cpu",
        preferred_provider="cpu",
        fallback_providers=[],
        always_on=True,
        notes="Handles approved order workflow, deterministic validation and broker execution orchestration."
    ),
}


def get_model(model_id: str) -> ModelSpec:
    try:
        return MODELS[model_id]
    except KeyError as exc:
        raise KeyError(f"Unknown PowerX model/agent: {model_id}") from exc


def list_models() -> List[ModelSpec]:
    return list(MODELS.values())


def list_by_category(category: str) -> List[ModelSpec]:
    return [m for m in MODELS.values() if m.category == category]


def list_always_on() -> List[ModelSpec]:
    return [m for m in MODELS.values() if m.always_on]
