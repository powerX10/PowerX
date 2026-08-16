from dataclasses import dataclass, field
from typing import Any
@dataclass
class Attachment:
    name:str; mime_type:str; data_b64:str|None=None; url:str|None=None
@dataclass
class MARequest:
    text:str=""; messages:list[dict[str,Any]]=field(default_factory=list)
    attachments:list[Attachment]=field(default_factory=list)
    product_id:str="powerx"; user_id:str|None=None; founder_mode:bool=False
    preferred_runtime:str|None=None; metadata:dict[str,Any]=field(default_factory=dict)
@dataclass
class PlannedStep:
    capability:str; model_ids:list[str]; payload:dict[str,Any]; parallel_group:int=0
@dataclass
class MAResponse:
    ok:bool; assistant_name:str; text:str|None=None
    artifacts:list[dict[str,Any]]=field(default_factory=list)
    internal:dict[str,Any]=field(default_factory=dict)
