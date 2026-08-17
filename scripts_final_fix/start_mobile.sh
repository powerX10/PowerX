#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$HOME/PowerX";pkg install -y tmux wget >/dev/null;command -v termux-wake-lock >/dev/null 2>&1&&termux-wake-lock||true
T="$(cat "$HOME/.config/powerx/node_token")";export PYTHONPATH="$HOME/PowerX"
tmux kill-session -t powerx-mobile-local 2>/dev/null||true;tmux kill-session -t powerx-mobile-worker 2>/dev/null||true
tmux new-session -d -s powerx-mobile-local "cd $HOME/PowerX; export PYTHONPATH=$HOME/PowerX; exec python deploy_phase12/mobile_edge/local_inference.py >>$HOME/powerx-mobile-local.log 2>&1"
sleep 2
tmux new-session -d -s powerx-mobile-worker "cd $HOME/PowerX; export PYTHONPATH=$HOME/PowerX; export POWERX_NODE_TOKEN='$T'; exec python deploy_phase12/mobile_edge/worker.py >>$HOME/powerx-mobile-worker.log 2>&1"
echo "PowerX mobile node started."
