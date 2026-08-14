import json
from powerx.runtime_mobile.device.capability import detect_device, recommended_mobile_tier

cap = detect_device()
print(json.dumps({
    "device": cap.__dict__,
    "recommended_mobile_tier": recommended_mobile_tier(cap),
}, indent=2))
