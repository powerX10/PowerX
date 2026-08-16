from __future__ import annotations
import time
import urllib.request
from dataclasses import dataclass
from .config import FabricNode

@dataclass(frozen=True)
class NodeHealth:
    node_id: str
    healthy: bool
    status: int | None = None
    detail: str = ""


def check_node(
    node: FabricNode,
    timeout: float = 60.0,
    retries: int = 2,
    retry_delay: float = 2.0,
) -> NodeHealth:
    if not node.endpoint:
        return NodeHealth(node.id, False, None, "endpoint_unset")

    url = node.endpoint.rstrip("/") + "/health"
    last_error = ""

    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PowerX-Runtime-Fabric/12"},
        )

        if node.token:
            req.add_header("Authorization", f"Bearer {node.token}")

        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read(4096).decode("utf-8", "replace")
                return NodeHealth(
                    node.id,
                    200 <= r.status < 500,
                    r.status,
                    body,
                )
        except Exception as exc:
            last_error = str(exc)

            if attempt < retries:
                time.sleep(retry_delay)

    return NodeHealth(
        node.id,
        False,
        None,
        last_error or "health_check_failed",
    )
