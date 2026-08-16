from dataclasses import dataclass
@dataclass(frozen=True)
class MobileProfile: id:str;model_id:str;min_ram_gb:float;min_free_storage_gb:float;threads:int;context:int
PROFILES=[MobileProfile("mobile-3b","qwen25-3b-general",6.0,3.0,4,4096),MobileProfile("mobile-4b","qwen3-4b-reasoning",8.0,4.5,6,4096),MobileProfile("mobile-6b","qwen-6b-mobile",12.0,7.0,8,4096)]
def choose_profile(ram_gb,free_storage_gb,thermal_ok=True):
 if not thermal_ok:return None
 e=[p for p in PROFILES if ram_gb>=p.min_ram_gb and free_storage_gb>=p.min_free_storage_gb]
 return e[-1] if e else None
