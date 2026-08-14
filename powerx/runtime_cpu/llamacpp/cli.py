import argparse
import json

from powerx.runtime_cpu.llamacpp.controller import CPURuntimeController
from powerx.runtime_cpu.llamacpp.files import validate_gguf


def main():
    parser = argparse.ArgumentParser(prog="powerx-cpu")
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate-model")
    v.add_argument("path")

    s = sub.add_parser("start")
    s.add_argument("model_id")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8200)

    s = sub.add_parser("stop")
    s.add_argument("model_id")

    s = sub.add_parser("status")
    s.add_argument("model_id")

    args = parser.parse_args()

    if args.cmd == "validate-model":
        print(json.dumps(validate_gguf(args.path), indent=2))
        return

    ctl = CPURuntimeController()
    if args.cmd == "start":
        out = ctl.start(args.model_id, host=args.host, port=args.port)
    elif args.cmd == "stop":
        out = ctl.stop(args.model_id)
    else:
        out = ctl.status(args.model_id)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
