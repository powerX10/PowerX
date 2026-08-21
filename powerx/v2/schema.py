from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Literal

RuntimeClass = Literal["mock", "cpu", "gpu16", "gpu24", "gpu40", "gpu80", "lightning", "external"]

class ModelBinding(BaseModel):
    runtime_class: RuntimeClass
    enabled: bool = True
    priority: int = 50
    min_ram_gb: float | None = None
    min_vram_gb: float | None = None
    max_concurrent: int = 1

class ModelSpec(BaseModel):
    id: str
    display_name: str
    source_repo: str | None = None
    warehouse_path: str
    format: str
    adapter: str
    enabled: bool = True
    capabilities: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    bindings: list[ModelBinding] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class Registry(BaseModel):
    version: int
    name: str = "PowerX V2 Canonical Registry"
    models: list[ModelSpec]

class PowerXRequest(BaseModel):
    text: str = ""
    capability: str | None = None
    product_id: str = "powerx"
    user_id: str | None = None
    preferred_runtime: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

class PowerXResponse(BaseModel):
    ok: bool
    model_id: str | None = None
    runtime: str | None = None
    text: str | None = None
    artifact_url: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
