# Technical Architecture — [PROJECT_NAME] (Mobile)

**Version:** 1.0.0
**Platform:** React Native + Expo (iOS + Android)
**Target Team Size:** [TEAM_SIZE]
**Environment:** Local dev via Expo Go / dev build; CI via EAS Build

---

## I. Technology Stack

### 1. Mobile (React Native + Expo)

| Technology | Version | Role |
| --- | --- | --- |
| React Native | 0.74+ | Cross-platform UI framework |
| Expo SDK | 51+ | Managed workflow, native modules |
| TypeScript | 5.x | Type safety |
| Expo Router | 3.x | File-based navigation (pages in `app/`) |
| TanStack Query | 5.x | Server state, caching, background refetch |
| Zustand | 4.x | Lightweight client state (auth, UI prefs) |
| Axios | 1.x | HTTP client — all calls via `src/lib/api.ts` |
| NativeWind | 4.x | Tailwind CSS utility classes for RN |
| expo-secure-store | latest | Secure JWT storage (replaces localStorage) |
| react-native-mmkv | 2.x | Fast local key-value cache |

**Decisions:**
- **Expo managed workflow** over bare RN: eliminates native build config for team, EAS handles builds.
- **Expo Router** over React Navigation: file-based routing reduces boilerplate, deep-link support built-in.
- **TanStack Query** for all API data: consistent loading/error/refetch patterns; no manual fetch state.
- **Zustand** for auth token state only — server state lives in TanStack Query cache.
- **NativeWind** for styling: same Tailwind class vocabulary as web stack, lower context switch.
- **expo-secure-store** for tokens: iOS Keychain / Android Keystore backed, never plain AsyncStorage.

---

### 2. Backend API (pair with web-nestjs-react or web-nextjs-supabase)

Mobile app consumes a REST API. See paired stack profile for backend architecture.

Base URL configured in `src/lib/api.ts` via `API_BASE_URL` env var (set in `app.config.ts`).

---

### 3. Testing

| Tool | Scope | Location |
| --- | --- | --- |
| Jest + RNTL | Unit + component | `src/**/__tests__/` |
| Detox | E2E on simulator/device | `e2e/` |
| MSW | API mocking in tests | `src/mocks/` |

---

## II. Repository Structure

```
[project-root]/
├── app/                     ← Expo Router screens (file = route)
│   ├── (auth)/              ← Auth group (login, register)
│   ├── (tabs)/              ← Main tab navigation
│   └── _layout.tsx          ← Root layout + providers
├── src/
│   ├── components/          ← Reusable UI components
│   │   ├── ui/              ← Atoms (Button, Input, Badge)
│   │   └── [feature]/       ← Feature-specific composites
│   ├── hooks/               ← Custom hooks (useAuth, use[Feature])
│   ├── lib/
│   │   └── api.ts           ← Axios instance + interceptors
│   ├── store/               ← Zustand stores
│   ├── types/               ← Shared TypeScript types
│   └── schemas/             ← Zod validation schemas
├── e2e/                     ← Detox E2E tests
├── docs/
├── specs/
├── .harness/
└── app.config.ts            ← Expo config (env vars, plugins)
```

---

## III. Layer Order (enforced by layer_lint.py)

```
types → api → store → hooks → components → screens(app/)
```

- `types/` — no imports from other layers
- `api/` (lib/api.ts) — imports types only
- `store/` — imports types + api
- `hooks/` — imports types + api + store
- `components/` — imports types + hooks; no direct api/store imports
- `screens/` (`app/`) — imports all layers; orchestrates

---

## IV. Architecture Rules

### Navigation
- File-based routing via Expo Router — screen = file in `app/`
- Tab groups in `(tabs)/`, auth flow in `(auth)/`
- Deep links configured in `app.config.ts` `scheme` field

### API Communication
- All HTTP calls via `src/lib/api.ts` Axios instance
- Auth token injected via request interceptor
- Token refresh via response interceptor (401 → refresh → retry)
- Never call `fetch()` directly — use Axios instance only

### Authentication
- JWT access token (1h) + refresh token (7d)
- Stored in `expo-secure-store` — never in plain AsyncStorage
- Zustand `authStore` holds decoded user + token state
- On app start: read from SecureStore → validate → hydrate store

### State Management
- **Server state** (API data): TanStack Query — `useQuery` / `useMutation`
- **Auth + UI state**: Zustand stores in `src/store/`
- **Form state**: React Hook Form + Zod resolver
- No Redux, no Context API for data (only for theme/locale if needed)

### Styling
- NativeWind 4 + Tailwind config in `tailwind.config.js`
- Platform-specific overrides: `Platform.select()` or `.ios.tsx` / `.android.tsx` suffixes
- No inline `style={{}}` objects except for dynamic values (e.g., animated transforms)

### Testing Standards
- Coverage target: ≥ 75% on hooks and business logic
- Component tests with RNTL: test behavior, not implementation
- Mock API with MSW in unit tests — never mock fetch/axios directly
- Detox E2E covers critical user flows: login, main feature, logout

### Security
- No secrets in source code — use `app.config.ts` + EAS Secrets for builds
- Certificate pinning for production API calls (if required)
- Deep link validation to prevent link hijacking
- Biometric auth via `expo-local-authentication` for sensitive screens

---

## V. Quality Gates

| Gate | Tool | Threshold |
| --- | --- | --- |
| Type check | tsc --noEmit | 0 errors |
| Lint | ESLint + RN plugin | 0 violations |
| Unit + component | Jest + RNTL | ≥ 75% coverage |
| E2E | Detox | critical flows pass |
| Build | EAS Build | iOS + Android succeed |
