import json
from powerx.runtime_cpu.llamacpp.controller import CPURuntimeController
from powerx.runtime_cpu.llamacpp.profiles import CPU_PROFILES

ctl = CPURuntimeController()
print(json.dumps(
    {model_id: ctl.status(model_id) for model_id in CPU_PROFILES},
    indent=2,
))
