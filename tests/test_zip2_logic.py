import os, tempfile
from pathlib import Path
from powerx.v2.resource_probe import probe
from powerx.v2.warehouse import WarehouseClient

def test_probe():
    s=probe(".")
    assert s.cpu_count>=1
    assert s.disk_free_gb>=0

def test_local_warehouse_copy():
    with tempfile.TemporaryDirectory() as w, tempfile.TemporaryDirectory() as c:
        src=Path(w)/"PowerX/Models/demo";src.mkdir(parents=True);(src/"model.gguf").write_bytes(b"x")
        os.environ["POWERX_WAREHOUSE_ROOT"]=w
        client=WarehouseClient();dest=Path(c)/"demo"
        client.sync_to("PowerX/Models/demo",dest)
        assert (dest/"model.gguf").exists()
