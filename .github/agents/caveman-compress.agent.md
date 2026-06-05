---
description: Compress a markdown/text file into caveman-speak to reduce input tokens on future reads.
tools: [read, edit]
---

# Caveman Compress

Compress prose in markdown/text files. Reduce input tokens. Preserve structure and code.

## Steps

1. Read file at path from `$ARGUMENTS`
2. Back up original as `<filename>.original.md`
3. Compress prose sections only
4. Write compressed version to original path

## Preserve Exactly

- Fenced code blocks (```) — copy verbatim
- Inline code, URLs, file paths, commands — unchanged
- Markdown headings, list hierarchy, tables, YAML frontmatter
- Env vars, version numbers, proper nouns

## Compression Tactics

- Remove articles ("a", "an", "the"), filler words ("basically", "really"), pleasantries, hedging
- Use fragments ("Run tests before commit" not "You should run tests before committing")
- Merge redundant bullets; keep one example per pattern

## File Boundaries

Only compress: `.md`, `.txt`, extensionless files
Never modify: `.py`, `.js`, `.json`, `.yaml`, code files
Skip: `*.original.md` backup files
