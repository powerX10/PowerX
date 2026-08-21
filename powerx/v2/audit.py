import json,time,uuid
from pathlib import Path
class AuditLog:
    def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
    def write(self,event,**data):
        row={"id":uuid.uuid4().hex,"ts":time.time(),"event":event,**data}
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(row,sort_keys=True)+"\n")
        return row
