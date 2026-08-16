"""Beam CPU fallback endpoint. Deploy: beam deploy deploy_phase12/beam_cpu/app.py:handler"""
import os
from beam import endpoint, Image, QueueDepthAutoscaler

image = Image(python_version="python3.11", python_packages=["fastapi", "httpx"])

@endpoint(
    name="powerx-beam-cpu",
    cpu=4.0,
    memory="16Gi",
    gpu="",
    image=image,
    timeout=3600,
    workers=1,
    autoscaler=QueueDepthAutoscaler(min_containers=0, max_containers=4, tasks_per_container=1),
)
def handler(**inputs):
    return {
        "ok": True,
        "provider": "beam",
        "runtime_class": "cpu",
        "model_id": inputs.get("model_id"),
        "capability": inputs.get("capability"),
        "payload": inputs.get("payload", {}),
    }
