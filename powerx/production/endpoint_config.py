import json
import os
from powerx.production.runtime_registry import RuntimeRegistry, RuntimeTarget


def registry_from_env() -> RuntimeRegistry:
    registry = RuntimeRegistry()
    raw = os.getenv("POWERX_RUNTIME_ENDPOINTS_JSON", "").strip()
    if not raw:
        return registry

    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("POWERX_RUNTIME_ENDPOINTS_JSON must be a JSON array.")

    for item in data:
        registry.register(RuntimeTarget(
            id=str(item["id"]),
            model_id=str(item["model_id"]),
            runtime_class=str(item["runtime_class"]),
            base_url=str(item["base_url"]).rstrip("/"),
            priority=int(item.get("priority", 100)),
            api_key=item.get("api_key"),
        ))
    return registry
