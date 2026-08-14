import unittest
from unittest.mock import patch
from powerx.runtime_mobile.device.capability import DeviceCapability, recommended_mobile_tier


class DeviceTests(unittest.TestCase):
    def test_12gb_device(self):
        cap = DeviceCapability("Linux", "aarch64", 12288, 8000, 10000, True)
        self.assertEqual(recommended_mobile_tier(cap), "4b_quantized")

    def test_6gb_device(self):
        cap = DeviceCapability("Linux", "aarch64", 6144, 3000, 3000, True)
        self.assertEqual(recommended_mobile_tier(cap), "1b_to_3b_quantized")


if __name__ == "__main__":
    unittest.main()
