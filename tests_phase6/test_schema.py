import unittest
from powerx.final.schema import Message, UnifiedInferenceRequest
class T(unittest.TestCase):
    def test_req(self):
        r=UnifiedInferenceRequest("simple_chat",[Message("user","hi")])
        self.assertEqual(r.task,"simple_chat")
if __name__=="__main__":unittest.main()
