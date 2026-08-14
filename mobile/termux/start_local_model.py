import argparse
import json
import os
import sys

from powerx.runtime_cpu.llamacpp.files import validate_gguf
from powerx.runtime_cpu.llamacpp.process import LlamaCppServerManager
from powerx.runtime_cpu.llamacpp.profile import LlamaCppProfile
from powerx.runtime_mobile.device.capability import detect_device, recommended_mobile_tier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--port", type=int, default=8300)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--ctx", type=int, default=8192)
    args = parser.parse_args()

    cap = detect_device()
    check = validate_gguf(args.model)

    print(json.dumps({
        "device": cap.__dict__,
        "recommended_tier": recommended_mobile_tier(cap),
        "model": check,
    }, indent=2))

    if not check["ok"]:
        raise SystemExit(2)

    profile = LlamaCppProfile(
        id="mobile-local",
        model_path_env="POWERX_MOBILE_MODEL",
        served_model_name="powerx-mobile-local",
        context_size=args.ctx,
        threads=args.threads,
        batch_size=128,
        gpu_layers=0,
    )

    manager = LlamaCppServerManager(state_dir=".powerx-mobile-runtime")
    state = manager.start(
        profile,
        model_path=args.model,
        host="127.0.0.1",
        port=args.port,
        startup_timeout=600,
    )
    print(json.dumps(state.__dict__, indent=2))


if __name__ == "__main__":
    main()
