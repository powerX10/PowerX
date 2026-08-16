import os, unittest
from powerx.runtime_fabric.config import load_fabric_config
from powerx.runtime_fabric.scheduler import FabricScheduler, TaskIntent

class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.scheduler = FabricScheduler(load_fabric_config("config_phase12/runtime_fabric.json"))

    def test_normal_is_cpu_first(self):
        self.assertEqual(self.scheduler.runtime_order(TaskIntent("chat", "normal"))[0], "cpu")

    def test_small_mobile_task_is_mobile_first(self):
        order = self.scheduler.runtime_order(TaskIntent("embedding", "small", user_device_available=True))
        self.assertEqual(order[0], "mobile")

    def test_video_is_gpu_only(self):
        self.assertEqual(self.scheduler.runtime_order(TaskIntent("video_generate", "heavy")), ["gpu16"])

    def test_market_is_cpu_only(self):
        self.assertEqual(self.scheduler.runtime_order(TaskIntent("forecasting", "market")), ["cpu"])

    def test_cpu_provider_failover_order(self):
        nodes = self.scheduler.config.nodes_for("cpu")
        self.assertEqual([n.id for n in nodes], ["modal-cpu-primary", "beam-cpu-fallback"])
