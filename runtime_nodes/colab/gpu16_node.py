import asyncio, os
from runtime_nodes.common.heartbeat import heartbeat_loop
async def main():
    await heartbeat_loop("gpu16",os.environ["POWERX_COLAB_PUBLIC_URL"],
        ["chat","code","research","reasoning","vision","image_generate","video_generate","file_analyze"],
        ["3b","4b","6b","gpu-heavy"],
        ram_gb=float(os.getenv("POWERX_COLAB_RAM_GB","12")),
        vram_gb=float(os.getenv("POWERX_COLAB_VRAM_GB","16")))
if __name__=="__main__": asyncio.run(main())
