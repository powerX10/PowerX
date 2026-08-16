from __future__ import annotations
import json, urllib.request
from .config import FabricNode


def invoke_node(node: FabricNode, payload: dict, timeout: float = 300.0) -> dict:
    if not node.endpoint:
        raise RuntimeError(f"Endpoint unset for {node.id}")
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        node.endpoint.rstrip("/") + "/infer",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if node.token:
        req.add_header("Authorization", f"Bearer {node.token}")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())
