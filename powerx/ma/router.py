from dataclasses import dataclass
import os
@dataclass(frozen=True)
class Target: runtime_class:str; endpoint:str|None; token:str|None
def targets(cap,preferred=None):
    if cap in {"image_generate","image_edit","video_generate","vision","chart_analysis"}: order=["gpu16","cpu"]
    elif cap in {"chat","embedding","financial_sentiment"}: order=["mobile","cpu","gpu16"]
    else: order=["cpu","gpu16","mobile"]
    if preferred in order: order.remove(preferred);order.insert(0,preferred)
    env={"cpu":("POWERX_MODAL_CPU_URL","POWERX_MODAL_CPU_TOKEN"),
         "gpu16":("POWERX_BROKER_URL","POWERX_WORKER_TOKEN"),
         "mobile":("POWERX_BROKER_URL","POWERX_WORKER_TOKEN")}
    return [Target(rt,os.getenv(env[rt][0]),os.getenv(env[rt][1])) for rt in order]
