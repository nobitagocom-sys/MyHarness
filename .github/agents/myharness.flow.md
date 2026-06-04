# MyHarness — Pipeline Flow

> Describes the operational flow of the multi-agent system for the Feature Development Pipeline.
> Model names shown are **provider-dependent** — see `.harness/models/catalog.yaml` for the active mapping.
> Current provider is set in `.specify/init-options.json` (`ai` field).

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  myharness.orchestrator                         │
│               [orchestrator tier] — full pipeline autonomy      │
│                                                                 │
│  📋 .harness/agents/protocols/                                  │
│  📝 .harness/agents/steps/                                      │
│  📄 .harness/agents/templates/    📊 docs/output/run-logs/      │
└──────────┬──────────────────────────────────────────────────────┘
           │ delegates to specialist sub-agents
           ▼
┌──────────────────────────────────────────────────────────────────┐
│  myharness.srs          │  myharness.bd           │  myharness.dd          │
│  myharness.specify      │  myharness.clarify      │  myharness.plan        │
│  myharness.tasks        │  myharness.implement    │  myharness.testkit     │
│  myharness.review.spec  │  myharness.review.plan  │  myharness.review.code │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Pipeline Flow — 5 Phases, 16 Steps

```
USER INPUT ($ARGUMENTS: feature description)
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 1: DESIGN (Steps 0–4)                                    ║
║  📄 .harness/agents/steps/steps-01-04-design.md                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 0 ─ orchestrator (self)                                    ║
║  │  Detect existing spec in specs/ directory                    ║
║  │  → mode = CREATE or UPDATE                                   ║
║  ▼                                                               ║
║  STEP 1 ─ myharness.srs [synthesis tier]                         ║
║  │  Input:  srs-systems/ (overview + module detail + wireframe) ║
║  │  Output: docs/output/design-docs/srs/srs-<MOD>-<name>.md    ║
║  │  Report: 01-srs-report.md                                    ║
║  ▼                                                               ║
║  STEP 2 ─ myharness.bd [synthesis tier]                          ║
║  │  Input:  SRS + system overview + technical architecture      ║
║  │  Output: docs/output/design-docs/bd/bd-<MOD>-<name>.md      ║
║  │  Report: 02-bd-report.md                                     ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] markers             ║
║  ▼                                                               ║
║  STEP 3 ─ myharness.specify [synthesis tier]                     ║
║  │  Input:  Feature desc + SRS + BD                             ║
║  │  Output: specs/<feature-id>/spec.md                          ║
║  │  Report: 03-specify-report.md                                ║
║  │  🔧 Post-check: orchestrator auto-resolves [NEEDS CLARIFICATION] ║
║  ▼                                                               ║
║  STEP 4 ─ myharness.clarify [synthesis tier]                     ║
║     Input:  spec.md                                             ║
║     Output: spec.md (updated) + 04-clarify-qa.md               ║
║     Report: 04-clarify-report.md                                ║
║     ⚠️  NO HUMAN PAUSE — auto-resolve all questions             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 2: REVIEW (Steps 5–7)                                    ║
║  📄 .harness/agents/steps/steps-05-07-review.md                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 5 ─ myharness.review.spec [review tier]     🔄 GATE       ║
║  │  Input:  spec.md + SRS + constitution                        ║
║  │  Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║  │  Report: 05-review-spec-report.md                            ║
║  │                                                               ║
║  │  ❌ REJECTED → myharness.specify fixes → re-review (max 5x)  ║
║  │  ✅/⚠️ → continue                                            ║
║  ▼                                                               ║
║  STEP 6 ─ myharness.plan [coding tier]                           ║
║  │  Input:  spec.md + constitution + docs/technical_architecture.md ║
║  │  Output: plan.md + data-model.md + contracts/ + research.md  ║
║  │  Report: 06-plan-report.md                                   ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] in plan artifacts    ║
║  ▼                                                               ║
║  STEP 7 ─ myharness.review.plan [review tier]     🔄 GATE       ║
║     Input:  plan.md + spec.md + data-model.md + tech arch       ║
║     Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║     Report: 07-review-plan-report.md                            ║
║                                                                  ║
║     ❌ REJECTED → myharness.plan fixes → re-review (max 5x)     ║
║     ✅/⚠️ → continue                                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 3: DETAIL DESIGN (Steps 8–9)                             ║
║  📄 .harness/agents/steps/steps-08-09-detail.md                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 8 ─ myharness.dd [coding tier]                             ║
║  │  Input:  BD + SRS + spec + plan + tech arch                  ║
║  │  Output: docs/output/design-docs/dd/dd-<MOD>-<name>.md      ║
║  │  Report: 08-dd-report.md                                     ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] in DD                ║
║  ▼                                                               ║
║  STEP 8b ─ myharness.testkit [review tier]                       ║
║  │  Mode:   gen-testcases                                       ║
║  │  Input:  SRS + BD + DD + spec + plan                         ║
║  │  Output: docs/output/design-docs/testcase/testcase-<MOD>-<name>.md ║
║  │  Report: 08b-testcases-report.md                             ║
║  ▼                                                               ║
║  STEP 9 ─ myharness.tasks [synthesis tier]                       ║
║     Input:  plan.md + spec.md + data-model.md                   ║
║     Output: specs/<feature-id>/tasks.md                         ║
║     Report: 09-tasks-report.md                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 4: IMPLEMENTATION & QA (Steps 10–12)                     ║
║  📄 .harness/agents/steps/steps-10-12-implement.md              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 10 ─ myharness.implement [coding tier]          🔄 GATE   ║
║  │  Input:  tasks.md + plan.md + data-model.md + contracts/     ║
║  │  Output: src/modules/<module>/ (source code)                 ║
║  │  Phase 1: implement all tasks                                ║
║  │  Phase 2: build & fix all errors                             ║
║  │  Report: 10-implement-report.md (incl. Screen Verification)  ║
║  │  ⚡ REAL EXECUTION — npm build, docker up, npm start         ║
║  │                                                               ║
║  │  ❌ Build fails → auto-fix → re-build (max 5x)               ║
║  │  ✅ Build success + app starts → continue                    ║
║  ▼                                                               ║
║  STEP 11 ─ myharness.review.code [review tier]        🔄 GATE   ║
║  │  Input:  source code + spec + tasks + constitution           ║
║  │  Check:  code quality + DB data usage (no mock data)         ║
║  │  Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║  │  Report: 11-review-code-report.md                            ║
║  │                                                               ║
║  │  ❌ REJECTED → myharness.implement fixes → re-review (max 5x)║
║  │  ✅/⚠️ → continue                                            ║
║  ▼                                                               ║
║  STEP 12 ─ myharness.testkit [review tier]            🔄 GATE   ║
║     Mode:   run-tests                                           ║
║     Input:  testcases + running app                             ║
║     Output: testreport-<MOD>-<name>.md                          ║
║     Report: 12-testkit-report.md                                ║
║     ⚡ REAL EXECUTION — Jest + Playwright                       ║
║                                                                  ║
║     ❌ FAIL → 🔙 BACK-TO-PLAN (myharness.plan → ... → re-test)  ║
║     ✅ PASS → continue                                          ║
║     Max 3 BACK-TO-PLAN cycles → force continue with defects    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 5: LAUNCH (Step 13)                                      ║
║  📄 .harness/agents/steps/step-13-launch.md                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 13 ─ orchestrator (direct: build + DB + launch)           ║
║  │  Build BE + connect DB + build FE + start services           ║
║  │  Report: 13-launch-report.md (incl. Launch Status)           ║
║  │  ⚡ REAL EXECUTION — npm build, docker up, npm build+start   ║
║  │  open_browser_page → user sees working UI                    ║
║  ▼                                                               ║
║  ✅ PIPELINE COMPLETE                                            ║
║  │  Write final pipeline-completion report                      ║
║  │  Write [END] orchestrator log entry                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 3. Agent Roster

> Model assignments are managed in `.harness/models/catalog.yaml`.
> Run `bash .harness/agents/sync-models.sh --provider all` after changing models.

### 3.1 Generation Agents (synthesis + coding tiers)

| Agent | Tier | Steps | Role | Primary Output |
|-------|------|-------|------|----------------|
| `myharness.srs` | synthesis | 1 | Requirements analysis → SRS | `srs-<MOD>-<name>.md` |
| `myharness.bd` | synthesis | 2 | External design (BD) | `bd-<MOD>-<name>.md` |
| `myharness.specify` | synthesis | 3 | Create feature spec | `spec.md` |
| `myharness.clarify` | synthesis | 4 | Detect & resolve ambiguities | `spec.md` (updated) |
| `myharness.plan` | coding | 6 | Implementation planning | `plan.md`, `data-model.md`, `contracts/` |
| `myharness.dd` | coding | 8 | Detailed design (DD) | `dd-<MOD>-<name>.md` |
| `myharness.tasks` | synthesis | 9 | Task decomposition | `tasks.md` |
| `myharness.implement` | coding | 10,12,13 | Code implementation + build + launch | `src/modules/<mod>/` |

### 3.2 Review Agents (review tier — quality gates)

| Agent | Tier | Steps | Role | Gate |
|-------|------|-------|------|------|
| `myharness.review.spec` | review | 5 | Review spec vs SRS | 🔄 Auto-Retry (max 5) |
| `myharness.review.plan` | review | 7 | Review plan vs spec | 🔄 Auto-Retry (max 5) |
| `myharness.review.code` | review | 11 | Review code vs spec/constitution | 🔄 Auto-Retry (max 5) |

### 3.3 QA Agent (review tier — independent testing)

| Agent | Tier | Steps | Mode | Role |
|-------|------|-------|------|------|
| `myharness.testkit` | review | 8b | `gen-testcases` | Generate test cases from SRS+BD+DD |
| `myharness.testkit` | review | 12 | `run-tests` | Execute tests (Jest + Playwright) |

### 3.4 Orchestrator

| Agent | Tier | Steps | Role |
|-------|------|-------|------|
| `myharness.orchestrator` | orchestrator | ALL | Coordinate the entire pipeline, auto-resolve all issues |

### 3.5 Tier → Model Mapping (per provider)

| Tier | Copilot model | Claude Code model | Used by |
|------|--------------|-------------------|---------|
| synthesis | GPT-5.4 | claude-opus-4-5 | srs, bd, specify, clarify, tasks, srs.system, constitution |
| coding | GPT-5.3-Codex | claude-sonnet-4-6 | plan, dd, implement |
| review | claude-sonnet-4-6 | claude-sonnet-4-6 | review.*, testkit, init, analyze, checklist |
| orchestrator | claude-sonnet-4-6 | claude-sonnet-4-6 | orchestrator |

---

## 4. Communication Mechanisms (Context Exchange)

### 4.1 Orchestrator → Sub-Agent: Structured $ARGUMENTS

```yaml
feature-id: 001-xxx
module-id: mod01
module-keyword: [KEYWORD]
pipeline-context: docs/output/run-logs/001-xxx/run-context.yaml
mode: autonomous
language: English
```

### 4.2 Sub-Agent → Orchestrator: Step Result Block

```yaml
<!-- STEP-RESULT
step: 1
agent: myharness.srs
status: SUCCESS
feature-id: 001-xxx
module-id: mod01
artifacts:
  srs-path: docs/output/design-docs/srs/srs-mod01-xxx.md
  report: docs/output/run-logs/001-xxx/reports/01-srs-report.md
