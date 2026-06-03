# Backend Generation Rules (NestJS + Prisma)

Module structure and seed data are defined in `docs/technical_architecture.md` — Section II (Repository Structure) and Section IV (Mock Data Seeding).

## Controller Rules

- **Location:** `backend/src/[module]/[module].controller.ts`
- **Thin controllers only:** receive request → trigger guard → validate DTO → call one service method.
- **Auth:** `@UseGuards(JwtAuthGuard)` and `@Roles()` on all protected routes.

## Service Rules

- **Location:** `backend/src/[module]/[module].service.ts`
- All business logic lives here — never in controllers.
- Use Prisma client for all DB operations — **no raw SQL**.
- Role filtering: ADMIN/MANAGER see all; EMPLOYEE sees only own objectives.
- Throw typed NestJS exceptions: `NotFoundException`, `ForbiddenException`.

## Prisma Rules

- `backend/prisma/schema.prisma` is the **single source of truth** for all tables.
- Migrations: `npx prisma migrate dev --name <name>` — never edit migration files manually.
- Use Prisma-generated types: `Prisma.ObjectiveCreateInput`, `Prisma.KeyResultUpdateInput`.

## Seed Rules

After any schema change, always update `backend/prisma/seed.ts`.

- Pattern: `upsert` keyed on stable identifiers (email for users, id for objectives/KRs).
- Running seed twice must produce no duplicates.
- Run: `docker-compose exec backend npx prisma db seed`

See `docs/technical_architecture.md` Section IV for the full seed template and data minimums.
