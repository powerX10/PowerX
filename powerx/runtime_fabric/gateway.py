from __future__ import annotations
from .scheduler import FabricScheduler, TaskIntent
from .health import check_node
from .client import invoke_node

class NoFabricNode(RuntimeError):
    pass

class RuntimeFabricGateway:
    def __init__(self, scheduler: FabricScheduler | None = None):
        self.scheduler = scheduler or FabricScheduler()

    def infer(self, task: TaskIntent, payload: dict) -> dict:
        attempts = []
        for node in self.scheduler.candidates(task):
            health = check_node(node)
            if not health.healthy:
                attempts.append({"node": node.id, "ok": False, "error": health.detail})
                continue
            try:
                result = invoke_node(node, {"capability": task.capability, "payload": payload})
                return {"ok": True, "node": node.id, "provider": node.provider, "result": result, "attempts": attempts}
            except Exception as exc:
                attempts.append({"node": node.id, "ok": False, "error": str(exc)})
        raise NoFabricNode({"capability": task.capability, "attempts": attempts})
