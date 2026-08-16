from __future__ import annotations
from pydantic import BaseModel, Field

class TradingRequest(BaseModel):
    symbol: str
    market: str = "auto"
    timeframe: str = "auto"
    query: str
    user_level: str = "beginner"
    chart_image_url: str | None = None
    price_data: list[dict] = Field(default_factory=list)
    indicators: dict = Field(default_factory=dict)
    fundamentals: dict = Field(default_factory=dict)
    news: list[dict] = Field(default_factory=list)
    derivatives: dict = Field(default_factory=dict)
    portfolio: dict = Field(default_factory=dict)

class AgentFinding(BaseModel):
    role: str
    model_id: str | None = None
    stance: str = "neutral"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    summary: str
    evidence: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    raw: dict = Field(default_factory=dict)

class TradingReport(BaseModel):
    symbol: str
    market: str
    timeframe: str
    consensus: str
    confidence: float = Field(ge=0.0, le=1.0)
    beginner_explanation: str
    findings: list[AgentFinding]
    conflicts: list[str] = Field(default_factory=list)
    risk_controls: dict = Field(default_factory=dict)
    actionability: str = "analysis_only"
