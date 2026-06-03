# Technical Architecture — [PROJECT_NAME]

**Version:** [VERSION]
**Purpose:** Defines the system technical architecture, stack decisions, and constraints.
**Target Team Size:** [TEAM_SIZE]
**Environment:** [ENVIRONMENT]

> **Instructions:** Replace all [PLACEHOLDER] content with actual project information.
> Copy from `.harness/stacks/<stack-name>/technical_architecture.md` as a baseline.

---

## I. Technology Stack

### Active Stack Profile

Stack profile this project is using: `.harness/stacks/[STACK_NAME]/`

> Copy the full stack profile content here when onboarding a new project.

| Layer | Technology | Version | Role |
| --- | --- | --- | --- |
| [Frontend] | [Framework] | [Version] | [Role] |
| [Backend] | [Framework] | [Version] | [Role] |
| [Database] | [DB] | [Version] | [Role] |
| [Auth] | [Method] | — | [Role] |
| [Testing] | [Tools] | [Version] | [Role] |

---

## II. Repository Structure

```
[PROJECT_ROOT]/
├── [backend_dir]/      ← Backend source
├── [frontend_dir]/     ← Frontend source
├── [e2e_dir]/          ← End-to-end tests
├── docs/               ← Input, architecture, output
├── specs/              ← Spec Kit artifacts per feature
├── .harness/           ← MyHarness control plane
└── .specify/           ← Spec Kit config
```

---

## III. Module Structure

[Describe module/domain organization here]

---

## IV. Layer Order

[Declare the enforced layer order for layer_lint.py]

Example: `types → config → repo → service → runtime`

---

## V. Key Architectural Decisions

[Document ADRs inline or reference `.harness/kb/decisions/`]

---

## VI. Infrastructure & Deployment

[Docker, CI/CD, environment config]

---

## VII. Quality Standards

- Test coverage: ≥ [N]%
- Linting: zero violations
- Security: OWASP Top 10 compliance
