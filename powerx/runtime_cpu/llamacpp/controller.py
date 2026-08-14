import os

from powerx.runtime_cpu.llamacpp.process import LlamaCppServerManager
from powerx.runtime_cpu.llamacpp.profiles import get_cpu_profile


class CPURuntimeController:
    def __init__(self):
        self.manager = LlamaCppServerManager()

    def start(
        self,
        model_id: str,
        *,
        host: str = "127.0.0.1",
        port: int = 8200,
    ) -> dict:
        profile = get_cpu_profile(model_id)
        path = os.getenv(profile.model_path_env)
        if not path:
            raise RuntimeError(
                f"{profile.model_path_env} is not configured."
            )
        return self.manager.start(
            profile,
            model_path=path,
            host=host,
            port=port,
        ).__dict__

    def stop(self, model_id: str) -> dict:
        return self.manager.stop(model_id)

    def status(self, model_id: str) -> dict:
        return self.manager.status(model_id)
