# MyHarness — Context Index

> **Protocol**: Read this file first every session. Match task → agent → mount read_globs. Do not read outside declared boundaries.

---

## Agent Routing Table

| Task keyword | Agent | Workflow |
|---|---|---|
| **init, setup, onboard, new project, configure stack** | **`myharness.init`** | **Project initialization (run first)** |
| orchestrator, orchestrate, run pipeline, full pipeline | `myharness.orchestrator` | Full 13-step pipeline |
| SRS, software requirements, requirements spec | `myharness.srs` | Step 1 |
| BD, basic design, external design, 外部設計 | `myharness.bd` | Step 2 |
| spec, specify, feature spec | `myharness.specify` | Step 3 |
| clarify, ambiguity, clarification | `myharness.clarify` | Step 4 |
| review spec | `myharness.review.spec` | Step 5 gate |
| plan, implementation plan | `myharness.plan` | Step 6 |
| review plan | `myharness.review.plan` | Step 7 gate |
| DD, detail design, internal design, 内部設計 | `myharness.dd` | Step 8 |
| test cases, generate tests | `myharness.testkit` | Step 8b |
| tasks, task list, task breakdown | `myharness.tasks` | Step 9 |
| implement, code, build, fix | `myharness.implement` | Step 10 |
| review code, code review | `myharness.review.code` | Step 11 gate |
| run tests, QA, testing | `myharness.testkit` | Step 12 |
| system SRS, all modules SRS | `myharness.srs.system` | Pre-flow |
| analyze, cross-artifact | `myharness.analyze` | On demand |
| checklist, quality checklist | `myharness.checklist` | On demand |
| issues, GitHub issues | `myharness.taskstoissues` | On demand |

---

## Key Directories

```
.github/agents/        ← All myharness.*.agent.md definitions
.github/prompts/       ← All myharness.*.prompt.md files
.github/agents/protocols/  ← Shared protocols
.github/agents/steps/      ← Step definitions (read on demand)
.github/agents/templates/  ← Report + token templates

.harness/              ← Control plane (health, enforce, roles, KB, models)
  enforce/             ← scope_guard.py, layer_lint.py
  health/              ← runner.py + 8 checks
  roles/               ← Role boundary definitions
  kb/                  ← Knowledgebase (project, modules, decisions)
  models/              ← catalog.yaml, routing.yaml
  logs/agent.jsonl     ← Event log for health checks

.specify/memory/constitution.md  ← MyHarness Constitution
docs/input/change-request/cr-input.md           ← Raw CR input
docs/input/change-request/       ← CR files + registry.yaml
specs/<feature-id>/              ← spec.md, plan.md, tasks.md
docs/output/design-docs/         ← SRS, BD, DD, testcase, testreport
docs/output/run-logs/            ← Per-feature run logs + reports
```

---

## Pre-run Checklist

1. `python .harness/enforce/scope_guard.py --role implement --staged` — no violations
2. `python .harness/enforce/layer_lint.py` — architecture clean
3. `python .harness/health/runner.py` — score ≥ 70

---

## Metric Targets

| Metric | Target |
|---|---|
| Health score | ≥ 70 |
| Scope violations | 0 |
| Layer violations | 0 |
| Token budget usage | < 85% |
| Test coverage | ≥ 80% |
