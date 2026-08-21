from __future__ import annotations
import json, hashlib, time
from pathlib import Path

def sha256(path: str | Path, chunk=1024*1024):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def write_artifact_manifest(project_dir, final_path, composition, plan):
    p=Path(project_dir)/"artifact-manifest.json"
    payload={
        "version":1,"created_at":time.time(),"project_id":plan.project_id,
        "final":{"path":str(final_path),"sha256":sha256(final_path),**composition},
        "requested_duration_seconds":plan.duration_seconds,
        "segment_count":len(plan.segments),
        "metadata":plan.metadata,
    }
    p.write_text(json.dumps(payload,indent=2,sort_keys=True))
    return payload
