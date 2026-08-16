from pathlib import Path
from powerx.controlplane.models import ManagedModel, RuntimeBinding
from powerx.controlplane.store import ControlPlaneStore
from powerx.controlplane.resolver import DynamicRuntimeResolver

def test_dynamic_cpu_gpu_routing(tmp_path: Path):
    db = tmp_path / "db.json"
    seed = tmp_path / "seed.json"
    seed.write_text('{"version":1,"models":[]}')
    s = ControlPlaneStore(str(db), str(seed))
    s.upsert(ManagedModel(id="m", display_name="M", capabilities=["chart"], bindings=[
        RuntimeBinding(runtime_class="cpu", priority=30),
        RuntimeBinding(runtime_class="gpu16", priority=10),
    ]))
    r = DynamicRuntimeResolver(s)
    assert r.candidates("chart")[0].runtime_class == "gpu16"
    s.patch("m", {"routing": {"mode":"cpu_only","runtime_order":["cpu"],"allow_fallback":False,"max_attempts":1}})
    assert r.candidates("chart", "cpu")[0].runtime_class == "cpu"
