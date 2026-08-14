from __future__ import annotations
from dataclasses import dataclass
import json
import shutil
import subprocess


@dataclass(frozen=True)
class GPUDevice:
    index: int
    name: str
    total_vram_mb: int
    free_vram_mb: int | None
    compute_capability: str | None = None


class GPUCapabilityDetector:
    @staticmethod
    def nvidia_available() -> bool:
        return shutil.which("nvidia-smi") is not None

    @classmethod
    def detect(cls) -> list[GPUDevice]:
        if not cls.nvidia_available():
            return []

        cmd = [
            "nvidia-smi",
            "--query-gpu=index,name,memory.total,memory.free,compute_cap",
            "--format=csv,noheader,nounits",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return []

        devices: list[GPUDevice] = []
        for line in result.stdout.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 5:
                continue
            devices.append(
                GPUDevice(
                    index=int(parts[0]),
                    name=parts[1],
                    total_vram_mb=int(float(parts[2])),
                    free_vram_mb=int(float(parts[3])),
                    compute_capability=parts[4] or None,
                )
            )
        return devices

    @classmethod
    def best_device(cls) -> GPUDevice | None:
        devices = cls.detect()
        if not devices:
            return None
        return max(devices, key=lambda d: (d.free_vram_mb or 0, d.total_vram_mb))

    @classmethod
    def summary(cls) -> dict:
        devices = cls.detect()
        return {
            "nvidia_available": bool(devices),
            "devices": [d.__dict__ for d in devices],
        }
