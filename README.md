# MyHarness

AI-SDLC Engineering Kit — spec-driven pipeline with control plane enforcement.

Combines execution engine (13-step pipeline, Spec Kit, IPA docs) with control plane (scope enforcement, health monitoring, role boundaries).

---

## Quick Start

### 1. Init a new project (automated agent)

```
@myharness.init ProjectName: MyApp, Description: Internal HR system, Team: 4
```

Agent `myharness.init` will:

- Read available stacks from `.harness/stacks/` and ask you to pick one
- Copy the selected stack profile and fill in all placeholders automatically
- Create project constitution and config

### 2. Prepare your input

There are two scenarios depending on where you are in the project lifecycle:

---

#### Scenario A — New project (full product spec)

You have a full product spec, PRD, or requirements document for the whole system.

**Step 2a:** Run the system SRS agent to extract all modules and features from your document:

```
/myharness.srs.system <path-to-your-spec-file>
```

This reads your spec and generates `docs/output/srs-systems/` — the canonical requirements baseline used by all downstream agents. Your input can be any format: a markdown doc, a folder of files, a PRD, raw notes.

**Step 2b:** Run the orchestrator with a feature description:

```
/myharness.orchestrator <feature or system description>
```

At STEP 0, the orchestrator **automatically detects** that `docs/output/srs-systems/srs-overview-system.md` exists, reads it, and skips SRS re-generation. All downstream steps (BD, spec, plan, implement…) use the pre-generated SRS as primary input — nothing is regenerated from scratch.

---

#### Scenario B — Adding a feature or change request to an existing project

You already have a running project and want to build a new feature.

Open **`docs/input/change-request/cr-input.md`** and fill in your requirements:

| Section | What to write |
| --- | --- |
| **CR Title** | Short name for this feature/change |
| **Requirement Description** | What the feature should do |
| **Context** | Why it's needed, business rationale |
| **Functional Requirements** | List of concrete behaviors (FR-001, FR-002…) |
| **Non-Functional Requirements** | Performance, security, scale concerns |
| **Out of scope** | What this change explicitly does NOT cover |

Raw notes, user stories, or copied Jira tickets all work — agents will structure it.

Then run:

```
/myharness.orchestrator <feature name>
```

At STEP 0, the orchestrator checks `docs/input/change-request/registry.yaml` — if the feature already exists it switches to UPDATE mode automatically.

---

> **Note:** `/myharness.orchestrator` does not take module IDs or flags as input. STEP 0 auto-detects project state (new vs update, SRS pre-generated vs not) from the filesystem. You only need to describe what to build.
>
> `docs/technical_architecture.md` is filled in automatically by `myharness.init` — you don't need to edit it manually.

---

## Available Stacks

Stacks are defined in `.harness/stacks/` — each subdirectory is a stack profile with its own `stack.yaml`, templates, and KB.

When you run `@myharness.init`, it reads this directory dynamically and presents the available options. To add a new stack, copy `_template/` and fill in `stack.yaml`.

See `.harness/stacks/README.md` for the full list and descriptions.

---

## Pipeline (13 Steps)

```
myharness.orchestrator orchestrates:

STEP 1  myharness.srs          → SRS (requirements doc)
STEP 2  myharness.bd           → BD (basic design)
STEP 3  myharness.specify      → spec.md
STEP 4  myharness.clarify      → resolve ambiguities
STEP 5  myharness.review.spec  → review gate (auto-retry)
STEP 6  myharness.plan         → plan.md + data-model
STEP 7  myharness.review.plan  → review gate (auto-retry)
STEP 8  myharness.dd           → DD (detail design)     ┐ parallel
STEP 9  myharness.tasks        → tasks.md               ┘
STEP 8b myharness.testkit      → test cases
STEP 10 myharness.implement    → source code (BE ∥ FE)
STEP 11 myharness.review.code  → code review gate
STEP 12 myharness.testkit      → run tests (BACK-TO-PLAN on fail)
STEP 13 orchestrator direct            → build + launch
```

Partial range runs:

```
myharness.steprange → partial pipeline execution (start_step → end_step)
```

---

## Backup State and Resume

When context is getting large, the workflow should checkpoint state so the next run can resume exactly where it stopped.

Detailed design for this feature run: [docs/output/run-logs/001-simple-login-app/backup-state-design.md](docs/output/run-logs/001-simple-login-app/backup-state-design.md)

