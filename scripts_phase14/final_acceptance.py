import json
from powerx.final_product.acceptance import FinalAcceptance
r=FinalAcceptance(".").run();print(json.dumps(r,indent=2));raise SystemExit(0 if r["coding_complete"] else 1)
