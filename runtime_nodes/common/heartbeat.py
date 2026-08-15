import asyncio, os, socket, httpx
async def heartbeat_loop(runtime_class,base_url,capabilities,model_tiers,ram_gb=0,vram_gb=0,always_on=False):
    fabric=os.environ["POWERX_FABRIC_URL"].rstrip("/")
    node_id=os.getenv("POWERX_NODE_ID",f"{runtime_class}-{socket.gethostname()}")
    while True:
        payload={"id":node_id,"runtime_class":runtime_class,"base_url":base_url,
                 "capabilities":capabilities,"model_tiers":model_tiers,
                 "always_on":always_on,"available":True,"load":0.0,
                 "ram_gb":ram_gb,"vram_gb":vram_gb}
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                await c.post(fabric+"/v1/nodes/heartbeat",json=payload)
        except Exception:
            pass
        await asyncio.sleep(30)
