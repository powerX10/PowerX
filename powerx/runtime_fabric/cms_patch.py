from __future__ import annotations
from powerx.controlplane.store import ControlPlaneStore

CPU_FIRST_CAPS = {
    "financial_sentiment", "news_sentiment", "forecasting", "timeseries_forecast",
    "rerank", "research", "retrieval", "embedding", "semantic_search",
    "speech_to_text", "text_to_speech", "technical_indicators", "support_resistance",
    "price_action", "risk_management", "research_backtest", "chat", "general_reasoning"
}
GPU_PREFERRED_CAPS = {"vision", "chart_analysis", "image_generate", "video_generate"}
MOBILE_ALLOWED_CAPS = {"chat", "embedding", "financial_sentiment", "semantic_search", "beginner_explain"}


def apply_cpu_first_policy(store: ControlPlaneStore | None = None) -> dict:
    store = store or ControlPlaneStore()
    changed = 0
    for model in store.list():
        caps = set(model.capabilities)
        order = list(model.routing.runtime_order)
        if caps & GPU_PREFERRED_CAPS:
            desired = ["gpu16", "cpu", "mobile", "cloud"]
        elif caps & CPU_FIRST_CAPS:
            desired = ["cpu", "mobile", "gpu16", "cloud"] if caps & MOBILE_ALLOWED_CAPS else ["cpu", "gpu16", "cloud", "mobile"]
        else:
            desired = ["cpu", "gpu16", "mobile", "cloud"]
        available = {b.runtime_class for b in model.bindings if b.enabled}
        desired = [x for x in desired if x in available]
        desired += [x for x in order if x not in desired and x in available]
        if desired and desired != model.routing.runtime_order:
            patch = model.model_dump()
            patch["routing"]["mode"] = "auto"
            patch["routing"]["runtime_order"] = desired
            store.upsert(type(model).model_validate(patch))
            changed += 1
    return {"ok": True, "changed": changed, "models": len(store.list())}
