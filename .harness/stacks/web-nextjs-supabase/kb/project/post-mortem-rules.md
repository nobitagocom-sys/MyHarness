# Post-Mortem Rules — web-nextjs-supabase

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

## P-10: Error Boundaries
Wrap router root in `<AppErrorBoundary>`.

## P-11: Axios Interceptor
Configure base URL and auth token refresh in a single `api.ts` client file.
