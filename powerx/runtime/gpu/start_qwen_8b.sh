#!/usr/bin/env bash
set -euo pipefail
python -m powerx.runtime.gpu.cli start qwen-8b --host 127.0.0.1 --port 8101
