import unittest
from powerx.fabric.registry import RuntimeFabricRegistry
from powerx.fabric.router import RuntimeFabricRouter
from powerx.fabric.schema import RuntimeNode
from powerx.fabric.policy import TaskProfile
class T(unittest.TestCase):
    def test_cpu_light(self):
        r=RuntimeFabricRegistry()
        r.heartbeat(RuntimeNode("cpu","cpu","http://cpu",{"chat"},{"3b","4b"},True))
        r.heartbeat(RuntimeNode("gpu","gpu16","http://gpu",{"chat"},{"6b","gpu-heavy"},vram_gb=16))
        self.assertEqual(RuntimeFabricRouter(r).resolve(TaskProfile("chat","3b",continuous=True)).id,"cpu")
    def test_gpu_heavy(self):
        r=RuntimeFabricRegistry()
        r.heartbeat(RuntimeNode("gpu","gpu16","http://gpu",{"video_generate"},{"gpu-heavy"},vram_gb=16))
        self.assertEqual(RuntimeFabricRouter(r).resolve(TaskProfile("video_generate","gpu-heavy",True)).id,"gpu")
