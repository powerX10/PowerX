from dataclasses import dataclass
import httpx


@dataclass(frozen=True)
class RuntimeEndpoint:
    name: str
    base_url: str
    runtime_class: str
    model_id: str


async def endpoint_healthy(endpoint: RuntimeEndpoint) -> bool:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(endpoint.base_url.rstrip("/") + "/models")
            return r.is_success
    except httpx.HTTPError:
        return False


async def choose_first_healthy(
    endpoints: list[RuntimeEndpoint],
    preferred_order: list[str],
) -> RuntimeEndpoint | None:
    by_name = {e.name: e for e in endpoints}

    for name in preferred_order:
        endpoint = by_name.get(name)
        if endpoint and await endpoint_healthy(endpoint):
            return endpoint

    for endpoint in endpoints:
        if await endpoint_healthy(endpoint):
            return endpoint

    return None
