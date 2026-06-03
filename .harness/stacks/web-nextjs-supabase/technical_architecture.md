# Technical Architecture — [PROJECT_NAME]

**Version:** 1.0.0
**Stack:** Next.js 14 App Router + Supabase
**Target Team Size:** [TEAM_SIZE]
**Environment:** Vercel (production) / localhost (dev via Supabase local)

---

## I. Technology Stack

### 1. Frontend + API (Next.js 14)

| Technology | Version | Role |
| --- | --- | --- |
| Next.js | 14.x | Full-stack framework (RSC + App Router) |
| TypeScript | 5.x | Type safety |
| TanStack Query | 5.x | Client-side server state cache |
| Tailwind CSS | 3.x | Utility-first styling |
| Zod | 3.x | Schema validation (shared server + client) |
| React Hook Form | 7.x | Form state |

**Decisions:**
- **App Router + RSC** over Pages Router: data fetching in server components eliminates client waterfall.
- **Server Actions** for mutations: type-safe form submissions without manual API route boilerplate.
- **TanStack Query** for client-side data that needs refetch/optimistic update (e.g., realtime feeds).
- RSC data → no TanStack Query needed (direct async/await in component).

---

### 2. Backend (Supabase)

| Service | Role |
| --- | --- |
| Supabase Postgres | Primary relational database |
| Supabase Auth | Authentication (email/password, OAuth, magic link) |
| Supabase Realtime | Live data subscriptions |
| Supabase Storage | File uploads |
| Supabase Edge Functions | Custom serverless logic (Deno runtime) |

**Decisions:**
- **Supabase Auth** over custom JWT: handles token refresh, session cookies, OAuth providers out of box.
- **Row Level Security (RLS)** for authorization: policies enforced at DB level, not just API layer.
- **supabase-js client** in RSC via `createServerClient()` from `@supabase/ssr`.
- **Supabase CLI** for local dev: `supabase start` spins up local Postgres + Auth + Studio.

---

### 3. Database (Supabase Postgres)

| Component | Tool | Notes |
| --- | --- | --- |
| Migrations | Supabase CLI | `supabase/migrations/` — versioned SQL |
| Types | `supabase gen types` | Auto-generated from schema |
| RLS Policies | SQL in migrations | Enforced per table per role |
| Seed | `supabase/seed.sql` | Idempotent INSERT ON CONFLICT |

---

## II. Repository Structure

```
[project-root]/
├── app/                          ← Next.js App Router
│   ├── (auth)/                   ← Auth pages (login, register)
│   ├── (dashboard)/              ← Protected pages
│   ├── api/                      ← API Routes (if needed beyond Server Actions)
│   └── layout.tsx                ← Root layout + providers
├── components/
│   ├── ui/                       ← Atoms (Button, Input, Badge)
│   └── [feature]/                ← Feature composites
├── lib/
│   ├── supabase/
│   │   ├── client.ts             ← Browser client (createBrowserClient)
│   │   └── server.ts             ← Server client (createServerClient)
│   ├── actions/                  ← Server Actions per domain
│   └── schemas/                  ← Zod schemas (shared)
├── supabase/
│   ├── migrations/               ← SQL migration files
│   └── seed.sql                  ← Dev seed data
├── e2e/                          ← Playwright tests
├── docs/
└── specs/
```

---

## III. Layer Order

```
types → lib/schemas → lib/supabase → lib/actions → components → app/
```

- `app/` (pages/layouts) may import all layers
- `components/` must NOT import from `app/` or `lib/actions/`
- `lib/actions/` (Server Actions) must NOT import from `components/`
- `lib/supabase/` — no business logic, only client creation

---

## IV. Architecture Rules

### Data Fetching Strategy
- **RSC (Server Component)**: `await supabaseServer.from('table').select()` — no loading state needed
- **Client mutations**: Server Actions via `useTransition` + `action` prop or `startTransition`
- **Realtime / optimistic**: TanStack Query + Supabase Realtime subscription

### Authentication
- Supabase Auth session via cookies (`@supabase/ssr`)
- Server: `createServerClient()` with `cookies()` from `next/headers`
- Client: `createBrowserClient()` — singleton in `lib/supabase/client.ts`
- Protected routes via `middleware.ts` — redirect to `/login` if no session
- RLS policies enforce per-user data access at DB level

### Server Actions
```ts
// lib/actions/[domain].ts
'use server';
import { createServerClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';

export async function createItem(data: ItemInput) {
  const supabase = createServerClient();
  const { error } = await supabase.from('items').insert(data);
  if (error) throw new Error(error.message);
  revalidatePath('/dashboard');
}
```

### RLS Policy Pattern
```sql
-- Every table MUST have RLS enabled
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Users see only their own rows
CREATE POLICY "users_own_items" ON items
  FOR ALL USING (auth.uid() = user_id);
```

### Testing Standards
- Coverage target: ≥ 80% on Server Actions and utility functions
- Vitest for unit tests — mock Supabase client
- Playwright E2E covers: auth flow + primary CRUD + RLS boundary test

---

## V. Quality Gates

| Gate | Tool | Threshold |
| --- | --- | --- |
| Type check | tsc --noEmit | 0 errors |
| Lint | ESLint + Next.js plugin | 0 violations |
| Unit tests | Vitest | ≥ 80% on lib/actions |
| E2E | Playwright | critical flows pass |
| RLS check | Custom SQL test | policies present on all tables |
