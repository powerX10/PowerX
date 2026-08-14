from pathlib import Path


def validate_gguf(path: str) -> dict:
    p = Path(path).expanduser().resolve()

    if not p.exists():
        return {"ok": False, "error": "model file does not exist", "path": str(p)}

    if not p.is_file():
        return {"ok": False, "error": "model path is not a file", "path": str(p)}

    size = p.stat().st_size
    if size < 1024 * 1024:
        return {"ok": False, "error": "model file is unexpectedly small", "path": str(p)}

    with p.open("rb") as f:
        magic = f.read(4)

    if magic != b"GGUF":
        return {
            "ok": False,
            "error": "file is not a valid GGUF model",
            "path": str(p),
        }

    return {
        "ok": True,
        "path": str(p),
        "size_bytes": size,
        "size_gb": round(size / (1024 ** 3), 3),
    }
