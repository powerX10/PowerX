import os, subprocess, time
class LlamaCppManager:
    def __init__(self,binary=None):
        self.binary=binary or os.getenv("POWERX_LLAMA_SERVER","llama-server")
        self.proc=None
    def start(self,model_file,host="127.0.0.1",port=8080,ctx=8192,threads=None):
        if self.proc and self.proc.poll() is None: return
        cmd=[self.binary,"-m",str(model_file),"--host",host,"--port",str(port),"-c",str(ctx)]
        if threads: cmd += ["-t",str(threads)]
        self.proc=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        time.sleep(1)
        if self.proc.poll() is not None: raise RuntimeError("llama-server exited during startup")
    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:self.proc.kill()
        self.proc=None
