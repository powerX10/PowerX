"""Colab GPU16 pull-worker skeleton.

Colab is not treated as an always-on public server. It polls a PowerX broker URL,
executes GPU jobs, then POSTs results. This survives NAT and avoids hardcoding a
Colab public URL. Set POWERX_BROKER_URL and POWERX_WORKER_TOKEN in the notebook.
"""
import json, os, time, urllib.request
BROKER = os.environ["POWERX_BROKER_URL"].rstrip("/")
TOKEN = os.getenv("POWERX_WORKER_TOKEN", "")

def request(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(BROKER+path, data=data, headers={"Content-Type":"application/json", "Authorization":f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode())

while True:
    try:
        job = request("/workers/pull?runtime_class=gpu16")
        if not job.get("job"):
            time.sleep(3); continue
        # Actual image/video/vision adapter is selected from CMS on the GPU node.
        request("/workers/result", {"job_id": job["job"]["id"], "ok": False, "error": "adapter_not_started"})
    except Exception:
        time.sleep(5)
