# ADR-0002: Prisma Portable Schema (SQLite Dev / PostgreSQL Prod)

**Date:** 2026-06-03
**Status:** Accepted

## Decision

Prisma schema MUST be portable between SQLite (local dev) and PostgreSQL (production). The following rules apply to every project using this stack:

1. **No `enum` blocks** in `schema.prisma` — use `String` with `@default("VALUE")`.
2. **No `@db.*` annotations** (`@db.VarChar()`, `@db.Text`, etc.) — these are provider-specific and break SQLite.
3. **Default `provider` = `sqlite`** in `schema.prisma` for local dev.
4. **`domain-enums.ts`** at `backend/src/common/types/domain-enums.ts` holds all enumeration values.
5. **Never import enum types from `@prisma/client`** — import from `domain-enums.ts` only.

## Rationale

Discovered via Post-Mortem P-09. SQLite does not support Prisma `enum` blocks or provider-specific annotations. Using them causes local dev migrations to fail, forcing developers to run a full PostgreSQL stack just to run `prisma migrate dev`. The portable pattern (String + domain-enums.ts) works identically on both providers and keeps local dev frictionless.

## Consequences

- Enum values validated at application layer (NestJS class-validator), not DB layer.
- All enum values documented in `domain-enums.ts` — single source of truth.
- `myharness.review.code` enforces this rule under Category 9 (Prisma Portable Schema).

## References

- Post-Mortem rule: `.harness/stacks/web-nestjs-react/kb/project/post-mortem-rules.md` § P-09
- Tech stack ADR: `ADR-0001-tech-stack.md`
