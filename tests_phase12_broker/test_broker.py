import tempfile
import unittest
from powerx.runtime_fabric.broker import JobBroker


class BrokerTests(unittest.TestCase):
    def test_submit_pull_complete(self):
        with tempfile.TemporaryDirectory() as d:
            b = JobBroker(f"{d}/broker.sqlite3")
            created = b.submit("gpu16", "image_generate", {"prompt": "x"})
            self.assertEqual(created.status, "queued")

            pulled = b.pull("gpu16")
            self.assertIsNotNone(pulled)
            self.assertEqual(pulled.id, created.id)
            self.assertEqual(pulled.status, "running")

            done = b.complete(
                pulled.id,
                ok=True,
                result={"image_b64": "abc"},
            )
            self.assertEqual(done.status, "completed")
            self.assertEqual(done.result["image_b64"], "abc")

    def test_runtime_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            b = JobBroker(f"{d}/broker.sqlite3")
            b.submit("mobile", "embedding", {"text": "a"})
            self.assertIsNone(b.pull("gpu16"))
            self.assertIsNotNone(b.pull("mobile"))


if __name__ == "__main__":
    unittest.main()
