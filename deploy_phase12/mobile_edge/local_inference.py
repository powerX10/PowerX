import json,os,subprocess,time,urllib.request,pathlib
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
H=pathlib.Path.home();BASE=H/".local/powerx-mobile/prebuilt/llama-b10173";SERVER=BASE/"llama-server";CLI=BASE/"llama-cli";CACHE=H/".cache/powerx-mobile/models";CACHE.mkdir(parents=True,exist_ok=True);LP=18081;PORT=8080
S={"qwen25-3b-general":("Qwen/Qwen2.5-3B-Instruct-GGUF","qwen2.5-3b-instruct-q4_k_m.gguf",5.0),"qwen25-coder-3b":("Qwen/Qwen2.5-Coder-3B-Instruct-GGUF","qwen2.5-coder-3b-instruct-q4_k_m.gguf",5.0),"qwen3-4b-reasoning":("Qwen/Qwen3-4B-GGUF","Qwen3-4B-Q4_K_M.gguf",7.0)};A={"model":None,"proc":None}
def ram():
 try:return round(os.sysconf("SC_PHYS_PAGES")*os.sysconf("SC_PAGE_SIZE")/1024**3,2)
 except:return 0
def supported():return[k for k,v in S.items() if ram()>=v[2]]
def model(mid):
 repo,file,need=S[mid]
 if ram()<need:raise RuntimeError(f"{mid} needs about {need} GB RAM; device reports {ram()} GB")
 p=CACHE/file
 if not p.exists():subprocess.run(["wget","-c","-O",str(p),f"https://huggingface.co/{repo}/resolve/main/{file}?download=true"],check=True)
 return p
def ensure(mid):
 if A["model"]==mid and A["proc"] and A["proc"].poll() is None:return
 p=model(mid)
 if A["proc"] and A["proc"].poll() is None:A["proc"].terminate();A["proc"].wait(timeout=5)
 if not SERVER.exists():return
 env=os.environ.copy();env["LD_LIBRARY_PATH"]=str(BASE)+":"+env.get("LD_LIBRARY_PATH","");A["proc"]=subprocess.Popen([str(SERVER),"-m",str(p),"--host","127.0.0.1","--port",str(LP),"-c","4096","-t",str(max(2,(os.cpu_count() or 4)-2))],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT);A["model"]=mid
 for _ in range(90):
  try:
   if urllib.request.urlopen(f"http://127.0.0.1:{LP}/health",timeout=2).status==200:return
  except:time.sleep(1)
 raise RuntimeError("mobile llama-server start timeout")
def infer(b):
 mid=b.get("model_id") or "qwen25-3b-general";p=b.get("payload") or {};ensure(mid);msgs=p.get("messages") or [];text=p.get("text") or ""
 if text and (not msgs or msgs[-1].get("content")!=text):msgs=[*msgs,{"role":"user","content":text}]
 if SERVER.exists():
  req=urllib.request.Request(f"http://127.0.0.1:{LP}/v1/chat/completions",data=json.dumps({"messages":msgs or [{"role":"user","content":text}],"max_tokens":512,"temperature":0.2}).encode(),headers={"Content-Type":"application/json"});return{"ok":True,"runtime_class":"mobile","model_id":mid,"result":json.loads(urllib.request.urlopen(req,timeout=900).read().decode())}
 q=model(mid);env=os.environ.copy();env["LD_LIBRARY_PATH"]=str(BASE)+":"+env.get("LD_LIBRARY_PATH","");prompt="\n".join(f"{m.get('role')}: {m.get('content')}" for m in msgs) or text;o=subprocess.run([str(CLI),"-m",str(q),"-p",prompt,"-n","512","-t",str(max(2,(os.cpu_count() or 4)-2)),"--simple-io","--no-display-prompt"],env=env,text=True,capture_output=True,timeout=900);return{"ok":True,"runtime_class":"mobile","model_id":mid,"result":{"text":o.stdout.strip()}}
class X(BaseHTTPRequestHandler):
 def j(self,s,x):b=json.dumps(x).encode();self.send_response(s);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):self.j(200,{"ok":True,"ram_gb":ram(),"supported_models":supported(),"active_model":A["model"]}) if self.path=="/health" else self.j(404,{"ok":False})
 def do_POST(self):
  try:n=int(self.headers.get("Content-Length","0"));self.j(200,infer(json.loads(self.rfile.read(n) or b"{}")))
  except Exception as e:self.j(500,{"ok":False,"error":str(e)})
 def log_message(self,*a):pass
print("PowerX mobile",ram(),"GB",supported());ThreadingHTTPServer(("127.0.0.1",PORT),X).serve_forever()
