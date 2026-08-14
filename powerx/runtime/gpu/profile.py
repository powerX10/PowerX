from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class GPUModelProfile:
    id: str
    model_ref: str
    served_model_name: str
    min_vram_gb: float
    max_model_len: int
    gpu_memory_utilization: float = 0.90
    quantization: str | None = None
    dtype: str = "auto"
    enforce_eager: bool = False
    trust_remote_code: bool = False
    extra_args: tuple[str, ...] = field(default_factory=tuple)

    def vllm_args(self, *, host: str, port: int) -> list[str]:
        args = [
            "vllm", "serve", self.model_ref,
            "--served-model-name", self.served_model_name,
            "--host", host,
            "--port", str(port),
            "--max-model-len", str(self.max_model_len),
            "--gpu-memory-utilization", str(self.gpu_memory_utilization),
            "--dtype", self.dtype,
        ]
        if self.quantization:
            args += ["--quantization", self.quantization]
        if self.enforce_eager:
            args.append("--enforce-eager")
        if self.trust_remote_code:
            args.append("--trust-remote-code")
        args.extend(self.extra_args)
        return args
