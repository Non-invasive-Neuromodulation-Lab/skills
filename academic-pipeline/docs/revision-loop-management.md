## Revision Loop Management

- Stage 3 (first review) -> Stage 4 (revision) -> Stage 3' (verification review) -> Stage 4' (re-revision, if needed) -> Stage 4.5 (final verification)
- **Maximum 1 round of RE-REVISE** (Stage 4'): If Stage 3' gives Major, enter Stage 4' for revision then proceed directly to Stage 4.5 (no return to review)
- **Pipeline overrides academic-paper's max 2 revision rule**: In the pipeline, revisions are limited to Stage 4 + Stage 4' (one round each), replacing academic-paper's max 2 rounds rule
- Mark unresolved issues as Acknowledged Limitations
- Provide cumulative revision history (each round's decision, items addressed, unresolved items)

### Early-Stopping Criterion

At the end of each revision round, suggest stopping only when **no P0 issue remains**, **no unresolved decision-bearing regression remains**, **no applicable criterion has a substantive status change requiring another revision**, and **the author has no outstanding required action**. Explain the criterion-bound basis; do not compute a score delta or treat small label-count changes as convergence. The user can override. Hard cap: 2 full revision loops (Stage 4 + Stage 4').

### Budget Transparency (v3.2; interaction-count extension #89/#388)

At pipeline start, estimate token cost based on paper length, mode, and cross-model toggle. Present estimate and ask for user confirmation before Stage 1 begins.

Alongside the token estimate, present the **interaction-count budget**: long-horizon document corruption compounds with the number of document round-trips, not with token volume (DELEGATE-52, arXiv:2604.15597). Enumerate the round-trip caps the pipeline already enforces — 2 full revision loops (Early-Stopping above), 8 + 5 Socratic coaching rounds (Stage 3→4 / 3'→4'), and the integrity-gate fix→re-verify loop at Stages 2.5/4.5 — and state the worst-case round-trip total those caps imply for the chosen mode. At each stage checkpoint, report the accumulated round-trip count next to the stage status. **Advisory only**: the count never blocks; the per-loop caps remain the enforcement layer. A run that exceeds its stated worst case signals a loop the caps do not cover — surface that explicitly rather than silently continuing.

---
## Cross-run Adjudication Activity (#673; opt-in advisory side channel)

The state tracker section "Adjudication-activity metadata" is the single
producer/state authority. Each run receives one stable explicit `run_id`.
Structured handlers first durably apply their existing author-choice,
compliance-override, explicit-request, or MANDATORY-checkpoint routing/state
effect and only then best-effort append a data-minimized binding to the
five-row `pending_adjudication_activity_bindings[]` inventory. A refused
MANDATORY skip leaves state unchanged before the optional receipt stores
`skip_refused`. Author groups use `artifact_group_stage` and may preserve both
Stage 3 and Stage 3-prime; receipt stages use the complete Stage 1-through-6
closed enum, with no Stage 0. Compliance permits a plain report-only
captured-zero group and requires the paired action receipt only for a fully
qualifying override.

Terminal behavior is unchanged and runs first. After the completed/aborted
state is durable, and only for a user-selected local store, the orchestrator
passes explicit state/artifact-root paths and the explicit pending five rows to
`seal_terminal_inventory(state_path, artifact_root, pending_bindings)`, then
best-effort runs sealed-inventory `build-input`, idempotent `append-run`, and
optional `render`. The helper computes hashes; it does not read pending state,
accept caller hashes, infer sources, or scan. Root `run_id` plus sealed root
`adjudication_activity_sources` are exact authority. Any activity failure is an
advisory diagnostic and cannot affect the already-durable terminal outcome.

Activity data never enters a Material Passport, handoff, Process Record,
reviewer/model/observer/compliance input, gate, verdict, checkpoint input, or
stage transition. No live model, judge, eval, network/API, ambient clock,
directory scan, or glob participates. Full details and frozen receipt schemas
remain in `docs/design/2026-08-10-673-cross-run-adjudication-activity-spec.md`
and `../shared/contracts/activity/`.

---
## Auditability and replay boundaries

Pipeline artifacts are versioned, hashed, and auditable. Deterministic validators can be replayed against the same bytes and configuration. LLM-generated prose and semantic judgements are stochastic and are not byte-reproducibility guarantees; record model/configuration and evidence so differences can be inspected.

> See `../references/reproducibility_audit.md` for the standardized workflow contract, deterministic replay boundary, audit trail format, and artifact tracking.

---
## Stage 6: Process Summary Protocol

Produces the final process record: paper creation journey, collaboration quality evaluation (6 dimensions, 1-100), and AI self-reflection report.

**Terminal semantics (#528)**: Stage 6 is non-mandatory — the user may decline it at the Stage 5 completion checkpoint (Stage 6 marked `skipped`; the pipeline still terminates `completed`). When it runs, after the process record is delivered the orchestrator prompts for a terminal acknowledgement — `finish` / `end` / `done` / `confirm`, or an unambiguous natural-language equivalent that accepts the deliverables. On acknowledgement, Stage 6 is marked `completed` and the pipeline global state is set to `completed`; change requests (the other language version, content corrections) keep Stage 6 `in_progress` and are not acknowledgements. See `../references/pipeline_state_machine.md` § Stage 6 terminal semantics.

> See `../references/process_summary_protocol.md` for full workflow, required content structure, scoring dimensions, and output specifications.

---
## Collaboration Depth Observer (v3.5.0, advisory only — never blocks)

The `collaboration_depth_agent` observes the user's collaboration pattern with the pipeline. It is **advisory only** and **never blocks** progression at any checkpoint. It is `non-blocking` by design and carries `blocking: false` in its frontmatter as a structural guarantee.

**When invoked**: every FULL checkpoint, every SLIM checkpoint, and during Stage 6 record compilation (the whole-pipeline pass runs before the Process Record is generated and delivered, so its output can be a chapter of the record the user acknowledges). MANDATORY checkpoints (Stages 2.5 / 4.5 integrity gates) **do not** invoke the observer — those are integrity concerns and must not be diluted.

**What it does**: reads the dialogue range for the just-completed stage (at checkpoints) or the whole pipeline (during Stage 6 record compilation), scores the pattern against the canonical rubric at `../shared/collaboration_depth_rubric.md`, and emits an advisory block/chapter. Dimensions: Delegation Intensity, Cognitive Vigilance, Cognitive Reallocation, Zone Classification (Zone 1 / Zone 2 / Zone 3). Rubric is based on Wang & Zhang (2026) IJETHE 23:11 (DOI 10.1186/s41239-026-00585-x).

**Distinction from existing mechanisms**:

| Mechanism | What it evaluates | Blocking? |
|---|---|---|
| `integrity_verification_agent` (Stages 2.5 / 4.5) | Paper content — references, citations, data | Yes (blocking gate) |
| Stage 6 Collaboration Quality Evaluation (6 dims, 1–100) | AI's self-reflection on its own behaviour | No, but produced once only |
| `collaboration_depth_agent` (this observer) | The **user's** collaboration pattern (delegation intensity, vigilance, reallocation) | **No — never blocks. Advisory only.** |

**Non-blocking guarantees**:
- Observer output never appears on the "Flagged" line of any checkpoint.
- The `Ready to proceed?` prompt is unchanged by observer output.
- `blocked_by: collaboration_depth_agent` is never a legal state in `state_tracker`.
- If observer frontmatter ever asserts `blocking: true`, the orchestrator must refuse to dispatch it.

**Cross-model**: when `ARS_CROSS_MODEL` is set, the observer runs on both models and flags any dimension divergence > 2 points. Scores are never silently averaged across models.

> See `../agents/collaboration_depth_agent.md` for full scoring procedure and anti-sycophancy discipline; `../shared/collaboration_depth_rubric.md` for the canonical 4-dimension rubric.

---
## Anti-Patterns

Explicit prohibitions to prevent common failure modes:

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **Skipping integrity checks** | "The paper looks fine, skip Stage 2.5/4.5" | Integrity checks are MANDATORY; they cannot be auto-skipped regardless of perceived quality |
| 2 | **Orchestrator doing substantive work** | Pipeline orchestrator writes content or reviews the paper | Orchestrator only dispatches and coordinates; substantive work belongs to the sub-skills |
| 3 | **Auto-advancing past MANDATORY checkpoints** | Moving to next stage without user confirmation at FULL checkpoints | MANDATORY checkpoints require explicit user input before proceeding |
| 4 | **Quality degradation across stages** | Stage 4 revision is worse than Stage 2 draft because context window is exhausted | If Stage N output quality < Stage N-1, PAUSE and reload core principles before continuing |
| 5 | **Silently dropping reviewer concerns** | Revision addresses 8 of 10 concerns and hopes nobody notices | The R&R tracking table must account for every concern with explicit status |
| 6 | **Re-verifying only known issues at Stage 4.5** | Final integrity check only re-checks Stage 2.5 findings | Stage 4.5 must run a fresh from-scratch pass; revision may introduce new issues |
| 7 | **Inflating Collaboration Quality scores** | Giving 90/100 to avoid awkward self-criticism | Honesty first: no inflation, no pleasantries; cite specific evidence for every score |
| 8 | **Bypassing the Failure Mode Checklist block** (v3.2) | "The 7-mode checklist is new, let's skip it this run" | Stage 2.5/4.5 Failure Mode Checklist is MANDATORY and BLOCKING; there is no unrecorded bypass — every override requires user reasoning recorded for Stage 6 |

---
## Quality Standards

| Dimension | Requirement |
|-----------|------------|
| Stage detection | Correctly identify user's current stage and available materials |
| Mode recommendation | Recommend appropriate mode based on user preferences and material status |
| Material handoff | Stage-to-stage handoff materials are complete and correctly formatted |
| State tracking | Pipeline state updated in real time; Progress Dashboard accurate |
| **Mandatory checkpoint** | **User confirmation required after each stage completion** |
| **Mandatory integrity check** | **Stage 2.5 and 4.5 always run; continuation past a non-PASS result requires an explicit, recorded user decision** |
| **Mandatory failure mode checklist** (v3.2) | **Stage 2.5 and 4.5 must run the 7-mode AI research failure checklist; suspected failures block; overrides require user reasoning** |
| No overstepping | ⚠️ IRON RULE: Orchestrator does not perform substantive research/writing/reviewing, only dispatching |
| No forcing | ⚠️ IRON RULE: User can pause or exit pipeline at any time (but cannot skip integrity checks) |
| Auditable workflow | Same declared contract and deterministic validators can be replayed; model/configuration and stochastic outputs remain visible rather than promised identical |
| **Convergence-aware stopping** | **Suggest stopping only when no P0, unresolved decision-bearing regression, substantive criterion-status change, or outstanding required action remains; user can override** |
| **Budget transparency** (v3.2; #388) | **Token cost estimate + interaction-count budget (round-trip caps + accumulated count at checkpoints, advisory) + user confirmation at pipeline start** |

---
## Error Recovery

| Stage | Error | Handling |
|-------|-------|---------|
| Intake | Cannot determine entry point | Ask user what materials they have and their goal |
| Stage 1 | deep-research not converging | Suggest mode switch (socratic -> full) or narrow scope |
| Stage 2 | Missing research foundation | Suggest returning to Stage 1 to supplement research |
| Stage 2.5 | Still FAIL after 3 correction rounds | List unverifiable items; user decides whether to continue |
| Stage 3 | Review result is Reject | Provide options: major restructuring (Stage 2) or abandon |
| Stage 4 | Revision incomplete on all items | List unaddressed items; ask whether to continue |
| Stage 3' | Verification still has major issues | Enter Stage 4' for final revision |
| Stage 4' | Issues remain after revision | Mark as Acknowledged Limitations; proceed to Stage 4.5 |
| Stage 4.5 | Final verification FAIL | Fix and re-verify (max 3 rounds) |
| Any | User leaves midway | Save pipeline state; can resume from breakpoint next time |
| Any | Skill execution failure | Report error; suggest retry, pause, or mode switch. Do not skip mandatory integrity or failure-mode gates |

---
## Agent File References

| Agent | Definition File |
|-------|----------------|
| pipeline_orchestrator_agent | `../agents/pipeline_orchestrator_agent.md` |
| state_tracker_agent | `../agents/state_tracker_agent.md` |
| integrity_verification_agent | `../agents/integrity_verification_agent.md` |
| collaboration_depth_agent | `../agents/collaboration_depth_agent.md` |
| claim_ref_alignment_audit_agent | `../agents/claim_ref_alignment_audit_agent.md` |

---
## Reference Files

| Reference | Purpose |
|-----------|---------|
| `../references/pipeline_state_machine.md` | Complete state machine definition: all legal transitions, preconditions, actions |
| `../references/plagiarism_detection_protocol.md` | Phase D originality verification protocol + self-plagiarism + AI text characteristics |
| `../references/mode_advisor.md` | Unified cross-skill decision tree: maps user intent to optimal skill + mode |
| `../references/claim_verification_protocol.md` | Phase E claim verification protocol: claim extraction, source tracing, cross-referencing, verdict taxonomy |
| `../references/claim_audit_calibration_protocol.md` | v3.8 #103 claim_ref_alignment audit calibration: gold-set shape (T-C3), threshold gates FNR<0.15 / FPR<0.10 (T-C1), per-class FNR/FPR reporting (T-C2). Re-run via `PYTHONPATH=. python3 -m unittest scripts.test_claim_audit_calibration -v`. |
| `../references/ai_research_failure_modes.md` | 7-mode AI research failure checklist (Lu 2026), run at Stage 2.5 + 4.5 with blocking behaviour, reported at Stage 6 |
| `../references/team_collaboration_protocol.md` | Multi-person team coordination: role definitions, handoff protocol, version control, conflict resolution |
| `../references/integrity_review_protocol.md` | Stage 2.5 + 4.5 integrity verification: 5-phase protocol details |
| `../references/two_stage_review_protocol.md` | Two-stage review: Stage 3 full review + Stage 3' verification review |
| `../references/external_review_protocol.md` | External (human) reviewer feedback: 4-step intake/coaching/revision/verification |
| `../references/process_summary_protocol.md` | Stage 6: collaboration quality evaluation + AI self-reflection report |
| `../references/reproducibility_audit.md` | Standardized workflow contract, deterministic replay boundary, and audit trail format |
| `../references/progress_dashboard_template.md` | ASCII progress dashboard template |
| `../references/reinforcement_content.md` | Stage-specific reinforcement focus table for transitions |
| `../references/changelog.md` | Full version history |
| `../shared/handoff_schemas.md` | Cross-skill data contracts: 9 schemas for all inter-stage handoff artifacts |
| `../shared/collaboration_depth_rubric.md` | Collaboration Depth Observer rubric (v1.0): 4 dimensions based on Wang & Zhang (2026) IJETHE 23:11 |

---
## Templates

| Template | Purpose |
|----------|---------|
| `../templates/pipeline_status_template.md` | Progress Dashboard output template |

---
## Examples

| Example | Demonstrates |
|---------|-------------|
| `../examples/full_pipeline_example.md` | Complete pipeline conversation log (Stage 1-5, with integrity + 2-stage review) |
| `../examples/mid_entry_example.md` | Mid-entry example starting from Stage 2.5 (existing paper -> integrity check -> review -> revision -> finalization) |

---
## Output Language

Follows user language. Academic terminology retained in English.

---
## Integration with Other Skills

```
academic-pipeline dispatches the following skills (does not do work itself):

Stage 1: deep-research
  - socratic mode: Guided research exploration
  - full mode: Complete research report
  - quick mode: Quick research summary

Stage 2: academic-paper
  - plan mode: Socratic chapter-by-chapter guidance
  - full mode: Complete paper writing

Stage 2.5: integrity_verification_agent (Mode 1: pre-review)
Stage 4.5: integrity_verification_agent (Mode 2: final-check)

Stage 3: academic-paper-reviewer
  - full mode: Complete 5-person review (Journal-Fit Reviewer + R1/R2/R3 + Devil's Advocate)

Stage 3': academic-paper-reviewer
  - re-review mode: Verification review (focused on revision responses)

Stage 4/4': academic-paper (revision mode)
Stage 5: academic-paper (format-convert mode)
  - Step 1: Consume the citation-style decision recorded at the Stage 5 entry gate; ask which academic formatting style (APA 7.0 / Chicago / IEEE, etc.) only when no gate decision exists (direct format-convert / mid-entry invocation)
  - Step 2: Produce MD, then generate DOCX via Pandoc when available (otherwise provide conversion instructions)
  - Step 3: Produce LaTeX (using corresponding document class, e.g., apa7 class for APA 7.0)
  - Step 4: After user confirms content is correct, tectonic compiles PDF (final version)
  - Fonts: Times New Roman + Courier New (monospace)
  - ⚠️ IRON RULE: PDF must be compiled from LaTeX (HTML-to-PDF is prohibited)
```

---
