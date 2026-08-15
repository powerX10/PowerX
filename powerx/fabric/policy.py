from dataclasses import dataclass
@dataclass(frozen=True)
class TaskProfile:
    capability: str
    requested_tier: str="3b"
    heavy: bool=False
    device_local: bool=False
    continuous: bool=False

TIER_RANK={"3b":0,"4b":1,"6b":2,"gpu-heavy":3}

def node_order(task):
    if task.continuous and not task.heavy:
        return ("cpu","mobile","gpu16","cloud")
    if task.device_local and not task.heavy:
        return ("mobile","cpu","gpu16","cloud")
    if task.heavy or task.requested_tier=="gpu-heavy":
        return ("gpu16","cpu","mobile","cloud")
    return ("cpu","mobile","gpu16","cloud")
