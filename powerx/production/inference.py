from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import httpx

from powerx.production.policy import ExecutionPolicy, candidate_models
from powerx.production.runtime_registry import RuntimeRegistry, RuntimeTarget


class NoRuntimeAvailable(RuntimeError):
    pass


@dataclass
class InferenceResult:
    ok: bool
    model_id: str
    runtime_id: str
    runtime_class: str
    response: dict[str, Any]


class ProductionInferenceCoordinator:
    def __init__(
        self,
        registry: RuntimeRegistry,
        policy: ExecutionPolicy | None = None,
    ):
        self.registry = registry
        self.policy = policy or ExecutionPolicy()

    def _allowed(self, target: RuntimeTarget) -> bool:
        if target.runtime_class == "mobile" and not self.policy.allow_mobile_fallback:
            return False
        if target.runtime_class == "cpu" and not self.policy.allow_cpu_fallback:
            return False
        return target.runtime_class in self.policy.runtime_order

    def _sort_key(self, target: RuntimeTarget):
        try:
            runtime_rank = self.policy.runtime_order.index(target.runtime_class)
        except ValueError:
            runtime_rank = 999
        return (runtime_rank, target.priority)

    async def resolve(self, task: str) -> RuntimeTarget:
        for model_id in candidate_models(task):
            targets = [
                t for t in self.registry.for_model(model_id)
                if self._allowed(t)
            ]
            targets.sort(key=self._sort_key)
            for target in targets:
                if await self.registry.healthy(target):
                    return target

        raise NoRuntimeAvailable(
            f"No healthy compatible PowerX runtime is available for task '{task}'."
        )

    async def chat(
        self,
        *,
        task: str,
        messages: list[dict[str, Any]],
        max_tokens: int = 1024,
    ) -> InferenceResult:
        excluded: set[str] = set()
        last_error: Exception | None = None

        for _ in range(self.policy.max_attempts):
            target = await self._resolve_excluding(task, excluded)
            excluded.add(target.id)

            headers = {"Content-Type": "application/json"}
            if target.api_key:
                headers["Authorization"] = f"Bearer {target.api_key}"

            try:
                async with httpx.AsyncClient(timeout=180) as client:
                    r = await client.post(
                        target.base_url.rstrip("/") + "/chat/completions",
                        headers=headers,
                        json={
                            "model": target.model_id,
                            "messages": messages,
                            "max_tokens": max_tokens,
                        },
                    )
                    r.raise_for_status()
                    return InferenceResult(
                        ok=True,
                        model_id=target.model_id,
                        runtime_id=target.id,
                        runtime_class=target.runtime_class,
                        response=r.json(),
                    )
            except httpx.HTTPError as exc:
                last_error = exc

        raise NoRuntimeAvailable(
            f"All eligible PowerX runtimes failed. Last error: {last_error}"
        )

    async def _resolve_excluding(
        self,
        task: str,
        excluded: set[str],
    ) -> RuntimeTarget:
        for model_id in candidate_models(task):
            targets = [
                t for t in self.registry.for_model(model_id)
                if self._allowed(t) and t.id not in excluded
            ]
            targets.sort(key=self._sort_key)
            for target in targets:
                if await self.registry.healthy(target):
                    return target
        raise NoRuntimeAvailable(
            f"No additional healthy runtime available for '{task}'."
        )
