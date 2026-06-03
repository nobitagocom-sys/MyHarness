# GitHub Copilot Instructions — [PROJECT_NAME]

Stack: **Next.js 14 App Router + Supabase + TypeScript**.
Read `docs/technical_architecture.md` before generating any code.

---

## Library Restriction

Use ONLY libraries in `docs/technical_architecture.md`. No new installs without approval.

---

## App Router Rules

- Pages/layouts live in `app/` — file = route
- Server Components by default — add `'use client'` only when needed (event handlers, hooks, browser APIs)
- Never `'use client'` on a page that only needs server data — fetch in RSC directly

```tsx
// ✅ CORRECT — server component fetches data directly
async function ObjectivesPage() {
  const supabase = createServerClient();
  const { data } = await supabase.from('objectives').select('*');
  return <ObjectiveList items={data} />;
}

// ❌ WRONG — unnecessary client component for static data
'use client';
function ObjectivesPage() {
  const [data, setData] = useState([]);
  useEffect(() => { supabase.from('objectives').select('*').then(...) }, []);
}
```

---

## Server Action Rules

- All mutations via Server Actions in `lib/actions/[domain].ts`
- Mark file with `'use server'` at top
- Always call `revalidatePath()` or `revalidateTag()` after mutation
- Return typed result `{ data, error }` — never throw to client

```ts
// ✅ CORRECT
'use server';
export async function createObjective(input: ObjectiveInput) {
  const supabase = createServerClient();
  const { data, error } = await supabase.from('objectives').insert(input).select().single();
  if (error) return { data: null, error: error.message };
  revalidatePath('/dashboard');
  return { data, error: null };
}
```

---

## Supabase Client Rules

- Server components / Server Actions: `createServerClient()` from `lib/supabase/server.ts`
- Client components: `createBrowserClient()` from `lib/supabase/client.ts` — use singleton pattern
- Never import server client in `'use client'` components — causes build error
- Use generated types: `import type { Database } from '@/types/supabase'`

```ts
// ✅ CORRECT — typed query
const { data } = await supabase
  .from('objectives')
  .select('id, title, user_id')
  .returns<Database['public']['Tables']['objectives']['Row'][]>();
```

---

## RLS Rules

- Every new table MUST have RLS enabled in migration
- Every policy MUST use `auth.uid()` for user-scoped data
- Test RLS boundaries in E2E: logged-out user gets 0 rows, other user's data blocked

```sql
-- ✅ REQUIRED for every table
ALTER TABLE [table] ENABLE ROW LEVEL SECURITY;
CREATE POLICY "[table]_user_policy" ON [table]
  FOR ALL USING (auth.uid() = user_id);
```

---

## Component Rules

- `components/ui/` — atoms only, no Supabase/business logic
- `components/[feature]/` — may use TanStack Query hooks for realtime data
- Server Components pass data as props to Client Components — no prop drilling through multiple layers
- No `useEffect` for data fetching in client components — use TanStack Query or RSC

---

## Styling Rules

- Tailwind CSS only — no CSS modules, no styled-components
- `cn()` utility for conditional classes (clsx + tailwind-merge)
- Dark mode via `class` strategy if needed — not `media`

---

## Anti-patterns

- No `'use client'` on pages that only display server-fetched data
- No direct `fetch()` to Supabase REST API — use supabase-js client
- No Supabase server client in `'use client'` components
- No tables without RLS enabled
- No mutations in GET routes or server components — use Server Actions
- No hardcoded Supabase URLs/keys in source — use `NEXT_PUBLIC_SUPABASE_URL` env vars
