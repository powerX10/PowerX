#!/data/data/com.termux/files/usr/bin/bash

export POWERX_LLAMA_CLI="$HOME/.local/powerx-mobile/prebuilt/llama-b10173/llama-cli"
export LD_LIBRARY_PATH="$HOME/.local/powerx-mobile/prebuilt/llama-b10173:${LD_LIBRARY_PATH:-}"
