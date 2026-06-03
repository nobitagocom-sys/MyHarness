# Active Skills Registry

Place `.yaml` skill definition files here to register them with the harness.

Each file defines one active skill that agents may reference.
The `cross_ref_validator` health check verifies workflow steps reference only skills listed here.

## Format

```yaml
id: myharness.implement
description: "Implementation agent — write source code"
tier: coding
model_alias: gpt_codex
```

## Empty registry

When this directory contains no `.yaml` files, `cross_ref_validator` skips skill reference
validation for workflows — no false positives are generated.
