#!/data/data/com.termux/files/usr/bin/bash
tmux kill-session -t powerx-mobile-worker 2>/dev/null || true
tmux kill-session -t powerx-mobile-local 2>/dev/null || true
echo "PowerX mobile runtime stopped."