metrics:
  fea-count: 12
  tbc-count: 3
verdict: APPROVED
next-inputs:
  srs-path: docs/output/design-docs/srs/srs-mod01-xxx.md
/STEP-RESULT -->
```

### 4.3 Pipeline Context File (shared state)

```
docs/output/run-logs/<feature-id>/run-context.yaml
```

- Created at Step 0 (immutable fields: feature-id, module-id, tech-stack)
- Updated after each step with artifact paths + metrics from STEP-RESULT
- Sub-agents read this file to discover outputs from prior steps

---

## 5. Gate Mechanisms

### 5.1 Report Hard Gate ⛔

- Applies to: **EVERY step** (after completion)
- Requirement: Report file MUST exist with all required sections
- Protocol: `.harness/agents/protocols/report-gate-protocol.md`

### 5.2 Review Gate 🔄

- Applies to: Steps 5, 7, 11 (review agents)
- Logic: REJECTED → fix agent corrects → re-review (maximum 5 times)
- Protocol: `.harness/agents/protocols/gate-retry-protocol.md`

### 5.3 Build Gate 🔄

- Applies to: Step 10 (implementation + build & fix)
- Logic: Build fail → auto-fix → re-build (maximum 5 times)

### 5.4 Test Gate 🔙

- Applies to: Step 12 (test execution)
- Logic: Test FAIL → **BACK-TO-PLAN** (return to Step 6 → re-plan → re-implement → re-test)
- Maximum 3 BACK-TO-PLAN cycles → force continue

### 5.5 Auto-Resolve 🔧

- Applies to: When encountering `[NEEDS CLARIFICATION]` markers
- Logic: Orchestrator automatically resolves using optimal assumption, logs to report
- Protocol: `.harness/agents/protocols/auto-resolve-protocol.md`

---

## 6. Repository Structure

```
.harness/agents/                    ← shared, provider-independent
├── sync-models.sh                  ← sync agents for copilot or claude-code
├── protocols/                      ← runtime protocols (read on-demand)
│   ├── auto-resolve-protocol.md
│   ├── gate-retry-protocol.md
│   ├── report-gate-protocol.md
│   ├── timestamp-protocol.md
│   ├── log-formats.md
│   ├── implement-delegation.md
│   ├── step-result-block.md
│   ├── pipeline-context.md
│   ├── scope-guard-protocol.md
│   ├── run-state-protocol.md
│   └── health-check-protocol.md
├── steps/                          ← step definitions (read on-demand)
│   ├── steps-01-04-design.md
│   ├── steps-05-07-review.md
│   ├── steps-08-09-detail.md
│   ├── steps-10-12-implement.md
│   └── step-13-launch.md
└── templates/                      ← shared report templates
    ├── report-templates.md
    ├── pipeline-completion.md
    └── token-report-template.md

