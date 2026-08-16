import unittest
from powerx.ma.model_catalog import MODEL_IDS,MODEL_ADAPTERS
from powerx.ma.adapter_contracts import SUPPORTED_ADAPTERS
from powerx.ma.planner import MAPlanner
from powerx.ma.schema import MARequest
class T(unittest.TestCase):
    def test_20(self):
        self.assertEqual(len(MODEL_IDS),20);self.assertEqual(set(MODEL_IDS),set(MODEL_ADAPTERS))
        self.assertTrue(all(a in SUPPORTED_ADAPTERS for a in MODEL_ADAPTERS.values()))
    def test_image(self):self.assertEqual(MAPlanner().plan(MARequest(text="generate image"))[0].model_ids,["sdxl-base"])
