from __future__ import annotations
from dataclasses import dataclass
from .models import ManagedModel

@dataclass(frozen=True)
class RuntimeLaunchConfig:
    model_id: str
    runtime_class: str
    model_ref: str
    warehouse_path: str | None
    endpoint: str | None
    args: dict


def build_launch_config(model: ManagedModel, runtime_class: str) -> RuntimeLaunchConfig:
    binding = next((b for b in model.bindings if b.runtime_class == runtime_class and b.enabled), None)
    if not binding:
        raise KeyError(f"No enabled {runtime_class} binding for {model.id}")
    args = dict(model.config.get(runtime_class, {}))
    return RuntimeLaunchConfig(
        model_id=model.id,
        runtime_class=runtime_class,
        model_ref=model.source_repo or model.id,
        warehouse_path=model.warehouse_path,
        endpoint=binding.endpoint,
        args=args,
    )
