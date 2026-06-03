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

# Check if target dirs are intact (allow re-sync even if already on target)
needs_sync=false
if [[ "$TARGET" == "claude" ]]; then
    [[ ! -d "$REPO_ROOT/.claude/agents" ]] && needs_sync=true
    [[ ! -d "$REPO_ROOT/.claude/commands" ]] && needs_sync=true
fi

if [[ "$CURRENT" == "$TARGET" ]] && [[ "$needs_sync" == "false" ]]; then
    echo "Already on provider: $TARGET"
    print_status
    exit 0
fi

if [[ "$CURRENT" == "$TARGET" ]]; then
    echo "Provider is '$TARGET' but output dirs are missing — re-syncing ..."
else
    echo "Switching from '$CURRENT' → '$TARGET' ..."
fi
echo ""

# 1. Update init-options.json
set_provider_in_json "$TARGET"
echo "  ✓ .specify/init-options.json  ai = $TARGET"

# 2. Clean up outgoing provider's generated dirs
if [[ "$TARGET" == "claude" ]]; then
    # Switching to claude — nothing to clean on copilot side (source files, keep them)
    :
else
    # Switching to copilot — remove .claude/ so Claude Code won't load stale agents
    if [[ -d "$REPO_ROOT/.claude" ]]; then
        rm -rf "$REPO_ROOT/.claude"
        echo "  ✓ Removed .claude/ (inactive provider)"
    fi
fi

# 3. Sync agent files + commands for target provider
if [[ -f "$SYNC_SCRIPT" ]]; then
    if [[ "$TARGET" == "claude" ]]; then
        bash "$SYNC_SCRIPT" --provider claude
    else
        bash "$SYNC_SCRIPT" --provider copilot
    fi
fi
echo "  ✓ Synced agents and commands"

# 3. Update agent context file (CLAUDE.md or copilot-instructions.md)
UPDATE_SCRIPT="$SCRIPT_DIR/update-agent-context.sh"
TEMPLATE="$REPO_ROOT/.specify/templates/claude-instructions-template.md"
CLAUDE_MD="$REPO_ROOT/CLAUDE.md"

if [[ "$TARGET" == "claude" ]]; then
    echo ""
    if [[ ! -f "$CLAUDE_MD" ]]; then
        if [[ -f "$TEMPLATE" ]]; then
            cp "$TEMPLATE" "$CLAUDE_MD"
            echo "  ✓ Created CLAUDE.md (from claude-instructions-template.md)"
        else
            echo "  ✗ Template not found at $TEMPLATE — CLAUDE.md not created"
        fi
    else
        # CLAUDE.md exists — try updating with plan context if available
        if [[ -f "$UPDATE_SCRIPT" ]]; then
            bash "$UPDATE_SCRIPT" claude 2>/dev/null && echo "  ✓ Updated CLAUDE.md" \
                || echo "  ✓ CLAUDE.md already exists (no plan.md to update from)"
        fi
    fi
else
    echo ""
    if [[ -f "$UPDATE_SCRIPT" ]]; then
        echo "  Updating copilot-instructions.md context..."
        bash "$UPDATE_SCRIPT" copilot 2>/dev/null || echo "  (skipped — no plan.md found yet)"
    fi
fi

echo ""
echo "Done. Active provider:"
print_status
