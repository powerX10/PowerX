import unittest
from powerx.models.catalog import list_models, get_model


class CatalogTests(unittest.TestCase):
    def test_catalog_has_models(self):
        self.assertGreaterEqual(len(list_models()), 9)

    def test_gpt_oss_20b_runtime(self):
        self.assertEqual(get_model("gpt-oss-20b").preferred_runtime, "gpu16")


if __name__ == "__main__":
    unittest.main()
