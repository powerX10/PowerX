import hashlib
from pathlib import Path

def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8*1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def write_checksums(root: Path):
    lines = []
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name != "SHA256SUMS"):
        lines.append(f"{sha256_file(p)}  {p.relative_to(root)}")
    (root/"SHA256SUMS").write_text("\n".join(lines) + ("\n" if lines else ""))

def verify_checksums(root: Path):
    f = root/"SHA256SUMS"
    if not f.exists():
        return ["SHA256SUMS missing"]
    errors=[]
    for line in f.read_text().splitlines():
        expected, rel = line.split("  ",1)
        p = root/rel
        if not p.exists(): errors.append(f"missing:{rel}")
        elif sha256_file(p) != expected: errors.append(f"mismatch:{rel}")
    return errors
