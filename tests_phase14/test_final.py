import unittest
from powerx.final_product.branding import ProductBranding
from powerx.ma.model_catalog import MODEL_IDS,MODEL_ADAPTERS
from powerx.ma.adapter_contracts import SUPPORTED_ADAPTERS
class T(unittest.TestCase):
 def test_ma_private(self):
  self.assertEqual(ProductBranding.resolve("powerx",True).assistant_name,"MA")
  self.assertNotEqual(ProductBranding.resolve("powerx",False).assistant_name,"MA")
 def test_product_brand(self):
  self.assertEqual(ProductBranding.resolve("zerion-x1").assistant_name,"Zerion AI")
 def test_20(self):
  self.assertEqual(len(MODEL_IDS),20);self.assertTrue(all(MODEL_ADAPTERS[m] in SUPPORTED_ADAPTERS for m in MODEL_IDS))
