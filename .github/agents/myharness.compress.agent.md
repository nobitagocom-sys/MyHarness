---
description: "Compress large SRS and BD artifacts into lightweight summary files for downstream pipeline steps. Reduces token load on Steps 2-7 by ~60% without losing spec fidelity."
model: claude-haiku-4-5-20251001
tools: [read, edit]
argument-hint: "feature-id=<id> module-id=<mod-id> srs-full-path=<path> bd-full-path=<path>"
---

## Purpose

Create compressed summary versions of SRS and BD files after Step 1b completes.
Downstream agents (Steps 2–7) read the summary files instead of the full originals.
Full originals are preserved unchanged — summaries are additive, never destructive.

## User Input

```text
$ARGUMENTS
```

> **Copilot — Argument Resolution:** If you see the literal text `$ARGUMENTS` (not substituted with real content), treat the **entire preceding user message** as the argument value. Do NOT ask the user to repeat their input — extract the intent directly from what they typed.

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
...

## Business Rules
| BR-ID | Rule (1 sentence) |
|-------|-------------------|
| BR-001 | <rule> |
...

## Non-Functional Requirements (key only)
- Performance: <key target>
- Security: <key requirement>

## Entity List
<comma-separated list of domain entities>

## Integration Points
<comma-separated list>
```

**Compression rules:**
- FR descriptions: keep title + 1-sentence acceptance criteria only
- Business rules: 1 sentence per rule — drop rationale/examples
- NFRs: keep numeric targets only — drop explanation prose
- Remove all ASCII wireframes from SRS
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
<compact description, max 5 lines>

## Layout Pattern
<1-2 sentences>

## Component Inventory
<comma-separated list>

## API Endpoints Referenced
| Method | Path | Screen |
|--------|------|--------|
| GET | /api/orders | SCR-mod01-01 |
...
```

**Compression rules:**
- Remove all full ASCII wireframe blocks — keep screen inventory table only
- Remove color spec details beyond primary brand color
- Target: ≤ 25% of original line count

## Step 3 — Output STEP-RESULT

Report file: `docs/output/run-logs/<feature-id>/reports/01c-compress-report.md`

Include compression stats table and output paths.

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
