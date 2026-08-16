import modal

app = modal.App("powerx-production-gateway")
runtime_secret = modal.Secret.from_name("powerx-runtime")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("fastapi", "uvicorn", "httpx")
    .add_local_python_source("powerx")
    .add_local_dir("apps/powerx_production_api", remote_path="/root/apps/powerx_production_api")
)

@app.function(
    image=image,
    cpu=1.0,
    memory=1024,
    timeout=3600,
    secrets=[runtime_secret],
    min_containers=1,
    max_containers=4,
)
@modal.asgi_app()
def api():
    from apps.powerx_production_api.main import app as web
    return web
