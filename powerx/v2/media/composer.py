from __future__ import annotations
import json, subprocess
from pathlib import Path

class FFmpegComposer:
    def __init__(self, ffmpeg: str = "ffmpeg", ffprobe: str = "ffprobe"):
        self.ffmpeg = ffmpeg
        self.ffprobe = ffprobe

    def _probe(self, p: Path):
        cmd=[self.ffprobe,"-v","error","-show_entries","format=duration","-of","json",str(p)]
        out=subprocess.check_output(cmd, text=True)
        return float(json.loads(out)["format"]["duration"])

    def compose(self, segment_paths: list[str], output_path: str, width=1280, height=720, fps=24) -> dict:
        if not segment_paths:
            raise ValueError("no segments supplied")
        paths=[Path(x) for x in segment_paths]
        missing=[str(p) for p in paths if not p.is_file() or p.stat().st_size == 0]
        if missing:
            raise FileNotFoundError(f"missing/empty segments: {missing[:5]}")
        out=Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        concat=out.with_suffix(".concat.txt")
        concat.write_text("\n".join("file '" + str(p.resolve()).replace("'", "'\\''") + "'" for p in paths))
        vf=f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps={fps}"
        cmd=[
            self.ffmpeg,"-y","-f","concat","-safe","0","-i",str(concat),
            "-vf",vf,"-c:v","libx264","-preset","medium","-crf","18",
            "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)
        ]
        subprocess.check_call(cmd)
        duration=self._probe(out)
        return {"output_path":str(out),"duration_seconds":duration,"segments":len(paths),
                "width":width,"height":height,"fps":fps}
