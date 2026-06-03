# Technical Architecture — [PROJECT_NAME]

**Version:** 1.0.0
**Purpose:** [What this document defines]
**Target Team Size:** [N] developers
**Environment:** [localhost-first / cloud / hybrid]

---

## I. Technology Stack

### 1. Frontend / Client

| Technology | Version | Role |
| --- | --- | --- |
| [Framework] | [x.x] | [Role] |
| [Build tool] | [x.x] | [Role] |
| [State management] | [x.x] | [Role] |
| [HTTP client] | [x.x] | [Role] |
| [Styling] | [x.x] | [Role] |

**Decisions:**
- [Why this framework over alternatives]
- [Key constraints or trade-offs]

---

### 2. Backend / API

| Technology | Version | Role |
| --- | --- | --- |
| [Runtime] | [x.x] | [Role] |
| [Framework] | [x.x] | [Role] |
| [ORM / DB driver] | [x.x] | [Role] |
| [Auth library] | [x.x] | [Role] |

**Decisions:**
- [Why this framework]
- [Auth strategy and rationale]
- [Config / env strategy]

---

### 3. Database

| Technology | Version | Role |
| --- | --- | --- |
| [DB engine] | [x.x] | Primary store |
| [Migration tool] | [x.x] | Schema management |

**Decisions:**
- [DB choice rationale]
- [Migration strategy]
- [Index strategy]

---

### 4. Infrastructure & Dev Environment

| Component | Tool | Notes |
| --- | --- | --- |
| Container | Docker + Compose | [local dev setup] |
| CI | [GitHub Actions / etc.] | [pipeline description] |
| Secrets | [.env / config service] | [strategy] |

---

## II. Repository Structure

```
[project-root]/
├── [backend_dir]/
│   ├── src/
│   │   ├── [module-a]/
│   │   └── [module-b]/
│   ├── test/
│   └── [config files]
├── [frontend_dir]/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── [other dirs]
│   └── [config files]
├── [e2e_dir]/
├── docs/
├── specs/
├── .harness/
└── .specify/
```

---

## III. Module Structure

[Describe how the codebase is organized into modules/domains]

### Module List

| Module | Path | Responsibility |
| --- | --- | --- |
| [module-a] | [path] | [what it owns] |
| [module-b] | [path] | [what it owns] |

---

## IV. Layer Order (enforced by layer_lint.py)

```
[layer-1] → [layer-2] → [layer-3] → [layer-4]
```

Import rules:
- `[layer-N]` may import from `[layer-N-1]` and below
- `[layer-1]` (lowest) must NOT import from any other layer
- Violations are blocked by pre-commit hook

---

## V. Architecture Rules

### API Design
- [REST / GraphQL / gRPC] — [constraints]
- [Versioning strategy]
- [Error response format]

### Data Access
- [ORM usage rules]
- [No raw SQL policy]
- [Pagination standard]

### Authentication & Authorization
- [Auth method]
- [Token strategy]
- [Guard application rules]

### Testing Standards
- Coverage target: ≥ 80% on business logic
- [Unit test location and naming]
- [Integration test tooling]
- [E2E test tooling]

### Security
- [Input validation approach]
- [Injection prevention]
- [Credential handling]

---

## VI. Quality Gates

| Gate | Tool | Threshold |
| --- | --- | --- |
| Lint | [tool] | 0 violations |
| Type check | [tool] | 0 errors |
| Unit tests | [tool] | ≥ 80% coverage |
| Integration tests | [tool] | all pass |
| Security scan | [tool] | no critical |
