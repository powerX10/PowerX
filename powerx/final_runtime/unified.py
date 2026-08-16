from __future__ import annotations
from .gateway import DynamicInferenceGateway

class UnifiedPowerX:
    def __init__(self, gateway: DynamicInferenceGateway | None = None):
        self.gateway = gateway or DynamicInferenceGateway()

    async def chat(self, messages: list[dict], capability: str = "chat", max_tokens: int = 900, preferred_runtime: str | None = None):
        return await self.gateway.openai_chat(capability, messages, max_tokens=max_tokens, preferred_runtime=preferred_runtime)

    async def image(self, prompt: str, **options):
        return await self.gateway.infer("image_generate", {"prompt":prompt, **options})

    async def video(self, prompt: str, **options):
        return await self.gateway.infer("video_generate", {"prompt":prompt, **options})

    async def transcribe(self, audio_ref: str, **options):
        return await self.gateway.infer("speech_to_text", {"audio_ref":audio_ref, **options})

    async def speak(self, text: str, **options):
        return await self.gateway.infer("text_to_speech", {"text":text, **options})

    async def research(self, query: str, context: dict | None = None):
        return await self.gateway.openai_chat("deep_reasoning", [{"role":"user","content":query}], max_tokens=1800)
