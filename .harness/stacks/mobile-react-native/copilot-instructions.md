# GitHub Copilot Instructions — [PROJECT_NAME] (Mobile)

Stack: **React Native + Expo + TypeScript**.
Read `docs/technical_architecture.md` before generating any code.

---

## Library Restriction

Use ONLY libraries in `docs/technical_architecture.md`. No new installs without approval.
Expo managed workflow — any native module addition requires `expo install`, not `npm install`.

---

## Screen & Navigation Rules

- Screens live in `app/` (Expo Router file-based) — one file = one route
- Never use `navigation.navigate()` in render body — use `<Redirect>` or `router.push()` in event handlers
- Auth guard via root `_layout.tsx` — check Zustand `authStore.isAuthenticated`
- Tab navigation in `app/(tabs)/` — each tab is a `_layout.tsx` + screen files

```tsx
// ✅ CORRECT — redirect in effect or layout
if (!isAuthenticated) return <Redirect href="/login" />;

// ❌ WRONG — navigate during render
if (!isAuthenticated) navigation.navigate('Login');
```

---

## Component Rules

- Atoms (`src/components/ui/`): Button, Input, Badge — no business logic
- Feature composites (`src/components/[feature]/`): use hooks, no direct API calls
- No `useQuery` / `useMutation` in components — extract to custom hooks in `src/hooks/`
- Styling: NativeWind classes only — no `StyleSheet.create({})` except animated values

```tsx
// ✅ CORRECT
<View className="flex-1 bg-gray-50 px-4">
  <Text className="text-lg font-semibold text-gray-800">{title}</Text>
</View>

// ❌ WRONG — inline style object
<View style={{ flex: 1, backgroundColor: '#f9fafb', padding: 16 }}>
```

---

## Hook Rules

- `useAuth()` — reads Zustand authStore, exposes `user`, `login()`, `logout()`
- `use[Feature]()` — wraps TanStack Query for a domain (e.g., `useObjectives()`)
- Hooks NEVER import from `components/` — unidirectional dependency

```ts
// ✅ CORRECT — hook owns query
export function useObjectives() {
  return useQuery({ queryKey: ['objectives'], queryFn: api.getObjectives });
}

// ❌ WRONG — component calls API directly
const { data } = useQuery({ queryFn: () => axios.get('/objectives') });
```

---

## API & Auth Rules

- All HTTP via `src/lib/api.ts` Axios instance — never `fetch()` directly
- Token stored in `expo-secure-store` — never `AsyncStorage`
- Interceptor handles 401 → refresh → retry automatically
- API base URL from `process.env.EXPO_PUBLIC_API_URL` (set in `app.config.ts`)

```ts
// src/lib/api.ts pattern
const api = axios.create({ baseURL: process.env.EXPO_PUBLIC_API_URL });
api.interceptors.request.use(config => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

---

## State Rules

- Server data → TanStack Query (never `useState` for API results)
- Auth + UI prefs → Zustand store
- Form data → React Hook Form + Zod

```ts
// ✅ CORRECT — server state via TQ
const { data: objectives } = useObjectives();

// ❌ WRONG — useState for server data
const [objectives, setObjectives] = useState([]);
useEffect(() => { axios.get('/objectives').then(r => setObjectives(r.data)); }, []);
```

---

## Testing Rules

- Use React Native Testing Library — test user behavior, not implementation
- Mock API calls with MSW (`src/mocks/handlers.ts`) — never mock axios/fetch directly
- Detox E2E: write for critical flows only (login → main screen → core action → logout)

---

## Anti-patterns

- No `StyleSheet.create` for static styles — use NativeWind classes
- No `AsyncStorage` for tokens — use `expo-secure-store`
- No direct `axios.get()` in components — use hooks
- No `useEffect` + `setState` for server data — use TanStack Query
- No screen logic in `_layout.tsx` — layout only, business logic in screens/hooks
