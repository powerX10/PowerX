from .policy import TIER_RANK, node_order
class RuntimeFabricRouter:
    def __init__(self, registry):
        self.registry=registry
    def resolve(self, task):
        rank=TIER_RANK.get(task.requested_tier,0)
        for cls in node_order(task):
            eligible=[]
            for n in self.registry.nodes():
                if n.runtime_class != cls: continue
                if task.capability not in n.capabilities: continue
                if not any(TIER_RANK.get(t,-1)>=rank for t in n.model_tiers): continue
                eligible.append(n)
            if eligible:
                return sorted(eligible,key=lambda x:x.load)[0]
        raise RuntimeError("No live compatible PowerX runtime")
