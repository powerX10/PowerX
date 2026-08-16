from .schema import MARequest,PlannedStep
from .model_catalog import CAPABILITY_MODELS
class MAPlanner:
    def plan(self,r:MARequest):
        t=(r.text+" "+" ".join(str(x.get("content","")) for x in r.messages)).lower()
        caps=[]
        if any(a.mime_type.startswith("audio/") for a in r.attachments): caps.append("speech_to_text")
        if any(a.mime_type.startswith("image/") for a in r.attachments): caps.append("vision")
        checks=[
          (("generate image","create image","image banao"),"image_generate"),
          (("generate video","create video","video banao"),"video_generate"),
          (("code","python","typescript","javascript","github"),"coding"),
          (("chart","candlestick","price action","support resistance"),"chart_analysis"),
          (("forecast","time series","timeseries"),"forecasting"),
          (("sentiment","news tone"),"financial_sentiment"),
          (("voice reply","tts","read aloud"),"text_to_speech"),
          (("deep analysis","strategy","risk","portfolio","macro"),"deep_reasoning")]
        for keys,cap in checks:
            if any(k in t for k in keys): caps.append(cap)
        if not caps: caps=["chat"]
        out=[]
        for i,cap in enumerate(dict.fromkeys(caps)):
            out.append(PlannedStep(cap,CAPABILITY_MODELS[cap],{
                "text":r.text,"messages":r.messages,"attachments":[a.__dict__ for a in r.attachments],
                "metadata":r.metadata},0 if cap in {"financial_sentiment","forecasting"} else i+1))
        return out
