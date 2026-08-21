#!/usr/bin/env python3
from powerx.v2.registry import ModelRegistry
from powerx.v2.runtime import infer_capability

r = ModelRegistry()
models = r.all()
assert len(models) >= 20, f"Expected at least 20 models, got {len(models)}"
assert infer_capability("make a video course") == "video_generate"
assert infer_capability("Nifty breakout support resistance") == "trading_analysis"
assert r.best_for("chat"), "No chat model"
assert r.best_for("video_generate"), "No video model"
assert r.best_for("trading_analysis"), "No trading model"
print("PowerX V2 Zip1 smoke test passed")
print("models:", len(models))
print("chat:", r.best_for("chat")[0].id)
print("video:", r.best_for("video_generate")[0].id)
print("trading:", r.best_for("trading_analysis")[0].id)
