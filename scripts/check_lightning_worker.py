#!/usr/bin/env python3
import json, os, urllib.request
url=os.environ.get("POWERX_LIGHTNING_WORKER_URL","http://127.0.0.1:8081").rstrip("/")+"/health"
req=urllib.request.Request(url)
t=os.environ.get("POWERX_LIGHTNING_WORKER_TOKEN","")
if t:req.add_header("Authorization",f"Bearer {t}")
with urllib.request.urlopen(req,timeout=20) as r:
    print(json.dumps(json.load(r),indent=2))