.harness/models/
├── catalog.yaml                    ← single source of truth for model assignments
└── routing.yaml                    ← phase → tier routing

.github/agents/                     ← Copilot provider
├── copilot-instructions.md         ← Copilot context file
├── myharness.*.agent.md            ← Copilot agent definitions
└── myharness.flow.md               ← this file

.github/prompts/                    ← Copilot slash commands
└── myharness.*.prompt.md

.claude/agents/                     ← Claude Code provider (generated)
└── myharness.*.md

.claude/commands/                   ← Claude Code slash commands (generated)
└── myharness.*.md

.specify/scripts/bash/
└── switch-provider.sh              ← switch between copilot and claude-code
```

---

## 7. Output Structure (Runtime)

```
docs/output/
├── design-docs/
│   ├── srs/srs-mod01-xxx.md               ← Step 1
│   ├── bd/bd-mod01-xxx.md                 ← Step 2
│   ├── dd/dd-mod01-xxx.md                 ← Step 8
│   ├── testcase/testcase-mod01-xxx.md     ← Step 8b
│   └── testreport/testreport-mod01-xxx.md ← Step 12
│
└── run-logs/<feature-id>/
    ├── 00-myharness.log.md                ← orchestrator log (all steps)
    ├── run-context.yaml                   ← shared state
    └── reports/
        ├── 01-srs-report.md
        ├── 02-bd-report.md
        ├── 03-specify-report.md
        ├── 04-clarify-report.md
        ├── 05-review-spec-report.md
        ├── 06-plan-report.md
        ├── 07-review-plan-report.md
        ├── 08-dd-report.md
        ├── 08b-testcases-report.md
        ├── 09-tasks-report.md
        ├── 10-implement-report.md
        ├── 11-review-code-report.md
        ├── 12-testkit-report.md
        └── 13-launch-report.md

specs/<feature-id>/
├── spec.md                                ← Step 3
├── plan.md                                ← Step 6
├── data-model.md                          ← Step 6
├── research.md                            ← Step 6
├── tasks.md                               ← Step 9
├── contracts/*.md                         ← Step 6
└── checklists/requirements.md             ← Step 3
```

---

## 8. BACK-TO-PLAN Cycle (Special Flow)

When Step 12 (test execution) FAILS:

```
STEP 12 FAIL
    │
    ▼
orchestrator logs [BACK-TO-PLAN]
    │
    ▼
STEP 6  myharness.plan        ← re-plan with failure context
    │
    ▼
STEP 7  myharness.review.plan ← re-review plan
    │
    ▼
STEP 8  myharness.dd          ← re-generate DD
    │
    ▼
STEP 9  myharness.tasks       ← re-generate tasks
    │
    ▼
STEP 10 myharness.implement   ← re-implement + build
    │
    ▼
STEP 11 myharness.review.code ← re-review code
    │
    ▼
STEP 12 myharness.testkit     ← re-test
    │
    ├─ ✅ PASS → STEP 13 (fix & launch)
    └─ ❌ FAIL → repeat cycle (max 3 total)
              └─ After 3 cycles → force STEP 13 with known defects
```
