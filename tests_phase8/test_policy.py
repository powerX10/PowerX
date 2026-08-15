import unittest
from powerx.fabric.policy import TaskProfile,node_order
from runtime_nodes.mobile.model_policy import choose_mobile_tier
class T(unittest.TestCase):
    def test_cpu(self): self.assertEqual(node_order(TaskProfile("chat",continuous=True))[0],"cpu")
    def test_gpu(self): self.assertEqual(node_order(TaskProfile("video_generate","gpu-heavy",True))[0],"gpu16")
    def test_3b(self): self.assertEqual(choose_mobile_tier(6,4).tier,"3b")
    def test_remote(self): self.assertEqual(choose_mobile_tier(4,2).tier,"remote")
