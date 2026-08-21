class VoiceOrchestrator:
    def __init__(self,stt,ma,tts): self.stt=stt; self.ma=ma; self.tts=tts
    def handle_audio(self,audio_payload,context=None):
        stt=self.stt.run(audio_payload); text=stt.get("text",""); response=self.ma(text,context or {}); spoken=self.tts.run({"text":response.get("text","")})
        return {"transcript":text,"response":response,"audio":spoken}
