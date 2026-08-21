import unittest
from powerx.v2.policy import PermissionPolicy
from powerx.v2.errors import PowerXPermissionError
class T(unittest.TestCase):
    def test_high_risk_requires_approval(self):
        p=PermissionPolicy(founder_mode=True)
        with self.assertRaises(PowerXPermissionError):p.check("broker_order",False)
        self.assertTrue(p.check("broker_order",True))
