from .tools.base import ToolRegistry
from .tools.github_http import TOOLS as G
from .tools.files import TOOLS as F
from .tools.web_research import TOOLS as W
def default_tools():
    r=ToolRegistry()
    for t in [*G,*F,*W]: r.register(t)
    return r
