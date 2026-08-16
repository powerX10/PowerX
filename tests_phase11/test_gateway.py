import tempfile, unittest
from pathlib import Path
from powerx.controlplane.store import ControlPlaneStore
from powerx.final_runtime.registry_sync import FinalRegistrySync
from powerx.final_runtime.gateway import DynamicInferenceGateway

class GatewayTests(unittest.IsolatedAsyncioTestCase):
    async def test_financial_sentiment_has_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            store=ControlPlaneStore(path=str(Path(td)/"cms.json"), seed_path="config_models/powerx_models.json")
            FinalRegistrySync(store=store).sync(False)
            g=DynamicInferenceGateway(store)
            x=await g.candidates("financial_sentiment")
            self.assertGreaterEqual(len(x),3)

    async def test_media_is_gpu_preferred(self):
        with tempfile.TemporaryDirectory() as td:
            store=ControlPlaneStore(path=str(Path(td)/"cms.json"), seed_path="config_models/powerx_models.json")
            FinalRegistrySync(store=store).sync(False)
            g=DynamicInferenceGateway(store)
            x=await g.candidates("image_generate")
            self.assertTrue(x)
            self.assertEqual("gpu16",x[0]["runtime_class"])

if __name__ == "__main__": unittest.main()
