# Frontend Generation Rules (React + Vite)

File locations and folder structure are defined in `docs/technical_architecture.md` — Section II (Repository Structure).

## Layout Rules

- Use semantic HTML only: `<div>`, `<nav>`, `<aside>`, `<main>`, `<section>`.
- **Never** import any external UI/layout library.

```tsx
// ✅ CORRECT
<div className="flex justify-between items-center mb-6">
  <h1 className="text-xl font-semibold text-gray-800">My OKRs</h1>
  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700">
    + New OKR
  </button>
</div>
```

## Data Fetching (TanStack Query)

Query keys — must be descriptive and include filter params:

```typescript
['objectives', { quarter: 'Q2/2026', ownerId }]
['objective', id]
['key-results', objectiveId]
```

Mutations — always invalidate relevant queries `onSuccess`:

```typescript
const updateProgress = useMutation({
  mutationFn: (data: UpdateProgressDto) => api.updateKRProgress(krId, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['objective', objectiveId] });
    queryClient.invalidateQueries({ queryKey: ['objectives'] });
  },
});
```

## API Call Rules

- All network requests must be functions in `frontend/src/lib/api.ts`.
- Components call `api.*` functions — **never** call Axios directly in components.
- Base URL: `import.meta.env.VITE_API_BASE_URL` (e.g., `http://localhost:3000/api/v1`).
- Auth tokens are in HttpOnly cookies — do **not** manually attach `Authorization` headers.

## Forms (React Hook Form + Zod)

```typescript
// frontend/src/schemas/objective.schema.ts
import { z } from 'zod';

export const createObjectiveSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
  ownerId: z.number().int().positive('Owner is required'),
  quarter: z.string().regex(/^Q[1-4]\/\d{4}$/, 'Format must be Q2/2026'),
});

export type CreateObjectiveFormData = z.infer<typeof createObjectiveSchema>;

const { register, handleSubmit, formState: { errors } } = useForm<CreateObjectiveFormData>({
  resolver: zodResolver(createObjectiveSchema),
});
```
