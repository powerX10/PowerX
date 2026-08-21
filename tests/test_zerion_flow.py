import unittest
from powerx.v2.zerion.schema import TradingIntent
from powerx.v2.zerion.risk import evaluate_setup
from powerx.v2.zerion.state import TradeApprovalState
class T(unittest.TestCase):
 def test_gate(self):
  i=TradingIntent('NIFTY50',10000,2000,5000);e=evaluate_setup(i,{'planned_loss':1800,'potential_reward':5600,'confidence':0.84,'required_margin':9000});self.assertTrue(e['eligible']);s=TradeApprovalState();k=s.create({});self.assertEqual(s.approve(k)['status'],'approved')
