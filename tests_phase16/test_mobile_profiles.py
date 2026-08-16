import unittest
from powerx.mobile_profiles import choose_profile
class T(unittest.TestCase):
 def test3(self):self.assertEqual(choose_profile(6,4).id,"mobile-3b")
 def test4(self):self.assertEqual(choose_profile(8,5).id,"mobile-4b")
 def test6(self):self.assertEqual(choose_profile(12,8).id,"mobile-6b")
 def testfallback(self):self.assertIsNone(choose_profile(4,2))
