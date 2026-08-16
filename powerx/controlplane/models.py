from __future__ import annotations
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, ClassVar, Literal

RuntimeClass = Literal["cpu", "gpu16", "mobile", "cloud", "disabled"]
_ALLOWED_RUNTIME = {"cpu", "gpu16", "mobile", "cloud", "disabled"}
_ALLOWED_MODES = {"auto", "cpu_only", "gpu_only", "mobile_first", "custom"}
_ALLOWED_FORMATS = {"gguf", "transformers", "diffusers", "custom"}


def _dump(value: Any) -> Any:
    if isinstance(value, _CompatModel):
        return {k: _dump(v) for k, v in value.__dict__.items()}
    if is_dataclass(value):
        return _dump(asdict(value))
    if isinstance(value, dict):
        return {k: _dump(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_dump(v) for v in value]
    return value


class _CompatModel:
    """Tiny Pydantic-v2-compatible surface for PowerX core.

    Keeps ``model_validate`` and ``model_dump`` used by Phase 9-11 while avoiding
    pydantic-core/Rust compilation on Android/Termux. API deployments may still
    install FastAPI/Pydantic separately.
    """

    @classmethod
    def model_validate(cls, value: Any):
        if isinstance(value, cls):
            return value
        if not isinstance(value, dict):
            raise TypeError(f"{cls.__name__}.model_validate expects dict or {cls.__name__}")
        return cls(**value)

    def model_dump(self, mode: str | None = None) -> dict[str, Any]:
        return _dump(self)


@dataclass
class RuntimeBinding(_CompatModel):
    runtime_class: RuntimeClass
    enabled: bool = True
    priority: int = 100
    endpoint: str | None = None
    max_concurrent: int = 1
    min_ram_gb: float = 0.0
    min_vram_gb: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.runtime_class not in _ALLOWED_RUNTIME:
            raise ValueError(f"Invalid runtime_class: {self.runtime_class}")
        self.priority = int(self.priority)
        self.max_concurrent = int(self.max_concurrent)
        self.min_ram_gb = float(self.min_ram_gb)
        self.min_vram_gb = float(self.min_vram_gb)
        if not 0 <= self.priority <= 10000:
            raise ValueError("priority must be between 0 and 10000")
        if not 1 <= self.max_concurrent <= 128:
            raise ValueError("max_concurrent must be between 1 and 128")
        if self.min_ram_gb < 0 or self.min_vram_gb < 0:
            raise ValueError("RAM/VRAM requirements cannot be negative")
        self.metadata = dict(self.metadata or {})


@dataclass
class RoutingPolicy(_CompatModel):
    mode: Literal["auto", "cpu_only", "gpu_only", "mobile_first", "custom"] = "auto"
    runtime_order: list[RuntimeClass] = field(default_factory=lambda: ["gpu16", "cpu", "mobile", "cloud"])
    allow_fallback: bool = True
    max_attempts: int = 3

    def __post_init__(self):
        if self.mode not in _ALLOWED_MODES:
            raise ValueError(f"Invalid routing mode: {self.mode}")
        self.runtime_order = list(self.runtime_order or [])
        invalid = [x for x in self.runtime_order if x not in _ALLOWED_RUNTIME]
        if invalid:
            raise ValueError(f"Invalid runtime_order values: {invalid}")
        self.max_attempts = int(self.max_attempts)
        if not 1 <= self.max_attempts <= 20:
            raise ValueError("max_attempts must be between 1 and 20")


@dataclass
class ManagedModel(_CompatModel):
    id: str
    display_name: str
    source_repo: str | None = None
    warehouse_path: str | None = None
    format: Literal["gguf", "transformers", "diffusers", "custom"] = "custom"
    capabilities: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    enabled: bool = True
    quantization: str | None = None
    bindings: list[RuntimeBinding] = field(default_factory=list)
    routing: RoutingPolicy = field(default_factory=RoutingPolicy)
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not str(self.id).strip():
            raise ValueError("id is required")
        if not str(self.display_name).strip():
            raise ValueError("display_name is required")
        if self.format not in _ALLOWED_FORMATS:
            raise ValueError(f"Invalid model format: {self.format}")
        self.capabilities = [str(x) for x in (self.capabilities or [])]
        self.roles = [str(x) for x in (self.roles or [])]
        self.bindings = [RuntimeBinding.model_validate(x) for x in (self.bindings or [])]
        self.routing = RoutingPolicy.model_validate(self.routing)
        self.config = dict(self.config or {})
