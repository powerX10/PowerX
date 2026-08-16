from pathlib import Path
EXPECTED=["qwen25-3b-general","qwen3-4b-reasoning","qwen25-coder-3b","qwen25-vl-3b-chart","phi4-mini-deep",
"finbert-sentiment","finbert-tone","financial-news-distilroberta","financialbert-sentiment","chronos-small","timesfm-200m",
"moirai-small","granite-ttm","granite-tspulse","bge-reranker-base","minilm-embedding","whisper-small","kokoro-tts","sdxl-base","wan21-1.3b"]
class FinalAcceptance:
 def __init__(self,root="."):self.root=Path(root)
 def run(self):
  from powerx.ma.model_catalog import MODEL_IDS,MODEL_ADAPTERS
  from powerx.ma.adapter_contracts import SUPPORTED_ADAPTERS
  req=["apps/control_center/lib/powerx.ts","apps/control_center/app/api/powerx/chat/route.ts","apps/powerx_production_api/main.py",
  "powerx/ma/orchestrator.py","powerx/ma/planner.py","deploy_phase12/mobile_edge/local_inference.py","deploy_phase13/gpu16_worker/worker.py"]
  miss=[x for x in req if not(self.root/x).exists()];mm=[x for x in EXPECTED if x not in MODEL_IDS]
  bad=[m for m,a in MODEL_ADAPTERS.items() if a not in SUPPORTED_ADAPTERS]
  ok=not miss and not mm and not bad and len(MODEL_IDS)==20
  return {"phase":14,"coding_complete":ok,"models":len(MODEL_IDS),"missing_models":mm,"unsupported_adapters":bad,"missing_files":miss,"beam_optional":True}
