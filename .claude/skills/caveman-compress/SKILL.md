# Caveman Compress

Compress natural language files (CLAUDE.md, todos, memory files) into caveman-speak to reduce input tokens.

## Activation

Trigger: `/caveman-compress <filepath>` or "compress this memory file"

## Process

1. Read the target file
2. Compress prose sections only — preserve all code, URLs, structure
3. Back up original as `FILE.original.md`
4. Write compressed version to original path

## Critical Preservation Rules

- Code blocks (fenced ``` and indented) — copy EXACTLY, no modifications
- Inline code (`backticks`), URLs, file paths, commands, technical terms — unchanged
- All markdown headings, list hierarchies, tables, YAML frontmatter — kept
- Environment variables, version numbers, proper nouns — preserved

## Compression Tactics

- Remove articles, filler words ("basically", "really"), pleasantries, hedging
- Use fragments ("Run tests before commit" not full sentences)
- Merge redundant bullets; keep one example per pattern

## File Boundaries

Only compress: `.md`, `.txt`, extensionless files
Never modify: `.py`, `.js`, `.json`, `.yaml`, and other code files
Skip: `FILE.original.md` backups
