import unittest
from powerx.runtime_cpu.llamacpp.profile import LlamaCppProfile


class LlamaProfileTests(unittest.TestCase):
    def test_server_args(self):
        p = LlamaCppProfile(
            id="test",
            model_path_env="MODEL",
            served_model_name="test",
            context_size=4096,
            threads=4,
        )
        args = p.server_args(
            binary="llama-server",
            model_path="/tmp/model.gguf",
            host="127.0.0.1",
            port=8300,
        )
        self.assertEqual(args[0], "llama-server")
        self.assertIn("/tmp/model.gguf", args)
        self.assertIn("8300", args)


if __name__ == "__main__":
    unittest.main()
