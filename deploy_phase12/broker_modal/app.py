"""PowerX Phase 12 broker API on Modal.

Hosts the Runtime Fabric control API plus durable pull-worker queue for Colab
GPU16 and mobile workers. SQLite broker data lives on a persistent Modal Volume.
"""
import os
import modal

app = modal.App("powerx-runtime-broker")
volume = modal.Volume.from_name("powerx-runtime-broker-data", create_if_missing=True)
secret = modal.Secret.from_name("powerx-drive")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("fastapi", "uvicorn", "httpx")
    .add_local_python_source("powerx")
    .add_local_dir("apps/runtime_fabric_api", remote_path="/root/apps/runtime_fabric_api")
    .add_local_dir("config_phase12", remote_path="/root/config_phase12")
    .add_local_file("data/model_cms.json", remote_path="/root/data/model_cms.json")
)

@app.function(
    image=image,
    cpu=1.0,
    memory=2048,
    timeout=3600,
    volumes={"/broker": volume},
    secrets=[secret],
    min_containers=1,
    max_containers=2,
)
@modal.asgi_app()
def api():
    os.environ["POWERX_BROKER_DB"] = "/broker/runtime_broker.sqlite3"
    os.environ.setdefault("POWERX_MODEL_CMS_DB", "/root/data/model_cms.json")
    from apps.runtime_fabric_api.main import app as web
    return web
