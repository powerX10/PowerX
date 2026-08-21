from dataclasses import dataclass,field
from .errors import PowerXPermissionError
READ_ONLY={"repo_read","file_read","search","status","market_read"}
LOW_RISK={"file_write","test_run","branch_create","draft_pr","notify","tts","stt"}
HIGH_RISK={"deploy_production","broker_order","delete_data","rotate_secret","force_push","db_write"}
@dataclass
class PermissionPolicy:
    founder_mode:bool=False
    allowed:set[str]=field(default_factory=lambda:set(READ_ONLY|LOW_RISK))
    denied:set[str]=field(default_factory=set)
    def check(self,action,explicit_approval=False):
        if action in self.denied: raise PowerXPermissionError(f"Action denied: {action}")
        if action in READ_ONLY:return True
        if action in LOW_RISK and (action in self.allowed or self.founder_mode):return True
        if action in HIGH_RISK:
            if self.founder_mode and explicit_approval:return True
            raise PowerXPermissionError(f"Explicit approval required: {action}")
        if action in self.allowed:return True
        raise PowerXPermissionError(f"Action not allowed: {action}")
