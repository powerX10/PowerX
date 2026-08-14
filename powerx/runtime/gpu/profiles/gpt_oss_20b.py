from powerx.runtime.gpu.profile import GPUModelProfile

GPT_OSS_20B = GPUModelProfile(
    id="gpt-oss-20b",
    model_ref="openai/gpt-oss-20b",
    served_model_name="openai/gpt-oss-20b",
    min_vram_gb=16.0,
    max_model_len=32768,
    gpu_memory_utilization=0.92,
    dtype="auto",
)
