# new-spec/ — New Project Input

Put your product requirements here before running `@myharness.srs.system`.

---

## What to put here

Anything that describes what the system should do:

- Full PRD or product spec (markdown, text)
- Feature list with screen/flow descriptions
- Wireframe descriptions or user stories
- Mixed-language content (Vietnamese, English) — agents handle both
- Multiple files or subfolders — agent reads the whole folder

The agent will extract all modules, features, business rules, actors, and flows. The more detail you provide, the fewer `[TBC]` gaps it will flag.

**You do not need to follow any specific format.** Raw notes work. The agent structures it for you.

---

## How to use

1. Replace `spec.md` with your actual document, or add more files alongside it.
2. Run: `@myharness.srs.system docs/input/new-spec/`
3. Review output in `docs/output/srs-systems/`
4. Run pipeline per module: `@myharness.orchestrator MOD-01`, `@myharness.orchestrator MOD-02`, …

---

## What the agent generates

From your input, `myharness.srs.system` produces:

```
docs/output/srs-systems/
├── srs-overview-system.md        ← system-wide overview, module index, ERD, NFR
└── mod01-<name>/
    ├── srs-mod01-detail.md       ← full feature list + business rules per module
    └── srs-mod01-wireframe.md    ← UI/UX requirements per module
```

These files are the canonical input for `@myharness.orchestrator` and all downstream agents.
