from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import signal
import subprocess
import time

import httpx

from powerx.runtime_cpu.llamacpp.files import validate_gguf
from powerx.runtime_cpu.llamacpp.profile import LlamaCppProfile


@dataclass
class LlamaCppState:
    model_id: str
    pid: int
    base_url: str
    model_path: str


class LlamaCppServerManager:
    def __init__(
        self,
        *,
        binary: str | None = None,
        state_dir: str = ".powerx-cpu-runtime",
    ):
        self.binary = binary or os.getenv("LLAMA_SERVER_BIN") or shutil.which("llama-server")
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _pid_file(self, model_id: str) -> Path:
        return self.state_dir / f"{model_id}.pid"

    def _log_file(self, model_id: str) -> Path:
        return self.state_dir / f"{model_id}.log"

    @staticmethod
    def _alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def status(self, model_id: str) -> dict:
        p = self._pid_file(model_id)
        if not p.exists():
            return {"running": False, "model_id": model_id}
        try:
            pid = int(p.read_text().strip())
        except Exception:
            p.unlink(missing_ok=True)
            return {"running": False, "model_id": model_id}
        if not self._alive(pid):
            p.unlink(missing_ok=True)
            return {"running": False, "model_id": model_id}
        return {"running": True, "model_id": model_id, "pid": pid}

    def start(
        self,
        profile: LlamaCppProfile,
        *,
        model_path: str,
        host: str = "127.0.0.1",
        port: int = 8200,
        startup_timeout: int = 600,
    ) -> LlamaCppState:
        if not self.binary:
            raise RuntimeError(
                "llama-server was not found. Set LLAMA_SERVER_BIN or install llama.cpp."
            )

        check = validate_gguf(model_path)
        if not check["ok"]:
            raise RuntimeError(check["error"])

        if self.status(profile.id).get("running"):
            raise RuntimeError(f"{profile.id} is already running.")

        log_handle = open(self._log_file(profile.id), "ab", buffering=0)

        proc = subprocess.Popen(
            profile.server_args(
                binary=self.binary,
                model_path=check["path"],
                host=host,
                port=port,
            ),
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
                    f"{profile.id} exited during startup. "
                    f"See {self._log_file(profile.id)}"
                )
            try:
                with httpx.Client(timeout=4) as client:
                    r = client.get(base_url + "/models")
                    if r.is_success:
                        return LlamaCppState(
                            model_id=profile.id,
                            pid=proc.pid,
                            base_url=base_url,
                            model_path=check["path"],
                        )
            except Exception as exc:
                last_error = exc
            time.sleep(2)

        self.stop(profile.id)
        raise TimeoutError(
            f"{profile.id} did not become healthy. Last error: {last_error}"
        )

    def stop(self, model_id: str, timeout: int = 20) -> dict:
        state = self.status(model_id)
        if not state.get("running"):
            return {"stopped": True, "was_running": False, "model_id": model_id}

        pid = int(state["pid"])
        try:
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            self._pid_file(model_id).unlink(missing_ok=True)
            return {"stopped": True, "was_running": False, "model_id": model_id}

        deadline = time.time() + timeout
        while time.time() < deadline:
            if not self._alive(pid):
                self._pid_file(model_id).unlink(missing_ok=True)
                return {"stopped": True, "was_running": True, "model_id": model_id}
            time.sleep(1)

        try:
            os.killpg(pid, signal.SIGKILL)
        finally:
            self._pid_file(model_id).unlink(missing_ok=True)

        return {
            "stopped": True,
            "was_running": True,
            "forced": True,
            "model_id": model_id,
        }
