from pathlib import Path
class FileSystemTool:
    def __init__(self,root,policy): self.root=Path(root).resolve(); self.policy=policy
    def _safe(self,p):
        x=(self.root/p).resolve()
        if self.root not in x.parents and x!=self.root: raise ValueError("path escapes workspace")
        return x
    def read(self,path): self.policy.check("file_read"); return self._safe(path).read_text()
    def write(self,path,content):
        self.policy.check("file_write"); p=self._safe(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content); return str(p)
