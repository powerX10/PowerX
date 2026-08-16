from dataclasses import dataclass
import os
@dataclass(frozen=True)
class AssistantIdentity:
    name:str; expose_model_details:bool=False
class IdentityResolver:
    def resolve(self,product_id:str,founder_mode:bool=False):
        p=(product_id or "powerx").lower()
        if p=="powerx" and founder_mode:
            return AssistantIdentity("MA",True)
        env="POWERX_ASSISTANT_NAME_"+p.upper().replace("-","_")
        defaults={"zerion-x1":"Zerion AI","zerionx1":"Zerion AI","biluxe10":"Biluxe AI","sidra":"Sidra AI","powerx":"PowerX AI"}
        return AssistantIdentity(os.getenv(env,defaults.get(p,"AI Assistant")),False)