Effectiveness scorecard template (A/B baseline vs backup): [docs/output/run-logs/001-simple-login-app/backup-effectiveness-scorecard.md](docs/output/run-logs/001-simple-login-app/backup-effectiveness-scorecard.md)

Auto report output (generated): [docs/output/run-logs/001-simple-login-app/backup-effectiveness-auto.md](docs/output/run-logs/001-simple-login-app/backup-effectiveness-auto.md)

Generate auto report:

```bash
python docs/output/run-logs/001-simple-login-app/backup_effectiveness.py \
    --backup-run docs/output/run-logs/001-simple-login-app \
    --output docs/output/run-logs/001-simple-login-app/backup-effectiveness-auto.md \
    --run-name 001-simple-login-app
```

Compare with baseline run:

```bash
python docs/output/run-logs/001-simple-login-app/backup_effectiveness.py \
    --backup-run docs/output/run-logs/001-simple-login-app \
    --baseline-run docs/output/run-logs/<baseline-run-id> \
    --output docs/output/run-logs/001-simple-login-app/backup-effectiveness-auto.md \
    --run-name 001-simple-login-app
```

### What to persist

- `state.yaml` for minimal run status and fast resume (`state`, `last_completed_step`, `completed_steps`, retry counts, token summary)
- `run-context.yaml` as canonical source for step outputs and artifact paths
- a checkpoint snapshot file (`checkpoint.md` or `checkpoint.jsonl`) with timestamp, current step, open issues, and next action
- final summary artifacts (`token-report.md`, `pipeline-completion.md`) at end-of-run

### When to checkpoint

- after each step completes
- after each review gate result (`REJECTED` or `APPROVED_WITH_CONDITIONS`)
- before dispatching high-risk steps (`implement`, `test`, `launch`)
- before context budget becomes critical (recommended thresholds: 70% / 85% / 95%)

### Resume order

1. Read `state.yaml` to determine `last_completed_step`.
2. Read `run-context.yaml` to recover latest artifact paths.
3. Read nearest checkpoint snapshot for open issues and next action.
4. Continue from `last_completed_step + 1` (or explicit resume step).

---

## Agents

See [INDEX.md](INDEX.md) for the full routing table.

| Agent | Role |
|---|---|
| `myharness.init` | **Project initialization** — run first when onboarding a new project |
| `myharness.orchestrator` | Orchestrator — coordinates the full pipeline |
| `myharness.steprange` | Partial pipeline runner — execute only `start_step` → `end_step` |
| `myharness.srs/bd/dd` | IPA document generation |
| `myharness.specify/clarify/plan/tasks` | Spec Kit core |
| `myharness.implement` | Code generation |
| `myharness.review.*` | Quality gates |
| `myharness.testkit` | Test generation + execution |

---

## Control Plane (`.harness/`)

```
.harness/
├── enforce/          ← scope_guard.py, layer_lint.py (pre-commit)
├── health/           ← health runner + 8 checks (post-pipeline)
├── roles/            ← role boundary definitions per agent
├── stacks/           ← stack profiles (web/mobile/template)
├── kb/               ← knowledgebase (project, modules, decisions, post-mortem)
├── models/           ← model catalog + routing policy
└── logs/             ← agent.jsonl (event log for health checks)
```

---

## Directory Structure

```
.github/agents/            ← myharness.*.agent.md (20 agents)
.github/agents/protocols/  ← Shared protocols
.github/agents/steps/      ← Step definitions
.github/agents/templates/  ← Report + token templates
.harness/                  ← Control plane (see above)
.specify/                  ← Spec Kit config + constitution

docs/
├── technical_architecture.md  ← Project tech stack (generated by myharness.init, read by all agents)
├── input/                     ← YOU WRITE HERE before running the pipeline
│   ├── README.md              ← Start here — explains which folder to use
│   ├── new-spec/              ← Full product spec for new projects → feed to @myharness.srs.system
│   └── change-request/        ← Feature/CR for existing projects → feed to @myharness.orchestrator
└── output/                    ← Generated by agents — do not edit manually
    ├── srs-systems/           ← System-wide SRS (from myharness.srs.system)
    ├── design-docs/           ← SRS, BD, DD per module
    └── run-logs/              ← Pipeline logs and phase reports

specs/                         ← Spec Kit artifacts per feature run
```
