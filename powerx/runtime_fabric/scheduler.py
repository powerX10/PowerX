from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .config import FabricConfig, FabricNode, load_fabric_config

TaskSize = Literal["small", "normal", "heavy", "market"]

@dataclass(frozen=True)
class TaskIntent:
    capability: str
    size: TaskSize = "normal"
    user_device_available: bool = False
    requires_gpu: bool = False

class FabricScheduler:
    """Provider-aware routing above Phase 9 runtime classes.

    Phase 9 still decides which models can run on cpu/gpu16/mobile. Phase 12
    decides which live provider node should serve that runtime class.
    """
    def __init__(self, config: FabricConfig | None = None):
        self.config = config or load_fabric_config()

    def runtime_order(self, task: TaskIntent) -> list[str]:
        p = self.config.policy
        gpu_only = set(p.get("gpu_only_capabilities", []))
        gpu_pref = set(p.get("gpu_preferred_capabilities", []))
        mobile_caps = set(p.get("mobile_capabilities", []))

        if task.requires_gpu or task.capability in gpu_only:
            return ["gpu16"]
        if task.size == "market":
            return list(p.get("market_daemon_order", ["cpu"]))
        if task.size == "heavy" or task.capability in gpu_pref:
            return list(p.get("heavy_task_order", ["gpu16", "cpu"]))
        if task.size == "small" and task.user_device_available and task.capability in mobile_caps:
            return list(p.get("small_user_task_order", ["mobile", "cpu", "gpu16"]))
        return list(p.get("normal_server_task_order", ["cpu", "mobile", "gpu16"]))

    def candidates(self, task: TaskIntent) -> list[FabricNode]:
        out: list[FabricNode] = []
        for runtime_class in self.runtime_order(task):
            if runtime_class == "mobile" and not task.user_device_available:
                continue
            out.extend(self.config.nodes_for(runtime_class))
        return out
