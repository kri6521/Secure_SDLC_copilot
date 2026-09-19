import json
from datetime import datetime, timezone
from pathlib import Path

AUDIT_FILE = Path("audit_logs/audit.jsonl")

def audit(stage, actor, action, result, evidence=None):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "actor": actor,
        "action": action,
        "result": result,
        "evidence": evidence or {},
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    return event
