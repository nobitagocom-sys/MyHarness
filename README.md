# MyHarness

Spec-driven AI pipeline. You describe a feature — agents turn it into requirements, design, code, and tests automatically (13 steps).

Runs on **GitHub Copilot** (default) or **Claude Code**. Same commands work on both.

---

## Quick Start

**1. Pick provider** (default is `copilot`, skip if fine):

```bash
bash .specify/scripts/bash/switch-provider.sh claude    # or: copilot
```

**2. Initialize the project** (first time only):

```
/myharness.init ProjectName: MyApp, Description: Internal HR system, Team: 4
```

Asks you to pick a stack, then sets up the config and tech architecture doc.

**3. Write what you want to build, then run the pipeline:**

| You have | Command |
| --- | --- |
| **New spec/PRD** (file) | `/myharness.orchestrator --N <path-to-spec-file>` |
| **Change request** on existing feature | `/myharness.orchestrator --CR <feature-id> <path-to-cr-file>` |
| Not sure / just describe it | `/myharness.orchestrator <feature description>` |

The flag tells the orchestrator the mode directly, so you don't have to remember the filesystem rules:

- `--N` → **CREATE** mode (new spec → split into modules)
- `--CR` → **UPDATE** mode (apply change request to an existing feature)
- *no flag* → auto-detect CREATE vs UPDATE from your files

Examples:

```
/myharness.orchestrator --N docs/input/new-spec/my_feature.md
/myharness.orchestrator --CR feat-login docs/input/change-request/cr-input.md
/myharness.orchestrator add user profile page
```

**Run only part of it / recover a stalled run** (optional) — `orchestrator-control` runs a step range then stops, and is also the recovery path when a run dies mid-step:

```
/myharness.orchestrator-control from=1 to=7 --N docs/input/new-spec/my_feature.md   # run steps 1–7 then stop
/myharness.orchestrator-control from=6 to=6 <feature-id>                            # re-run only step 6
/myharness.orchestrator-control from=0 to=13 <feature-id>                           # resume a stalled run
```

It reads `state.yaml` to know the last completed step, so a plain `<feature-id>` resumes from where it stopped. `from=N to=N` re-runs a single step.

> **Big multi-module spec?** Run `/myharness.srs.system <spec-path>` first to build one shared requirements baseline for all modules, then run the orchestrator. For a single feature you can skip it.

---

## What cr-input.md needs

| Section | What to write |
| --- | --- |
| CR Title | Short feature name |
| Requirement Description | What it should do |
| Context | Why it's needed |
| Functional Requirements | Concrete behaviors (FR-001…) |
| Non-Functional Requirements | Performance, security, scale |
| Out of scope | What it does NOT cover |

Raw notes or Jira tickets work too — agents structure it.

---

## The 13 Steps

```
1  SRS          → requirements
2  BD           → basic design
3  specify      → spec.md
4  clarify      → resolve ambiguities
5  review.spec  → gate
6  plan         → plan.md + data model
7  review.plan  → gate
8  DD + tasks   → detail design + tasks.md
9  testkit      → test cases
10 implement    → code (backend ∥ frontend)
11 review.code  → gate
12 testkit      → run tests
13 orchestrator → build + launch
```

---

## Stacks

`/myharness.init` lets you choose:

| Stack | For |
| --- | --- |
| `web-nestjs-react` | NestJS + React + Prisma |
| `web-nextjs-supabase` | Next.js + Supabase |
| `mobile-react-native` | React Native |

---

## Where things go

```
docs/input/    ← YOU write here (cr-input.md or full spec)
docs/output/   ← agents generate here — don't edit by hand
specs/         ← spec.md, plan.md, tasks.md per feature
```

For full details (control plane, models, agent routing) see [INDEX.md](INDEX.md).
