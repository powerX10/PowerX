from __future__ import annotations
import asyncio
from powerx.controlplane.store import ControlPlaneStore
from .warehouse import RcloneWarehouse
from .gateway import DynamicInferenceGateway

REQUIRED_CAPABILITIES = {
    "chat","deep_reasoning","coding","chart_analysis","financial_sentiment","forecasting",
    "risk_management","strategy_selection","research","speech_to_text","text_to_speech",
    "image_generate","video_generate"
}

class FinalReadinessAudit:
    def __init__(self, store: ControlPlaneStore | None = None, warehouse: RcloneWarehouse | None = None):
        self.store = store or ControlPlaneStore()
        self.warehouse = warehouse or RcloneWarehouse()

    async def run(self, check_endpoints: bool = False) -> dict:
        models = self.store.list()
        warehouse = []
        capabilities = set()
        endpoint_checks = []
        gateway = DynamicInferenceGateway(self.store)
        for model in models:
            if model.enabled: capabilities.update(model.capabilities)
            if model.warehouse_path:
                warehouse.append({"model_id":model.id,"path":model.warehouse_path,"exists":self.warehouse.exists(model.warehouse_path)})
            if check_endpoints:
                for binding in model.bindings:
                    if binding.enabled and binding.endpoint:
                        endpoint_checks.append({"model_id":model.id,"runtime":binding.runtime_class,"endpoint":binding.endpoint,"healthy":await gateway._healthy(binding.endpoint)})
        numbered = [m for m in models if m.id in {
            "qwen25-3b-general","qwen3-4b-reasoning","qwen25-coder-3b","qwen25-vl-3b-chart","phi4-mini-deep",
            "finbert-sentiment","finbert-tone","financial-news-distilroberta","financialbert-sentiment","chronos-small",
            "timesfm-200m","moirai-small","granite-ttm","granite-tspulse","bge-reranker-base","minilm-embedding",
            "whisper-small","kokoro-82m","sdxl-base","wan21-t2v-1.3b"}]
        missing_caps = sorted(REQUIRED_CAPABILITIES - capabilities)
        missing_files = [x for x in warehouse if not x["exists"]]
        unhealthy = [x for x in endpoint_checks if not x["healthy"]]
        code_ready = len(numbered) == 20 and not missing_caps and not missing_files
        operational_ready = code_ready and (not check_endpoints or not unhealthy)
        return {
            "code_ready": code_ready,
            "operational_ready": operational_ready,
            "registered_models": len(models),
            "final_roster_models": len(numbered),
            "missing_capabilities": missing_caps,
            "missing_warehouse_objects": missing_files,
            "endpoint_checks": endpoint_checks,
            "unhealthy_or_unset_checked_endpoints": unhealthy
        }
