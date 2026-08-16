import unittest
from powerx.runtime_fabric.config import load_fabric_config
from powerx.runtime_fabric.market_loop import MarketDaemon, MarketSnapshot
from powerx.runtime_fabric.trade_flow import TradeConfirmationGate

class MarketTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load_fabric_config("config_phase12/runtime_fabric.json")

    def test_low_confidence_does_not_notify(self):
        d = MarketDaemon(self.cfg)
        snap = MarketSnapshot("TEST", 1.0, 100.0)
        self.assertIsNone(d.evaluate_scores(snap, {"price_action": .5, "risk": .6}, "long"))

    def test_high_confidence_creates_opportunity(self):
        d = MarketDaemon(self.cfg)
        snap = MarketSnapshot("TEST", 1.0, 100.0)
        opp = d.evaluate_scores(snap, {"price_action": .9, "risk": .88, "forecast": .86}, "long")
        self.assertIsNotNone(opp)
        self.assertGreaterEqual(opp.confidence, self.cfg.market.opportunity_threshold)

    def test_confirmation_required(self):
        gate = TradeConfirmationGate(require_confirmation=True, auto_trade=False)
        d = gate.evaluate(.9, .8, user_confirmed=False)
        self.assertFalse(d.allowed)
        self.assertEqual(d.status, "awaiting_confirmation")
        self.assertTrue(gate.evaluate(.9, .8, user_confirmed=True).allowed)
