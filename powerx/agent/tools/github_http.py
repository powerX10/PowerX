import os, httpx, base64
from .base import Tool
API="https://api.github.com"
def _headers():
    token=os.getenv("POWERX_GITHUB_TOKEN")
    if not token: raise RuntimeError("POWERX_GITHUB_TOKEN is not configured")
    return {"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
async def github_read(args):
    async with httpx.AsyncClient(timeout=60) as c:
        r=await c.get(f"{API}/repos/{args['repo']}/contents/{args.get('path','')}",headers=_headers(),params={"ref":args.get("ref","main")})
        r.raise_for_status(); return r.json()
async def github_commit_file(args):
    repo,path=args["repo"],args["path"]; branch=args.get("branch","main")
    payload={"message":args.get("message","PowerX agent update"),"content":base64.b64encode(args["content"].encode()).decode(),"branch":branch}
    async with httpx.AsyncClient(timeout=60) as c:
        cur=await c.get(f"{API}/repos/{repo}/contents/{path}",headers=_headers(),params={"ref":branch})
        if cur.status_code==200: payload["sha"]=cur.json()["sha"]
        r=await c.put(f"{API}/repos/{repo}/contents/{path}",headers=_headers(),json=payload)
        r.raise_for_status(); return r.json()
TOOLS=[Tool("github_read","Read GitHub repository content.",github_read),Tool("github_commit_file","Create/update one file and commit it.",github_commit_file,True)]
