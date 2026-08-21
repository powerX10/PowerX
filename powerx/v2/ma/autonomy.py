from dataclasses import dataclass,field
import uuid,time
@dataclass
class TaskStep: kind:str; action:str; args:dict=field(default_factory=dict); approval_required:bool=False
@dataclass
class AutonomousTask: task_id:str; goal:str; steps:list[TaskStep]; created_at:float; status:str="planned"
class AutonomousPlanner:
    def plan(self,goal):
        t=goal.lower(); steps=[]
        if any(k in t for k in ("repo","github","code","fix","error","bug")):
            steps += [TaskStep("tool","repo_read"),TaskStep("model","coding"),TaskStep("tool","file_write"),TaskStep("tool","test_run"),TaskStep("model","verify")]
        if "deploy" in t: steps.append(TaskStep("tool","deploy_production",approval_required=True))
        return AutonomousTask(uuid.uuid4().hex,goal,steps,time.time())
