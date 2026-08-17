import json,os,time,urllib.request,threading
B=os.getenv("POWERX_PUBLIC_URL","https://power-x-1.vercel.app").rstrip("/")+"/api/runtime";T=os.getenv("POWERX_NODE_TOKEN") or os.getenv("POWERX_WORKER_TOKEN","");N=os.getenv("POWERX_MOBILE_NODE_ID","mobile-"+os.uname().nodename);L="http://127.0.0.1:8080"
def c(path,p=None,t=120,base=None):data=None if p is None else json.dumps(p).encode();req=urllib.request.Request((base or B)+path,data=data,headers={"Content-Type":"application/json","Authorization":"Bearer "+T});return json.loads(urllib.request.urlopen(req,timeout=t).read().decode())
def hb():
 while True:
  try:
   h=c("/health",t=10,base=L);c("/nodes/heartbeat",{"node_id":N,"name":"Android Device","runtime_class":"mobile","models":h.get("supported_models",[]),"capabilities":["chat","coding","deep_reasoning"],"ram_gb":h.get("ram_gb"),"active_model":h.get("active_model")})
  except Exception as e:print("heartbeat",e)
  time.sleep(15)
threading.Thread(target=hb,daemon=True).start();print("POWERX MOBILE NODE ONLINE")
while True:
 try:
  j=c(f"/jobs/pull?runtime_class=mobile&node_id={N}",t=60).get("job")
  if not j:time.sleep(1);continue
  try:r=c("/infer",j,t=1200,base=L);c("/jobs/result",{"job_id":j["id"],"ok":bool(r.get("ok",True)),"result":r if r.get("ok",True) else None,"error":r.get("error")})
  except Exception as e:c("/jobs/result",{"job_id":j["id"],"ok":False,"error":str(e)})
 except KeyboardInterrupt:break
 except Exception as e:print("mobile",e);time.sleep(3)
