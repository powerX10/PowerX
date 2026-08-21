from dataclasses import dataclass
@dataclass
class TradingIntent:
 symbol:str
 capital:float
 max_planned_loss:float
 target_potential_reward:float
 approval_required:bool=True
