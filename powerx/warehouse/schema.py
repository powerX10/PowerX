from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class ModelSpec:
    id: str
    tier: Literal["3b","4b","6b","gpu-heavy"]
    format: Literal["gguf","transformers","diffusers","custom"]
    capabilities: tuple[str, ...]
    source_repo: str
    revision: str = "main"
    allow_patterns: tuple[str, ...] = ()
    warehouse_subdir: str = ""
    min_ram_gb: float = 0.0
    min_vram_gb: float = 0.0
    notes: str = ""

    @property
    def folder_name(self):
        return self.warehouse_subdir or self.id.replace("/", "__")
