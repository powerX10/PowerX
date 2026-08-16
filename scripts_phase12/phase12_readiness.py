#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from powerx.runtime_fabric.config import load_fabric_config
from powerx.runtime_fabric.health import check_node
from powerx.controlplane.store import ControlPlaneStore
cfg = load_fabric_config()
store = ControlPlaneStore()
health = [check_node(n).__dict__ for n in cfg.nodes]
print(json.dumps({
    "phase": 12,
    "registered_models": len(store.list()),
    "cpu_nodes": [n.id for n in cfg.nodes_for("cpu")],
    "gpu16_nodes": [n.id for n in cfg.nodes_for("gpu16")],
    "mobile_nodes": [n.id for n in cfg.nodes_for("mobile")],
    "endpoint_health": health,
    "code_ready": len(store.list()) >= 20,
    "live_runtime_ready": any(x["healthy"] for x in health),
}, indent=2))
