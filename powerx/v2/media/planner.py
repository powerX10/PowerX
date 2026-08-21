from __future__ import annotations
import hashlib, math, re, uuid
from pathlib import Path
from .schema import MediaProjectRequest, MediaProjectPlan, MediaSegment

def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:40] or "project"

def expand_scene_prompt(base: str, index: int, total: int, metadata: dict) -> str:
    style = metadata.get("style", "photorealistic, coherent, cinematic")
    subject = metadata.get("subject", "")
    continuity = metadata.get("continuity", "maintain same identity, wardrobe, lighting logic and environment unless scene requires change")
    chapter = metadata.get("chapter", "")
    return (
        f"{base}\n"
        f"Segment {index+1}/{total}. {chapter}\n"
        f"{subject}\n"
        f"Visual direction: {style}. {continuity}. "
        f"Create a self-contained shot that naturally continues from the previous shot and can cut cleanly into the next."
    ).strip()

class LongFormPlanner:
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)

    def plan(self, req: MediaProjectRequest) -> MediaProjectPlan:
        if req.duration_seconds <= 0:
            raise ValueError("duration_seconds must be > 0")
        if req.segment_seconds < 2 or req.segment_seconds > 60:
            raise ValueError("segment_seconds must be between 2 and 60")
        if req.width < 256 or req.height < 256:
            raise ValueError("invalid output dimensions")
        project_id = req.project_id or f"{_slug(req.prompt)}-{uuid.uuid4().hex[:8]}"
        total = math.ceil(req.duration_seconds / req.segment_seconds)
        segs = []
        for i in range(total):
            start = i * req.segment_seconds
            dur = min(req.segment_seconds, req.duration_seconds - start)
            raw = f"{project_id}:{i}:{start}:{dur}".encode()
            seg_id = hashlib.sha1(raw).hexdigest()[:16]
            out = self.project_root / project_id / "segments" / f"{i:06d}-{seg_id}.mp4"
            segs.append(MediaSegment(
                index=i,
                segment_id=seg_id,
                start_seconds=start,
                duration_seconds=dur,
                prompt=expand_scene_prompt(req.prompt, i, total, req.metadata),
                output_path=str(out),
                metadata={"chapter": req.metadata.get("chapter"), "total_segments": total},
            ))
        return MediaProjectPlan(
            project_id=project_id, prompt=req.prompt, duration_seconds=req.duration_seconds,
            width=req.width, height=req.height, fps=req.fps, segment_seconds=req.segment_seconds,
            segments=segs, metadata=req.metadata
        )
