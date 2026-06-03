# TypeScript Type Safety Rules

Type safety is mandatory. Always verify types after generating code.

Domain types (`Objective`, `KeyResult`, `User`) and API response envelope are defined in `docs/technical_architecture.md` — Section VI (API Design). Use those as the source of truth, do not redefine them.

## Forbidden Patterns

```typescript
// ❌ Never use 'any'
const data: any = response.data;

// ❌ Never leave props untyped
function Component(props) { ... }

// ❌ Never call Axios directly in components
const response = await axios.get('/api/v1/objectives');
```

## Required Patterns

```typescript
// ✅ Typed component props
interface OKRCardProps {
  objective: Objective;
  onEdit?: (id: number) => void;
}

// ✅ Backend DTO matching frontend interface
export class CreateObjectiveDto {
  @IsString() @IsNotEmpty() title: string;
  @IsString() @IsOptional() description?: string;
  @IsInt() @IsPositive() ownerId: number;
  @IsString() @Matches(/^Q[1-4]\/\d{4}$/) quarter: string;
}
```

## Consistency Rules

- **Frontend ↔ Backend:** DTOs in backend must have matching interfaces in `frontend/src/types/`.
- **Enums:** `Role` (`ADMIN | MANAGER | EMPLOYEE`) and `Status` (`NOT_STARTED | IN_PROGRESS | COMPLETED`) must be identical in both layers.
- **Zod Schemas:** `frontend/src/schemas/` must align with backend `class-validator` rules on the corresponding DTO.

## Pre-Submit Checklist

- [ ] No `any` types
- [ ] All component props properly typed
- [ ] API calls have typed parameters and responses
- [ ] DTOs consistent between frontend and backend
- [ ] Role/Status enum values identical across codebase
- [ ] Zod schemas align with backend `class-validator` rules
