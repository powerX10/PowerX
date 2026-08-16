from __future__ import annotations
import json, os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class FabricNode:
    id: str
    provider: str
    runtime_class: str
    priority: int
    enabled: bool
    endpoint_env: str
    token_env: str | None = None
    always_available: bool = False

    @property
    def endpoint(self) -> str | None:
        value = os.getenv(self.endpoint_env, "").strip()
        return value or None

    @property
    def token(self) -> str | None:
        if not self.token_env:
            return None
        value = os.getenv(self.token_env, "").strip()
        return value or None

@dataclass(frozen=True)
class MarketPolicy:
    scan_interval_seconds: int = 15
    strategy_refresh_seconds: int = 300
    opportunity_threshold: float = 0.78
    high_confidence_threshold: float = 0.86
    require_user_confirmation: bool = True
    auto_trade_default: bool = False
    max_signal_age_seconds: int = 120

@dataclass(frozen=True)
class FabricConfig:
    policy: dict
    nodes: tuple[FabricNode, ...] = field(default_factory=tuple)
    market: MarketPolicy = field(default_factory=MarketPolicy)

    def nodes_for(self, runtime_class: str) -> list[FabricNode]:
        return sorted(
            [n for n in self.nodes if n.enabled and n.runtime_class == runtime_class],
            key=lambda n: n.priority,
        )


def load_fabric_config(path: str | None = None) -> FabricConfig:
    p = Path(path or os.getenv("POWERX_FABRIC_CONFIG", "config_phase12/runtime_fabric.json"))
    data = json.loads(p.read_text())
    nodes = tuple(FabricNode(**x) for x in data.get("nodes", []))
    market = MarketPolicy(**data.get("market", {}))
    return FabricConfig(policy=dict(data.get("policy", {})), nodes=nodes, market=market)
