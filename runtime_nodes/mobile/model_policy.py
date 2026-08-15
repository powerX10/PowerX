from dataclasses import dataclass
@dataclass(frozen=True)
class MobileChoice:
    tier:str; reason:str

def choose_mobile_tier(total_ram_gb,free_storage_gb,battery_percent=100,charging=True):
    if total_ram_gb>=16 and free_storage_gb>=8 and (charging or battery_percent>=50):
        return MobileChoice("6b","high-RAM mobile")
    if total_ram_gb>=10 and free_storage_gb>=6:
        return MobileChoice("4b","mid/high mobile")
    if total_ram_gb>=6 and free_storage_gb>=4:
        return MobileChoice("3b","minimum PowerX mobile tier")
    return MobileChoice("remote","route to CPU/GPU; device cannot safely run minimum 3B")
