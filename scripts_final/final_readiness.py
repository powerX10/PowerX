from __future__ import annotations
import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from powerx.final_runtime.readiness import FinalReadinessAudit

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check-endpoints", action="store_true")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    result = await FinalReadinessAudit().run(check_endpoints=a.check_endpoints)
    print(json.dumps(result, indent=2))
    if a.strict and not result["operational_ready"]:
        raise SystemExit(2)

if __name__ == "__main__":
    asyncio.run(main())
