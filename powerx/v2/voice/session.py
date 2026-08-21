import time,uuid
class VoiceSession:
    def __init__(self,wake_words=None,idle_seconds=60):
        self.wake_words=[x.lower() for x in (wake_words or ["hey ma","ma"])]; self.id=uuid.uuid4().hex; self.active=False; self.last=time.time(); self.idle_seconds=idle_seconds
    def feed_text(self,text):
        now=time.time()
        if self.active and now-self.last>self.idle_seconds:self.active=False
        if any(w in text.lower() for w in self.wake_words):self.active=True
        self.last=now; return self.active
