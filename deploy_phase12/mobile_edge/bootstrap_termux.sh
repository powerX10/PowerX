#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$HOME/.local/powerx-mobile"
SRC="$BASE/llama.cpp"
MODEL_DIR="$HOME/.cache/powerx-mobile/models"
MODEL="$MODEL_DIR/qwen2.5-0.5b-instruct-q4_k_m.gguf"
MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf?download=true"

echo "=== POWERX MOBILE BOOTSTRAP ==="
pkg update -y
pkg install -y git cmake ninja clang make wget python

mkdir -p "$BASE" "$MODEL_DIR"

if [ ! -d "$SRC/.git" ]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$SRC"
else
  git -C "$SRC" pull --ff-only || true
fi

echo "=== USE PREBUILT LLAMA CLI ==="
PREBUILT="$HOME/.local/powerx-mobile/prebuilt/llama-b10173"
export POWERX_LLAMA_CLI="$PREBUILT/llama-cli"
export LD_LIBRARY_PATH="$PREBUILT:${LD_LIBRARY_PATH:-}"

if [ ! -x "$POWERX_LLAMA_CLI" ]; then
  echo "Missing prebuilt llama-cli: $POWERX_LLAMA_CLI"
  exit 1
fi

"$POWERX_LLAMA_CLI" --version

if [ ! -s "$MODEL" ]; then
  echo "=== AUTO-DOWNLOAD MOBILE MODEL (~491 MB) ==="
  wget -c -O "$MODEL" "$MODEL_URL"
else
  echo "=== MOBILE MODEL ALREADY CACHED ==="
fi

echo "=== READY ==="
echo "llama-cli: $SRC/build/bin/llama-cli"
echo "model:     $MODEL"
