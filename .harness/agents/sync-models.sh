#!/usr/bin/env bash
# sync-models.sh — Apply model values from .harness/models/catalog.yaml to agent .md files.
# Run this whenever you update catalog.yaml.
#
# Usage:
#   bash .harness/agents/sync-models.sh                   # sync Copilot agents (.github/agents/)
#   bash .harness/agents/sync-models.sh --provider claude # sync Claude Code agents (.claude/agents/)
#   bash .harness/agents/sync-models.sh --provider all    # sync both

set -euo pipefail

HARNESS_AGENTS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HARNESS_AGENTS_DIR/../.." && pwd)"
COPILOT_AGENTS_DIR="$REPO_ROOT/.github/agents"
PROMPTS_DIR="$REPO_ROOT/.github/prompts"
CONFIG="$REPO_ROOT/.harness/models/catalog.yaml"
PROVIDER="copilot"

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --provider) PROVIDER="$2"; shift 2 ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: catalog.yaml not found at $CONFIG" >&2; exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 required" >&2; exit 1
fi

# ---------------------------------------------------------------------------
# Copilot sync: patch model: field in .github/agents/*.agent.md
# ---------------------------------------------------------------------------
sync_copilot() {
python3 - "$COPILOT_AGENTS_DIR" "$CONFIG" <<'PYEOF'
import sys, re, pathlib

agents_dir = pathlib.Path(sys.argv[1])
config_path = pathlib.Path(sys.argv[2])
text = config_path.read_text()

# Parse models: section (copilot)
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
        m = re.match(r'^\s{2}([\w.\-]+):\s+\{[^}]*model:\s+(\w+)', line)
        if m:
            alias = m.group(2)
            agent_models[m.group(1)] = model_aliases.get(alias, alias)

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
    print("Synced Copilot agents from .harness/models/catalog.yaml:")
    print("\n".join(updated))
else:
    print("Copilot agents: no changes needed.")
PYEOF
}

