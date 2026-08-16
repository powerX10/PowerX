import time,gc
class DynamicModelLifecycle:
    def __init__(self,limits=None):self.limits=limits or {"gpu16":1,"cpu":3,"mobile":1};self.loaded={}
    def touch(self,rt,mid,obj=None):self.loaded[(rt,mid)]={"obj":obj,"at":time.time()}
    def make_room(self,rt,keep=()):
        xs=[(k,v) for k,v in self.loaded.items() if k[0]==rt and k[1] not in keep]
        while len([k for k in self.loaded if k[0]==rt])>=self.limits.get(rt,1) and xs:
            k,_=sorted(xs,key=lambda z:z[1]["at"])[0];self.loaded.pop(k,None);gc.collect()
            try:
                import torch;torch.cuda.empty_cache()
            except Exception:pass
            xs=[(k,v) for k,v in self.loaded.items() if k[0]==rt and k[1] not in keep]
