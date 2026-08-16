from __future__ import annotations
import json
from pathlib import Path
from powerx.controlplane.models import ManagedModel
from powerx.controlplane.store import ControlPlaneStore

class FinalRegistrySync:
    """Imports the Phase 11 20-model seed into Phase 9 CMS without making it immutable."""
    def __init__(self, store: ControlPlaneStore | None = None, seed: str | Path = "config_final/model_registry_20.json"):
        self.store = store or ControlPlaneStore()
        self.seed = Path(seed)

    def load(self) -> list[ManagedModel]:
        data = json.loads(self.seed.read_text())
        return [ManagedModel.model_validate(x) for x in data.get("models", [])]

    def sync(self, preserve_existing_runtime_overrides: bool = True) -> dict:
        existing = {m.id: m for m in self.store.list()}
        added = updated = preserved = 0
        for seeded in self.load():
            current = existing.get(seeded.id)
            if current and preserve_existing_runtime_overrides:
                merged = seeded.model_dump()
                # CMS runtime controls are authoritative once an operator changed them.
                merged["enabled"] = current.enabled
                merged["bindings"] = [b.model_dump() for b in current.bindings]
                merged["routing"] = current.routing.model_dump()
                cfg = dict(seeded.config)
                cfg.update(current.config)
                merged["config"] = cfg
                self.store.upsert(ManagedModel.model_validate(merged))
                preserved += 1
            else:
                self.store.upsert(seeded)
                if current: updated += 1
                else: added += 1
        return {"ok": True, "seed_models": len(self.load()), "added": added, "updated": updated, "preserved_runtime_overrides": preserved}
