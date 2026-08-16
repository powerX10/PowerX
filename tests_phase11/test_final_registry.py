import json, tempfile, unittest
from pathlib import Path
from powerx.controlplane.store import ControlPlaneStore
from powerx.final_runtime.registry_sync import FinalRegistrySync

class FinalRegistryTests(unittest.TestCase):
    def test_exact_twenty_seed_models_and_dynamic_bindings(self):
        seed=Path("config_final/model_registry_20.json")
        data=json.loads(seed.read_text())
        self.assertEqual(20,len(data["models"]))
        self.assertTrue(all(m["bindings"] for m in data["models"]))
        self.assertTrue(all("routing" in m for m in data["models"]))

    def test_sync_preserves_cms_runtime_overrides(self):
        with tempfile.TemporaryDirectory() as td:
            db=Path(td)/"cms.json"
            store=ControlPlaneStore(path=str(db), seed_path="config_models/powerx_models.json")
            first=store.get("qwen25-3b-general")
            first.bindings[0].priority=777
            store.upsert(first)
            out=FinalRegistrySync(store=store).sync(True)
            self.assertEqual(20,out["seed_models"])
            self.assertEqual(777,store.get("qwen25-3b-general").bindings[0].priority)

if __name__ == "__main__": unittest.main()
