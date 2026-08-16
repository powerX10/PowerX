from dataclasses import dataclass
import os
@dataclass(frozen=True)
class ProductBranding:
    product_id:str;assistant_name:str;founder_mode:bool=False
    @classmethod
    def resolve(cls,product_id:str,founder_mode:bool=False):
        p=(product_id or "powerx").lower()
        if p=="powerx" and founder_mode:return cls(p,"MA",True)
        e="POWERX_ASSISTANT_NAME_"+p.upper().replace("-","_")
        d={"powerx":"PowerX AI","zerion-x1":"Zerion AI","zerionx1":"Zerion AI","biluxe10":"Biluxe AI","sidra":"Sidra AI"}
        return cls(p,os.getenv(e,d.get(p,"AI Assistant")),False)
