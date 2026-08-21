import subprocess
DENY_TOKENS=("rm -rf /","mkfs","dd if=","shutdown","reboot",":(){:|:&};:")
class ShellTool:
    def __init__(self,cwd,policy,timeout=120): self.cwd=cwd; self.policy=policy; self.timeout=timeout
    def run(self,command,write=False):
        self.policy.check("test_run" if not write else "file_write")
        if any(x in command.lower() for x in DENY_TOKENS): raise RuntimeError("dangerous shell command blocked")
        p=subprocess.run(command,shell=True,cwd=self.cwd,text=True,capture_output=True,timeout=self.timeout)
        return {"returncode":p.returncode,"stdout":p.stdout[-20000:],"stderr":p.stderr[-20000:]}
