import json
from pathlib import Path

def run():
    log = Path(".harness/logs/agent.jsonl")
    if not log.exists():
        return {"context_coverage": "N/A", "context_waste_pct": 0, "status": "no_logs"}
    
    total, covered, wasted = 0, 0, 0
    for line in log.read_text().splitlines():
        try:
            e = json.loads(line)
            if e.get("type") == "agent_call":
                total += 1
                injected = len(e.get("context_files", []))
                accessed = len(set(e.get("accessed_files", [])) & set(e.get("context_files", [])))
                covered += accessed
                wasted += (injected - accessed)
        except: pass
    
    cov = (covered / total) if total else 1.0
    waste = (wasted / (total * 5)) if total else 0  # avg 5 files/call
    return {
        "context_coverage": round(cov, 2),
        "context_waste_pct": round(min(waste * 100, 100), 1),
        "total_calls": total
    }
