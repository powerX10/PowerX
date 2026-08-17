import os,time,json,urllib.request,subprocess,threading,pathlib
BROKER=os.environ.get("POWERX_PUBLIC_URL","https://power-x-1.vercel.app").rstrip("/")+"/api/runtime";TOKEN=os.environ["POWERX_NODE_TOKEN"];NODE=os.environ.get("POWERX_CPU_NODE_ID","cpu-primary")
CACHE=pathlib.Path(os.path.expanduser(os.environ.get("POWERX_CPU_MODEL_CACHE","~/.cache/powerx-cpu/models")));CACHE.mkdir(parents=True,exist_ok=True);SERVER=os.environ.get("POWERX_LLAMA_SERVER","llama-server")
S={"qwen25-3b-general":("Qwen/Qwen2.5-3B-Instruct-GGUF","qwen2.5-3b-instruct-q4_k_m.gguf"),"qwen3-4b-reasoning":("Qwen/Qwen3-4B-GGUF","Qwen3-4B-Q4_K_M.gguf"),"qwen25-coder-3b":("Qwen/Qwen2.5-Coder-3B-Instruct-GGUF","qwen2.5-coder-3b-instruct-q4_k_m.gguf")};active={"model":None,"proc":None};PORT=19091
def call(path,payload=None,timeout=60):data=None if payload is None else json.dumps(payload).encode();req=urllib.request.Request(BROKER+path,data=data,headers={"Content-Type":"application/json","Authorization":"Bearer "+TOKEN});return json.loads(urllib.request.urlopen(req,timeout=timeout).read().decode())
def ram():
 try:return round(os.sysconf("SC_PHYS_PAGES")*os.sysconf("SC_PAGE_SIZE")/1024**3,2)
 except:return 0
def heartbeat():
 while True:
  try:call("/nodes/heartbeat",{"node_id":NODE,"name":"PowerX CPU Primary","runtime_class":"cpu","models":list(S),"capabilities":["chat","coding","deep_reasoning"],"ram_gb":ram()})
  except Exception as e:print("heartbeat",e)
  time.sleep(15)
def model(mid):
 repo,file=S[mid];p=CACHE/file
 if not p.exists():subprocess.run(["wget","-c","-O",str(p),f"https://huggingface.co/{repo}/resolve/main/{file}?download=true"],check=True)
 return p
def ensure(mid):
 if active["model"]==mid and active["proc"] and active["proc"].poll() is None:return
 if active["proc"] and active["proc"].poll() is None:active["proc"].terminate();active["proc"].wait(timeout=8)
 p=model(mid);active["proc"]=subprocess.Popen([SERVER,"-m",str(p),"--host","127.0.0.1","--port",str(PORT),"-c","4096","-t",str(max(2,(os.cpu_count() or 4)-1))],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT);active["model"]=mid
 for _ in range(120):
  try:
   if urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health",timeout=2).status==200:return
  except:time.sleep(1)
 raise RuntimeError("llama-server start timeout")
def infer(j):
 mid=j["model_id"];ensure(mid);p=j.get("payload") or {};msgs=p.get("messages") or [];text=p.get("text") or ""
 if text and (not msgs or msgs[-1].get("content")!=text):msgs=[*msgs,{"role":"user","content":text}]
 req=urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/chat/completions",data=json.dumps({"messages":msgs or [{"role":"user","content":text}],"max_tokens":512,"temperature":0.2}).encode(),headers={"Content-Type":"application/json"});return json.loads(urllib.request.urlopen(req,timeout=900).read().decode())
threading.Thread(target=heartbeat,daemon=True).start();print("POWERX CPU NODE ONLINE")
while True:
 try:
  j=call(f"/jobs/pull?runtime_class=cpu&node_id={NODE}",timeout=60).get("job")
  if not j:time.sleep(1);continue
  try:call("/jobs/result",{"job_id":j["id"],"ok":True,"result":infer(j)})
  except Exception as e:call("/jobs/result",{"job_id":j["id"],"ok":False,"error":str(e)})
 except KeyboardInterrupt:break
 except Exception as e:print("worker",e);time.sleep(3)
