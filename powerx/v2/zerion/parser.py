import re
from .schema import TradingIntent
def parse_trading_request(text,defaults=None):
    defaults=defaults or {}; t=text.lower(); symbol="NIFTY50" if "nifty" in t else defaults.get("symbol","NIFTY50")
    nums=[float(x.replace(",","")) for x in re.findall(r'₹?\s*([\d,]+(?:\.\d+)?)',text)]
    return TradingIntent(symbol,defaults.get("capital",nums[0] if nums else 0),defaults.get("max_planned_loss",nums[1] if len(nums)>1 else 0),defaults.get("target_potential_reward",nums[2] if len(nums)>2 else 0),True)
