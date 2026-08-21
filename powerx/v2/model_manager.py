from __future__ import annotations
import gc, os, time
from collections import OrderedDict
from threading import RLock
from typing import Any
from .adapters import ADAPTERS
from .cache import ModelCache
from .errors import AdapterUnavailable
from .schema import ModelSpec

class ModelManager:
    def __init__(self):
        self.cache = ModelCache()
        self.max_loaded = int(os.getenv("POWERX_MAX_LOADED_MODELS", "1"))
        self.loaded: OrderedDict[str, Any] = OrderedDict()
        self.lock = RLock()

    def _evict_loaded(self):
        while len(self.loaded) >= self.max_loaded and self.loaded:
            _, adapter = self.loaded.popitem(last=False)
            try: adapter.unload()
            except Exception: pass
            del adapter
            gc.collect()
            try:
                import torch
                if torch.cuda.is_available(): torch.cuda.empty_cache()
            except Exception: pass

    def get(self, spec: ModelSpec):
        with self.lock:
            if spec.id in self.loaded:
                adapter = self.loaded.pop(spec.id)
                self.loaded[spec.id] = adapter
                return adapter
            cls = ADAPTERS.get(spec.adapter)
            if not cls:
                raise AdapterUnavailable(f"Adapter not included in Zip 2: {spec.adapter}")
            path = self.cache.ensure(spec)
            self._evict_loaded()
            adapter = cls(spec, path)
            adapter.load()
            self.loaded[spec.id] = adapter
            return adapter

    def run(self, spec: ModelSpec, payload: dict[str, Any]) -> dict[str, Any]:
        started = time.time()
        adapter = self.get(spec)
        result = adapter.run(payload)
        result.setdefault("model_id", spec.id)
        result.setdefault("latency_sec", round(time.time() - started, 3))
        return result

    def unload(self, model_id: str | None = None) -> list[str]:
        with self.lock:
            ids = [model_id] if model_id else list(self.loaded.keys())
            removed=[]
            for mid in ids:
                adapter=self.loaded.pop(mid, None)
                if adapter:
                    try: adapter.unload()
                    except Exception: pass
                    removed.append(mid)
            gc.collect()
            try:
                import torch
                if torch.cuda.is_available(): torch.cuda.empty_cache()
            except Exception: pass
            return removed
