from abc import ABC, abstractmethod
from typing import Any


class SpecializedModel(ABC):
    @abstractmethod
    async def infer(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> bool:
        raise NotImplementedError
