# Test Case List — [Feature Name]

<!-- GENERATION RULES (read before filling):
  - One consolidated master table per section (UT, AT, E2E, IT).
  - DO NOT split into per-test-case sub-tables.
  - TC-IDs: UT-NNN, AT-NNN, E2E-NNN, IT-NNN (no "TC-" prefix).
  - Initialize Execution Result, Verdict, Notes to "—" (filled by run-tests mode).
  - Every FEA-xxx needs ≥1 TC. Every BR-xxx needs ≥1 normal + abnormal + boundary TC.
  - Every SCR-MOD-xx-nn needs ≥1 layout E2E + ≥1 functional E2E.
  - Every public DD method needs ≥1 UT. Every DD API endpoint needs ≥1 normal + auth + validation AT.
-->

## Basic Information

| Item | Content |
|------|---------|
| Feature | [Feature Name] |
| Module ID | [MOD-ID] |
| Feature ID | [feature-id] |
| Generated At | [YYYY-MM-DD] |
| Agent | myharness.testkit (claude-sonnet-4-6) |
| Output Path | docs/output/design-docs/testcase/testcase-[MOD-ID]-[short-name].md |

---

## §1 Unit Tests (UT)

> Source: DD class/method designs → executed with Jest

<!-- RULE: One row per test case. All columns required. Use "—" for empty cells. -->

| TC-ID | Test Target | Test Content | Input | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|-------------|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|
| UT-001 | [ClassName#methodName] | [Normal/Boundary/Abnormal case description] | [input values] | [expected output or exception] | Normal/Boundary/Abnormal | [DD §X.Y, BR-XXX] | — | — | — |

---

## §2 API Tests (AT)

> Source: DD internal API contracts + BD external interface → executed with Jest + Supertest

<!-- RULE: Every endpoint needs: 1 normal + 1 auth failure (401/403) + 1 validation error. -->

| TC-ID | Endpoint | Method | Test Content | Request | Expected Status | Expected Body | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|----------|--------|--------------|---------|-----------------|---------------|----------|--------------|------------------|---------|-------|
| AT-001 | [/api/v1/resource] | [GET/POST/...] | [Normal: list returns data] | [headers + body] | 200 | [response shape] | Normal | [DD §X, BD SCR-xx] | — | — | — |
| AT-002 | [/api/v1/resource] | [GET] | [Auth: no token → 401] | [no Authorization] | 401 | { error: UNAUTHORIZED } | Abnormal | [DD §X] | — | — | — |
| AT-003 | [/api/v1/resource] | [POST] | [Validation: missing required field] | [body without required] | 400 | { error: VALIDATION_ERROR } | Abnormal | [DD §X, BR-XXX] | — | — | — |

---

## §3 UI/E2E Tests (E2E)

> Source: BD screen designs + SRS user flows → executed with Playwright

<!-- RULE: Every SCR-MOD-xx-nn needs ≥1 layout verification + ≥1 functional flow test. -->

| TC-ID | Screen | URL | Test Content | Steps | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|--------|-----|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|
| E2E-001 | [SCR-MOD-xx-01] | [/path] | [Layout: all BD items present] | [1. Navigate to URL; 2. Assert elements visible] | [All BD-defined items rendered] | Layout | [BD SCR-xx-01] | — | — | — |
| E2E-002 | [SCR-MOD-xx-01] | [/path] | [Function: submit form succeeds] | [1. Fill form; 2. Click submit; 3. Assert success message] | [Success message shown, data saved] | Functional | [BD SCR-xx-01, FEA-xxx] | — | — | — |

---

## §4 Integration Tests (IT)

> Source: DD sequence diagrams + data flow → executed with Jest + testcontainers-node (real DB)

<!-- RULE: No in-memory DB. Use real PostgreSQL/MySQL via testcontainers-node. -->

| TC-ID | Test Target | Test Content | Precondition | Steps | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|-------------|--------------|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|
| IT-001 | [Service + DB] | [Create entity persists to DB] | [Empty DB] | [1. Call service.create(); 2. Query DB directly] | [Record exists in DB with correct fields] | Normal | [DD §X sequence, data-model] | — | — | — |

---

## §5 Test Coverage Targets

| Layer | Target | Tool |
|-------|--------|------|
| Backend services (UT) | ≥ 80% line coverage | Istanbul/c8 |
| API endpoints (AT) | 100% endpoints covered | Jest + Supertest |
| UI screens (E2E) | 100% SCR-xxx covered | Playwright |
| Integration flows (IT) | All DD sequences covered | testcontainers-node |

---

## §6 Traceability Matrix

<!-- Every FEA-xxx and BR-xxx from SRS must appear here with ≥1 TC. -->

| Requirement ID | Type | Description | Covered By | Coverage |
|----------------|------|-------------|------------|----------|
| FEA-001 | Functional | [requirement description] | UT-001, AT-001, E2E-001 | ✅ |
| BR-001 | Business Rule | [rule description] | UT-001, UT-002, UT-003 | ✅ |
| SCR-MOD-xx-01 | Screen | [screen name] | E2E-001, E2E-002 | ✅ |
