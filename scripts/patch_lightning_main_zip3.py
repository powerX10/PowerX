from pathlib import Path
p=Path("apps/lightning_worker/main.py")
s=p.read_text()
if "media_routes" not in s:
    s += "\n\n# PowerX V2 ZIP3 routes\nfrom apps.lightning_worker.media_routes import router as media_router\nfrom apps.lightning_worker.forecast_routes import router as forecast_router\napp.include_router(media_router)\napp.include_router(forecast_router)\n"
    p.write_text(s)
print("ZIP3 routes patched into apps/lightning_worker/main.py")
