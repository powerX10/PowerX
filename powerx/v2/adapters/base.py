from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from ..schema import ModelSpec

class ModelAdapter(ABC):
    name: str
    def __init__(self, spec: ModelSpec, model_path: Path):
        self.spec = spec
        self.model_path = model_path
        self.loaded = False

    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> dict[str, Any]: ...

    def unload(self) -> None:
        self.loaded = False
