## Operational Modes (11 Modes)

See `../references/mode_selection_guide.md` for details.

| Mode | Trigger | Agents | Output |
|------|---------|--------|--------|
| `full` | "Write a paper" | All 9 (+ 11 if quantitative) | Complete paper draft (with figures if applicable) |
| `outline-only` | "Paper outline" | 1->2->3 | Detailed outline + evidence map |
| `revision` | "Revise paper" | 8->5->6 | Patch document + deterministically applied revised draft + apply report (#390; revision log via `../templates/revision_tracking_template.md`) |
| `abstract-only` | "Write abstract" | 1->7 | English abstract + keywords |
| `lit-review` | "Literature review" | 1->2 | Annotated bibliography + synthesis |
| `format-convert` | "Convert to LaTeX" / "Convert citations to [format]" | 9 only | Formatted document; includes citation format conversion (APA 7 / Chicago / MLA / IEEE / Vancouver) |
| `citation-check` | "Check citations" | 6 only | Citation error report |
| `plan` | "guide my paper" / "help me plan my paper" | 1->10->3->4 | Chapter Plan + INSIGHT Collection |
| `revision-coach` | "parse reviews" / "revision roadmap" / "I got reviewer comments" / "should we push back" / "conference rebuttal" / "grant panel response" / explicitly identified real committee correspondence | 12 only | Peer-review path: immutable Roadmap core + explicit author sidecar + optional Tracking Template/Response Skeleton. Committee path: separate #668 concern tracker + placeholder response skeleton; no Schema 11, reviewer obligation/severity, or determination. |
| **`disclosure`** (v3.2) | **"AI disclosure for Nature" / "generate AI usage statement"** | **9 only** | **Default venue path: `REQUIRED` / `ACTION_ONLY` / `NOT_REQUIRED` / `UNKNOWN` applicability plus typed halt status; policy-anchor path: anchor-specific render** |
| **`rebuttal-audit`** | **"audit my response" / "check my rebuttal" / "did I miss any reviewer comment"** (requires BOTH reviewer comments AND an existing rebuttal draft) | **12 only (parse-only)** | **Rebuttal QA report: per-comment coverage + gaps + risk flags. No new response generated; advisory only. Does NOT emit Schema 11 / Material Passport / verified status.** |

**Disclosure dispatch contract:** when mode=`disclosure`, agent 9 takes its standalone branch and MUST load `../references/disclosure_mode_protocol.md` before producing text. It does not run normal Phase 7 formatting or substitute the generic full-pipeline AI statement; the protocol selects the venue database or policy-anchor path and owns all halt/render decisions.

### Quick Mode Selection Guide

| Your Situation | Recommended Mode | Spectrum |
|----------------|-----------------|----------|
| Starting from scratch with a clear RQ | `full` | balanced |
| Need help planning before writing | `plan` | originality |
| Just need an outline | `outline-only` | balanced |
| Have a draft, received review feedback | `revision` | fidelity |
| Have unstructured reviewer comments | `revision-coach` | balanced |
| Have comments from a real committee/institutional review office to track | `revision-coach` committee-correspondence variant | fidelity |
| Just need an abstract | `abstract-only` | fidelity |
| Need to check/fix citations | `citation-check` | fidelity |
| Need to convert format (LaTeX, DOCX) or citation style | `format-convert` | fidelity |
| Want a systematic literature review paper | `lit-review` | fidelity |
| Need a venue-specific AI-usage disclosure bundle for submission | `disclosure` | fidelity |
| Have a written rebuttal draft to QA against reviewer comments | `rebuttal-audit` | fidelity |

**Spectrum** (v3.2): *fidelity* = template-heavy, predictable output; *balanced* = default; *originality* = exploratory, template-light. See `../shared/mode_spectrum.md` for the full cross-skill spectrum table.

Not sure? Start with `plan` — it will guide you step by step. `disclosure` is a finishing step — run it after the paper is drafted, targeting the venue you plan to submit to.

**Committee-correspondence routing:** use the `revision-coach` variant only when the
user explicitly identifies a real committee/institutional review office. Load
`../references/committee_correspondence_protocol.md`; do not infer official authority
from tone. The separate artifact is a source-accounted drafting aid and never enters
peer-review Schema 11.

### Mode Selection Logic

> See `../references/mode_selection_guide.md` for trigger-to-mode mappings and the full selection flowchart.

---
## Rebuttal-Audit Mode

`rebuttal-audit` evaluates an author's **existing** rebuttal / response-to-reviewers draft for coverage, tone, and evidence. It is advisory QA — it does **not** write or rewrite the response.

**Input gate (routing):** activate `rebuttal-audit` only when the user supplies BOTH (a) the reviewer comments / decision letter AND (b) an existing rebuttal/response draft to evaluate. If only (a) is present (no draft yet), route to `revision-coach` (which *generates* a response skeleton). If intent is ambiguous, clarify rather than guess.

**What it produces:**
- Per-comment coverage table — every reviewer concern marked `addressed` / `partially` / `missing` in the draft.
- Gap list — concerns the draft fails to answer.
- Risk flags — tone too combative, claims made without evidence, or a response that misreads the reviewer's actual point.
- Improvement suggestions (advisory).

**IRON RULE — integrity boundary (no false certification):** `rebuttal-audit` reuses `revision_coach_agent`'s comment-parsing capability, but a standalone invocation runs **outside** the pipeline and therefore never passes Stage 4.5 final integrity. It **MUST NOT** emit a Schema 11 `commitment_extracted` ledger, **MUST NOT** write to the Material Passport, and **MUST NOT** mark the package `ready_to_submit` or any verified status. Producing a Schema 11 artifact would falsely imply the response entered the pipeline's traceability system. The output is an advisory QA report only.

**Boundary vs `re-review`:** `academic-paper-reviewer`'s `re-review` mode verifies the **revised manuscript** (did the author's claimed changes actually appear in the paper) and runs inside the pipeline. `rebuttal-audit` verifies the **response letter itself** (does the rebuttal cover every comment, is its tone/evidence sound) and runs standalone, advisory. Different artifacts, different layers.

