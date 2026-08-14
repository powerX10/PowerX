import json
from powerx.runtime_cpu.llamacpp.process import LlamaCppServerManager

manager = LlamaCppServerManager(state_dir=".powerx-mobile-runtime")
print(json.dumps(manager.stop("mobile-local"), indent=2))
