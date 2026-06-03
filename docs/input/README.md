# docs/input/ — Input Guide

This folder is the **entry point for all pipeline runs**. Put your requirements here before running any agent.

---

## Which folder to use?

| Situation | Folder | Agent to run after |
| --- | --- | --- |
| **New project** — you have a full product spec, PRD, or requirements doc for the whole system | `new-spec/` | `@myharness.srs.system` |
| **Existing project** — adding a feature, fixing something, or a stakeholder change request | `change-request/` | `@myharness.orchestrator` |

---

## new-spec/

For **new projects**: drop your product requirements document here before running `@myharness.srs.system`.

```text
new-spec/
├── README.md          ← this explains what to put here
└── spec.md            ← your input document (rename or replace as needed)
```

`@myharness.srs.system` reads everything in this folder and generates `docs/output/srs-systems/` — the canonical requirements used by all downstream agents. After that, run `@myharness.orchestrator MOD-XX` per module.

Accepted formats: markdown, plain text, mixed-language docs, multiple files in a subfolder. The agent handles structuring — just put your raw content in.

---

## change-request/

For **adding features or changes** to an existing project.

```text
change-request/
├── registry.yaml      ← log of all CRs (update when adding/completing a CR)
└── cr-input.md        ← fill this in before running @myharness.orchestrator
```

Edit `cr-input.md` with your requirements, then run `@myharness.orchestrator <feature name>`.

---

## docs/technical_architecture.md

Sits at `docs/technical_architecture.md` (not inside `input/`). Filled in automatically by `@myharness.init` from the selected stack profile. All agents read it for tech stack context. Do not edit manually unless you need to override the stack.
