import argparse
import json
from powerx.runtime.gpu.capabilities import GPUCapabilityDetector
from powerx.runtime.gpu.controller import GPURuntimeController


def main():
    parser = argparse.ArgumentParser(prog="powerx-gpu")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("detect")

    s = sub.add_parser("start")
    s.add_argument("model_id")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8100)

    s = sub.add_parser("stop")
    s.add_argument("model_id")

    s = sub.add_parser("status")
    s.add_argument("model_id")

    args = parser.parse_args()

    if args.cmd == "detect":
        print(json.dumps(GPUCapabilityDetector.summary(), indent=2))
        return

    ctl = GPURuntimeController()

    if args.cmd == "start":
        result = ctl.start(args.model_id, args.host, args.port)
    elif args.cmd == "stop":
        result = ctl.stop(args.model_id)
    else:
        result = ctl.status(args.model_id)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
