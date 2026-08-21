from dataclasses import dataclass,field,asdict
import uuid,time
@dataclass
class PowerXRequest:
    product_id:str; user_id:str|None; text:str; metadata:dict=field(default_factory=dict); request_id:str=field(default_factory=lambda:uuid.uuid4().hex); created_at:float=field(default_factory=time.time)
    def to_dict(self):return asdict(self)
