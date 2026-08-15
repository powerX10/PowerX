from dataclasses import dataclass, field
@dataclass
class RuntimeNode:
    id: str
    runtime_class: str
    base_url: str
    capabilities: set[str]
    model_tiers: set[str]
    always_on: bool=False
    available: bool=True
    load: float=0.0
    ram_gb: float=0.0
    vram_gb: float=0.0
    metadata: dict=field(default_factory=dict)
