#!/usr/bin/env bash
# switch-provider.sh — Switch AI provider between copilot and claude.
#
# Usage:
#   ./switch-provider.sh copilot       # Switch to GitHub Copilot
#   ./switch-provider.sh claude   # Switch to Claude Code
#   ./switch-provider.sh               # Show current provider

set -euo pipefail

SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

INIT_OPTIONS="$REPO_ROOT/.specify/init-options.json"
CATALOG="$REPO_ROOT/.harness/models/catalog.yaml"
SYNC_SCRIPT="$REPO_ROOT/.harness/agents/sync-models.sh"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

current_provider() {
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('ai','copilot'))" "$INIT_OPTIONS"
}

set_provider_in_json() {
    local provider="$1"
    python3 - "$INIT_OPTIONS" "$provider" <<'PYEOF'
import json, sys, pathlib
path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
data["ai"] = sys.argv[2]
path.write_text(json.dumps(data, indent=2) + "\n")
PYEOF
}

print_status() {
    local provider
    provider=$(current_provider)
    echo ""
    if [[ "$provider" == "claude" ]]; then
        echo "  Active provider: claude"
        echo "  Agents dir:      .claude/agents/"
        echo "  Context file:    CLAUDE.md"
        echo "  Models:          Anthropic (claude-opus-4-5 / claude-sonnet-4-6)"
    else
        echo "  Active provider: copilot"
        echo "  Agents dir:      .github/agents/"
        echo "  Context file:    .github/agents/copilot-instructions.md"
        echo "  Models:          GitHub Copilot (GPT-5.4 / GPT-5.3-Codex)"
    fi
    echo ""
}

# ---------------------------------------------------------------------------
# No argument → show status
# ---------------------------------------------------------------------------
if [[ $# -eq 0 ]]; then
    echo "Current provider:"
    print_status
    echo "Usage: switch-provider.sh [copilot|claude]"
    exit 0
fi

TARGET="$1"

if [[ "$TARGET" != "copilot" && "$TARGET" != "claude" ]]; then
    echo "ERROR: unknown provider '$TARGET'. Use: copilot | claude" >&2
    exit 1
fi

CURRENT=$(current_provider)

if [[ "$CURRENT" == "$TARGET" ]]; then
    echo "Already on provider: $TARGET"
    print_status
    exit 0
fi

echo "Switching from '$CURRENT' → '$TARGET' ..."
echo ""

# 1. Update init-options.json
set_provider_in_json "$TARGET"
echo "  ✓ .specify/init-options.json  ai = $TARGET"

# 2. Sync models for the new provider
echo ""
echo "Syncing models for provider '$TARGET' ..."
bash "$SYNC_SCRIPT" --provider "$TARGET"
echo ""

echo "Done. Active provider:"
print_status
