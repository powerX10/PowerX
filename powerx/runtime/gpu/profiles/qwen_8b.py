from powerx.runtime.gpu.profile import GPUModelProfile

QWEN_8B = GPUModelProfile(
    id="qwen-8b",
    model_ref="Qwen/Qwen3-8B",
    served_model_name="qwen3-8b",
    min_vram_gb=10.0,
    max_model_len=32768,
    gpu_memory_utilization=0.88,
    dtype="auto",
)
