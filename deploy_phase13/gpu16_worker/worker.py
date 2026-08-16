import base64,gc,io,json,os,time,urllib.request
BROKER=os.environ["POWERX_BROKER_URL"].rstrip("/");TOKEN=os.getenv("POWERX_WORKER_TOKEN","");loaded={}
def call(path,p=None):
    d=None if p is None else json.dumps(p).encode();r=urllib.request.Request(BROKER+path,data=d,headers={"Content-Type":"application/json","Authorization":f"Bearer {TOKEN}"})
    with urllib.request.urlopen(r,timeout=120) as x:return json.loads(x.read().decode())
def clear():
    loaded.clear();gc.collect()
    try:
        import torch;torch.cuda.empty_cache()
    except Exception:pass
def infer(j):
    p=j.get("payload") or {};mid=p.get("model_id");cap=j.get("capability")
    if loaded and mid not in loaded:clear()
    if cap in {"image_generate","image_edit"}:
        import torch
        from diffusers import StableDiffusionXLPipeline
        if mid not in loaded:
            src=os.getenv("POWERX_SDXL_LOCAL","/content/drive/MyDrive/PowerX/Models/19-image-sdxl")
            loaded[mid]=StableDiffusionXLPipeline.from_pretrained(src,torch_dtype=torch.float16,use_safetensors=True).to("cuda")
        im=loaded[mid](p.get("prompt",""),width=int(p.get("width",1024)),height=int(p.get("height",1024)),num_inference_steps=int(p.get("steps",30))).images[0]
        b=io.BytesIO();im.save(b,format="PNG");return {"mime_type":"image/png","image_b64":base64.b64encode(b.getvalue()).decode()}
    if cap=="video_generate":
        import torch
        from diffusers import WanPipeline
        if mid not in loaded:
            src=os.getenv("POWERX_WAN_LOCAL","/content/drive/MyDrive/PowerX/Models/20-video-wan21-1.3b")
            loaded[mid]=WanPipeline.from_pretrained(src,torch_dtype=torch.float16).to("cuda")
        return {"frames":loaded[mid](prompt=p.get("prompt",""),num_inference_steps=int(p.get("steps",30))).frames}
    raise RuntimeError(f"gpu16 adapter not active for {cap}")
print("POWERX PHASE13 GPU16 WORKER ONLINE")
while True:
    try:
        q=call("/workers/pull?runtime_class=gpu16");j=q.get("job")
        if not j:time.sleep(2);continue
        try:call("/workers/result",{"job_id":j["id"],"ok":True,"result":infer(j)})
        except Exception as e:call("/workers/result",{"job_id":j["id"],"ok":False,"error":str(e)})
    except KeyboardInterrupt:break
    except Exception as e:print(repr(e));time.sleep(5)
