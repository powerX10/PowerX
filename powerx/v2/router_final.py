def route_request(product_id,text):
    t=(text or "").lower()
    if product_id=="zerion-x1":return "zerion"
    if product_id=="bilux10":return "bilux_teacher"
    if any(k in t for k in ("repo","github","fix code","bug")):return "ma_autonomous_coding"
    if "video" in t:return "media"
    if any(k in t for k in ("voice","speak","read aloud")):return "voice"
    return "chat"
