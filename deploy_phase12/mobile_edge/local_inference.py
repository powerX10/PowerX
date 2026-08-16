from __future__ import annotations

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from powerx.runtime_fabric.chat_bridge import mobile_prompt

HOST = os.getenv("POWERX_MOBILE_HOST", "127.0.0.1")
PORT = int(os.getenv("POWERX_MOBILE_PORT", "8080"))
MODEL = Path(os.path.expanduser(os.getenv(
    "POWERX_MOBILE_MODEL",
    "~/.cache/powerx-mobile/models/qwen2.5-0.5b-instruct-q4_k_m.gguf",
)))
LLAMA = Path(os.path.expanduser(os.getenv(
    "POWERX_LLAMA_CLI",
    "~/.local/powerx-mobile/llama.cpp/build/bin/llama-cli",
)))
THREADS = int(os.getenv("POWERX_MOBILE_THREADS", str(max(2, (os.cpu_count() or 4) - 2))))
MAX_TOKENS = int(os.getenv("POWERX_MOBILE_MAX_TOKENS", "256"))


def run_inference(body: dict) -> dict:
    if not LLAMA.exists():
        raise RuntimeError(f"llama-cli missing: {LLAMA}")
    if not MODEL.exists():
        raise RuntimeError(f"mobile model missing: {MODEL}")

    prompt = mobile_prompt(body)
    payload = body.get("payload") if isinstance(body.get("payload"), dict) else body
    max_tokens = int(payload.get("max_tokens", MAX_TOKENS))

    cmd = [
        str(LLAMA),
        "-m", str(MODEL),
        "-p", prompt,
        "-n", str(max_tokens),
        "-t", str(THREADS),
        "--temp", str(float(payload.get("temperature", 0.2))),
        "--no-display-prompt",
        "--simple-io",
    ]
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout)[-4000:])
    return {
        "ok": True,
        "runtime_class": "mobile",
        "model_id": "qwen2.5-0.5b-instruct-q4_k_m",
        "text": p.stdout.strip(),
    }


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        raw = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {
                "ok": LLAMA.exists() and MODEL.exists(),
                "runtime_class": "mobile",
                "llama_cli": str(LLAMA),
                "model": str(MODEL),
                "model_ready": MODEL.exists(),
            })
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        if self.path != "/infer":
            self._json(404, {"ok": False, "error": "not_found"})
            return
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n) or b"{}")
            self._json(200, run_inference(body))
        except Exception as exc:
            self._json(500, {"ok": False, "error": str(exc)})

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    print(f"PowerX mobile inference listening on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
