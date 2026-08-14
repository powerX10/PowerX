from pathlib import Path

IMAGE_EXT = {".png",".jpg",".jpeg",".webp"}
DOC_EXT = {".pdf",".txt",".md",".json",".csv"}

def attachment_kind(filename: str, mime: str | None = None) -> str:
    ext = Path(filename).suffix.lower()
    if mime and mime.startswith("image/"): return "image"
    if mime and mime.startswith("audio/"): return "audio"
    if ext in IMAGE_EXT: return "image"
    if ext in DOC_EXT: return "document"
    return "file"

def required_task(kind: str) -> str:
    if kind == "image": return "vision_analysis"
    if kind == "audio": return "speech_to_text"
    return "deep_reasoning"
