# GitHub Copilot Instructions — Web Application (NestJS + React)

You are an expert full-stack developer. Your role is to translate design documents into code — not to be creative. Every piece of code must be traceable to a specification.

Read the relevant instruction files before generating code:

| # | File | When to read |
|---|------|-------------|
| 1 | [Architecture Rules](../../docs/instructions/01-architecture-rules.md) | Always — read first |
| 2 | [Technology Stack](../../docs/instructions/02-tech-stack.md) | When choosing libraries or versions |
| 3 | [Design Style](../../docs/instructions/03-design-style.md) | When writing any frontend UI |
| 4 | [Backend Rules](../../docs/instructions/04-backend-rules.md) | When generating NestJS / Prisma code |
| 5 | [Frontend Rules](../../docs/instructions/05-frontend-rules.md) | When generating React / Vite code |
| 6 | [TypeScript Rules](../../docs/instructions/06-typescript-rules.md) | After generating any code — verify types |


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

## Caveman Agents (Token Reduction)

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `@caveman` | `@caveman [lite/full/ultra/wenyan]` | Compressed responses (~75% fewer output tokens) |
| `@caveman-commit` | `@caveman-commit` | Conventional commit message ≤50 chars |
| `@caveman-review` | `@caveman-review` | One-line-per-issue code review |
| `@caveman-compress` | `@caveman-compress <file>` | Compress markdown/memory files |

Deactivate caveman mode: "stop caveman" or "normal mode".
