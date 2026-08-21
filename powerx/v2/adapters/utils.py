from __future__ import annotations
from pathlib import Path

TEXT_MODEL_SUFFIXES = (".gguf",)
AUDIO_SUFFIXES = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm")

def first_file(root: Path, suffixes: tuple[str, ...]) -> Path:
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in suffixes and not p.name.lower().startswith("mmproj"))
    if not files:
        raise FileNotFoundError(f"No file matching {suffixes} under {root}")
    return files[0]

def find_mmproj(root: Path) -> Path | None:
    files = sorted(p for p in root.rglob("*.gguf") if "mmproj" in p.name.lower())
    return files[0] if files else None
