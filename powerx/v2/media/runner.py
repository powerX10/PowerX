from __future__ import annotations
from pathlib import Path
from .checkpoints import CheckpointStore
from .composer import FFmpegComposer
from .artifacts import write_artifact_manifest

class LongFormRunner:
    def __init__(self, video_adapter, project_root, max_attempts=3):
        self.adapter=video_adapter; self.project_root=Path(project_root); self.max_attempts=max_attempts

    def render(self, plan):
        pdir=self.project_root/plan.project_id
        store=CheckpointStore(pdir)
        completed=[]
        previous=None
        for seg in plan.segments:
            if store.is_complete(seg.segment_id):
                completed.append(seg.output_path); previous=seg.output_path; continue
            tries=0
            while tries < self.max_attempts:
                tries += 1
                try:
                    store.mark_started(seg.segment_id,seg.output_path)
                    payload={
                        "prompt":seg.prompt,"output_path":seg.output_path,
                        "width":plan.width,"height":plan.height,"fps":plan.fps,
                        "reference_video":previous,
                    }
                    result=self.adapter.run(payload)
                    store.mark_complete(seg.segment_id,seg.output_path,result)
                    completed.append(seg.output_path); previous=seg.output_path
                    break
                except Exception as e:
                    store.mark_failed(seg.segment_id,str(e))
                    if tries >= self.max_attempts: raise
        final=str(pdir/"final"/f"{plan.project_id}-720p.mp4")
        composition=FFmpegComposer().compose(completed,final,plan.width,plan.height,plan.fps)
        manifest=write_artifact_manifest(pdir,final,composition,plan)
        return {"ok":True,"project_id":plan.project_id,"final":final,"manifest":manifest}
