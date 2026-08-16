#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$HOME/PowerX"

if [ -z "${POWERX_BROKER_URL:-}" ]; then
  export POWERX_BROKER_URL="https://tradewithzara63--powerx-runtime-broker-api.modal.run"
fi

if [ -z "${POWERX_WORKER_TOKEN:-}" ] && [ -f "$HOME/.config/powerx/worker_token" ]; then
  export POWERX_WORKER_TOKEN="$(cat "$HOME/.config/powerx/worker_token")"
fi

export PYTHONPATH="$HOME/PowerX"
export POWERX_LLAMA_CLI="$HOME/.local/powerx-mobile/prebuilt/llama-b10173/llama-cli"
export LD_LIBRARY_PATH="$HOME/.local/powerx-mobile/prebuilt/llama-b10173:${LD_LIBRARY_PATH:-}"

bash deploy_phase12/mobile_edge/bootstrap_termux.sh

tmux kill-session -t powerx-mobile-local 2>/dev/null || true
tmux kill-session -t powerx-mobile-worker 2>/dev/null || true

tmux new-session -d -s powerx-mobile-local \
  "cd $HOME/PowerX; export PYTHONPATH=$HOME/PowerX; export POWERX_LLAMA_CLI=$HOME/.local/powerx-mobile/prebuilt/llama-b10173/llama-cli; export LD_LIBRARY_PATH=$HOME/.local/powerx-mobile/prebuilt/llama-b10173; exec python deploy_phase12/mobile_edge/local_inference.py >> $HOME/powerx-mobile-local.log 2>&1"

sleep 2

tmux new-session -d -s powerx-mobile-worker \
  "cd $HOME/PowerX; export PYTHONPATH=$HOME/PowerX; export POWERX_BROKER_URL=$POWERX_BROKER_URL; export POWERX_WORKER_TOKEN=$POWERX_WORKER_TOKEN; exec python deploy_phase12/mobile_edge/worker.py >> $HOME/powerx-mobile-worker.log 2>&1"

echo "PowerX mobile runtime started."
