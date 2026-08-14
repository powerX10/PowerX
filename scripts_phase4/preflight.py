import json
from powerx.production.readiness import run_preflight

result = run_preflight()
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["ready"] else 1)
