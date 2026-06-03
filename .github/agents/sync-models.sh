#!/usr/bin/env bash
# sync-models.sh — Apply model values from .harness/models/catalog.yaml to all agent .md files.
# Run this whenever you update catalog.yaml.
# Usage: bash .github/agents/sync-models.sh

set -euo pipefail

AGENTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$AGENTS_DIR/../.." && pwd)"
CONFIG="$REPO_ROOT/.harness/models/catalog.yaml"

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: catalog.yaml not found at $CONFIG" >&2; exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 required" >&2; exit 1
fi

python3 - "$AGENTS_DIR" "$CONFIG" <<'PYEOF'
import sys, re, pathlib

agents_dir = pathlib.Path(sys.argv[1])
config_path = pathlib.Path(sys.argv[2])
text = config_path.read_text()

# Parse models: aliases → actual model strings
model_aliases = {}
in_models = False
for line in text.splitlines():
    if re.match(r'^models:', line):
        in_models = True; continue
    if in_models:
        if re.match(r'^\S', line):
            in_models = False; continue
        m = re.match(r'^\s{2}(\w+):\s+"([^"]+)"', line)
        if m:
            model_aliases[m.group(1)] = m.group(2)

# Parse agents: name → alias
agent_models = {}
in_agents = False
for line in text.splitlines():
    if re.match(r'^agents:', line):
        in_agents = True; continue
    if in_agents:
        if re.match(r'^\S', line):
            in_agents = False; continue
        m = re.match(r'^\s{2}([\w.]+):\s+\{[^}]*model:\s+(\w+)', line)
        if m:
            alias = m.group(2)
            agent_models[m.group(1)] = model_aliases.get(alias, alias)

# Patch each agent .md file
updated = []
for md_file in sorted(agents_dir.glob("*.md")):
    agent_key = md_file.stem.replace(".agent", "")
    if agent_key not in agent_models:
        continue
    target_model = agent_models[agent_key]
    content = md_file.read_text()
    new_content, count = re.subn(
        r'^(model:\s*)(.+)$',
        lambda m, t=target_model: f"{m.group(1)}{t}",
        content, flags=re.MULTILINE
    )
    if count and content != new_content:
        md_file.write_text(new_content)
        updated.append(f"  {md_file.name}: → {target_model}")
    elif count:
        updated.append(f"  {md_file.name}: already {target_model} (no change)")

if updated:
    print("Synced from .harness/models/catalog.yaml:")
    print("\n".join(updated))
else:
    print("No changes needed.")
PYEOF
