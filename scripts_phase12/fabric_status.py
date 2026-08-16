#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from powerx.runtime_fabric.config import load_fabric_config
from powerx.runtime_fabric.health import check_node
cfg = load_fabric_config()
for node in cfg.nodes:
    h = check_node(node)
    print(f"{node.id:24} runtime={node.runtime_class:6} provider={node.provider:6} endpoint={'SET' if node.endpoint else 'UNSET':5} healthy={h.healthy} detail={h.detail[:120]}")
