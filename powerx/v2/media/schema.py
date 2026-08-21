from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class MediaProjectRequest:
    prompt: str
    duration_seconds: int
    width: int = 1280
    height: int = 720
    fps: int = 24
    segment_seconds: int = 8
    project_id: str | None = None
    voice: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MediaSegment:
    index: int
    segment_id: str
    start_seconds: float
    duration_seconds: float
    prompt: str
    output_path: str
    reference_image: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class MediaProjectPlan:
    project_id: str
    prompt: str
    duration_seconds: int
    width: int
    height: int
    fps: int
    segment_seconds: int
    segments: list[MediaSegment]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)
