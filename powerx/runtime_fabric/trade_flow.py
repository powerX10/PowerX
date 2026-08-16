from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TradeDecision:
    allowed: bool
    status: str
    reason: str

class TradeConfirmationGate:
    def __init__(self, require_confirmation: bool = True, auto_trade: bool = False):
        self.require_confirmation = require_confirmation
        self.auto_trade = auto_trade

    def evaluate(self, confidence: float, threshold: float, user_confirmed: bool = False) -> TradeDecision:
        if confidence < threshold:
            return TradeDecision(False, "rejected", "confidence_below_threshold")
        if self.auto_trade:
            return TradeDecision(True, "approved_auto", "auto_trade_enabled")
        if self.require_confirmation and not user_confirmed:
            return TradeDecision(False, "awaiting_confirmation", "user_confirmation_required")
        return TradeDecision(True, "approved", "conditions_met")
