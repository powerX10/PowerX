#!/usr/bin/env python3
from pathlib import Path
import json, os
reg=Path(os.getenv("POWERX_REGISTRY_PATH","config/powerx_v2_model_registry.json"))
root=Path(os.getenv("POWERX_WAREHOUSE_ROOT","/mnt/powerx_warehouse"))
data=json.loads(reg.read_text())
missing=[]
for m in data["models"]:
    p=root/m["warehouse_path"]
    ok=p.exists()
    print(("OK  " if ok else "MISS"),m["id"],"->",p)
    if not ok:missing.append(m["id"])
print(f"\nFound {len(data['models'])-len(missing)}/{len(data['models'])} locally. Missing local paths: {len(missing)}")
print("Note: missing local paths may still be available through POWERX_RCLONE_REMOTE.")
