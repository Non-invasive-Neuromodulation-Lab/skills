# Examples

## Example 1

Input list:
1. Smith, J. (2020). Signal processing in TMS-EEG. Journal of Neural Methods. https://doi.org/10.1016/j.jneumeth.2020.108900
2. Doe A, 2019, Brain stimulation review, NeuroReport, doi:10.1000/xyz123
3. Brown et al. Neural markers and outcomes.

Expected findings:
- Entry 3 missing explicit year.
- Entry 3 likely incomplete structure.
- Entry 2 DOI format warning if malformed tokenization is detected.
- In strict + doi-web-check mode, each DOI gets resolved or flagged as unresolved/unavailable.

## Example 2

Input list:
- Lee, T. (2021). Cortical metrics. Frontiers in Human Neuroscience. https://example.com/article
- Lee, T. (2021). Cortical metrics. Frontiers in Human Neuroscience. https://example.com/article

Expected findings:
- Duplicate entry detected.
- No structural error if fields are complete.

## Example 3

Command:
python .github/skills/reference-list-validity-checker/scripts/check_references.py --file refs.md --mode strict --doi-web-check

Expected findings:
- Style consistency info if year token format is mixed.
- DOI status summary with resolved and unresolved counts.
