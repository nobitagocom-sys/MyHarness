# Flow Agent — Pipeline

> Describes the operational flow of the multi-agent system for the Feature Development Pipeline.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  myharness.orchestrator (Orchestrator)                         │
│               claude-sonnet-4-6 — Orchestrator                  │
│                                                                 │
│  📋 protocols/    📝 steps/    📄 templates/    📊 logs/       │
└──────────┬──────────────────────────────────────────────────────┘
           │ delegates to 12 specialist sub-agents
           ▼
┌──────────────────────────────────────────────────────────────────┐
│  myharness.srs                │  myharness.bd                │  myharness.dd       │
│  myharness.specify        │  myharness.clarify       │  myharness.plan │
│  myharness.tasks          │  myharness.implement     │               │
│  myharness.review.spec         │  myharness.review.plan        │               │
│  myharness.review.code         │  myharness.testkit           │               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Pipeline Flow — 5 Phases, 16 Steps

```
USER INPUT ($ARGUMENTS: feature description)
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 1: DESIGN (Steps 0–4)                                   ║
║  📄 steps/steps-01-04-design.md                                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 0 ─ orchestrator (self)                                           ║
║  │  Detect existing spec in specs/ directory                    ║
║  │  → mode = CREATE or UPDATE                                   ║
║  ▼                                                               ║
║  STEP 1 ─ myharness.srs (GPT-5.4)                                    ║
║  │  Input:  srs-systems/ (overview + module detail + wireframe) ║
║  │  Output: docs/output/design-docs/srs/srs-<MOD>-<name>.md            ║
║  │  Report: 01-srs-report.md                                   ║
║  ▼                                                               ║
║  STEP 2 ─ myharness.bd (GPT-5.4)                                     ║
║  │  Input:  SRS + system overview + technical architecture      ║
║  │  Output: docs/output/design-docs/bd/bd-<MOD>-<name>.md              ║
║  │  Report: 02-bd-report.md                                    ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] markers             ║
║  ▼                                                               ║
║  STEP 3 ─ myharness.specify (GPT-5.4)                            ║
║  │  Input:  Feature desc + SRS + BD                             ║
║  │  Output: specs/<feature-id>/spec.md                          ║
║  │  Report: 03-specify-report.md                                ║
║  │  🔧 Post-check: orchestrator auto-resolves [NEEDS CLARIFICATION]    ║
║  ▼                                                               ║
║  STEP 4 ─ myharness.clarify (GPT-5.4)                            ║
║     Input:  spec.md                                              ║
║     Output: spec.md (updated) + 04-clarify-qa.md               ║
║     Report: 04-clarify-report.md                                ║
║     ⚠️  NO HUMAN PAUSE — auto-resolve all questions             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 2: REVIEW (Steps 5–7)                                    ║
║  📄 steps/steps-05-07-review.md                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 5 ─ myharness.review.spec (claude-sonnet-4-6)   🔄 GATE         ║
║  │  Input:  spec.md + SRS + constitution                        ║
║  │  Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║  │  Report: 05-review-spec-report.md                            ║
║  │                                                               ║
║  │  ❌ REJECTED → myharness.specify fixes → re-review (max 5x)   ║
║  │  ✅/⚠️ → continue                                            ║
║  ▼                                                               ║
║  STEP 6 ─ myharness.plan (GPT-5.3-Codex)                         ║
║  │  Input:  spec.md + constitution + docs/technical_architecture.md     ║
║  │  Output: plan.md + data-model.md + contracts/ + research.md  ║
║  │  Report: 06-plan-report.md                                   ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] in plan artifacts   ║
║  ▼                                                               ║

║  STEP 7 ─ myharness.review.plan (claude-sonnet-4-6)   🔄 GATE         ║
║     Input:  plan.md + spec.md + data-model.md + tech arch       ║
║     Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║     Report: 07-review-plan-report.md                            ║
║                                                                  ║
║     ❌ REJECTED → myharness.plan fixes → re-review (max 5x)      ║
║     ✅/⚠️ → continue                                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 3: DETAIL DESIGN (Steps 8–9)                             ║
║  📄 steps/steps-08-09-detail.md                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 8 ─ myharness.dd (GPT-5.3-Codex)                               ║
║  │  Input:  BD + SRS + spec + plan + tech arch                  ║
║  │  Output: docs/output/design-docs/dd/dd-<MOD>-<name>.md              ║
║  │  Report: 08-dd-report.md                                     ║
║  │  🔧 Auto-Resolve: [NEEDS CLARIFICATION] in DD               ║
║  ▼                                                               ║
║  STEP 8b ─ myharness.testkit (claude-sonnet-4-6)                      ║
║  │  Mode:   gen-testcases                                       ║
║  │  Input:  SRS + BD + DD + spec + plan                         ║
║  │  Output: docs/output/design-docs/testcase/testcase-<MOD>-<name>.md  ║
║  │  Report: 08b-testcases-report.md                             ║
║  │  orchestrator validates: FEA/BR/SCR coverage ≥ 1 TC each            ║
║  ▼                                                               ║
║  STEP 9 ─ myharness.tasks (GPT-5.4)                              ║
║     Input:  plan.md + spec.md + data-model.md                   ║
║     Output: specs/<feature-id>/tasks.md                         ║
║     Report: 09-tasks-report.md                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 4: IMPLEMENTATION & QA (Steps 10–12)                     ║
║  📄 steps/steps-10-12-implement.md                               ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 10 ─ myharness.implement (GPT-5.3-Codex)        🔄 GATE   ║
║  │  Input:  tasks.md + plan.md + data-model.md + contracts/     ║
║  │  Output: src/modules/<module>/ (source code)                 ║
║  │  Phase 1: implement all tasks                                 ║
║  │  Phase 2: build & fix all errors                              ║
║  │  Report: 10-implement-report.md (incl. Screen Verification) ║
║  │  ⚡ REAL EXECUTION — npm build, docker up, npm start          ║
║  │                                                               ║
║  │  ❌ Build fails → auto-fix → re-build (max 5x)              ║
║  │  ✅ Build success + app starts → continue                    ║
║  ▼                                                               ║
║  STEP 11 ─ myharness.review.code (claude-sonnet-4-6)  🔄 GATE         ║
║  │  Input:  source code + spec + tasks + constitution           ║
║  │  Check:  code quality + DB data usage (no mock data)         ║
║  │  Verdict: ✅ APPROVED / ⚠️ CONDITIONS / ❌ REJECTED          ║
║  │  Report: 11-review-code-report.md                            ║
║  │                                                               ║
║  │  ❌ REJECTED → myharness.implement fixes → re-review (max 5x) ║
║  │  ✅/⚠️ → continue                                            ║
║  ▼                                                               ║
║  STEP 12 ─ myharness.testkit (claude-sonnet-4-6)     🔄 GATE         ║
║     Mode:   run-tests                                            ║
║     Input:  testcases + running app                              ║
║     Output: testreport-<MOD>-<name>.md                          ║
║     Report: 12-testkit-report.md                                 ║
║     ⚡ REAL EXECUTION — Jest + Playwright                      ║
║                                                                  ║
║     ❌ FAIL → 🔙 BACK-TO-PLAN (myharness.plan → ... → re-test)  ║
║     ✅ PASS → continue                                          ║
║     Max 3 BACK-TO-PLAN cycles → force continue with defects    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    │
    ▼
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 5: LAUNCH (Step 13)                                       ║
║  📄 steps/step-13-launch.md                                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 13 ─ orchestrator (direct: build + DB + launch)                  ║
║  │  Build BE + connect DB + build FE + start services           ║
║  │  Report: 13-launch-report.md (incl. Launch Status)           ║
║  │  ⚡ REAL EXECUTION — npm build, docker up, npm build+start   ║
║  │  open_browser_page → user sees working UI                    ║
║  ▼                                                               ║
║  ✅ PIPELINE COMPLETE                                            ║
║  │  Write final pipeline-completion report                      ║
║  │  Write [END] orchestrator log entry                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 3. Agent Roster

### 3.1 Generation Agents (artifact creation)

| Agent | Model | Steps | Role | Primary Output |
|-------|-------|-------|------|----------------|
| `myharness.srs` | GPT-5.4 | 1 | Requirements analysis → SRS | `srs-<MOD>-<name>.md` |
| `myharness.bd` | GPT-5.4 | 2 | External design (BD / External Design) | `bd-<MOD>-<name>.md` |
| `myharness.specify` | GPT-5.4 | 3 | Create feature spec | `spec.md` |
| `myharness.clarify` | GPT-5.4 | 4 | Detect & resolve ambiguities | `spec.md` (updated) |
| `myharness.plan` | GPT-5.3-Codex | 6 | Implementation planning | `plan.md`, `data-model.md`, `contracts/` |
| `myharness.dd` | GPT-5.3-Codex | 8 | Detailed design (DD / Internal Design) | `dd-<MOD>-<name>.md` |
| `myharness.tasks` | GPT-5.4 | 9 | Task decomposition | `tasks.md` |
| `myharness.implement` | GPT-5.3-Codex | 10,12,13 | Code implementation + build + launch | `src/modules/<mod>/` |

### 3.2 Review Agents (quality assurance)

| Agent | Model | Steps | Role | Gate |
|-------|-------|-------|------|------|
| `myharness.review.spec` | claude-sonnet-4-6 | 5 | Review spec vs SRS | 🔄 Auto-Retry (max 5) |
| `myharness.review.plan` | claude-sonnet-4-6 | 7 | Review plan vs spec | 🔄 Auto-Retry (max 5) |
| `myharness.review.code` | claude-sonnet-4-6 | 11 | Review code vs spec/constitution | 🔄 Auto-Retry (max 5) |

### 3.3 QA Agent (independent testing)

| Agent | Model | Steps | Mode | Role |
|-------|-------|-------|------|------|
| `myharness.testkit` | claude-sonnet-4-6 | 8b | `gen-testcases` | Generate test cases from SRS+BD+DD |
| `myharness.testkit` | claude-sonnet-4-6 | 12 | `run-tests` | Execute tests (Jest + Playwright) |

### 3.4 orchestrator Orchestrator

| Agent | Model | Steps | Role |
|-------|-------|-------|------|
| `myharness.orchestrator` | claude-sonnet-4-6 | ALL | Coordinate the entire pipeline, auto-resolve all issues |

### 3.5 Model Selection Rationale by Group

| Group | Agents | Main Task | Preferred Model | Technical Reason |
|-------|--------|-----------|-----------------|------------------|
| Requirements and specification synthesis | `myharness.srs`, `myharness.bd`, `myharness.specify` | Convert large upstream inputs into formal, internally consistent specification documents | `GPT-5.4` | `GPT-5.4` is a good fit because it handles long-context document synthesis well and keeps structure and terminology stable while writing. That makes it suitable for turning large upstream inputs into long-form specifications with consistent organization and wording. |
| Planning and implementation design | `myharness.plan`, `myharness.dd`, `myharness.implement` | Translate approved requirements into implementable technical design and executable code changes | `GPT-5.3-Codex` | `GPT-5.3-Codex` is a good fit because it is stronger at code-centric reasoning, including code-adjacent design, patch creation and editing, interface- and typing-aware implementation, and build/test-fix loops. That makes it suitable for translating requirements into implementable technical design and executable source changes. |
| Review and orchestration | `myharness.review.spec`, `myharness.review.plan`, `myharness.review.code`, `myharness.testkit`, `myharness.orchestrator` | Evaluate artifacts, control pipeline progression, and decide pass/fail or retry actions across steps | `claude-sonnet-4-6` | `claude-sonnet-4-6` is a good fit because it is stronger at review and critique, long-context comparison across artifacts, inconsistency and coverage-gap detection, and consistent decision-making. That makes it suitable for gate pass/fail decisions and multi-step pipeline orchestration. |

---

## 4. Communication Mechanisms (Context Exchange)

### 4.1 orchestrator → Sub-Agent: Structured $ARGUMENTS

```yaml
feature-id: 001-xxx
module-id: mod01
module-keyword: [KEYWORD]
pipeline-context: docs/output/run-logs/001-xxx/run-context.yaml
mode: autonomous
language: Vietnamese
```

### 4.2 Sub-Agent → orchestrator: Step Result Block

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
- Sub-agents read this file to discover outputs from prior steps → **no need to re-read large files**

---

## 5. Gate Mechanisms

### 5.1 Report Hard Gate ⛔
- Applies to: **EVERY step** (after completion)
- Requirement: Report file MUST exist with all required sections
- Protocol: `protocols/report-gate-protocol.md`

### 5.2 Review Gate 🔄
- Applies to: Steps 5, 7, 11 (review agents)
- Logic: REJECTED → fix agent corrects → re-review (maximum 5 times)
- Protocol: `protocols/gate-retry-protocol.md`

### 5.3 Build Gate 🔄
- Applies to: Step 10 (implementation + build & fix)
- Logic: Build fail → auto-fix → re-build (maximum 5 times)

### 5.4 Test Gate 🔙
- Applies to: Step 12 (test execution)
- Logic: Test FAIL → **BACK-TO-PLAN** (return to Step 6 → re-plan → re-implement → re-test)
- Maximum 3 BACK-TO-PLAN cycles → force continue

### 5.5 Auto-Resolve 🔧
- Applies to: When encountering `[NEEDS CLARIFICATION]` markers
- Logic: orchestrator automatically resolves using optimal assumption, logs to report
- Protocol: `protocols/auto-resolve-protocol.md`

---

## 6. File Structure

```
.github/agents/
├── myharness.orchestrator.agent.md          ← Orchestrator (~163 lines)
├── myharness.srs.agent.md                  ← Step 1
├── myharness.bd.agent.md                   ← Step 2
├── myharness.specify.agent.md          ← Step 3
├── myharness.clarify.agent.md          ← Step 4
├── myharness.review.spec.agent.md           ← Step 5
├── myharness.plan.agent.md             ← Step 6
├── myharness.review.plan.agent.md           ← Step 7
├── myharness.dd.agent.md                   ← Step 8
├── myharness.testkit.agent.md              ← Steps 8b, 12
├── myharness.tasks.agent.md            ← Step 9
├── myharness.implement.agent.md        ← Step 10
├── myharness.review.code.agent.md           ← Step 11
│
├── protocols/                        ← Protocols (read on-demand)
│   ├── auto-resolve-protocol.md
│   ├── gate-retry-protocol.md
│   ├── report-gate-protocol.md
│   ├── timestamp-protocol.md
│   ├── log-formats.md
│   ├── implement-delegation.md
│   ├── step-result-block.md
│   └── pipeline-context.md
│
├── steps/                            ← Step definitions (read on-demand)
│   ├── steps-01-04-design.md
│   ├── steps-05-07-review.md
│   ├── steps-08-09-detail.md
│   ├── steps-10-12-implement.md
│   └── step-13-launch.md
│
└── templates/                        ← Shared templates
    ├── report-templates.md           ← Universal report structure
    └── pipeline-completion.md        ← Pipeline completion template
