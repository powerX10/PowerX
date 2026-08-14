import unittest
from powerx.runtime.gpu.profiles.registry import get_gpu_profile

class ProfileTests(unittest.TestCase):
    def test_gpt_oss_20b_profile(self):
        p = get_gpu_profile("gpt-oss-20b")
        self.assertEqual(p.model_ref, "openai/gpt-oss-20b")
        self.assertGreaterEqual(p.min_vram_gb, 16)

    def test_vllm_args(self):
        p = get_gpu_profile("qwen-8b")
        args = p.vllm_args(host="127.0.0.1", port=8101)
        self.assertIn("serve", args)
        self.assertIn("8101", args)

if __name__ == "__main__":
    unittest.main()
