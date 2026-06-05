---
description: "Compress large SRS and BD artifacts into lightweight summary files for downstream pipeline steps. Reduces token load on Steps 2-7 by ~60% without losing spec fidelity."
model: claude-haiku-4-5-20251001
tools: [Read, Write]
---

## Purpose

Create compressed summary versions of SRS and BD files after Step 1b completes.
Downstream agents (Steps 2–7) read the summary files instead of the full originals.
Full originals are preserved unchanged — summaries are additive, never destructive.

## User Input

```text
$ARGUMENTS
```

Required fields from orchestrator:

```yaml
feature-id: <feature-id>
module-id: <mod-id>
srs-full-path: docs/output/design-docs/srs/srs-<mod-id>-<keyword>.md
bd-full-path: docs/output/design-docs/bd/bd-<mod-id>-<keyword>.md   # optional — may not exist yet
output-dir: docs/output/design-docs/summaries/
pipeline-context: docs/output/run-logs/<feature-id>/run-context.yaml
```

## Step 1 — Compress SRS

Read `srs-full-path`. Extract and write `<output-dir>/srs-<mod-id>-summary.md` with this structure:

```markdown
# SRS Summary — <module-name>
> Auto-generated summary. Full SRS: <srs-full-path>
> Generated: <ISO-timestamp>

## Module Overview
<2-3 sentence summary of what this module does>

## Functional Requirements

| FR-ID | Title | Priority | Acceptance Criteria (condensed) |
|-------|-------|----------|----------------------------------|
| FR-001 | <title> | Must | <1 sentence AC> |
| FR-002 | <title> | Must | <1 sentence AC> |
...

## Business Rules
| BR-ID | Rule (1 sentence) |
|-------|-------------------|
| BR-001 | <rule> |
...

## Non-Functional Requirements (key only)
- Performance: <key target>
- Security: <key requirement>
- Availability: <key target>

## Entity List
<comma-separated list of domain entities, e.g.: Order, OrderLine, TradeFlow, Supplier>

## Integration Points
<comma-separated list, e.g.: D365 BC, JWT Auth, CSV Export>
```

**Compression rules:**
- FR descriptions: keep title + 1-sentence acceptance criteria only — drop full description paragraphs
- Business rules: 1 sentence per rule — drop rationale/examples
- NFRs: keep numeric targets only — drop explanation prose
- Remove all ASCII wireframes from SRS (those belong in BD only)
- Remove duplicate information already in the overview section
- Target: ≤ 30% of original line count

## Step 2 — Compress BD (if bd-full-path exists)

Read `bd-full-path`. Extract and write `<output-dir>/bd-<mod-id>-summary.md` with this structure:

```markdown
# BD Summary — <module-name>
> Auto-generated summary. Full BD: <bd-full-path>
> Generated: <ISO-timestamp>

## Screen Inventory

| Screen-ID | Screen Name | Route | Primary Actions |
|-----------|-------------|-------|-----------------|
| SCR-mod01-01 | <name> | /<route> | <action1>, <action2> |
...

## Navigation Flow
<compact description: which screens link to which, max 5 lines>

## Layout Pattern
<1-2 sentences: e.g., "Left sidebar navigation with 256px width. Header fixed at 64px. Content area uses card grid layout.">

## Component Inventory (unique components only)
<comma-separated list of reusable components, e.g.: OrderTable, StatusBadge, DateRangePicker>

## API Endpoints Referenced
| Method | Path | Screen |
|--------|------|--------|
| GET | /api/orders | SCR-mod01-01 |
...
```

**Compression rules:**
- Remove all full ASCII wireframe blocks — keep only the screen inventory table
- Remove color spec details beyond the primary brand color
- Remove responsive breakpoint details
- Remove copy/label text samples
- Target: ≤ 25% of original line count

## Step 3 — Output STEP-RESULT

Write the step result block and report the output paths so the orchestrator can update `run-context.yaml`.

Report file: `docs/output/run-logs/<feature-id>/reports/01c-compress-report.md`

```markdown
# STEP 1c: Artifact Compression Report

**Feature**: <feature-id>
**Timestamp**: <ISO>

## Summary
| Artifact | Original Lines | Summary Lines | Reduction |
|----------|---------------|---------------|-----------|
| SRS | <N> | <N> | <X>% |
| BD | <N> | <N> | <X>% |

## Output Paths
- SRS summary: docs/output/design-docs/summaries/srs-<mod-id>-summary.md
- BD summary: docs/output/design-docs/summaries/bd-<mod-id>-summary.md

## Verdict: COMPLETE
```

## Step Result Block — MANDATORY

```yaml
<!-- STEP-RESULT
step: 1c
agent: myharness.compress
status: SUCCESS | FAILED
feature-id: <feature-id>
module-id: <mod-id>
artifacts:
  srs-summary: docs/output/design-docs/summaries/srs-<mod-id>-summary.md
  bd-summary: docs/output/design-docs/summaries/bd-<mod-id>-summary.md
  report: docs/output/run-logs/<feature-id>/reports/01c-compress-report.md
metrics:
  srs-reduction-pct: <N>
  bd-reduction-pct: <N>
next-inputs: {}
/STEP-RESULT -->
```
