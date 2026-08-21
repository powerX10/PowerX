import unittest
from powerx.v2.router_final import route_request
class T(unittest.TestCase):
 def test_routes(self):
  self.assertEqual(route_request('zerion-x1','nifty'),'zerion');self.assertEqual(route_request('bilux10','join'),'bilux_teacher');self.assertEqual(route_request('powerx','fix github repo'),'ma_autonomous_coding')
