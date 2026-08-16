#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from powerx.runtime_fabric.cms_patch import apply_cpu_first_policy
print(apply_cpu_first_policy())
