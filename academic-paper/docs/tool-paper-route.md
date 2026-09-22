# Tool Paper (Design & Evaluation) Route

Usage guide for the 7th paper type (v3.4.0, Pattern 7). For papers whose **primary subject is a built tool/artifact** — e.g., a clinical decision-support system — covering design description, pilot/usability/simulation evaluation, development-process studies, and evaluation protocols. This is a **family of structures, not one template**: the route adapts via `tool_paper_variant`. A tool paper is **not a systematic review and not a clinical trial** — the route enforces neither PRISMA expectations nor primary-endpoint/randomization demands.

## Invocation

- **Trigger words** (in the skill description and intake): "tool paper", "design and evaluation paper", "CDSS paper", "usability paper", "protocol paper" — or select **Tool Paper (Design & Evaluation)** in intake Step 2.
- Example: *"Write a tool paper about my NINM Safety screening app — we ran a pilot with 12 participants and have timing logs."*
- Intake then asks the **variant** (`tool_paper_variant`) and, at Step 8, the **artifact inventory** (below). The Paper Configuration Record gains two conditional rows (Tool Paper Variant, Artifact Declaration) — omitted entirely for non-tool papers.

## Sub-routes (`tool_paper_variant`)

| Variant | When it applies | Required sections | Forbidden |
|---------|----------------|-------------------|-----------|
| `tool_evaluation` | An evaluation exists (pilot, simulation, deployed use) | E1–E8 + **S1** | — |
| `usability_process` | Usability / engineering-process evaluation (walkthroughs, issue logs); no clinical outcomes demanded | E1–E8 + **S2** | — |
| `protocol_design` | A PROTOCOL for planned evaluation only | E1–E8 (+X1 protocol block) | **S1, S2 — results-reporting FAILs the gate** |

E1–E8 mandatory core: title/abstract, background, artifact description, development/design methods, evaluation-or-design status (status word mandatory: pilot / walkthrough / simulated / planned), discussion/limitations, conclusion, references. Extensions X1–X5 (protocol block, process-artifact inventory, verdict taxonomy, pilot timing table, per-UI-region issue tables) are documented patterns, not schema changes.

## What the scholar supplies manually

ARS never invents artifact data. Each item becomes one `tool_artifact_provenance[]` entry (Material Passport) with `content_units[]` — the concrete quantities/metrics claims may rest on:

| Scholar supplies | `artifact_kind` |
|------------------|-----------------|
| App/source code, repository | `code_repository` |
| Architecture diagrams | `architecture_diagram` |
| Rule/threshold inventories, knowledge bases | `rule_inventory` / `knowledge_base` |
| Screenshots, interface mockups | `screenshot` / `interface_mockup` |
| Timing/performance logs | `timing_log` / `performance_log` |
| Pilot data, usability session data | `usability_data` |
| Simulation scenarios, simulation outputs | `simulation_scenario` / `simulation_output` |
| Protocol documents | `protocol_document` |
| Intermediate development artifacts (task inventories, concept lists) | `process_artifact` |
| Ethics/IRB approval | declared for **S5 Ethics/IRB** prose (not itself passport evidence) |

## Evidence model (mirrors #260 experiment provenance)

1. **`tool_artifact_intake_declaration`** — passport-level, scholar-set: `{status: artifacts_declared | no_artifacts_declared | legacy_unknown, declared_at, declared_by: scholar}`.
2. **`tool_artifact_provenance[]`** — one entry per artifact (`shared/contracts/passport/tool_artifact_provenance_entry.schema.json`): `artifact_id` (frozen at intake), `artifact_kind`, `locator`, `produced_by`, `content_units[]`, `negative_findings[]`, `known_limitations[]` (keys required; `[]` allowed).
3. **Claim join** — `claim_intent_manifest.claims[].planned_artifact_ids[]`; `intended_evidence_kind: artifact` (new enum value). Mixed literature+artifact claims allowed; audited on both paths, worst-verdict-wins.
4. **`artifact_alignment_results[]`** — produced by the integrity agent **at the gate** (`shared/contracts/passport/artifact_alignment_result.schema.json`): verdicts `ALIGNED / OVERSTATED / NOT_SUPPORTED_BY_PROVENANCE / PROVENANCE_INSUFFICIENT`, rule_version AA-v1.

## Integrity gate (Phase C5, route-conditional)

