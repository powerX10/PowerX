from pathlib import Path
from .base import Tool
ROOT=Path.home()/".powerx_workspace"; ROOT.mkdir(parents=True,exist_ok=True)
def _safe(path):
    p=(ROOT/path).resolve()
    if ROOT.resolve() not in p.parents and p != ROOT.resolve(): raise ValueError("Path escapes PowerX workspace")
    return p
async def file_read(args):
    p=_safe(args["path"]); return {"path":str(p.relative_to(ROOT)),"content":p.read_text()}
async def file_write(args):
    p=_safe(args["path"]); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(args["content"]); return {"ok":True,"path":str(p.relative_to(ROOT))}
TOOLS=[Tool("file_read","Read a workspace file.",file_read),Tool("file_write","Write a workspace file.",file_write,True)]
