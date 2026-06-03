# Test Execution Report — [Feature Name]

<!-- USAGE (run-tests mode, Phase C — pipeline summary report):
  1. Read the testcase file as source of truth for all TC-IDs and test content.
  2. Fill §1–§6 with actual execution results from Phase B.
  3. DO NOT rename, add prefixes, reorder, or change any TC-ID from the testcase file.
  4. No TC-ID may have Execution Result = "—" (all must be PASS, FAIL, or SKIP with reason).
  5. Write in Vietnamese. TC-IDs, file paths, and code remain in English.
-->

## §1 Test Execution Summary

| Category | Total | Passed | Failed | Skipped | Pass Rate |
|----------|-------|--------|--------|---------|-----------|
| Unit Tests (UT) | — | — | — | — | —% |
| API Tests (AT) | — | — | — | — | —% |
| UI/E2E Tests (E2E) | — | — | — | — | —% |
| Integration Tests (IT) | — | — | — | — | —% |
| **Total** | **—** | **—** | **—** | **—** | **—%** |

**Execution Date:** [YYYY-MM-DD HH:mm]
**Agent:** myharness.testkit (claude-sonnet-4-6)
**Feature ID:** [feature-id]
**Module ID:** [MOD-ID]

---

## §2 Coverage Results

| Module | Line Coverage | Branch Coverage | Threshold | Verdict |
|--------|---------------|-----------------|-----------|---------|
| backend/src/modules/[feature]/ | —% | —% | ≥ 80% | ✅/❌ |

---

## §3 Unit Test Results (UT)

<!-- Copy ALL UT rows from testcase-[MOD-ID]-[name].md. Fill Execution Result, Verdict, Notes only. -->

| TC-ID | Test Target | Test Content | Input | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|-------------|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|

---

## §4 API Test Results (AT)

<!-- Copy ALL AT rows from testcase file. Fill result columns only. -->

| TC-ID | Endpoint | Method | Test Content | Request | Expected Status | Expected Body | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|----------|--------|--------------|---------|-----------------|---------------|----------|--------------|------------------|---------|-------|

---

## §5 UI/E2E Test Results (E2E)

<!-- Copy ALL E2E rows from testcase file. Fill result columns only. -->

| TC-ID | Screen | URL | Test Content | Steps | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|--------|-----|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|

---

## §6 Integration Test Results (IT)

<!-- Copy ALL IT rows from testcase file. Fill result columns only. -->

| TC-ID | Test Target | Test Content | Precondition | Steps | Expected Result | Category | Design Basis | Execution Result | Verdict | Notes |
|-------|-------------|--------------|--------------|-------|-----------------|----------|--------------|------------------|---------|-------|

---

## §7 Screen Verification Results

| Screen ID | Screen Name | URL | HTTP Status | BD Items Present | Layout Match | Data Present | Overall |
|-----------|-------------|-----|-------------|------------------|--------------|--------------|---------|
| SCR-MOD-xx-01 | [name] | [/path] | — | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

---

## §8 Failed Test Analysis

<!-- List every failed TC with root cause and severity. Empty if no failures. -->

| TC-ID | Failure Reason | Root Cause | Severity | Design Reference |
|-------|---------------|------------|----------|-----------------|

---

## §9 Retry Log

| Retry # | TC-ID | Fix Applied | Re-run Result |
|---------|-------|-------------|---------------|

---

## §10 SRS/BD/DD Compliance Check

| Check | Result | Notes |
|-------|--------|-------|
| All FEA-xxx requirements covered by tests | ✅/❌ | |
| All BR-xxx rules have normal + abnormal + boundary TC | ✅/❌ | |
| All SCR-xxx screens have layout + functional E2E | ✅/❌ | |
| BD layout compliance (header, sidebar, nav colors) | ✅/❌ | |
| API responses contain real DB data (not mock/empty) | ✅/❌ | |
| Prisma seed provides test data | ✅/❌ | |

---

## §11 Overall Verdict

**Verdict:** ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL

**Pass Conditions:**
- [ ] All UT pass with coverage ≥ 80%
- [ ] All AT pass (including auth and validation error cases)
- [ ] All E2E screens accessible (HTTP 200) with BD items present
- [ ] All IT pass with real DB (no in-memory substitutes)
- [ ] No mock/hardcoded data detected in screen responses

**Next Step:**
- ✅ PASS → proceed to STEP 13 (Launch)
- ❌ FAIL → orchestrator triggers BACK-TO-PLAN (STEP 6 → re-plan → re-implement → re-test)
