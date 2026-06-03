# Harness Workflows

Place `.yaml` workflow definition files here to define automated multi-step workflows.

The `cross_ref_validator` health check validates that every `skill:` reference in a workflow
step exists in `.harness/registry/active/`.

## Format

```yaml
id: example-workflow
description: "Example automated workflow"
steps:
  - id: step-1
    skill: myharness.srs
    input: docs/input/change-request/cr-input.md
  - id: step-2
    skill: myharness.bd
    depends_on: [step-1]
```

## Empty directory

When this directory contains no `.yaml` files, workflow validation is skipped — no errors.
