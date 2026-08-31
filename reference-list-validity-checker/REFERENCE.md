# Reference Rules

## What is checked

1. Reference list section detection
- Looks for headings such as References, Bibliography, Works Cited.

2. Entry extraction
- Supports numbered entries and bullet-like entries.
- Ignores empty lines and obvious heading lines.

3. Core validity checks
- Has a plausible publication year (1900-2099)
- Has author-like text before year
- Has post-year title-like segment

4. DOI and URL checks
- DOI must match pattern 10.<registrant>/<suffix>
- URL must start with http:// or https://
- Optional DOI web check resolves each DOI via https://doi.org/<doi>

5. Duplicate checks
- Normalized duplicate detection based on lowercase alphanumeric reduction.

## Modes

- basic: entry extraction, year, author-like, title-like, duplicates.
- standard: basic plus DOI and URL validity.
- strict: standard plus simple style consistency checks:
  - at least 70 percent of entries share the same leading pattern (numbered or non-numbered)
  - year placement consistency
  - year token formatting consistency (for example (2020) vs 2020)
  - sentence-ending punctuation consistency
  - optional DOI web resolution check

## Known limitations

- This checker validates structural quality, not factual bibliographic truth.
- DOI web checks only test resolvability, not citation correctness.
- It cannot guarantee style-guide-perfect punctuation.
