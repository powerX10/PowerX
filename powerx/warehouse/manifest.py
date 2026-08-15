import json
from dataclasses import asdict
from pathlib import Path
from .schema import ModelSpec

class WarehouseManifest:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text())
        out = {}
        for item in raw.get("models", []):
            item["capabilities"] = tuple(item.get("capabilities", []))
            item["allow_patterns"] = tuple(item.get("allow_patterns", []))
            out[item["id"]] = ModelSpec(**item)
        return out

    def save(self, models):
        self.path.write_text(json.dumps(
            {"version":1,"models":[asdict(m) for m in models]}, indent=2
        ) + "\n")
