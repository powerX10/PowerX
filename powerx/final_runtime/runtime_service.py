from __future__ import annotations
import asyncio
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from powerx.controlplane.runtime_config import build_launch_config
from powerx.controlplane.store import ControlPlaneStore
from .warehouse import RcloneWarehouse

@dataclass
class RunningModel:
    model_id: str
    runtime_class: str
    process: subprocess.Popen | None
    local_path: str
    endpoint: str | None
    started_at: float

class RuntimeSupervisor:
    """Stages a model from Drive and launches a CMS-configured adapter command.

    Binding metadata may contain `launch_command`, with placeholders:
    {model_path}, {model_id}, {port}. This keeps launch mechanics configurable in CMS.
    GGUF has a safe llama-server default; every other adapter must be provided by the runtime image/profile.
    """
    def __init__(self, runtime_class: str, store: ControlPlaneStore | None = None, warehouse: RcloneWarehouse | None = None, cache_root: str | None = None):
        self.runtime_class = runtime_class
        self.store = store or ControlPlaneStore()
        self.warehouse = warehouse or RcloneWarehouse()
        self.cache_root = cache_root or os.getenv("POWERX_RUNTIME_CACHE", f"~/.cache/powerx/{runtime_class}")
        self.running: dict[str, RunningModel] = {}

    def _binding(self, model):
        return next((b for b in model.bindings if b.runtime_class == self.runtime_class and b.enabled), None)

    def _command(self, model, local_path: Path, port: int) -> list[str]:
        binding = self._binding(model)
        if not binding: raise KeyError(f"No enabled {self.runtime_class} binding for {model.id}")
        template = (binding.metadata or {}).get("launch_command")
        if template:
            return shlex.split(str(template).format(model_path=str(local_path), model_id=model.id, port=port))
        adapter = model.config.get("adapter")
        if adapter in {"llamacpp", "llamacpp_vision"}:
            cmd = [os.getenv("POWERX_LLAMA_SERVER", "llama-server"), "-m", str(local_path), "--host", "0.0.0.0", "--port", str(port)]
            ctx = model.config.get(self.runtime_class, {}).get("context_size", 8192)
            cmd += ["-c", str(ctx)]
            if adapter == "llamacpp_vision":
                mm = model.config.get("mmproj_path")
                if mm:
                    mm_local = self.warehouse.stage(mm, self.cache_root, model.id + "-mmproj")
                    cmd += ["--mmproj", str(mm_local)]
            return cmd
        raise RuntimeError(f"Adapter '{adapter}' requires binding.metadata.launch_command for this runtime image")

    def start(self, model_id: str, port: int) -> RunningModel:
        if model_id in self.running and self.running[model_id].process and self.running[model_id].process.poll() is None:
            return self.running[model_id]
        model = self.store.get(model_id)
        if not model.enabled: raise RuntimeError(f"Model disabled in CMS: {model_id}")
        launch = build_launch_config(model, self.runtime_class)
        if not launch.warehouse_path: raise RuntimeError(f"No warehouse_path for {model_id}")
        local = self.warehouse.stage(launch.warehouse_path, self.cache_root, model_id)
        cmd = self._command(model, local, port)
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(1)
        if proc.poll() is not None: raise RuntimeError(f"Runtime command exited: {cmd}")
        item = RunningModel(model_id, self.runtime_class, proc, str(local), launch.endpoint, time.time())
        self.running[model_id] = item
        return item

    def stop(self, model_id: str):
        item = self.running.get(model_id)
        if not item or not item.process: return
        if item.process.poll() is None:
            item.process.terminate()
            try: item.process.wait(timeout=10)
            except subprocess.TimeoutExpired: item.process.kill()
        self.running.pop(model_id, None)
