from __future__ import annotations
import json, os, shutil, time
from pathlib import Path
from contextlib import contextmanager
from .schema import ModelSpec
from .settings import PowerXSettings
from .warehouse import WarehouseClient

class ModelCache:
    def __init__(self):
        self.settings = PowerXSettings.load()
        self.cache_root = self.settings.cache_root
        self.models_root = self.cache_root / "models"
        self.models_root.mkdir(parents=True, exist_ok=True)
        self.warehouse = WarehouseClient()
        self.max_cache_gb = float(os.getenv("POWERX_MAX_CACHE_GB", "0") or "0")

    def cached_path(self, spec: ModelSpec) -> Path:
        return self.models_root / spec.id.replace("/", "_")

    def marker_path(self, spec: ModelSpec) -> Path:
        return self.cached_path(spec) / ".powerx-ready.json"

    def exists(self, spec: ModelSpec) -> bool:
        return self.cached_path(spec).exists() and self.marker_path(spec).exists()

    @contextmanager
    def _lock(self, spec: ModelSpec, timeout: int = 1800):
        lock = self.models_root / f".{spec.id}.lock"
        start = time.time()
        while True:
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                break
            except FileExistsError:
                if time.time() - start > timeout:
                    raise TimeoutError(f"Timed out waiting for cache lock: {spec.id}")
                time.sleep(1)
        try:
            yield
        finally:
            lock.unlink(missing_ok=True)

    def ensure(self, spec: ModelSpec) -> Path:
        dest = self.cached_path(spec)
        if self.exists(spec):
            self.touch(dest)
            return dest
        with self._lock(spec):
            if self.exists(spec):
                self.touch(dest)
                return dest
            self.evict_if_needed()
            if dest.exists():
                shutil.rmtree(dest)
            self.warehouse.sync_to(spec.warehouse_path, dest)
            self.marker_path(spec).write_text(json.dumps({"model_id": spec.id, "warehouse_path": spec.warehouse_path, "cached_at": time.time()}), encoding="utf-8")
            self.touch(dest)
            return dest

    def touch(self, path: Path) -> None:
        now = time.time()
        try:
            os.utime(path, (now, now))
        except OSError:
            pass

    def usage_bytes(self) -> int:
        total = 0
        for root, _, files in os.walk(self.models_root):
            for f in files:
                try: total += (Path(root) / f).stat().st_size
                except OSError: pass
        return total

    def evict_if_needed(self, reserve_gb: float = 2.0) -> list[str]:
        if self.max_cache_gb <= 0:
            return []
        limit = max(0, self.max_cache_gb - reserve_gb) * (1024**3)
        removed: list[str] = []
        dirs = [p for p in self.models_root.iterdir() if p.is_dir()]
        dirs.sort(key=lambda p: p.stat().st_atime)
        while self.usage_bytes() > limit and dirs:
            victim = dirs.pop(0)
            removed.append(victim.name)
            shutil.rmtree(victim, ignore_errors=True)
        return removed
