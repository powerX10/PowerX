from __future__ import annotations
import json, os
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class TradingRole:
    id: str
    capability: str
    weight: float
    required: bool
    prompt: str

class TradingRoleRegistry:
    def __init__(self, path: str | None = None):
        self.path = Path(path or os.getenv("POWERX_TRADING_ROLES", "config_trading/trading_roles.json"))

    def all(self) -> list[TradingRole]:
        data = json.loads(self.path.read_text())
        return [TradingRole(**x) for x in data["roles"] if x.get("enabled", True)]
