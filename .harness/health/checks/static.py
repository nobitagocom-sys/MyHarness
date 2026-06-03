from pathlib import Path

def run():
    warnings, errors = 0, 0
    wf_count = len(list(Path(".harness/workflows").glob("*.yaml")))
    if wf_count == 0:
        errors += 1
    return {"warnings": warnings, "errors": errors, "workflows_found": wf_count}
