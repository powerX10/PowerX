from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from powerx.final_runtime.registry_sync import FinalRegistrySync

if __name__ == "__main__":
    print(FinalRegistrySync().sync(preserve_existing_runtime_overrides=True))
