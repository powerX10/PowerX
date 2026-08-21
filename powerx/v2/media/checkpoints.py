from __future__ import annotations
import json, os, time
from pathlib import Path
from typing import Any

class CheckpointStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)
        self.path = self.project_dir / "checkpoint.json"
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "segments": {}, "updated_at": None}
        return json.loads(self.path.read_text())

    def save(self, data: dict[str, Any]):
        data["updated_at"] = time.time()
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
        os.replace(tmp, self.path)

    def mark_started(self, segment_id: str, output_path: str):
        d = self.load()
        row = d["segments"].setdefault(segment_id, {})
        row.update({"status": "running", "output_path": output_path, "started_at": time.time()})
        self.save(d)

    def mark_complete(self, segment_id: str, output_path: str, meta: dict | None = None):
        d = self.load()
        d["segments"][segment_id] = {
            "status": "complete", "output_path": output_path,
            "completed_at": time.time(), "meta": meta or {}
        }
        self.save(d)

    def mark_failed(self, segment_id: str, error: str):
        d = self.load()
        row = d["segments"].setdefault(segment_id, {})
        row["status"] = "failed"
        row["error"] = error
        row["attempts"] = int(row.get("attempts", 0)) + 1
        row["failed_at"] = time.time()
        self.save(d)

    def is_complete(self, segment_id: str) -> bool:
        d = self.load()
        row = d["segments"].get(segment_id) or {}
        p = Path(row.get("output_path", ""))
        return row.get("status") == "complete" and p.is_file() and p.stat().st_size > 0
