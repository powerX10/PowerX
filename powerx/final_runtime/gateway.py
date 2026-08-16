from __future__ import annotations
import asyncio
import os
from typing import Any
import httpx
from powerx.controlplane.resolver import DynamicRuntimeResolver
from powerx.controlplane.store import ControlPlaneStore

class NoRuntimeAvailable(RuntimeError): pass

class DynamicInferenceGateway:
    """CMS-driven failover gateway. It never pins a capability to a fixed runtime in code."""
    def __init__(self, store: ControlPlaneStore | None = None):
        self.store = store or ControlPlaneStore()
        self.resolver = DynamicRuntimeResolver(self.store)

    async def _healthy(self, endpoint: str | None) -> bool:
        if not endpoint: return False
        base = endpoint.rstrip("/")
        if base.endswith("/v1"): base = base[:-3]
        try:
            async with httpx.AsyncClient(timeout=3) as c:
                r = await c.get(base + "/health")
                return r.status_code < 500
        except Exception:
            return False

    async def candidates(self, capability: str, preferred_runtime: str | None = None) -> list[dict]:
        out = []
        for x in self.resolver.candidates(capability, preferred_runtime):
            out.append(x.__dict__)
        return out

    async def infer(self, capability: str, payload: dict[str, Any], preferred_runtime: str | None = None) -> dict:
        candidates = await self.candidates(capability, preferred_runtime)
        attempts = []
        for candidate in candidates:
            endpoint = candidate.get("endpoint")
            if not await self._healthy(endpoint):
                attempts.append({**candidate, "ok": False, "error": "endpoint_unhealthy_or_unset"})
                continue
            try:
                async with httpx.AsyncClient(timeout=float(os.getenv("POWERX_INFERENCE_TIMEOUT", "300"))) as c:
                    r = await c.post(endpoint.rstrip("/") + "/infer", json={"model_id": candidate["model_id"], "capability": capability, "payload": payload})
                    r.raise_for_status()
                    return {"ok": True, "candidate": candidate, "result": r.json(), "attempts": attempts}
            except Exception as exc:
                attempts.append({**candidate, "ok": False, "error": str(exc)})
        raise NoRuntimeAvailable({"capability": capability, "attempts": attempts})

    async def openai_chat(self, capability: str, messages: list[dict], max_tokens: int = 900, preferred_runtime: str | None = None) -> dict:
        candidates = await self.candidates(capability, preferred_runtime)
        attempts = []
        for candidate in candidates:
            endpoint = candidate.get("endpoint")
            if not await self._healthy(endpoint):
                attempts.append({**candidate, "ok": False, "error": "endpoint_unhealthy_or_unset"})
                continue
            try:
                base = endpoint.rstrip("/")
                url = base + "/chat/completions" if base.endswith("/v1") else base + "/v1/chat/completions"
                async with httpx.AsyncClient(timeout=float(os.getenv("POWERX_INFERENCE_TIMEOUT", "300"))) as c:
                    r = await c.post(url, json={"model": candidate["model_id"], "messages": messages, "max_tokens": max_tokens})
                    r.raise_for_status()
                    return {"ok": True, "candidate": candidate, "result": r.json(), "attempts": attempts}
            except Exception as exc:
                attempts.append({**candidate, "ok": False, "error": str(exc)})
        raise NoRuntimeAvailable({"capability": capability, "attempts": attempts})
