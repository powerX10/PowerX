from dataclasses import dataclass
import psutil

@dataclass(frozen=True)
class ResourcePolicy:
    min_free_ram_mb: int = 1024
    max_system_memory_percent: float = 92.0
    max_system_cpu_percent: float = 98.0

def system_resources() -> dict:
    mem = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": mem.percent,
        "available_ram_mb": int(mem.available / 1024 / 1024),
    }

def can_start_work(policy: ResourcePolicy = ResourcePolicy()) -> tuple[bool, dict]:
    r = system_resources()
    ok = (
        r["available_ram_mb"] >= policy.min_free_ram_mb
        and r["memory_percent"] <= policy.max_system_memory_percent
        and r["cpu_percent"] <= policy.max_system_cpu_percent
    )
    return ok, r
