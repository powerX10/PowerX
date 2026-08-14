from dataclasses import dataclass

@dataclass(frozen=True)
class InstallableArtifact:
    id: str
    runtime: str
    format: str
    destination_env: str
    notes: str

ARTIFACT_SLOTS = {
    "mobile-primary": InstallableArtifact("mobile-primary","mobile","gguf","POWERX_MOBILE_PRIMARY_GGUF","Quantized local fallback"),
    "mobile-small": InstallableArtifact("mobile-small","mobile","gguf","POWERX_MOBILE_SMALL_GGUF","Smaller local fallback"),
    "cpu-qwen4b": InstallableArtifact("cpu-qwen4b","cpu","gguf","POWERX_QWEN4B_GGUF","CPU llama.cpp model"),
    "cpu-phi-mini": InstallableArtifact("cpu-phi-mini","cpu","gguf","POWERX_PHI_MINI_GGUF","CPU/mobile small model")
}
