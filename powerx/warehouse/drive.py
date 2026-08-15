import shutil, subprocess
from pathlib import Path

class MountedDriveWarehouse:
    def __init__(self, root: Path):
        self.root = root.expanduser()
        self.root.mkdir(parents=True, exist_ok=True)
    def exists(self, folder):
        p = self.root / folder
        return p.exists() and any(p.rglob("*"))
    def stage_to(self, folder, destination: Path):
        src = self.root / folder
        if not src.exists():
            raise FileNotFoundError(src)
        dst = destination / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return dst

class RcloneDriveWarehouse:
    def __init__(self, remote: str, root: str="PowerX/Models"):
        self.remote, self.root = remote.rstrip(":"), root.strip("/")
    def _r(self, folder):
        return f"{self.remote}:{self.root}/{folder}"
    def exists(self, folder):
        r = subprocess.run(["rclone","lsf",self._r(folder),"--max-depth","1"],
                           capture_output=True,text=True)
        return r.returncode == 0 and bool(r.stdout.strip())
    def stage_to(self, folder, destination: Path):
        dst = destination / folder
        dst.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rclone","copy",self._r(folder),str(dst),
                        "--transfers","4","--checkers","8","--fast-list"], check=True)
        return dst
