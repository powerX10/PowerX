from dataclasses import dataclass
from pathlib import Path
import os
import platform
import shutil


@dataclass(frozen=True)
class DeviceCapability:
    platform: str
    architecture: str
    total_ram_mb: int | None
    available_ram_mb: int | None
    free_storage_mb: int
    termux: bool


def _memory_linux() -> tuple[int | None, int | None]:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return None, None

    values = {}
    for line in meminfo.read_text(errors="ignore").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parts = value.strip().split()
        if parts and parts[0].isdigit():
            values[key] = int(parts[0]) // 1024

    return values.get("MemTotal"), values.get("MemAvailable")


def detect_device() -> DeviceCapability:
    total, available = _memory_linux()
    usage = shutil.disk_usage(str(Path.home()))

    return DeviceCapability(
        platform=platform.system(),
        architecture=platform.machine(),
        total_ram_mb=total,
        available_ram_mb=available,
        free_storage_mb=usage.free // (1024 * 1024),
        termux=bool(os.getenv("TERMUX_VERSION") or "com.termux" in os.getenv("PREFIX", "")),
    )


def recommended_mobile_tier(cap: DeviceCapability) -> str:
    ram = cap.total_ram_mb or 0
    storage = cap.free_storage_mb

    if ram >= 12000 and storage >= 5000:
        return "4b_quantized"
    if ram >= 8000 and storage >= 3500:
        return "3b_to_4b_quantized"
    if ram >= 6000 and storage >= 2500:
        return "1b_to_3b_quantized"
    return "1b_quantized"
