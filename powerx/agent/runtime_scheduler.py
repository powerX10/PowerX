from dataclasses import dataclass, field

@dataclass
class RuntimeSpec:
    id: str
    runtime_class: str
    capabilities: set[str]
    base_url: str
    model_id: str
    priority: int = 100
    api_key: str | None = None
    enabled: bool = True
    max_concurrent: int = 1
    busy: int = 0

@dataclass
class RuntimeScheduler:
    runtimes: list[RuntimeSpec] = field(default_factory=list)
    def register(self, spec):
        self.runtimes=[x for x in self.runtimes if x.id != spec.id]+[spec]
    def candidates(self, capability):
        rank={"gpu16":0,"mobile":1,"cpu":2,"cloud":3}
        out=[r for r in self.runtimes if r.enabled and capability in r.capabilities and r.busy < r.max_concurrent]
        return sorted(out,key=lambda r:(rank.get(r.runtime_class,99),r.priority,r.busy))