```

---

## 7. Output Structure (Runtime)

```
docs/output/
├── design-docs/
│   ├── srs/srs-mod01-xxx.md        ← Step 1
│   ├── bd/bd-mod01-xxx.md           ← Step 2
│   ├── dd/dd-mod01-xxx.md           ← Step 8
│   ├── testcase/testcase-mod01-xxx.md  ← Step 8b
│   └── testreport/testreport-mod01-xxx.md  ← Step 12
│
└── output_logs/<feature-id>/
    ├── 00-myharness.log.md                           ← orchestrator log (all steps)
    ├── run-context.yaml                    ← Shared state
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
├── spec.md                                      ← Step 3
├── plan.md                                      ← Step 6
├── data-model.md                                ← Step 6
├── research.md                                  ← Step 6
├── tasks.md                                     ← Step 9
├── contracts/*.md                               ← Step 6
└── checklists/requirements.md                   ← Step 3
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
STEP 6  myharness.plan       ← re-plan with failure context
    │
    ▼
STEP 7  myharness.review.plan        ← re-review plan
    │
    ▼
STEP 8  myharness.dd              ← re-generate DD
    │
    ▼
STEP 9  myharness.tasks      ← re-generate tasks
    │
    ▼
STEP 10 myharness.implement  ← re-implement + build
    │
    ▼
STEP 11 myharness.review.code      ← re-review code
    │
    ▼
STEP 12 myharness.testkit         ← re-test
    │
    ├─ ✅ PASS → STEP 13 (fix & launch)
    └─ ❌ FAIL → repeat cycle (max 3 total)
              └─ After 3 cycles → force STEP 13 with known defects
```
