import secrets,time
class TeacherRoom:
    def __init__(self,course_id,teacher_agent):
        self.course_id=course_id;self.teacher_agent=teacher_agent;self.code=f"{secrets.randbelow(1000000):06d}";self.created_at=time.time();self.students=set()
    def join(self,student_id,code):
        if code!=self.code:raise ValueError("invalid room code")
        self.students.add(student_id);return True
