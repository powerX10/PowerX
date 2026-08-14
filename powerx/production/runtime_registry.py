from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import httpx


@dataclass(frozen=True)
class RuntimeTarget:
    id: str
    model_id: str
    runtime_class: str
    base_url: str
    priority: int = 100
    api_key: str | None = None

    @property
    def models_url(self) -> str:
        return self.base_url.rstrip("/") + "/models"


class RuntimeRegistry:
    def __init__(self):
        self._targets: dict[str, RuntimeTarget] = {}

    def register(self, target: RuntimeTarget) -> None:
        self._targets[target.id] = target

    def unregister(self, target_id: str) -> None:
        self._targets.pop(target_id, None)

    def all(self) -> list[RuntimeTarget]:
        return sorted(self._targets.values(), key=lambda x: x.priority)

    def for_model(self, model_id: str) -> list[RuntimeTarget]:
        return [x for x in self.all() if x.model_id == model_id]

    async def healthy(self, target: RuntimeTarget, timeout: float = 3.0) -> bool:
        headers = {}
        if target.api_key:
            headers["Authorization"] = f"Bearer {target.api_key}"
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(target.models_url, headers=headers)
                return response.is_success
        except httpx.HTTPError:
            return False

    async def first_healthy(
        self,
        targets: Iterable[RuntimeTarget],
    ) -> RuntimeTarget | None:
        for target in sorted(targets, key=lambda x: x.priority):
            if await self.healthy(target):
                return target
        return None
