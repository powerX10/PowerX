from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class PowerXSettings:
    registry_path: Path
    warehouse_root: Path
    cache_root: Path
    api_key: str
    mock_mode: bool
    lightning_worker_url: str | None
    lightning_worker_token: str | None

    @staticmethod
    def load() -> "PowerXSettings":
        return PowerXSettings(
            registry_path=Path(os.getenv("POWERX_REGISTRY_PATH", "config/powerx_v2_model_registry.json")),
            warehouse_root=Path(os.getenv("POWERX_WAREHOUSE_ROOT", "/mnt/powerx_warehouse")),
            cache_root=Path(os.getenv("POWERX_CACHE_ROOT", ".powerx_cache")),
            api_key=os.getenv("POWERX_V2_API_KEY", ""),
            mock_mode=os.getenv("POWERX_MOCK_MODE", "1") == "1",
            lightning_worker_url=os.getenv("POWERX_LIGHTNING_WORKER_URL") or None,
            lightning_worker_token=os.getenv("POWERX_LIGHTNING_WORKER_TOKEN") or None,
        )
