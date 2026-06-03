# Post-Mortem Rules — MyHarness

Rules earned from real project runs. myharness.implement and myharness.review.code MUST read this.

## P-06: React Router Future Flags
When using React Router DOM v6, ALWAYS add future flags:
```tsx
<BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
```

## P-07: No navigate() During Render
NEVER call `navigate()` during render body. For conditional redirects use:
```tsx
if (isAuthenticated) return <Navigate to="/dashboard" replace />;
```

## P-08: ADMIN Role Query Logic
List/dashboard endpoints MUST handle ADMIN role seeing ALL records:
```ts
const where = user.role === 'ADMIN' ? {} : { ownerId: user.id };
```

## P-09: Prisma Portable Schema
- Do NOT use `enum` blocks in schema.prisma — use `String` with `@default("VALUE")`
- Do NOT use `@db.VarChar()`, `@db.Text`, or any provider-specific annotations
- Default provider MUST be `sqlite` for local dev portability
- Create `backend/src/common/types/domain-enums.ts` for all enumerations
- Import enum types from `domain-enums.ts`, NEVER from `@prisma/client`

## P-10: Error Boundaries
Wrap router root in `<AppErrorBoundary>`.

## P-11: Axios Interceptor
Configure base URL and auth token refresh in a single `api.ts` client file.
