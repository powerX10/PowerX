from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Callable, Iterable
from .config import FabricConfig, load_fabric_config

@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    timestamp: float
    price: float
    features: dict = field(default_factory=dict)

@dataclass(frozen=True)
class Opportunity:
    symbol: str
    confidence: float
    side: str
    rationale: tuple[str, ...]
    timestamp: float
    strategy_id: str | None = None

class MarketDaemon:
    """24x7 orchestration loop.

    Data acquisition, strategy engines and notification delivery are injected so
    Zerion can provide broker/market feeds without hard-coding any vendor here.
    """
    def __init__(self, config: FabricConfig | None = None):
        self.config = config or load_fabric_config()

    def evaluate_scores(self, snapshot: MarketSnapshot, scores: dict[str, float], side: str = "watch") -> Opportunity | None:
        if not scores:
            return None
        values = [max(0.0, min(1.0, float(v))) for v in scores.values()]
        confidence = sum(values) / len(values)
        if confidence < self.config.market.opportunity_threshold:
            return None
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        rationale = tuple(f"{k}:{v:.3f}" for k, v in ranked[:6])
        return Opportunity(snapshot.symbol, confidence, side, rationale, snapshot.timestamp)

    def run_forever(
        self,
        snapshots: Callable[[], Iterable[MarketSnapshot]],
        analyze: Callable[[MarketSnapshot], tuple[dict[str, float], str]],
        notify: Callable[[Opportunity], None],
        stop: Callable[[], bool] | None = None,
    ) -> None:
        stop = stop or (lambda: False)
        while not stop():
            for snap in snapshots():
                scores, side = analyze(snap)
                opp = self.evaluate_scores(snap, scores, side)
                if opp:
                    notify(opp)
            time.sleep(max(1, self.config.market.scan_interval_seconds))
