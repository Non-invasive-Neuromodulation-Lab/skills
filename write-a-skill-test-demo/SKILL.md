---
name: write-a-skill-test-demo
description: Build concise release notes from changelog text with clear sections and action items. Use when user asks to summarize release history, changelog entries, or version updates.
---

# Release Notes Summarizer Demo

## Quick start

1. Collect source text from changelog entries, commit summaries, or issue notes.
2. Group updates by type: Added, Changed, Fixed, Deprecated, Removed, Security.
3. Produce one short summary and one actionable list.

## Workflows

### 1. Summarize one version

- Input: one version block.
- Output:
  - Version heading
  - 3-6 bullet summary
  - Risk notes
  - Follow-up actions

### 2. Summarize multiple versions

- Input: multiple version blocks.
- Output:
  - Timeline in reverse chronological order
  - Top cross-version themes
  - Migration notes (if needed)

### 3. Convert technical notes for non-technical audience

- Replace implementation details with user impact.
- Keep exact version numbers and dates.
- Keep compatibility warnings explicit.

## Output format

- Title: product and version range
- Summary: short paragraph
- Highlights: grouped bullet list by change type
- Risks: explicit list or "None reported"
- Action items: numbered list

## Advanced features

See [REFERENCE.md](REFERENCE.md) and [EXAMPLES.md](EXAMPLES.md).
