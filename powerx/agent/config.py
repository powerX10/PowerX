import os
from .runtime_scheduler import RuntimeScheduler, RuntimeSpec
def scheduler_from_env():
    s=RuntimeScheduler()
    def add(prefix, runtime_class, caps, model):
        url=os.getenv(prefix+"_BASE_URL")
        if url: s.register(RuntimeSpec(prefix.lower(),runtime_class,set(caps),url,os.getenv(prefix+"_MODEL",model),api_key=os.getenv(prefix+"_API_KEY")))
    add("POWERX_GPU16_TEXT","gpu16",{"chat","code","research","file_analyze"},"Qwen2.5-Coder-7B-Instruct")
    add("POWERX_GPU16_VISION","gpu16",{"vision"},"Qwen2.5-VL-3B-Instruct")
    add("POWERX_GPU16_IMAGE","gpu16",{"image_generate"},"stable-diffusion-xl-base-1.0")
    add("POWERX_GPU16_VIDEO","gpu16",{"video_generate"},"Wan2.1-T2V-1.3B")
    add("POWERX_MOBILE_TEXT","mobile",{"chat","code","research","file_analyze"},"qwen2.5-coder-3b")
    add("POWERX_MOBILE_VISION","mobile",{"vision"},"qwen2.5-vl-3b")
    add("POWERX_MODAL_TEXT","cloud",{"chat","code","research","file_analyze"},"gpt-oss")
    add("POWERX_BEAM_TEXT","cloud",{"chat","code","research","file_analyze"},"gpt-oss")
    return s
