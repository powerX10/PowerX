from __future__ import annotations
from pathlib import Path
import os, shutil, subprocess, tempfile
from .errors import WarehouseError

class WarehouseClient:
    """Resolve model files from either a mounted/local warehouse or an rclone remote.

    Preferred production/dev flow on Lightning:
      Google Drive (rclone remote) -> Lightning local cache -> model adapter -> GPU/CPU.
    """
    def __init__(self):
        self.local_root = Path(os.getenv("POWERX_WAREHOUSE_ROOT", "/mnt/powerx_warehouse"))
        self.rclone_remote = os.getenv("POWERX_RCLONE_REMOTE", "").strip().rstrip(":")
        self.rclone_config = os.getenv("POWERX_RCLONE_CONFIG", "").strip()

    def local_source(self, warehouse_path: str) -> Path:
        return self.local_root / warehouse_path

    def _rclone_source(self, warehouse_path: str) -> str:
        if not self.rclone_remote:
            raise WarehouseError("POWERX_RCLONE_REMOTE is not configured and local warehouse path is missing")
        return f"{self.rclone_remote}:{warehouse_path}"

    def sync_to(self, warehouse_path: str, destination: Path) -> Path:
        src = self.local_source(warehouse_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            if src.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(src, destination)
            else:
                destination.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, destination / src.name)
            return destination

        remote = self._rclone_source(warehouse_path)
        if not shutil.which("rclone"):
            raise WarehouseError("rclone executable not found; install rclone or mount POWERX_WAREHOUSE_ROOT")

        tmp_parent = destination.parent
        tmp = Path(tempfile.mkdtemp(prefix=destination.name + ".partial-", dir=tmp_parent))
        cmd = ["rclone", "copy", remote, str(tmp), "--transfers", os.getenv("POWERX_RCLONE_TRANSFERS", "4"), "--checkers", os.getenv("POWERX_RCLONE_CHECKERS", "8"), "--progress"]
        if self.rclone_config:
            cmd += ["--config", self.rclone_config]
        try:
            p = subprocess.run(cmd, text=True, capture_output=True, check=False)
            if p.returncode != 0:
                raise WarehouseError(f"rclone copy failed: {p.stderr[-2000:]}")
            if destination.exists():
                shutil.rmtree(destination)
            tmp.rename(destination)
            return destination
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
