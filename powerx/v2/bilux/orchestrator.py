class BiluxTeacherOrchestrator:
    def __init__(self,retriever,llm,tts):self.retriever=retriever;self.llm=llm;self.tts=tts
    def answer(self,course_id,question,student_id=None):
        context=self.retriever(course_id,question);answer=self.llm({"question":question,"context":context,"role":"teacher"});text=answer["text"] if isinstance(answer,dict) else str(answer);audio=self.tts.run({"text":text})
        return {"text":text,"audio":audio,"student_id":student_id}
