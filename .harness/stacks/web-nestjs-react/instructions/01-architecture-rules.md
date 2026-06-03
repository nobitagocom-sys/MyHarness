# Architecture Rules

**Before generating any code, you must understand the project's structure.**

- **Architecture:** Refer to `docs/technical_architecture.md` for system design, module responsibilities, and technology stack.
- **Requirements:** Refer to `docs/input/change-request/cr-input.md` for functional requirements, use cases, and UI mockups.
- **Your role:** Translate designs into code — not to be creative or invent logic.

## Module Placement

| ✅ CORRECT | ❌ INCORRECT |
|---|---|
| Key result progress logic → `key-results` module | Key result logic inside `objectives` service |
| DB access → Prisma client only | Raw SQL in application code |
| Business logic → service layer | Business logic in controller |

## Library Restriction — Zero Tolerance

- **FORBIDDEN:** Installing ANY new library beyond those in `package.json`
- **MANDATORY:** Use ONLY libraries listed in `docs/technical_architecture.md`
- **EXCEPTION PROCESS:** If a new library is absolutely critical:
  1. Stop all code generation
  2. Ask explicit permission from user
  3. Justify purpose and why existing libraries cannot fulfil the requirement
  4. Wait for approval before proceeding

## TypeScript

- Use types and interfaces from the design documents.
- Do not create new types unless explicitly required by the design.
