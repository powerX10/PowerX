from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

RuntimeClass = Literal["cpu", "gpu16", "mobile", "cloud", "disabled"]

class RuntimeBinding(BaseModel):
    runtime_class: RuntimeClass
    enabled: bool = True
    priority: int = Field(default=100, ge=0, le=10000)
    endpoint: str | None = None
    max_concurrent: int = Field(default=1, ge=1, le=128)
    min_ram_gb: float = Field(default=0.0, ge=0)
    min_vram_gb: float = Field(default=0.0, ge=0)
    metadata: dict = Field(default_factory=dict)

class RoutingPolicy(BaseModel):
    mode: Literal["auto", "cpu_only", "gpu_only", "mobile_first", "custom"] = "auto"
    runtime_order: list[RuntimeClass] = Field(default_factory=lambda: ["gpu16", "cpu", "mobile", "cloud"])
    allow_fallback: bool = True
    max_attempts: int = Field(default=3, ge=1, le=20)

class ManagedModel(BaseModel):
    id: str
    display_name: str
    source_repo: str | None = None
    warehouse_path: str | None = None
    format: Literal["gguf", "transformers", "diffusers", "custom"] = "custom"
    capabilities: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    enabled: bool = True
    quantization: str | None = None
    bindings: list[RuntimeBinding] = Field(default_factory=list)
    routing: RoutingPolicy = Field(default_factory=RoutingPolicy)
    config: dict = Field(default_factory=dict)
