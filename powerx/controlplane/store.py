from __future__ import annotations
import json
import os
import threading
from pathlib import Path
from .models import ManagedModel

class ControlPlaneStore:
    def __init__(self, path: str | None = None, seed_path: str | None = None):
        self.path = Path(path or os.getenv("POWERX_MODEL_CMS_DB", "data/model_cms.json"))
        self.seed_path = Path(seed_path or os.getenv("POWERX_MODEL_CMS_SEED", "config_models/powerx_models.json"))
        self._lock = threading.RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._bootstrap()

    def _bootstrap(self):
        if self.seed_path.exists():
            data = json.loads(self.seed_path.read_text())
        else:
            data = {"version": 1, "models": []}
        self._write(data)

    def _read(self) -> dict:
        with self._lock:
            return json.loads(self.path.read_text())

    def _write(self, data: dict):
        with self._lock:
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
            tmp.replace(self.path)

    def list(self) -> list[ManagedModel]:
        return [ManagedModel.model_validate(x) for x in self._read().get("models", [])]

    def get(self, model_id: str) -> ManagedModel:
        for m in self.list():
            if m.id == model_id:
                return m
        raise KeyError(model_id)

    def upsert(self, model: ManagedModel) -> ManagedModel:
        data = self._read()
        models = data.setdefault("models", [])
        encoded = model.model_dump(mode="json")
        for i, item in enumerate(models):
            if item.get("id") == model.id:
                models[i] = encoded
                break
        else:
            models.append(encoded)
        data["version"] = int(data.get("version", 0)) + 1
        self._write(data)
        return model

    def patch(self, model_id: str, patch: dict) -> ManagedModel:
        model = self.get(model_id)
        merged = model.model_dump()
        for key, value in patch.items():
            if key in merged:
                merged[key] = value
        return self.upsert(ManagedModel.model_validate(merged))

    def delete(self, model_id: str) -> bool:
        data = self._read()
        before = len(data.get("models", []))
        data["models"] = [m for m in data.get("models", []) if m.get("id") != model_id]
        changed = len(data["models"]) != before
        if changed:
            data["version"] = int(data.get("version", 0)) + 1
            self._write(data)
        return changed

    def snapshot(self) -> dict:
        return self._read()
