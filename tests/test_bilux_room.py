import unittest
from powerx.v2.bilux.session import TeacherRoom
class T(unittest.TestCase):
 def test_room(self):
  r=TeacherRoom('c','ma');self.assertTrue(r.join('s',r.code))