---
## Revision Mode Patch Protocol (#390)

In revision mode, `draft_writer_agent` does NOT re-emit the complete paper. The round runs **anchorize → patch → deterministic apply → finalizer**, confining the regeneration surface to the blocks the revision explicitly touches (DELEGATE-52 blast-radius containment; spec `docs/design/2026-06-10-390-diff-patch-revision-mode-spec.md`):

1. **Anchorize** the draft (`scripts/ars_anchorize_draft.py` — idempotent, content-neutral): every block gets a stable `<!--block:BNNNN-->` marker and an exact manifest. Nothing rewrites the draft before apply.
2. **Bind explicit authority (#670):** validate the immutable `revision-roadmap/1.0`, exact registered claim surfaces, and complete `author-adjudication/1.0`. The roadmap keeps severity, obligation, cost scope, and bounded consequence independent; author triage and exact targets live only in the separate explicit sidecar.
3. **The writer emits current patch 1.1** (`../shared/contracts/patch/revision_patch.schema.json`) as a sidecar — every op cites only `will_address` items, stays inside exact target/operation scopes, and explicitly declares claim/collateral arrays. Registered claim movement needs an exact author-approved replacement; declined overlap needs exact collateral authority.
4. **Deterministic apply** (`scripts/ars_apply_revision_patch.py`) replays every binding before structural analysis or write. Current report format 1.3 carries the mechanically derived authorization witness and the honest `unregistered_claim_drift_review_required` E6 boundary. If E6 later detects a drift on an unregistered surface, the checkpoint has no default-open route: the author must explicitly choose `restore`, `authorize_with_reason`, or `pause`. Build and replay validation bind each choice to one explicitly named run-local raw session-event artifact; the sidecar retains its recomputed digest but neither path nor message. Untouched blocks remain byte-identical.
5. **Continuous evidence:** every review write, all-declined no-op, and integrity-correction round enters `revision-evidence-bundle/1.0`, from an exact integrity-PASS draft to the exact final draft. A scope escalation requires a new explicit sidecar or a narrower patch; legacy full re-emission cannot claim current authorization PASS.

Orchestrated runs follow `pipeline_orchestrator_agent.md` § Revision-Round Patch Sequencing; Mode B users run the same scripts by hand — exact commands in `../references/revision_patch_protocol.md`. Honest boundary: registered surfaces and exact edit authority are machine-replayed, but unregistered semantic drift still requires E6 review. `scripts/claim_strength_drift_disposition.py` closes explicit handling of reported rows only; it does not make model-mediated detection deterministic or complete. The `academic-paper full` in-pair Phase 6→4 loop is outside this standalone/pipeline revision contract.

---
## Plan Mode: Chapter-by-Chapter Guided Planning

Socratic mode that guides users through paper planning one chapter at a time. Builds a complete Paper Blueprint through structured dialogue.

> See `../references/plan_mode_protocol.md` for the full chapter-by-chapter dialogue flow and Paper Blueprint structure.

---
## Handoff Protocol: deep-research -> academic-paper

`intake_agent` automatically detects deep-research materials (RQ Brief /
Bibliography / Synthesis / INSIGHT Collection) and skips redundant steps. It
also requires the exact builder-produced `preregistration-artifact/1.0` handoff
receipt and, when provided, its explicitly named companion. Intake validates and
carries those bytes unchanged; it does not infer status, repair/rebuild the
sidecar, follow its display path, or substitute a planning template. A later
explicit user supply must be represented by a new sidecar from the named
deterministic builder. See `../deep-research/SKILL.md` Handoff Protocol and
`../shared/references/cross_document_consistency_advisory_protocol.md`.

---
## Failure Paths

See `../references/failure_paths.md` for details. Quick reference:

| Failure Scenario | Handling Strategy |
|---------|---------|
| Insufficient research foundation | Recommend running `deep-research` first |
| Wrong paper structure selected | Return to Phase 2, suggest alternative structure |
| Word count significantly over/under target | Identify problematic chapters, suggest trimming/expansion |
| Citation format entirely wrong | Re-run the entire citation phase |
| Peer review rejection | Analyze rejection reasons, suggest major revision or restructuring |
| Plan mode not converging | Suggest switching to outline-only mode |
| Incomplete handoff materials | List missing items, suggest supplementing or re-running |
| User abandons midway | Save completed Chapter Plan |

---
## Full Academic Pipeline

See `../academic-pipeline/SKILL.md` for the complete workflow.

---
## Phase 0: Configuration Interview

See `../agents/intake_agent.md` for the complete field definitions of the Phase 0 configuration interview. The interview covers 9 core items: paper type, discipline, target journal, citation format, output format, language, abstract, word count, and existing materials — plus co-authors, funding, optional style calibration, the domain evidence profile (Step 12), the citation-verification level (Step 13, #392), and the independent retraction policy (Step 14, #651). Both citation policies are mark-only by default with explicit strict opt-in, seeding `terminal_policies.citation_existence` and `terminal_policies.retraction` respectively. When an author confirms a venue/track/type target, Phase 0 also resolves the #683 `ReviewTargetContext` and initializes the #684 pointer-only binding manifest before any criteria-aware consumer runs; absence uses the explicit field-general `criteria_binding_unavailable` path. Outputs a Paper Configuration Record, awaiting user confirmation.

---
## File Structure

**Agent definitions**: `../agents/{agent_name}.md` — one file per agent (12 total, matching Agent Team table above).

**References** (28 files in `../references/`):
- Citation: `apa7_extended_guide`, ``citation_format_switcher`
- Writing: `academic_writing_style`, `writing_quality_check`, `writing_judgment_framework`
- Structure: `paper_structure_patterns` (6 types), `abstract_writing_guide`, `intro_title_rhetoric_guide` (CARS moves + title checklist)
- Domain: `hei_domain_glossary`, `journal_submission_guide`, `latex_template_reference`, `domain_evidence_profiles` (advisory screening profiles)
- Process: `failure_paths` (12 scenarios), `mode_selection_guide` (11 modes), `plan_mode_protocol`, `workflow_phase_details`, `revision_patch_protocol` (#390 Mode B commands + marker lifecycle)
- Ethics: `credit_authorship_guide` (CRediT 14 roles), `funding_statement_guide`, `statistical_visualization_standards`
- Disclosure (v3.2): `disclosure_mode_protocol` (default venue applicability/status bundle: `REQUIRED`, `ACTION_ONLY`, `NOT_REQUIRED`, `UNKNOWN`, plus typed halts; separate policy-anchor rendering), `venue_disclosure_policies` (v2 database: ICLR, NeurIPS, Nature, Science, ACL, EMNLP, plus medical-publishing policy targets — ICMJE, NEJM, The Lancet, JAMA, BMJ, PLOS, Frontiers)
- Integrity (v3.3): `anti_leakage_protocol` (knowledge isolation), `vlm_figure_verification` (optional VLM figure check)
- Policy anchors (#108): `policy_anchor_table`, `policy_anchor_disclosure_protocol`
- Meta: `changelog` (version history)
- Also: `../deep-research/references/apa7_style_guide.md` (base reference, extended here)

**Templates** (11 files in `../templates/`): `imrad`, `literature_review`, `case_study`, `theoretical_paper`, `policy_brief`, `conference_paper`, `latex_article_template.tex`, `abstract`, `credit_statement`, `funding_statement`, `revision_tracking` (4 status types).

**Examples** (8 files in `../examples/`): `imrad_hei_example`, `literature_review_example`, `plan_mode_guided_writing`, `revision_mode_example`, `revision_recovery_example`, `clinical_citation_verification_checklist`, `clinical_epistemic_status_example`, `version_family_reconciliation_example`.

---
## Anti-Patterns

Explicit prohibitions to prevent common failure modes:

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **AI-typical overused terms** | "delve into", "crucial", "it is important to note" = instant AI detection | Use discipline-specific vocabulary; see `../references/writing_quality_check.md` |
| 2 | **Em dash abuse** | More than 2 em dashes per page signals AI writing | Use parentheses, commas, or restructure the sentence |
| 3 | **Throat-clearing openers** | "In this section, we will discuss..." adds no information | Start with the claim or finding directly |
| 4 | **Uniform paragraph lengths** | Every paragraph is 4-5 sentences = monotonous AI rhythm | Vary paragraph length naturally (2-8 sentences) |
| 5 | **⚠️ IRON RULE: Fabricated citations** | Inventing plausible-sounding references that don't exist | Every citation must be verified via DOI or WebSearch; see `../academic-pipeline/agents/integrity_verification_agent.md` |
| 6 | **Sycophantic revision** | Accepting all reviewer feedback without critical evaluation | Use REVIEWER_DISAGREE status when reviewer is wrong; justify with evidence |
| 7 | **Scope creep during revision** | Adding unrequested sections/analyses to "improve" the paper | Revision addresses reviewer concerns only; new content requires explicit user approval |
| 8 | **Ignoring failure paths** | Continuing despite desk-reject signals or fatal methodology flaws | Check `../references/failure_paths.md`; invoke F11 Desk-Reject Recovery when triggered |

---
