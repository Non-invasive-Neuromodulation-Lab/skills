## Phase-by-phase Invocation Contract (v3.9.2)

academic-paper-reviewer runs in 3 phases internally (Phase 0 field analysis → Phase 1 panel review → Phase 2 editorial synthesis). Within the full ARS pipeline, this skill sits at the orchestrator's Phase 5 (Review), but each agent inside the reviewer skill is single-phase relative to the skill's own phase numbering.

Two invocation modes:

**Mode A — orchestrator-driven (default):** `pipeline_orchestrator_agent` (in `academic-pipeline` skill) dispatches `academic-paper-reviewer` as part of the full ARS pipeline Stage 3 (Review).

**Mode B — phase-by-phase (cross-session resume):** User invokes one reviewer agent per phase across sessions, or runs the full reviewer panel standalone via `/ars-review` equivalent.

In Mode B, **single-phase agents (Bucket A per `docs/design/2026-05-18-ars-v3.9.2-agent-phase-classification.md`) stay strictly within their assigned phase for writes**. The 6 Bucket A agents in academic-paper-reviewer are: `eic_agent`, `methodology_reviewer`, `domain_reviewer`, `perspective_reviewer`, `devils_advocate_reviewer` (all Phase 1 panel) + `editorial_synthesizer` (Phase 2 synthesis). Reading the full paper draft is **expected** for all reviewers — without context they cannot evaluate.

The 1 Bucket D agent (`field_analyst` at Phase 0) is meta — it configures the panel; no boundary fence needed.

The v3.6.2 Sprint Contract Protocol (paper-blind Phase 1 + paper-visible Phase 2 + data delimiter) additionally constrains all reviewer agents' within-phase discipline. Phase Boundary (phase scope) and Sprint Contract (within-phase paper-blind/paper-visible discipline) both apply — neither overrides the other.

Routing into Mode B requires explicit user signal — `/ars-<mode>` slash command or `[direct-mode]` prefix. Ambiguous cross-phase input defaults to clarification per `../shared/references/intent_clarification_protocol.md`.

