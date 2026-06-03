# GitHub Copilot Instructions — [PROJECT_NAME]

You are an expert developer for the **[PROJECT_NAME]** project.
Stack: [STACK_SUMMARY — e.g., NestJS + React + MySQL].

Read `docs/technical_architecture.md` before generating any code.

---

## Library Restriction

Use ONLY libraries in `docs/technical_architecture.md`. No new installs without approval.

---

## Coding Patterns

### [Backend Framework] Rules

- [Rule 1 — e.g., controllers only validate + delegate]
- [Rule 2 — e.g., services own all business logic]
- [Rule 3 — e.g., no raw SQL]

### [Frontend Framework] Rules

- [Rule 1 — e.g., pages in src/pages/, components in src/components/]
- [Rule 2 — e.g., all API calls via src/lib/api.ts]
- [Rule 3]

### Database / ORM Rules

- [Rule 1 — e.g., schema.prisma is single source of truth]
- [Rule 2 — e.g., use upsert for seed scripts]
- [Rule 3]

### Testing Rules

- [Rule 1 — e.g., test files co-located with source or in test/]
- [Rule 2 — coverage target]
- [Rule 3]

---

## File Structure Conventions

```
[Paste canonical file structure for this stack]
```

---

## Anti-patterns to Avoid

- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]
