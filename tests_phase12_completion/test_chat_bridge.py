import unittest
from powerx.runtime_fabric.chat_bridge import normalize_messages, chat_payload, mobile_prompt

class ChatBridgeTests(unittest.TestCase):
    def test_message_normalization(self):
        self.assertEqual(
            normalize_messages({"message": "hello"}),
            [{"role": "user", "content": "hello"}],
        )

    def test_chat_payload(self):
        p = chat_payload({"messages": [{"role": "user", "content": "hi"}], "max_tokens": 100})
        self.assertEqual(p["max_tokens"], 100)
        self.assertEqual(p["messages"][0]["content"], "hi")

    def test_mobile_prompt(self):
        text = mobile_prompt({"payload": {"messages": [{"role": "user", "content": "hello"}]}})
        self.assertIn("USER: hello", text)
        self.assertTrue(text.endswith("ASSISTANT:"))

if __name__ == "__main__":
    unittest.main()
