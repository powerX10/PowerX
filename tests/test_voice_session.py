import unittest
from powerx.v2.voice.session import VoiceSession
class T(unittest.TestCase):
 def test_wake(self):
  s=VoiceSession();self.assertFalse(s.feed_text('hello'));self.assertTrue(s.feed_text('hey ma open'))
