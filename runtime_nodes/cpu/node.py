import asyncio, os
from pathlib import Path
from runtime_nodes.cpu.llamacpp_manager import LlamaCppManager
from runtime_nodes.common.heartbeat import heartbeat_loop

async def main():
    model=Path(os.environ["POWERX_CPU_MODEL_FILE"])
    port=int(os.getenv("POWERX_CPU_PORT","8080"))
    m=LlamaCppManager()
    m.start(model,host="0.0.0.0",port=port,threads=int(os.getenv("POWERX_CPU_THREADS","4")))
    await heartbeat_loop("cpu",os.getenv("POWERX_CPU_PUBLIC_URL",f"http://127.0.0.1:{port}"),
                         ["chat","code","research","reasoning","file_analyze"],
                         ["3b","4b","6b"],ram_gb=float(os.getenv("POWERX_CPU_RAM_GB","8")),always_on=True)
if __name__=="__main__": asyncio.run(main())
