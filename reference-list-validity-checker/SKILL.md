---
name: reference-list-validity-checker
description: Validate a document reference list for structural quality, strict style consistency, duplicates, and real-time DOI reachability. Use when user asks to verify bibliography validity, run strict journal-style reference checks, or validate DOI and URL integrity.
---

# Reference List Validity Checker

## Quick start

1. Ask for the target document path and style expectation (APA, IEEE, Vancouver, custom).
2. Run the checker script for a deterministic baseline report.
3. Return:
- Overall status (pass, warning, fail)
- Per-entry findings
- Suggested fixes

## Workflow

### 1. Collect context

- Target file path.
- Required style requirement for strict runs (APA, IEEE, Vancouver, or custom).
- Optional strictness level:
  - basic: core structure and duplicates
  - standard: structure plus DOI or URL syntax checks
  - strict: standard plus journal-style consistency and DOI web checks

### 2. Run deterministic checks

Run:
python .github/skills/reference-list-validity-checker/scripts/check_references.py --file <path> --mode <basic|standard|strict> [--doi-web-check]

For strict journal-style review, include:
--mode strict --doi-web-check

### 3. Interpret results

Classify findings:
- Error: missing critical metadata or malformed reference structure.
- Warning: likely incomplete or inconsistent formatting.
- Info: optional improvements.

### 4. Produce final response

Always include:
- Summary counts (entries, errors, warnings, duplicates, DOI resolved/unresolved)
- Top 5 highest-impact fixes
- Corrected examples for the worst entries

## Output contract

- Keep recommendations actionable and entry-specific.
- Do not invent missing metadata.
- If a field cannot be inferred, mark as "needs source verification".
- If DOI web checks fail due to network issues, mark as "verification unavailable" instead of invalid.

## Advanced notes

See [REFERENCE.md](REFERENCE.md) and [EXAMPLES.md](EXAMPLES.md).
