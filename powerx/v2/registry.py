from __future__ import annotations
import json
from pathlib import Path
from .schema import Registry, ModelSpec
from .settings import PowerXSettings

class ModelRegistry:
    def __init__(self, path: str | Path | None = None):
        self.settings = PowerXSettings.load()
        self.path = Path(path) if path else self.settings.registry_path
        self._registry: Registry | None = None

    def load(self) -> Registry:
        if self._registry is None:
            with open(self.path, "r", encoding="utf-8") as f:
                self._registry = Registry.model_validate(json.load(f))
        return self._registry

    def all(self) -> list[ModelSpec]:
        return [m for m in self.load().models if m.enabled]

    def by_id(self, model_id: str) -> ModelSpec:
        for m in self.all():
            if m.id == model_id:
                return m
        raise KeyError(f"Unknown or disabled model_id: {model_id}")

    def for_capability(self, capability: str) -> list[ModelSpec]:
        return [m for m in self.all() if capability in m.capabilities or capability in m.roles]

    def best_for(self, capability: str, preferred_runtime: str | None = None) -> list[ModelSpec]:
        models = self.for_capability(capability)
        def score(m: ModelSpec) -> int:
            bindings = [b for b in m.bindings if b.enabled]
            if preferred_runtime:
                for b in bindings:
                    if b.runtime_class == preferred_runtime:
                        return b.priority
            return min([b.priority for b in bindings], default=999)
        return sorted(models, key=score)
