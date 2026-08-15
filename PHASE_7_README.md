# PowerX Phase 7 — Universal Agent + Local Runtime Fabric

PowerX remains the model/runtime/tool orchestration layer; trading logic stays in Zerion X1.

Adds:
- `/v1/agent` universal API
- capability routing
- 16 GB GPU and mobile runtime classes
- optional Modal/Beam fallbacks (disabled unless env URLs exist)
- GitHub read/write tools
- file tools
- provider-neutral web research adapter
- image/video routing

Reality:
A Vercel web page cannot directly commandeer Android GPU. The phone must run a local companion model server/Termux node and connect/expose that runtime to PowerX.
16 GB VRAM should not keep all models resident at once; load/schedule specialized runtimes.

Start:
`pip install -r requirements-phase7-agent.txt`
`uvicorn apps.agent_api.main:app --host 0.0.0.0 --port 8200`
