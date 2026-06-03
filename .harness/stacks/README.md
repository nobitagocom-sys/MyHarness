# MyHarness Stack References

Each subdirectory is a **stack profile** — a collection of reference files for a specific project type.

When starting a new project with MyHarness:

1. Copy the appropriate stack profile into the project root
2. Fill in project-specific information
3. Agents read from `docs/technical_architecture.md` and `.github/agents/copilot-instructions.md`

---

## Available Stacks

Each subdirectory (except `_template`) is a stack. Run `@myharness.init` to see the current list — it reads `stack.yaml` from each directory dynamically.

To add a new stack: copy `_template/`, rename the directory, and fill in `stack.yaml`.

---

## Stack Profile Structure

```
stacks/<stack-name>/
├── stack.yaml                  ← id, name, description, tech, placeholders, agent_hints
├── technical_architecture.md   ← Tech decisions, repo structure, coding rules
├── copilot-instructions.md     ← Coding rules for AI agents (copy → .github/agents/)
└── kb/                         ← Stack-specific knowledge base (post-mortem rules, decisions)
```

---

## Usage in a New Project

Run `@myharness.init` — it handles copying, placeholder filling, and KB setup automatically.

To add a custom stack, copy `_template/` and fill in all `[PLACEHOLDERS]` in `stack.yaml`.
