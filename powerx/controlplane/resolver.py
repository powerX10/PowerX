from __future__ import annotations
from dataclasses import dataclass
from .store import ControlPlaneStore

@dataclass(frozen=True)
class Resolution:
    model_id: str
    runtime_class: str
    endpoint: str | None
    priority: int
    reason: str

class DynamicRuntimeResolver:
    def __init__(self, store: ControlPlaneStore):
        self.store = store

    def candidates(self, capability: str, preferred_runtime: str | None = None) -> list[Resolution]:
        out: list[Resolution] = []
        for model in self.store.list():
            if not model.enabled or capability not in model.capabilities:
                continue
            order = model.routing.runtime_order
            for binding in model.bindings:
                if not binding.enabled or binding.runtime_class == "disabled":
                    continue
                if preferred_runtime and binding.runtime_class != preferred_runtime:
                    continue
                try:
                    rr = order.index(binding.runtime_class)
                except ValueError:
                    rr = 999
                out.append(Resolution(
                    model_id=model.id,
                    runtime_class=binding.runtime_class,
                    endpoint=binding.endpoint,
                    priority=rr * 10000 + binding.priority,
                    reason=f"cms:{model.routing.mode}:{capability}",
                ))
        return sorted(out, key=lambda x: x.priority)
