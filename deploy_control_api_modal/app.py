import modal

app = modal.App("powerx-control-api")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "fastapi",
        "uvicorn",
        "httpx",
    )
    .add_local_python_source("powerx")
    .add_local_dir(
        "apps/control_api",
        remote_path="/root/apps/control_api",
    )
)

@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("powerx-runtime"),
        modal.Secret.from_name("powerx-control"),
    ],
    timeout=900,
)
@modal.asgi_app()
def api():
    import sys
    sys.path.insert(0, "/root")
    from apps.control_api.main import app as web
    return web