**Enforcement (v3.9.2):** Phase Boundary blocks on Bucket A agents + advisory verifier (`scripts/check_pipeline_integrity.py`) + a deterministic PreToolUse write-scope guard in hook-enabled runtimes (#134 rescope, PR #294). Multi-phase envelope remains forward-scope (#134 Slices 3-5).

---
## Operational Modes (6 Modes)

| Mode | Trigger | Agents | Output |
|------|---------|--------|--------|
| `full` | Default / "full review" | All 7 agents | 5 review reports + Editorial Decision + Revision Roadmap |
| **`re-review`** | **Pipeline Stage 3' / "verification review"** | **Three dedicated contract calls owned by the orchestrating layer: per-item routed seat personas from the frozen Round-1 cards in Phase 1/2A, then one Phase 2B integration call (Journal-Fit Reviewer is a public persona and `EIC` a stable wire label, not an `eic_agent` dispatch); checker-backed closed rules derive the outcome; field_analyst NOT re-run — `re_review_mode_protocol.md` § Yardstick Continuity. Legacy single-pass only behind `ARS_RE_REVIEW_LEGACY=1`** | **Revision response checklist + residual issues + new Decision (or deferral/abort per contract)** |
| `quick` | "quick review" | field_analyst + eic | Journal-Fit Reviewer quick assessment + key issues list (15-minute version) |
| `methodology-focus` | "check methodology" | field_analyst + eic + methodology_reviewer | In-depth methodology review report (panel 2 under v3.6.2 sprint contract: Journal-Fit Reviewer + methodology) |
| `guided` | "guide me" | All + Socratic dialogue | Socratic issue-by-issue guided review |
| **`calibration`** (v3.2 + #611 tier) | **"calibrate reviewer" / "measure reviewer accuracy"** | **Explicit `directional`: 3 gold papers × 1 full panel; default `full`: 5-20 gold papers × 5 runs (3-run override); cross-model default-on** | **Directional raw boundary readout or full Calibration Report; tier-scoped session confidence disclosure** |

### Mode Selection Logic

```
"Review this paper"                      -> full
"Give me a quick look at this paper"     -> quick
"Help me check the methodology"          -> methodology-focus
"Does this paper have methodology issues"-> methodology-focus
"Guide me to improve this paper"         -> guided
"Walk me through the issues in my paper" -> guided
"Verification review" / "Check revisions"-> re-review
"How accurate is your review scoring?"   -> calibration
"Calibrate against these 10 papers"      -> calibration
"Run directional calibration on these 3 papers" -> calibration (directional tier)
```

---
## Re-Review Mode (Verification Review)

Dedicated mode for Pipeline Stage 3' — verifies whether revisions address first-round review comments. Uses R&R Traceability Matrix (Schema 11 + machine-readable sidecar) with Author's Claim + Verified? columns. Runs under the #576 three-gate evidence-before-persuasion contract: Phase 1 criteria commitment (revision-blind) → Phase 2A evidence verdict (persuasion-blind) → Phase 2B claim matching (letter revealed), checker-verified before any outcome surfaces.

**Input**: Original immutable Revision Roadmap + exact author-adjudication sidecar + Revision-Evidence Bundle + Original pre-revision draft (Phase 2A comparison base) + Revised manuscript + Response to Reviewers (optional; withheld until Phase 2B) + Editorial Decision Letter (optional) + Round-1 findings/cards + current patch 1.1/apply-report 1.3 chain. The #576 current 1.1 manifest hard-requires original, revised, roadmap, author, and bundle artifacts; mixed legacy/current chains fail.
**Output**: Verification Review Report with traceability matrix + new issues + Decision (or `user_review_required` deferral / fail-closed abort)

> See `../references/re_review_mode_protocol.md` for full verification logic, output format template, and Socratic guidance details.

---
## Guided Mode (Socratic Guided Review)

Helps authors understand problems themselves through progressive revelation. The Journal-Fit Reviewer opens with genuine strengths when they exist (never manufactured, #574 A1/B1), then gradually introduces deeper issues from each reviewer perspective.

> See `../references/guided_mode_protocol.md` for dialogue flow, rules, and progressive revelation sequence.

---
## Calibration Mode (v3.2)

Opt-in mode with a 3-paper directional tier or the 5-20-paper full tier. `full` remains the default and runs 5 panel replicates per paper (3-run budget override), producing bounded decision-level FNR / FPR / balanced accuracy and a target-specific candidate measured profile labelled `application_status: NOT_WIRED_TO_LIVE_REVIEW`. Each provenance artifact establishes context-ID separation only among the five seats in that panel; current tooling does not compare context IDs across replicates, so every output discloses cross-replicate freshness as unverified and never calls the repeats independent. It compares categorical criterion judgements when per-dimension gold annotations exist; it never creates a quality score or upgrades a current Schema 6 package. `directional` must be selected explicitly; it runs one full panel per paper, reports only exact verdicts, per-seat categorical judgements, raw lenient/exact/harsh counts, the Minor/Major boundary matrix, and raw severity-risk counts, and remains `NOT_CALIBRATED`. Cross-model is default-on in both tiers.

> See `../references/calibration_mode_protocol.md` for full spec: intake rules, ensembling methodology, output format, and failure cases this mode does not fix.

---
## Review Output Format

Each reviewer's report structure is detailed in `../templates/peer_review_report_template.md`.

### Devil's Advocate Report Structure (Special Format)

The Devil's Advocate uses a dedicated format, not the standard reviewer template:
- **Strongest Counter-Argument** (200-300 words)
- **Issue List** (categorized as CRITICAL / MAJOR / MINOR, with dimension and location)
- **Ignored Alternative Explanations/Paths**
- **Missing Stakeholder Perspectives**
- **Observations (Non-Defects)**

---
## Editorial Decision Format

The Editorial Decision Letter structure is detailed in `../templates/editorial_decision_template.md`.
The canonical per-mode decision authority table is `../references/editorial_decision_standards.md` §0. Under a sprint contract, its mechanical v2 engine governs; no qualitative matrix overrides a fired action.
## Cross-Model Reviewer Track (#540)

In ordinary review modes, the track applies to `full` only (the five-seat panel — `methodology-focus` has a two-seat contract, and `re-review`/`quick` have no Reviewer 2 seat, so the track and its provenance mandate do not apply there). Calibration is the explicit exception: it uses the canonical calibration-specific non-sprint, single-call Reviewer 2 transport and attempt-atomic substrate plan in `../shared/cross_model_verification.md`; it never borrows the `reviewer_full` two-call sprint payload. In ordinary `full`, when cross-model verification is active for the session — `ARS_CROSS_MODEL` configured AND the user has given the explicit cross-model consent (the env var is configuration, not consent; the manuscript is uploaded to the external provider) — Reviewer 2 runs on the cross-model family (a substrate swap inside the fixed five-seat panel — NOT the retired 6th-reviewer design; authority: `../shared/cross_model_verification.md` § Cross-Model Reviewer Track, incl. the #523 dispatching-layer transport and the two-call sprint-contract split). Otherwise all five personas share one model family on the normal primary-family routing, including any active `ARS_MODEL_TIERING` policy.

For every `reviewer_full` run, the dispatching layer records actual seat-level observations and builds then replay-validates `review-panel-provenance/1.0` using `scripts/review_panel_provenance.py` before synthesis. Missing observations remain `unknown`; an intended route, persona label, or configured provider never fills them. The Editorial Decision Letter renders all six axes separately and includes the derived same-family or family-unknown correlated-error disclosure when required. A dispatch failure records the actual fallback execution, never a silent or inferred swap. The artifact proves only its named provenance dimensions; it never establishes independent error processes.

---
## Integration

### Upstream/Downstream Relationships

```
deep-research --> academic-paper --> [integrity check] --> academic-paper-reviewer --> academic-paper (revision) --> academic-paper-reviewer (re-review) --> [final integrity] --> finalize
   (research)       (writing)         (integrity audit)      (review)                    (revision)                    (verification review)                (final verification)   (finalization)
```

### Specific Integration Methods

| Integration Direction | Description |
|----------------------|-------------|
| **Upstream: academic-paper -> reviewer** | Receives the complete paper output from `academic-paper` full mode, directly enters Phase 0 |
| **Upstream: integrity check -> reviewer** | In the Pipeline, the paper must pass integrity check before entering reviewer |
| **Downstream: reviewer -> academic-paper** | `revision-roadmap/1.0` remains immutable; revision mode additionally requires the exact claim-surface manifest and complete explicit `author-adjudication/1.0` sidecar |
| **Downstream: reviewer (re-review) -> integrity** | After re-review completes, proceeds to final integrity verification |

The upstream handoff also carries the exact #684 context/manifest/brief when a
criteria-aware target review is active. Re-review preserves that authority by
pointer; a changed target starts a new, explicitly non-comparable review id.

### Pipeline Usage Example

> See `../references/integration_guide.md` for a complete 9-step pipeline usage example.

---
## Agent File References

| Agent | Definition File |
|-------|----------------|
| field_analyst_agent | `../agents/field_analyst_agent.md` |
| eic_agent | `../agents/eic_agent.md` |
| methodology_reviewer_agent | `../agents/methodology_reviewer_agent.md` |
| domain_reviewer_agent | `../agents/domain_reviewer_agent.md` |
| perspective_reviewer_agent | `../agents/perspective_reviewer_agent.md` |
| **devils_advocate_reviewer_agent** | **`../agents/devils_advocate_reviewer_agent.md`** |
| editorial_synthesizer_agent | `../agents/editorial_synthesizer_agent.md` |

---
## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `../references/review_criteria_framework.md` | Structured review criteria framework (differentiated by paper type) | all reviewers |
| `../references/top_journals_by_field.md` | Top journal lists for major academic fields (Journal-Fit Reviewer role calibration) | field_analyst, eic |
| `../references/editorial_decision_standards.md` | Accept/Minor/Major/Reject criteria and decision matrix | eic, editorial_synthesizer |
| `../references/statistical_reporting_standards.md` | Statistical reporting standards + APA 7.0 format quick reference + red flag list | methodology_reviewer |
| `../references/quality_rubrics.md` | Criterion-bound narrative judgement for 7 review dimensions; every current live seat and Schema 6 package remains `NOT_CALIBRATED` because candidate-profile application is not wired | all reviewers |
| `../references/review_quality_thinking.md` | Cognitive framework for review quality: three lenses (internal validity, external validity, contribution), common reviewer traps, calibration questions | all reviewers |
| `../references/re_review_mode_protocol.md` | Full re-review verification logic (three-gate contract), R&R traceability output format, Socratic guidance after re-review | orchestrating layer; routed-seat Phase 1/2A calls; Phase 2B integration call |
| `../references/guided_mode_protocol.md` | Guided mode dialogue flow, progressive revelation sequence, dialogue rules | all reviewers |
| `../references/calibration_mode_protocol.md` | Calibration mode: explicit 3-paper directional tier plus the default 5-20-paper full measurement tier, Minor/Major boundary matrix, and tier-scoped session disclosure | all reviewers |
| `../references/review_panel_provenance_protocol.md` | Closed six-axis execution-provenance semantics, correlated-error disclosure, and deterministic build/replay rules; no binary independence reduction | dispatcher, editorial_synthesizer, re-review consumer |
| `../references/reviewer_sprint_prompt_source.md` | Canonical marked source for the five inline sprint-reviewer Phase 1/2 prompt fragments and the synthesizer protocol; runtime mirrors stay inline for bare dispatch and are exact-sync linted | five panel reviewers, editorial_synthesizer |
| `../references/integration_guide.md` | Complete 9-step pipeline usage example | — |
| `../references/changelog.md` | Full version history | — |

---
## Templates

| Template | Purpose |
|----------|---------|
| `../templates/peer_review_report_template.md` | Review report template used by each reviewer |
| `../templates/editorial_decision_template.md` | Editorial Decision Letter template (produced by `editorial_synthesizer_agent` in Phase 2 — not by the Journal-Fit Reviewer, #574 C2) |
| `../templates/revision_response_template.md` | Revision response template for authors (R->A->C format) |

---
## Examples

| Example | Demonstrates |
|---------|-------------|
| `../examples/hei_paper_review_example.md` | Full review example: "Impact of Declining Birth Rates on Management Strategies of Taiwan's Private Universities" |
| `../examples/interdisciplinary_review_example.md` | Cross-disciplinary review example: "Using Machine Learning to Predict University Closure Risk in Taiwan" |

---
## Anti-Patterns

Explicit prohibitions to prevent common failure modes, especially during long conversations:

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **Fabricating review comments** | Synthesizer invents critique not in any reviewer report | Every synthesis point must trace to a specific Phase 1 reviewer report |
| 2 | **Overlap suppression** | Reviewer omits or rewords a real finding to avoid duplicating peers — unexecutable under blindness (Iron Rule #2) and destroys the corroboration signal | Report what you find from your assigned angle; the synthesizer deduplicates and counts corroboration (#574 P0-3). Panel angle diversity is field_analyst's config-time job |
| 3 | **Ignoring Devil's Advocate CRITICAL findings** | Editorial Decision silently bypasses a DA CRITICAL without adjudicating it | Every DA CRITICAL is adjudicated visibly (Checkpoint Rule #4): a validated or genuinely unresolved one blocks Accept; one the Journal-Fit Reviewer adjudicates and rejects is recorded with rationale and does not veto by itself (#574 B1 — an unvalidated negative claim carries no more decision power than an unvalidated positive one) |
| 4 | **Rubber-stamp re-review** | Re-review says "all addressed" without verification | Each concern must be independently verified against the revised manuscript |
| 5 | **Sycophantic judgement inflation** | Marking a criterion met to avoid conflict despite contrary manuscript evidence | Apply the named criterion to anchored evidence; report `PARTLY_MEETS`, `DOES_NOT_MEET`, or `NOT_ASSESSED` when that is what the evidence supports |
| 6 | **Editing the manuscript** | Reviewer "helpfully" fixes the paper directly | READ-ONLY: produce reports, never modify the paper (Checkpoint Rule #6) |
| 7 | **Generic feedback** | "The methodology could be stronger" without specifics | Every criticism must include: what's wrong, where it is, and a proposed fix |

---