Active only when paper_type is Tool Paper **or** any artifact field is present — non-tool runs are byte-identical to pre-v3.4.0. FAIL conditions: missing declaration on the route; `artifacts_declared` with empty provenance; `no_artifacts_declared` with artifact claims/provenance; manuscript reporting artifact-derived results with neither refs nor `planned_artifact_ids`; malformed entries (absent `negative_findings`/`known_limitations` keys); dangling `planned_artifact_ids` (structural FAIL); `protocol_design` reporting collected results; simulation results without simulated framing (floors at OVERSTATED). D4-c uncited-assertion exemption extends to artifact-backed sentences (`planned_artifact_ids[]`), exactly as #260 exempts experiment-backed ones. **Outside the audit boundary:** artifact quality/utility, clinical safety, regulatory validity, trial power, clinical advice.

## Worked example — Exemplar A (Sun & Chan 2015, *BMC Med Inform Decis Mak* 2015;15:105)

A CDSS for a specific clinical screening task, evaluated in a pilot crossover study. Verified top-level structure maps to the schema as:

| Exemplar A section | Schema slot |
|--------------------|-------------|
| Abstract | E1 (status word: **pilot**) |
| Background | E2 (literature-cited claims — normal citation path) |
| Methods — tool design | E3 + E4 (artifact described inside Methods; placement flexible) |
| Methods — pilot crossover evaluation | E4 + E5 (**status: pilot**) |
| Results — screening time | S1 (required: `tool_evaluation` variant) — backed by `timing_log` artifact |
| Results — missed items | S1 — backed by `usability_data` artifact |
| Discussion | E6 (states pilot status + untested scope) |
| Conclusions | E7 |
| References | E8 |

Sample claim manifest rows:

```yaml
claims:
  - claim_id: C-001
    claim_text: "Prior CDSS evaluations in this domain report workflow disruption."
    intended_evidence_kind: normative          # literature-backed → planned_refs
    planned_refs: ["sun2015-related", "chan2014"]
  - claim_id: C-002
    claim_text: "Mean screening time with the tool was 92 s (pilot, n=12, crossover)."
    intended_evidence_kind: artifact           # pilot timing — artifact-backed
    planned_refs: []                           # required key — empty: no literature refs on an artifact-only claim
    planned_artifact_ids: ["pilot-timing-logs"]
  - claim_id: C-003
    claim_text: "The tool missed 3 items the control workflow caught."
    intended_evidence_kind: artifact
    planned_refs: []                           # required key — empty: no literature refs on an artifact-only claim
    planned_artifact_ids: ["pilot-missed-items"]
```

`pilot-timing-logs` (`artifact_kind: timing_log`) carries a `content_unit {unit_id: mean-time, metric: "mean screening time (s)", value: 92}`; C-002's gate verdict is judged against exactly that unit (`unit_pointer: pilot-timing-logs/mean-time`).

## Worked example — Exemplar B (Tremoulet 2022, *Digit Health* 2022;8:20552076221113696, PMC9364207) — `usability_process`

A usability evaluation of a clinical information tool by expert cognitive walkthrough — no clinical outcomes involved. Verified top-level structure maps to the schema as:

| Exemplar B section | Schema slot |
|--------------------|-------------|
| Abstract (Objective/Method/Results/Conclusion) | E1 (status word: **walkthrough**) |
| Introduction (tool context; tool description woven in) | E2 + E3 (placement flexible — woven into Introduction, per the exemplar) |
| Methods — Evaluators; Setting; cognitive-walkthrough Procedure | E4 + E5 (**status: walkthrough** — the evaluation process IS the subject) |
| Methods — task-list appendix + walkthrough question table | S6 Appendices (task inventory declared as a `process_artifact`) |
| Results — findings organized by 5 UI regions; positive features; prioritized issue tables | S2 (REQUIRED for `usability_process`) + X5 per-UI-region issue tables |
| Recommendations (numbered list) | S3 |
| Discussion and conclusions | E6 (states walkthrough status + untested scope, e.g. no end-user participants) + E7 |
| References | E8 |

Sample claim manifest rows (synthetic numbers, illustrative slugs; every row schema-valid — `planned_refs` present on every claim):

```yaml
claims:
  - claim_id: C-001
    claim_text: "Cognitive walkthroughs expose learnability and consistency problems in interface evaluation."
    intended_evidence_kind: definitional        # method literature → normal citation path
    planned_refs: ["wharton1994-cognitive-walkthrough"]
  - claim_id: C-002
    claim_text: "The walkthroughs identified 12 usability issues across the five interface regions."
    intended_evidence_kind: artifact
    planned_refs: []                           # required key — empty: no literature refs on an artifact-only claim
    planned_artifact_ids: ["usability-walkthrough-notes"]
  - claim_id: C-003
    claim_text: "Four issues were rated high-severity and prioritized for redesign."
    intended_evidence_kind: artifact
    planned_refs: []
    planned_artifact_ids: ["usability-walkthrough-notes"]
  - claim_id: C-004
    claim_text: "Evaluators completed all 10 tasks in the walkthrough task inventory."
    intended_evidence_kind: artifact
    planned_refs: []
    planned_artifact_ids: ["cw-task-list"]     # process_artifact — intermediate-artifact counts are auditable claims
```

