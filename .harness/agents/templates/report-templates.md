# Phase Report Templates

Sub-agents SHOULD reference these templates instead of embedding full report structures inline.
Read the appropriate template file BEFORE writing your phase report.

## Universal Report Structure

Every phase report MUST include these sections (in English):

```markdown
# STEP <NN>: <Report Title>

## Summary
- **Target Feature:** <feature name>
- **Created At:** <yyyy-MM-dd HH:mm:ss>
- **Agent:** <agent-name> (<model>)
- **Result:** ✅ Success / ❌ Failure

## Input
- <list input files>

## Output
| # | File | Path |
|---|---------|------|
| 1 | <file> | <path> |

## Key Decisions
- <list important decisions>

## Quality Assessment
| Category | Result |
|---------|------|
| <category> | ✅ / ❌ |

## Metrics
| Metric | Value |
|-----------|-----|
| <metric> | <N> |

## [AUTO-RESOLVED] Assumptions
| # | ID | Original Question | Automatic Answer | Rationale | Confidence |
|---|----|---------|---------|------|--------|

> If none apply: "No auto-resolved items."

## [NEEDS CLARIFICATION] Items
| # | ID | Description | Impact | Related |
|---|----|------|--------|------|

> If there are no unresolved items: "No unresolved items — all requirements are clear."

## Issues & Retries
> If there were no issues or retries: "No issues or retries."

## Next Step
- Next phase: `<agent>` (STEP N+1) — <purpose>
- Input: `<path>`
```

## Step-Specific Titles & Extra Sections

| NN | Report Title | Agent | Extra Sections |
|----|-------------|-------|----------------|
| 01 | SRS Generation Report | myharness.srs | — |
| 02 | BD Generation Report | myharness.bd | — |
| 03 | Specification Creation Report | myharness.specify | — |
| 04 | Specification Clarification Report | myharness.clarify | `## QA Summary` (full question + answer table) |
| 05 | Specification Review Report | myharness.review.spec | `## CRITICAL Issues` |
| 06 | Implementation Plan Report | myharness.plan | — |
| 07 | Plan Review Report | myharness.review.plan | `## CRITICAL Issues` |
| 08 | DD Generation Report | myharness.dd | — |
| 08b | Test Case Generation Report | myharness.testkit | — |
| 09 | Task Generation Report | myharness.tasks | — |
| 10 | Implementation and Build Verification Report | myharness.implement | `## Test Results`, `## Screen Verification` |
| 11 | Code Review Report | myharness.review.code | `## CRITICAL Issues`, `## Architecture Assessment` |
| 12 | Test Execution Report | myharness.testkit | `## Test Execution Summary`, `## Failed Test Details`, `## Coverage`, `## Overall Verdict` |
| 13 | Launch Report | orchestrator (direct) | `## Launch Status` |

## Review Agent Verdict Sections (Steps 5, 7, 11)

Review agents add:

```markdown
## Review Results
| Category | Result | CRITICAL | MINOR |
|---------|------|----------|-------|

## CRITICAL Issues
| # | Issue | Impact | Recommended Action |
|---|------|------|----------|

> If there are no critical issues: "No CRITICAL issues."
```

## Generation Agent Quality Sections (Steps 1, 2, 3, 6, 8, 9)

Generation agents include step-specific metrics in the `## Metrics` table. Examples:

- **SRS:** FEA count, TBC count, requirement count
- **BD:** screen count, logical table count, external interface count
- **Spec:** user story count, functional requirement count, screen count
- **Plan:** entity count, contract count, implementation phase count
- **DD:** physical table count, API count, batch job count
- **Tasks:** task count, phase count, dependency link count

---

## Claims & Evidence (MyHarness addition)

Every implementation report MUST include this section.
Review agents MUST reject reports missing evidence for business rule claims.

```yaml
claims:
  - id: CLAIM-001
    text: "<what was implemented>"
    evidence:
      - file: <path/to/file.ts>
        symbol: <functionName>
      - file: <path/to/test.ts>
        test: "<test description>"
```

Rule: No evidence = claim not accepted → review agent returns REJECTED.
