from __future__ import annotations
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class WarehouseObject:
    path: str
    is_dir: bool
    size: int | None = None

class RcloneWarehouse:
    def __init__(self, remote: str | None = None, rclone_bin: str | None = None):
        self.remote = remote or os.getenv("POWERX_WAREHOUSE_REMOTE", "PowerXWarehouse")
        self.rclone_bin = rclone_bin or os.getenv("POWERX_RCLONE_BIN", "rclone")

    def _target(self, path: str) -> str:
        return f"{self.remote}:{path.lstrip('/')}"

    def available(self) -> bool:
        return shutil.which(self.rclone_bin) is not None

    def _run(self, args: list[str], **kwargs):
        try:
            return subprocess.run([self.rclone_bin, *args], **kwargs)
        except FileNotFoundError:
            return None

    def exists(self, path: str) -> bool:
        p = self._run(
            ["lsjson", self._target(path), "--stat"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return bool(p and p.returncode == 0)

    def stat(self, path: str) -> dict | None:
        p = self._run(
            ["lsjson", self._target(path), "--stat"],
            text=True,
            capture_output=True,
        )
        if not p or p.returncode != 0:
            return None
        try:
            return json.loads(p.stdout)
        except json.JSONDecodeError:
            return None

    def stage(self, warehouse_path: str, cache_root: str | Path, model_id: str) -> Path:
        """Copy a model on demand; Drive remains the source-of-truth warehouse."""
        if not self.available():
            raise RuntimeError(f"rclone executable not available: {self.rclone_bin}")

        root = Path(os.path.expanduser(str(cache_root))) / model_id
        root.parent.mkdir(parents=True, exist_ok=True)
        src = self._target(warehouse_path)
        stat = self.stat(warehouse_path)
        if not stat:
            raise FileNotFoundError(src)

        if stat.get("IsDir"):
            root.mkdir(parents=True, exist_ok=True)
            p = self._run([
                "copy", src, str(root), "--checkers", "8", "--transfers", "4",
                "--retries", "10", "--low-level-retries", "20",
            ])
            if not p or p.returncode != 0:
                raise RuntimeError(f"rclone copy failed for {src}")
            return root

        root.mkdir(parents=True, exist_ok=True)
        out = root / Path(warehouse_path).name
        if not out.exists() or out.stat().st_size != int(stat.get("Size", -1)):
            p = self._run([
                "copyto", src, str(out), "--retries", "10", "--low-level-retries", "20"
            ])
            if not p or p.returncode != 0:
                raise RuntimeError(f"rclone copyto failed for {src}")
        return out
