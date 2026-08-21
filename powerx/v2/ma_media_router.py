from __future__ import annotations

def choose_capability(text: str, attachments=None):
    t=(text or "").lower()
    if any(k in t for k in ("4 hour video","four hour video","course video","long video","masterclass")):
        return "long_video_generate"
    if any(k in t for k in ("video banao","generate video","create video")):
        return "video_generate"
    if any(k in t for k in ("image banao","generate image","create image")):
        return "image_generate"
    if any(k in t for k in ("forecast","price forecast","time series","timeseries")):
        return "forecasting"
    return None