Two declared artifacts back these claims: `usability-walkthrough-notes` (`artifact_kind: usability_data`, `content_units`: per-region issues 3/4/2/1/2, total 12, high-severity 4; `negative_findings: ["no severe safety-critical issues identified"]`; `known_limitations: ["3 expert evaluators only; no end-user participants"]`) and `cw-task-list` (`artifact_kind: process_artifact`, `content_units`: task-count 10). Variant discipline: S2 REQUIRED, S1 optional and absent here; **no clinical-outcome claim anywhere** — the peer_reviewer adjustment explicitly forbids demanding outcomes or primary-endpoint evidence on `usability_process`; `slr_lineage` stays false (no PRISMA on a tool paper's background). At Phase C5, C-002..C-004 are judged against their declared units (aggregation across declared units is recorded in the row `rationale`); D4-c exempts them from uncited-assertion flagging because their manifest rows carry `planned_artifact_ids`.

## Worked example — Exemplar E (Lopez-Jimenez et al. 2025, *Am Heart J* — ACT-HF trial design) — `protocol_design`

A study protocol for a planned evaluation whose intervention is a software artifact — **results-reporting is forbidden on this variant**. Verified top-level structure maps to the schema as:

| Exemplar E section | Schema slot |
|--------------------|-------------|
| Background | E2 |
| Overview of trial design | E4 + X1 `trial_overview` |
| Study population | X1 `population` |
| Study intervention (the software) | E3 Artifact Description (the artifact is the intervention) |
| Study data collection | X1 `data_collection` |
| Endpoints | X1 `endpoints` |
| Discussion | E6 (status: **planned**; untested scope = everything — no data collected yet) |
| — (E5 status word: planned; abstract states protocol; E7/E8 as usual) | E1, E5, E7, E8 |

Sample claim manifest rows (synthetic numbers, illustrative slugs; all quantities PLANNED, future-tense framing — mirrors the `planned_vs_executed` `executed:false` discipline):

```yaml
claims:
  - claim_id: C-001
    claim_text: "Remote monitoring programmes in heart failure reduce readmission burden in selected populations."
    intended_evidence_kind: empirical
    planned_refs: ["ref-hf-remote-monitoring-meta"]
  - claim_id: C-002
    claim_text: "Standardised endpoint definitions improve cross-trial comparability."
    intended_evidence_kind: normative
    planned_refs: ["ref-endpoint-definitions"]
  - claim_id: C-003
    claim_text: "The study will randomise 520 participants across 2 arms with 2 co-primary endpoints."
    intended_evidence_kind: artifact
    planned_refs: []                           # required key — empty: no literature refs on an artifact-only claim
    planned_artifact_ids: ["study-protocol-doc"]
```

One declared artifact backs C-003: `study-protocol-doc` (`artifact_kind: protocol_document`, `content_units`: planned-sample-size 520, planned-arms 2, planned-co-primary 2; `known_limitations: ["no data collected yet; all endpoints are planned, none executed"]`). Variant rules (the negative path, deliberately explicit): **S1 and S2 are FORBIDDEN** — a Results/S-data sentence reporting COLLECTED data (e.g., an interim-analysis sentence with percentages and p-values) is a Phase C5 check-5 **FAIL that blocks the gate**, independent of provenance quality; it is also a forbidden-section violation the structure level rejects and the peer_reviewer adjustment rates Critical, and — if the sentence is in no manifest — an unexempt uncited assertion plus claim drift. Planned-evaluation prose only; the formatter must not upgrade the "planned" status word.

## Model tiering (#517)

No new agents; no manifest change. Route-relevant assignments per `shared/model_tiering.md`: **execution-type** — `intake` (variant + artifact intake), `draft_writer`, `citation_compliance`, `abstract_agent`, `formatter` (stamp-only), `field_analyst` (card generation); **judgment-type** — `structure_architect` (E/S schema selection), `socratic_mentor`, `peer_reviewer`, `literature_strategist`, `integrity_verification` (Phase C5 verdicts), and the reviewer panel's checkpoint surfaces (EIC + R1–R3 + Devil's Advocate + editorial synthesizer).

## Status and limits

This route is **uncalibrated** — no benchmark or calibration claims are made. Upstream CI scripts (`check_claim_audit_consistency.py`, `model_tiering_manifest.json`) are not present in every checkout; AP-INV-1..4 / AA-INV-1..2 invariants are specified for upstream lint adoption and verified locally by inspection and dry-run. Health-informatics papers describing clinical artifacts remain research outputs; clinical use, safety, and regulatory claims are outside this pipeline's scope.
