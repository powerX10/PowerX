from powerx.runtime.gpu.process import VLLMProcessManager
from powerx.runtime.gpu.profiles.registry import get_gpu_profile

class GPURuntimeController:
    def __init__(self):
        self.manager = VLLMProcessManager()

    def start(self, model_id: str, host: str="127.0.0.1", port: int=8100) -> dict:
        profile = get_gpu_profile(model_id)
        state = self.manager.start(profile, host=host, port=port)
        return state.__dict__

    def stop(self, model_id: str) -> dict:
        return self.manager.stop(model_id)

    def status(self, model_id: str) -> dict:
        return self.manager.status(model_id)
