from abc import ABC, abstractmethod

class STTProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str) -> dict: ...

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, output_path: str) -> dict: ...
