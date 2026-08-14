import importlib, json, os, shutil
checks=[]
for mod in ["fastapi","httpx","psutil","aiosqlite"]:
    try: importlib.import_module(mod); checks.append({"name":mod,"ok":True})
    except Exception as e: checks.append({"name":mod,"ok":False,"error":str(e)})
checks.append({"name":"POWERX_API_KEY","ok":bool(os.getenv("POWERX_API_KEY"))})
checks.append({"name":"runtime_endpoints","ok":bool(os.getenv("POWERX_RUNTIME_ENDPOINTS_JSON"))})
checks.append({"name":"disk_free_gt_1gb","ok":shutil.disk_usage(".").free>1024**3})
print(json.dumps({"ready":all(x["ok"] for x in checks),"checks":checks},indent=2))
raise SystemExit(0 if all(x["ok"] for x in checks) else 1)
