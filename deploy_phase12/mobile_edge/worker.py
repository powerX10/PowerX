"""Optional mobile edge pull-worker for small tasks.

The phone advertises only capabilities its local runtime can actually serve.
No large model is forced onto the device.
"""
import json, os, time, urllib.request
BROKER = os.environ["POWERX_BROKER_URL"].rstrip("/")
TOKEN = os.getenv("POWERX_MOBILE_EDGE_TOKEN", "")
LOCAL = os.getenv("POWERX_MOBILE_LOCAL_URL", "http://127.0.0.1:8080").rstrip("/")

def call(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json", "Authorization":f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read().decode())

while True:
    try:
        job = call(BROKER+"/workers/pull?runtime_class=mobile")
        if not job.get("job"):
            time.sleep(3); continue
        result = call(LOCAL+"/infer", job["job"])
        call(BROKER+"/workers/result", {"job_id": job["job"]["id"], "ok": True, "result": result})
    except Exception:
        time.sleep(5)
