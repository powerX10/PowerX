import unittest
from powerx.router.router import route_task
from powerx.router.task_types import TaskType


class RouterTests(unittest.TestCase):
    def test_deep_reasoning_routes_to_gpt_oss_20b(self):
        result = route_task(TaskType.DEEP_REASONING)
        self.assertEqual(result.model_id, "gpt-oss-20b")
        self.assertEqual(result.runtime, "gpu16")

    def test_vision_routes_to_vision_model(self):
        result = route_task(TaskType.VISION_ANALYSIS)
        self.assertEqual(result.model_id, "vision-4b")


if __name__ == "__main__":
    unittest.main()
