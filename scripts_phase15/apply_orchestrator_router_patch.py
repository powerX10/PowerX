from pathlib import Path
p=Path("powerx/ma/orchestrator.py");s=p.read_text();s=s.replace("for t in targets(step.capability,pref):","for t in targets(step.capability,pref,step.payload.get('metadata') or {}):");p.write_text(s);print("router metadata patch applied")
