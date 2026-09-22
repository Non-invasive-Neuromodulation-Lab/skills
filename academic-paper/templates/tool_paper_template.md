# Tool Paper (Design & Evaluation) Template

## Usage
This template provides the skeleton for a paper whose primary subject is a BUILT tool/artifact (e.g., a clinical decision-support system). It is Pattern 7 — a section SCHEMA, not a fixed section list: E1–E8 are mandatory, S-sections are selected by the `tool_paper_variant` chosen at intake. See `references/paper_structure_patterns.md` Pattern 7 and `docs/tool-paper-route.md`.

**Variant rules**: S1 (Results — Quantitative) is REQUIRED for `tool_evaluation` and FORBIDDEN for `protocol_design`. S2 (Results — Qualitative) is REQUIRED for `usability_process` and FORBIDDEN for `protocol_design`. E5 MUST carry a status word: pilot / walkthrough / simulated / planned.

---

# [Tool Name — What It Is and What It Does, in One Line]

**Author(s):** [Author Name(s)]
**Affiliation:** [Institution]
**Date:** [Date]

---

## E1. Abstract

[150-250 words. MUST state the evaluation status word explicitly: "we report a pilot evaluation…" / "a usability walkthrough study…" / "simulated evaluation on N scenarios…" / "we present a protocol for…". Formatting must not upgrade this status.]

**Keywords:** [4-6 keywords]

---

## E2. Background & Motivation

[The problem the artifact addresses; why existing approaches fall short; the gap. Literature claims here are cited normally (APA/IEEE/Vancouver per configuration).]

---

## E3. Artifact Description

[What the artifact IS: architecture, components, rule/threshold inventory, interface, version/commit. Placement is flexible — standalone section (default), inside E4, or woven into E2 where the exemplar structure demands it. Numbers describing the artifact come from declared `tool_artifact_provenance[]` entries, never invented.]

---

## E4. Development / Design Methods

[How the artifact was built: requirements, design decisions, knowledge sources, iterations. For `usability_process` this is the process itself and its intermediate artifacts (task inventories, concept lists). For `protocol_design` this covers the planned study design.]

---

## E5. Evaluation / Design Status

**Status: [pilot / walkthrough / simulated / planned]**

[What was evaluated, how, by/with whom, on what data or scenarios. The status word above must match the declared evidence: pilot = data from real use; walkthrough = inspection/usability sessions; simulated = simulation scenarios only; planned = not yet executed.]

### S1. Results — Quantitative *(REQUIRED for `tool_evaluation`; optional for `usability_process`; FORBIDDEN for `protocol_design`)*

[Numbers from declared artifact content_units: screening times, hit/miss rates, adherence percentages, simulated-case verdict counts. Simulation results always carry simulated framing ("in simulated cases…").]

### S2. Results — Qualitative *(REQUIRED for `usability_process`; optional for `tool_evaluation`; FORBIDDEN for `protocol_design`)*

[Issue tables by UI region, walkthrough findings, prioritized problems, positive features, process-artifact counts.]

---

## E6. Discussion & Limitations

[MUST state the evaluation status and the untested scope: what this evaluation does and does not show; declared `negative_findings[]` and `known_limitations[]` surface here. Do not claim clinical safety, validity, or utility beyond the declared evidence.]

---

## E7. Conclusion

[What the artifact + its status-level evidence contribute; next evaluation step.]

---

## E8. References

[Citation-format per configuration; artifact evidence needs no citation — it is declared in the Material Passport.]

---

## Optional Sections (include only when used)

### S3. Recommendations *(optional)*
[Numbered, actionable recommendations — e.g., UI changes from usability findings.]

### S4. Implementation Details *(optional)*
[Repository links, version pins, deployment notes.]

### S5. Ethics / IRB *(optional)*
[Approval or exemption statement; for human-participant evaluation.]

### S6. Appendices *(optional)*
[Task lists, walkthrough question sets, full issue tables, timing logs, scenario definitions.]

### S7. Related Work *(optional; standalone)*
[Only when the related-work survey is a standalone section rather than part of E2.]
