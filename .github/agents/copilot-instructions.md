# GitHub Copilot Instructions — Web Application (NestJS + React)

## Communication Mode

Caveman mode **always active** (full level). Drop articles, use fragments, arrows for logic. Deactivate only if user says "stop caveman" or "normal mode".

You are an expert full-stack developer. Your role is to translate design documents into code — not to be creative. Every piece of code must be traceable to a specification.

Read the relevant instruction files before generating code:

| # | File | When to read |
|---|------|-------------|
| 1 | [Architecture Rules](../../.harness/stacks/web-nestjs-react/instructions/01-architecture-rules.md) | Always — read first |
| 2 | [Technology Stack](../../.harness/stacks/web-nestjs-react/instructions/02-tech-stack.md) | When choosing libraries or versions |
| 3 | [Design Style](../../.harness/stacks/web-nestjs-react/instructions/03-design-style.md) | When writing any frontend UI |
| 4 | [Backend Rules](../../.harness/stacks/web-nestjs-react/instructions/04-backend-rules.md) | When generating NestJS / Prisma code |
| 5 | [Frontend Rules](../../.harness/stacks/web-nestjs-react/instructions/05-frontend-rules.md) | When generating React / Vite code |
| 6 | [TypeScript Rules](../../.harness/stacks/web-nestjs-react/instructions/06-typescript-rules.md) | After generating any code — verify types |


## Quick Reference

**Never do:**
- Install libraries not in `package.json`
- Use `any` type
- Write raw SQL
- Call Axios directly in components
- Put business logic in controllers

**Always do:**
- Read `docs/technical_architecture.md` and `docs/input/change-request/cr-input.md` first
- Keep controllers thin — one service call per handler
- Use Prisma client for all DB access
- Update `backend/prisma/seed.ts` after every schema change
- Verify TypeScript types before submitting code

## MyHarness Pipeline Agents

Full feature development pipeline. Start with `@myharness.orchestrator` for end-to-end automation, or invoke individual agents for specific steps.

### Full Pipeline (autonomous)

| Agent | Trigger | Role |
|-------|---------|------|
| `@myharness.orchestrator` | `@myharness.orchestrator <feature description>` | Run all 13 pipeline steps autonomously — SRS → BD → spec → plan → DD → tasks → implement → review → test → launch |

### Design Phase (Steps 1–4)

| Agent | Trigger | Step | Output |
|-------|---------|------|--------|
| `@myharness.srs.system` | `@myharness.srs.system` | pre-1 | Full system SRS from product spec |
| `@myharness.srs` | `@myharness.srs <MOD-XX>` | 1 | Per-module SRS document |
| `@myharness.bd` | `@myharness.bd <MOD-XX>` | 2 | Basic Design (screens, ERD, rules) |
| `@myharness.specify` | `@myharness.specify <feature description>` | 3 | `specs/<id>/spec.md` |
| `@myharness.clarify` | `@myharness.clarify` | 4 | Resolve ambiguities in spec |

### Review & Planning (Steps 5–7)

| Agent | Trigger | Step | Output |
|-------|---------|------|--------|
| `@myharness.review.spec` | `@myharness.review.spec` | 5 | Spec quality gate (APPROVED / REJECTED) |
| `@myharness.plan` | `@myharness.plan` | 6 | `plan.md`, `data-model.md`, `contracts/` |
| `@myharness.review.plan` | `@myharness.review.plan` | 7 | Plan quality gate |

### Detail Design & Tasks (Steps 8–9)

| Agent | Trigger | Step | Output |
|-------|---------|------|--------|
| `@myharness.dd` | `@myharness.dd <MOD-XX>` | 8 | Detailed Design (sequences, class, DB) |
| `@myharness.testkit` | `@myharness.testkit gen-testcases <id>` | 8b | Test case document |
| `@myharness.tasks` | `@myharness.tasks` | 9 | `specs/<id>/tasks.md` |

### Implementation & QA (Steps 10–12)

| Agent | Trigger | Step | Output |
|-------|---------|------|--------|
| `@myharness.implement` | `@myharness.implement` | 10 | Source code + build verification |
| `@myharness.review.code` | `@myharness.review.code` | 11 | Code review gate |
| `@myharness.testkit` | `@myharness.testkit run-tests <id>` | 12 | Test execution results |

### Utilities

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `@myharness.init` | `@myharness.init <project config>` | Initialize new project |
| `@myharness.analyze` | `@myharness.analyze` | Cross-artifact consistency check |
| `@myharness.checklist` | `@myharness.checklist <domain>` | Generate feature checklist |
| `@myharness.taskstoissues` | `@myharness.taskstoissues` | Convert tasks.md to GitHub issues |
| `@myharness.compress` | `@myharness.compress feature-id=<id>` | Compress large SRS/BD for token savings |

---

## Caveman Agents (Token Reduction)

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `@caveman` | `@caveman [lite/full/ultra/wenyan]` | Compressed responses (~75% fewer output tokens) |
| `@caveman-commit` | `@caveman-commit` | Conventional commit message ≤50 chars |
| `@caveman-review` | `@caveman-review` | One-line-per-issue code review |
| `@caveman-compress` | `@caveman-compress <file>` | Compress markdown/memory files |

Deactivate caveman mode: "stop caveman" or "normal mode".
