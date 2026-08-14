import unittest
from powerx.production.policy import candidate_models

class PolicyTests(unittest.TestCase):
    def test_deep_reasoning_has_gpu_and_fallback_models(self):
        models = candidate_models("deep_reasoning")
        self.assertEqual(models[0], "gpt-oss-20b")
        self.assertIn("qwen-4b-local", models)

    def test_no_trading_task(self):
        with self.assertRaises(KeyError):
            candidate_models("trade_execution")

if __name__ == "__main__":
    unittest.main()
