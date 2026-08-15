from dataclasses import dataclass
@dataclass
class Tool:
    name: str
    description: str
    fn: object
    write: bool=False
class ToolRegistry:
    def __init__(self): self._tools={}
    def register(self,t): self._tools[t.name]=t
    def get(self,n): return self._tools[n]
    def specs(self): return [{"name":t.name,"description":t.description,"write":t.write} for t in self._tools.values()]
