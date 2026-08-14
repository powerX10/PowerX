from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
import signal
import subprocess
import time

import httpx

from powerx.runtime.gpu.capabilities import GPUCapabilityDetector
from powerx.runtime.gpu.profile import GPUModelProfile


@dataclass
class RuntimeState:
    model_id: str
    pid: int
    host: str
    port: int
    base_url: str
    started_at: float


class VLLMProcessManager:
    def __init__(self, state_dir: str = ".powerx-runtime"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _pid_file(self, model_id: str) -> Path:
        return self.state_dir / f"{model_id}.pid"

    def _log_file(self, model_id: str) -> Path:
        return self.state_dir / f"{model_id}.log"

    def _is_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def status(self, model_id: str) -> dict:
        pid_file = self._pid_file(model_id)
        if not pid_file.exists():
            return {"running": False, "model_id": model_id}

        try:
            pid = int(pid_file.read_text().strip())
        except Exception:
            return {"running": False, "model_id": model_id}

        alive = self._is_alive(pid)
        if not alive:
            pid_file.unlink(missing_ok=True)
        return {"running": alive, "model_id": model_id, "pid": pid if alive else None}

    def start(
        self,
        profile: GPUModelProfile,
        *,
        host: str = "127.0.0.1",
        port: int = 8100,
        startup_timeout: int = 900,
    ) -> RuntimeState:
        current = self.status(profile.id)
        if current.get("running"):
            raise RuntimeError(f"{profile.id} is already running.")

        device = GPUCapabilityDetector.best_device()
        if device is None:
            raise RuntimeError("No NVIDIA GPU detected.")

        if device.total_vram_mb < int(profile.min_vram_gb * 1024):
            raise RuntimeError(
                f"{profile.id} requires about {profile.min_vram_gb}GB VRAM; "
                f"detected {device.total_vram_mb/1024:.1f}GB."
            )

        log_path = self._log_file(profile.id)
        log_handle = open(log_path, "ab", buffering=0)

        proc = subprocess.Popen(
            profile.vllm_args(host=host, port=port),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        self._pid_file(profile.id).write_text(str(proc.pid))
        base_url = f"http://{host}:{port}/v1"

        deadline = time.time() + startup_timeout
        last_error = None
        while time.time() < deadline:
            if proc.poll() is not None:
                self._pid_file(profile.id).unlink(missing_ok=True)
                raise RuntimeError(
                    f"{profile.id} exited during startup. See {log_path}"
                )
            try:
                with httpx.Client(timeout=5) as client:
                    response = client.get(base_url + "/models")
                    if response.is_success:
                        return RuntimeState(
                            model_id=profile.id,
                            pid=proc.pid,
                            host=host,
                            port=port,
                            base_url=base_url,
                            started_at=time.time(),
                        )
            except Exception as exc:
                last_error = exc
            time.sleep(3)

        self.stop(profile.id)
        raise TimeoutError(
            f"{profile.id} did not become healthy within {startup_timeout}s. "
            f"Last error: {last_error}. See {log_path}"
        )

    def stop(self, model_id: str, timeout: int = 30) -> dict:
        status = self.status(model_id)
        if not status.get("running"):
            return {"stopped": True, "model_id": model_id, "was_running": False}

        pid = int(status["pid"])
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            self._pid_file(model_id).unlink(missing_ok=True)
            return {"stopped": True, "model_id": model_id, "was_running": False}

        deadline = time.time() + timeout
        while time.time() < deadline:
            if not self._is_alive(pid):
                self._pid_file(model_id).unlink(missing_ok=True)
                return {"stopped": True, "model_id": model_id, "was_running": True}
            time.sleep(1)

        try:
            os.killpg(pid, signal.SIGKILL)
        finally:
            self._pid_file(model_id).unlink(missing_ok=True)

        return {"stopped": True, "model_id": model_id, "was_running": True, "forced": True}