# ---------------------------------------------------------------------------
# Claude Code sync: generate/update .claude/agents/*.md
# Tools mapping: Copilot → Claude Code
#   read, search  → Read, Bash
#   edit          → Edit, Write
#   execute, run  → Bash
#   todo          → TodoWrite
#   agent         → Task
#   web           → WebSearch, WebFetch
# ---------------------------------------------------------------------------
sync_claude_code() {
python3 - "$COPILOT_AGENTS_DIR" "$CONFIG" "$REPO_ROOT" <<'PYEOF'
import sys, re, pathlib

agents_dir   = pathlib.Path(sys.argv[1])
config_path  = pathlib.Path(sys.argv[2])
repo_root    = pathlib.Path(sys.argv[3])
claude_agents_dir = repo_root / ".claude" / "agents"
claude_agents_dir.mkdir(parents=True, exist_ok=True)

text = config_path.read_text()

# Parse claude_code_models: section
cc_models = {}
in_cc = False
for line in text.splitlines():
    if re.match(r'^claude_code_models:', line):
        in_cc = True; continue
    if in_cc:
        if re.match(r'^\S', line):
            in_cc = False; continue
        m = re.match(r'^\s{2}(\w+):\s+"([^"]+)"', line)
        if m:
            cc_models[m.group(1)] = m.group(2)

# Parse agents: name → alias
agent_aliases = {}
in_agents = False
for line in text.splitlines():
    if re.match(r'^agents:', line):
        in_agents = True; continue
    if in_agents:
        if re.match(r'^\S', line):
            in_agents = False; continue
        m = re.match(r'^\s{2}([\w.\-]+):\s+\{[^}]*model:\s+(\w+)', line)
        if m:
            agent_aliases[m.group(1)] = m.group(2)

def resolve_model(alias):
    return cc_models.get(alias, alias)

TOOLS_MAP = {
    "read":    ["Read"],
    "search":  ["Bash"],
    "edit":    ["Edit", "Write"],
    "execute": ["Bash"],
    "run":     ["Bash"],
    "todo":    ["TodoWrite"],
    "agent":   ["Task"],
    "web":     ["WebSearch", "WebFetch"],
    # MCP tools: pass through as-is (Claude Code supports MCP)
    "github/github-mcp-server/issue_write": ["github/github-mcp-server/issue_write"],
}

# Agents with no model: in source → assign a default tier
DEFAULT_MODEL_BY_KEY = {
    "myharness.analyze":      "claude_sonnet",
    "myharness.checklist":    "claude_sonnet",
    "myharness.constitution": "gpt_frontier",
}

def convert_tools(copilot_tools_str):
    # e.g. "[read, search, edit, todo]"
    inner = re.sub(r"[\[\]'\"]", "", copilot_tools_str).strip()
    names = [t.strip() for t in inner.split(",") if t.strip()]
    result = []
    for n in names:
        for cc in TOOLS_MAP.get(n, [n]):
            if cc not in result:
                result.append(cc)
    return result

updated, created = [], []
for src_file in sorted(agents_dir.glob("*.agent.md")):
    agent_key = src_file.stem.replace(".agent", "")  # e.g. myharness.srs
    if agent_key not in agent_aliases:
        continue

    alias = agent_aliases[agent_key]
    target_model = resolve_model(alias)
    if not target_model or target_model == alias:
        # fallback for agents with no model: in source
        fallback_alias = DEFAULT_MODEL_BY_KEY.get(agent_key, "claude_sonnet")
        target_model = resolve_model(fallback_alias)

    content = src_file.read_text(encoding="utf-8-sig")

    # Parse existing frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        continue
    fm_body = fm_match.group(1)
    body_after_fm = content[fm_match.end():]

    # Extract fields
    desc_m   = re.search(r'^description:\s*"?(.*?)"?\s*$', fm_body, re.MULTILINE)
    tools_m  = re.search(r'^tools:\s*(\[.*?\])', fm_body, re.MULTILINE)

    description = desc_m.group(1).replace('\n', ' ').strip() if desc_m else ""
    cc_tools = convert_tools(tools_m.group(1)) if tools_m else ["Read", "Edit", "Bash", "TodoWrite"]

    # Build Claude Code frontmatter
    tools_str = ", ".join(cc_tools)
    new_fm = f"""---
description: "{description}"
model: {target_model}
tools: [{tools_str}]
---
"""

    new_content = new_fm + body_after_fm

    dest_file = claude_agents_dir / f"{agent_key}.md"
    if dest_file.exists():
        if dest_file.read_text() != new_content:
            dest_file.write_text(new_content)
            updated.append(f"  {dest_file.name}: model={target_model}, tools=[{tools_str}]")
        # else no change — skip
    else:
        dest_file.write_text(new_content)
        created.append(f"  {dest_file.name}: model={target_model}, tools=[{tools_str}]")

if created:
    print("Created Claude Code agents in .claude/agents/:")
    print("\n".join(created))
if updated:
    print("Updated Claude Code agents in .claude/agents/:")
    print("\n".join(updated))
if not created and not updated:
    print("Claude Code agents: no changes needed.")
PYEOF

# Sync .claude/commands/ from .github/prompts/
python3 - "$PROMPTS_DIR" "$COPILOT_AGENTS_DIR" "$REPO_ROOT" <<'PYEOF'
import sys, re, pathlib

prompts_dir  = pathlib.Path(sys.argv[1])
agents_dir   = pathlib.Path(sys.argv[2])
repo_root    = pathlib.Path(sys.argv[3])
commands_dir = repo_root / ".claude" / "commands"
commands_dir.mkdir(parents=True, exist_ok=True)

# Load agent descriptions from agent .md files
agent_descs = {}
agent_hints = {}
for f in sorted(agents_dir.glob("*.agent.md")):
    key = f.stem.replace(".agent", "")
    text = f.read_text(encoding="utf-8-sig")
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    h = re.search(r'^argument-hint:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    if m:
        agent_descs[key] = m.group(1).strip().strip('"')
    if h:
        agent_hints[key] = h.group(1).strip().strip('"')

created, updated = [], []
for prompt_file in sorted(prompts_dir.glob("*.prompt.md")):
    content = prompt_file.read_text(encoding="utf-8-sig")
    # Extract agent: field from frontmatter
    m = re.search(r'^agent:\s*(.+)$', content, re.MULTILINE)
    if not m:
        continue
    agent_key = m.group(1).strip()
    cmd_name  = prompt_file.stem.replace(".prompt", "")  # e.g. myharness.specify

    desc = agent_descs.get(agent_key, agent_descs.get(cmd_name, ""))
    hint = agent_hints.get(agent_key, agent_hints.get(cmd_name, ""))

    hint_line = f"\n{hint}: $ARGUMENTS" if hint else "\n$ARGUMENTS"
    body = f"""{desc}

Use the agent: {agent_key}
{hint_line}
"""

    dest = commands_dir / f"{cmd_name}.md"
    if dest.exists():
        if dest.read_text() != body:
            dest.write_text(body)
            updated.append(f"  {dest.name}")
    else:
        dest.write_text(body)
        created.append(f"  {dest.name}")

if created:
    print("Created Claude Code commands in .claude/commands/:")
    print("\n".join(created))
if updated:
    print("Updated Claude Code commands in .claude/commands/:")
    print("\n".join(updated))
if not created and not updated:
    print("Claude Code commands: no changes needed.")
PYEOF
}

# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
# NOTE: Claude agents (.claude/agents/) are hand-maintained custom files and are
# NO LONGER generated from the Copilot sources. This script only syncs Copilot.
# `claude` / `all` are kept for backward compat but skip the Claude write so a
# stray invocation can never overwrite the custom Claude agents.
case "$PROVIDER" in
  copilot)
    sync_copilot
    ;;
  claude)
    echo "SKIP: Claude agents are hand-maintained — sync does not touch .claude/agents/." >&2
    echo "      Edit .claude/agents/*.md directly. (Nothing written.)" >&2
    ;;
  all)
    sync_copilot
    echo "SKIP: Claude agents are hand-maintained — only Copilot agents were synced." >&2
    ;;
  *)
    echo "ERROR: unknown provider '$PROVIDER'. Use: copilot | claude | all" >&2
    exit 1
    ;;
esac
