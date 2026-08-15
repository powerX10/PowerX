import json, shutil, time
from pathlib import Path

class LocalModelCache:
    def __init__(self, root: Path, max_bytes: int):
        self.root = root.expanduser()
        self.root.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes
        self.index = self.root/".powerx-cache.json"

    def _read(self):
        return json.loads(self.index.read_text()) if self.index.exists() else {}

    def _write(self,d):
        self.index.write_text(json.dumps(d, indent=2))

    def _size(self,p):
        return sum(x.stat().st_size for x in p.rglob("*") if x.is_file())

    def touch(self, model_id, path):
        d=self._read()
        d[model_id]={"path":str(path),"bytes":self._size(path),"last_used":time.time()}
        self._write(d)

    def ensure_space(self, required_bytes, protected=()):
        d=self._read()
        def used():
            return sum(v["bytes"] for v in d.values() if Path(v["path"]).exists())
        victims=sorted(
            ((k,v) for k,v in d.items() if k not in protected),
            key=lambda kv:kv[1]["last_used"]
        )
        while used()+required_bytes > self.max_bytes and victims:
            k,v=victims.pop(0)
            shutil.rmtree(v["path"], ignore_errors=True)
            d.pop(k,None)
        if used()+required_bytes > self.max_bytes:
            raise RuntimeError("Insufficient PowerX local model cache")
        self._write(d)
