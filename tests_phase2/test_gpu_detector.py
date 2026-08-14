import unittest
from unittest.mock import patch, MagicMock
from powerx.runtime.gpu.capabilities import GPUCapabilityDetector

class DetectorTests(unittest.TestCase):
    @patch("powerx.runtime.gpu.capabilities.shutil.which", return_value="/usr/bin/nvidia-smi")
    @patch("powerx.runtime.gpu.capabilities.subprocess.run")
    def test_detect(self, run, which):
        run.return_value = MagicMock(
            returncode=0,
            stdout="0, NVIDIA T4, 16384, 15000, 7.5\n"
        )
        devices = GPUCapabilityDetector.detect()
        self.assertEqual(devices[0].total_vram_mb, 16384)
        self.assertEqual(devices[0].index, 0)

if __name__ == "__main__":
    unittest.main()
