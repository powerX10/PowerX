from __future__ import annotations
import os
import shutil
from pathlib import Path

from powerx.production.endpoint_config import registry_from_env


def run_preflight() -> dict:
    checks = []

    api_key = os.getenv("POWERX_API_KEY", "")
    checks.append({
        "name": "api_key",
        "ok": len(api_key) >= 24,
        "detail": "configured" if api_key else "missing",
    })

    try:
        registry = registry_from_env()
        endpoints = registry.all()
        checks.append({
            "name": "runtime_endpoints",
            "ok": len(endpoints) > 0,
            "detail": f"{len(endpoints)} configured",
        })
    except Exception as exc:
        checks.append({
            "name": "runtime_endpoints",
            "ok": False,
            "detail": str(exc),
        })

    checks.append({
        "name": "disk_space",
        "ok": shutil.disk_usage(str(Path.home())).free > 1024**3,
        "detail": "at least 1GB free required",
    })

    return {
        "ready": all(c["ok"] for c in checks),
        "checks": checks,
    }
