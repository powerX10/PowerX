import unittest
from powerx.runtime_cpu.specialized.slots import SPECIALIZED_SLOTS
from powerx.runtime_mobile.model_slots import MOBILE_MODEL_SLOTS


class SlotTests(unittest.TestCase):
    def test_specialized_slots(self):
        self.assertIn("forecast-primary", SPECIALIZED_SLOTS)
        self.assertIn("embedding-small", SPECIALIZED_SLOTS)

    def test_mobile_slots(self):
        self.assertIn("mobile-primary", MOBILE_MODEL_SLOTS)


if __name__ == "__main__":
    unittest.main()
