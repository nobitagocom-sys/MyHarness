# GitHub Copilot Instructions — MyHarness Project

You are an expert developer working within the **MyHarness AI-SDLC pipeline**.
Your primary goal is to generate code that is secure, traceable to design documents,
and strictly follows this project's architecture.

> **Stack-specific rules** are in `docs/technical_architecture.md`.
> Read that file before generating any code.

---

## 1. Supreme Rule: Architecture First

Before generating any code:
1. Read `docs/technical_architecture.md` — stack, module structure, layer order
2. Read `docs/input/change-request/cr-input.md` — current requirement scope
3. Read `.specify/memory/constitution.md` — project principles

Do NOT invent features. Every piece of code must trace to a design document.

---

## 2. Library Restriction

⚠️ **ZERO TOLERANCE — do not install new libraries without approval.**

- Use ONLY libraries declared in `docs/technical_architecture.md` and `package.json`
- If a new library is critically needed: stop, ask user, justify, wait for approval

---

## 3. Code Generation Rules

### General
- All business logic in service layer — never in controllers or repositories
- Controllers: validate input → call service → return response only
- No hardcoded secrets — use environment variables or config service
- No mock/static data bypassing the persistence layer in production code
- Error handling: use framework-native exceptions, not bare try/catch everywhere

### Testing
- Write tests before implementation (TDD — red/green/refactor)
- Unit tests for all service methods
- Integration tests for all controller endpoints
- Coverage target: ≥ 80% on business logic

### Database
- All DB operations through the declared ORM — no raw SQL in application code
- Schema is single source of truth — never modify DB directly
- Seed scripts must be idempotent (upsert pattern)
- No in-memory substitutes for entities defined in the data model

---

## 4. Scope Guard

Do NOT write code outside the current feature's declared write scope.
Check `specs/<feature-id>/tasks.md` for the `write:` list of each task.

If a task requires files outside the write scope:
- Stop and flag it
- Do not silently create out-of-scope files

---

## 5. Post-Mortem Rules

Read `.harness/kb/project/post-mortem-rules.md` before writing source code.
Violations are caught by `myharness.review.code` and cause REJECTED verdict.

---

## 6. Stack-Specific Rules

See `.harness/stacks/` for the reference profile matching this project's stack.
The active stack profile is copied to:
- `docs/technical_architecture.md` — architecture decisions and constraints
- This file's Section 7 below — coding patterns specific to this stack

---

## 7. Project-Specific Coding Patterns

> **This section is populated from the active stack profile.**
> Copy patterns from `.harness/stacks/<stack-name>/copilot-instructions.md` § Coding Patterns
> when onboarding this project.

[Stack-specific patterns go here — e.g., NestJS module conventions, React component rules, etc.]
