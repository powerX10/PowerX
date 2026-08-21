import os,requests
from ..errors import PowerXExternalError
class GitHubTool:
    def __init__(self,policy,token=None): self.policy=policy; self.token=token or os.getenv("GITHUB_TOKEN")
    def _h(self):
        if not self.token: raise PowerXExternalError("GITHUB_TOKEN missing")
        return {"Authorization":f"Bearer {self.token}","Accept":"application/vnd.github+json"}
    def get_repo(self,full_name):
        self.policy.check("repo_read"); r=requests.get(f"https://api.github.com/repos/{full_name}",headers=self._h(),timeout=30)
        if r.status_code>=400: raise PowerXExternalError(f"github {r.status_code}: {r.text[:500]}")
        return r.json()
