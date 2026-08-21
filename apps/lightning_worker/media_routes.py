from __future__ import annotations
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from powerx.v2.media.schema import MediaProjectRequest
from powerx.v2.media.planner import LongFormPlanner
from powerx.v2.media.runner import LongFormRunner
from powerx.v2.adapters.wan_video import WanVideoAdapter
from powerx.v2.adapters.sdxl import SDXLAdapter

router=APIRouter(prefix="/v2/media",tags=["media"])
PROJECT_ROOT=Path(os.getenv("POWERX_PROJECT_ROOT","/tmp/powerx-projects"))

class ImageReq(BaseModel):
    model_path:str; prompt:str; output_path:str
    width:int=1024; height:int=1024; steps:int=30

class VideoReq(BaseModel):
    model_path:str; prompt:str; output_path:str
    width:int=1280; height:int=720; fps:int=24; num_frames:int=81; steps:int=30

class LongReq(BaseModel):
    model_path:str; prompt:str; duration_seconds:int
    segment_seconds:int=8; width:int=1280; height:int=720; fps:int=24
    project_id:str|None=None; metadata:dict=Field(default_factory=dict)

@router.post("/image")
def image(req:ImageReq):
    try:
        a=SDXLAdapter(req.model_path)
        return a.run(req.model_dump(exclude={"model_path"}))
    except Exception as e: raise HTTPException(500,str(e))

@router.post("/video")
def video(req:VideoReq):
    try:
        a=WanVideoAdapter(req.model_path)
        return a.run(req.model_dump(exclude={"model_path"}))
    except Exception as e: raise HTTPException(500,str(e))

@router.post("/long-video")
def long_video(req:LongReq):
    try:
        plan=LongFormPlanner(PROJECT_ROOT).plan(MediaProjectRequest(
            prompt=req.prompt,duration_seconds=req.duration_seconds,
            segment_seconds=req.segment_seconds,width=req.width,height=req.height,
            fps=req.fps,project_id=req.project_id,metadata=req.metadata
        ))
        return LongFormRunner(WanVideoAdapter(req.model_path),PROJECT_ROOT).render(plan)
    except Exception as e: raise HTTPException(500,str(e))
