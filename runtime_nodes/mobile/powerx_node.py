import os, urllib.request
for key,base in [
("POWERX_MOBILE_TEXT_BASE_URL",os.getenv("POWERX_MOBILE_TEXT_BASE_URL","http://127.0.0.1:8080")),
("POWERX_MOBILE_VISION_BASE_URL",os.getenv("POWERX_MOBILE_VISION_BASE_URL","http://127.0.0.1:8081"))]:
    try:
        with urllib.request.urlopen(base.rstrip("/")+"/health",timeout=2) as r: print(f"{key}={base} # online {r.status}")
    except Exception as e: print(f"{key}={base} # offline: {e}")
