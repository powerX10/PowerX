from __future__ import annotations
from dataclasses import dataclass, asdict
import os, shutil, subprocess

@dataclass
class ResourceSnapshot:
    cpu_count: int
    ram_total_gb: float | None
    disk_free_gb: float
    gpu_name: str | None
    gpu_vram_total_gb: float | None
    cuda_available: bool

    def as_dict(self):
        return asdict(self)

def _ram_total_gb() -> float | None:
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return round((pages * page_size) / (1024**3), 2)
    except Exception:
        return None

def probe(path: str = ".") -> ResourceSnapshot:
    free = shutil.disk_usage(path).free / (1024**3)
    gpu_name = None
    gpu_vram = None
    cuda = False
    try:
        p = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5, check=False,
        )
        if p.returncode == 0 and p.stdout.strip():
            row = p.stdout.strip().splitlines()[0]
            name, mb = [x.strip() for x in row.rsplit(",", 1)]
            gpu_name = name
            gpu_vram = round(float(mb) / 1024, 2)
            cuda = True
    except Exception:
        pass
    return ResourceSnapshot(
        cpu_count=os.cpu_count() or 1,
        ram_total_gb=_ram_total_gb(),
        disk_free_gb=round(free, 2),
        gpu_name=gpu_name,
        gpu_vram_total_gb=gpu_vram,
        cuda_available=cuda,
    )
