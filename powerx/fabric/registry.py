import time
class RuntimeFabricRegistry:
    def __init__(self, ttl_seconds=90):
        self.ttl_seconds=ttl_seconds
        self._nodes={}
    def heartbeat(self,node):
        self._nodes[node.id]=(node,time.time())
    def nodes(self):
        now=time.time()
        return [n for n,t in self._nodes.values() if n.available and now-t<=self.ttl_seconds]
    def snapshot(self):
        now=time.time()
        out=[]
        for n,t in self._nodes.values():
            out.append({**n.__dict__,
                        "capabilities":sorted(n.capabilities),
                        "model_tiers":sorted(n.model_tiers),
                        "age_seconds":round(now-t,2),
                        "healthy":n.available and now-t<=self.ttl_seconds})
        return out
