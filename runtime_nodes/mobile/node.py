import asyncio, os
from runtime_nodes.common.heartbeat import heartbeat_loop
async def main():
    await heartbeat_loop("mobile",os.getenv("POWERX_MOBILE_PUBLIC_URL","http://127.0.0.1:8080"),
                         ["chat","code","research","reasoning","file_analyze"],
                         [os.getenv("POWERX_MOBILE_TIER","3b")],
                         ram_gb=float(os.getenv("POWERX_MOBILE_RAM_GB","6")))
if __name__=="__main__": asyncio.run(main())
