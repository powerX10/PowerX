import json
from powerx.ma.model_catalog import MODEL_IDS,MODEL_ADAPTERS
from powerx.ma.adapter_contracts import SUPPORTED_ADAPTERS
bad=[m for m in MODEL_IDS if MODEL_ADAPTERS[m] not in SUPPORTED_ADAPTERS]
r={"phase":13,"models":len(MODEL_IDS),"adapter_mappings":len(MODEL_ADAPTERS),"unsupported":bad,"code_ready":len(MODEL_IDS)==20 and not bad}
print(json.dumps(r,indent=2));raise SystemExit(0 if r["code_ready"] else 1)
