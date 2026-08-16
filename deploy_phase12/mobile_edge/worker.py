"""PowerX mobile edge worker.

Pulls only `runtime_class=mobile` jobs. The required tiny model is bootstrapped
automatically by bootstrap_termux.sh; users do not manually download weights.
"""
import json
import os
import time
import urllib.request

BROKER = os.environ["POWERX_BROKER_URL"].rstrip("/")
TOKEN = os.getenv("POWERX_MOBILE_EDGE_TOKEN") or os.getenv("POWERX_WORKER_TOKEN", "")
LOCAL = os.getenv("POWERX_MOBILE_LOCAL_URL", "http://127.0.0.1:8080").rstrip("/")


def call(url, payload=None, timeout=300):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


print("POWERX MOBILE EDGE WORKER ONLINE")

while True:
    try:
        job_resp = call(BROKER + "/workers/pull?runtime_class=mobile", timeout=60)
        job = job_resp.get("job")
        if not job:
            time.sleep(3)
            continue

        try:
            result = call(LOCAL + "/infer", job, timeout=300)
            ok = bool(result.get("ok", True))
            call(BROKER + "/workers/result", {
                "job_id": job["id"],
                "ok": ok,
                "result": result if ok else None,
                "error": None if ok else result.get("error", "mobile inference failed"),
            }, timeout=60)
        except Exception as exc:
            call(BROKER + "/workers/result", {
                "job_id": job["id"],
                "ok": False,
                "error": str(exc),
            }, timeout=60)
    except KeyboardInterrupt:
        break
    except Exception as exc:
        print("MOBILE WORKER ERROR:", repr(exc))
        time.sleep(5)
