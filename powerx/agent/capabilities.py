KEYWORDS = {
    "image_generate": ("generate image","create image","image bana"),
    "video_generate": ("generate video","create video","video bana"),
    "code": ("code","github","repo","bug","fix","implement"),
    "research": ("research","search web","find latest","investigate"),
    "vision": ("analyze image","screenshot","chart image"),
    "speech_to_text": ("transcribe","voice message"),
    "text_to_speech": ("speak","voice output"),
    "file_analyze": ("pdf","document","file analyze","attachment"),
}
def infer_capability(messages, attachments):
    if attachments:
        if any(getattr(a,"mime_type","").startswith("image/") for a in attachments):
            return "vision"
        return "file_analyze"
    text=" ".join(str(m.get("content","")) for m in messages[-4:]).lower()
    for cap, words in KEYWORDS.items():
        if any(w in text for w in words):
            return cap
    return "chat"
