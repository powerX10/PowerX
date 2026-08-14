#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r powerx/runtime/gpu/requirements-gpu.txt

echo "PowerX GPU runtime dependencies installed."
echo "Detect GPU with:"
echo "python -m powerx.runtime.gpu.cli detect"
