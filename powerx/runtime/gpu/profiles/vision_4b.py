from powerx.runtime.gpu.profile import GPUModelProfile

VISION_4B = GPUModelProfile(
    id="vision-4b",
    model_ref="google/gemma-3-4b-it",
    served_model_name="gemma-3-4b",
    min_vram_gb=12.0,
    max_model_len=16384,
    gpu_memory_utilization=0.88,
    dtype="auto",
    trust_remote_code=True,
)
