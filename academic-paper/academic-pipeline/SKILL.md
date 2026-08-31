---
name: academic-pipeline
description:"Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> re-revise -> final integrity check -> finalize. Coordinates deep-research, academic-paper, and academic-paper-reviewer into a seamless 10-stage workflow with mandatory, coverage-bounded integrity checks, two-stage peer review, and auditable quality-assurance artifacts. Triggers on: academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow."
metadata:
  version: "3.21.1"
  last_updated: "2026-08-24"
  depends_on: "deep-research, academic-paper, academic-paper-reviewer"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - deep-research
    - academic-paper
    - academic-paper-reviewer
---

# Academic Pipeline v3.21.1 — Full Academic Research Workflow Orchestrator

A lightweight orchestrator that manages the complete academic pipeline from research exploration to final manuscript. It does not perform substantive work — it only detects stages, recommends modes, dispatches skills, manages transitions, and tracks state.

> **Routing discipline (v3.9.2):** see `shared/references/intent_clarification_protocol.md` for cross-skill routing rules. This skill assumes routing has already settled — ambiguous cross-phase materials should have been clarified upstream.

**v3.6.3 (opt-in):** Set `ARS_PASSPORT_RESET=1` to promote FULL checkpoints to context-reset boundaries. Use `resume_from_passport=<hash>` in a fresh session to continue from the recorded stage. See [`references/passport_as_reset_boundary.md`](references/passport_as_reset_boundary.md).

**v3.8 (opt-in):** Set `ARS_CLAIM_AUDIT=1` to enable the L3 claim-faithfulness audit gate at the Stage 4 → Stage 5 transition. When the flag is set, the orchestrator dispatches `claim_ref_alignment_audit_agent` after the v3.7.1 Cite-Time Provenance Finalizer and before `formatter_agent`'s hard gate. The audit emits `claim_audit_results[]` + `uncited_assertions[]` + `claim_drifts[]` + `constraint_violations[]` + `audit_sampling_summaries[]` aggregates per the 8-row matrix; HIGH-WARN classes gate-refuse output via the formatter REFUSE rules 6-10. Default OFF for v3.8.0 — ramp-on plan deferred to post-calibration evidence (spec §5 mode flag rationale). See `agents/claim_ref_alignment_audit_agent.md` and the orchestrator §3.6 prose.

**v2.0 Core Improvements**:
1. **Mandatory user confirmation checkpoints** — Each stage completion requires user confirmation before proceeding to the next step
2. **Academic integrity checks** — After paper completion and before review submission, run the declared reference, registered-claim, and reported-data checks; expose denominators, sampling, unknown states, and blocking verdicts
3. **Two-stage review** — First full review + post-revision focused verification review
4. **Final integrity check** — After revision completion, rerun the final-check contract from fresh inputs; `100%` applies only where the named registered population is explicitly complete
5. **Auditable** — Version, hash, and retain workflow artifacts; deterministic checks are replayable, while generative outputs are not promised byte-identical
6. **Process documentation** — Stage 6 generates a "Paper Creation Process Record" PDF documenting the human-AI collaboration history (delivered before the terminal acknowledgement that completes the pipeline)

## Quick Start

**Full workflow (from scratch):**
```
I want to write a research paper on the impact of AI on higher education quality assurance
```
--> academic-pipeline launches, starting from Stage 1 (RESEARCH)

**Mid-entry (existing paper):**
```
I already have a paper, help me review it
```
--> academic-pipeline detects mid-entry, starting from Stage 2.5 (INTEGRITY)

**Revision mode (received reviewer feedback):**
```
I received reviewer comments, help me revise
```
--> academic-pipeline detects, starting from Stage 4 (REVISE)

**Resume from passport (cross-session context reset, opt-in):**
```
resume_from_passport=<hash> [stage=<n>] [mode=<m>]
```
--> Loads the Material Passport (Schema 9), locates the `kind: boundary` entry matching `<hash>`, and confirms it has no later `kind: resume` entry consuming it. If `pending_decision` is set, the decision prompt fires first to capture the user's branch choice for the audit ledger; the prompt is never skipped, even when the user supplies `stage=`. After the prompt (or immediately if no `pending_decision`), the next stage is determined by: (a) `stage=<n>` CLI override if provided, else (b) the matched option's `next_stage`, else (c) the `next` field recorded in the boundary entry. CLI `stage=`/`mode=` overrides win over option routing.
- **Gate (emit)**: `ARS_PASSPORT_RESET=1` must be set in the emitting session. Without the flag, no `kind: boundary` entries are written and there is nothing to resume from.
- **Gate (resume)**: No flag required. Any session can invoke `resume_from_passport=<hash>` against a passport that carries a valid boundary entry matching the hash.
- **Intent**: Invoke in a *fresh* agent session. Resuming within the same session that emitted the boundary provides no token savings and may drop still-live in-session context.
- **Stage**: Any. Resumes at whatever stage the routing rules above determine.
- **Reference**: [`references/passport_as_reset_boundary.md`](references/passport_as_reset_boundary.md) — see §"`resume_from_passport` mode contract".

**Execution flow:**
1. Detect the user's current stage and available materials
2. Recommend the optimal mode for each stage
3. Dispatch the corresponding skill for each stage
4. **After each stage completion, proactively prompt and wait for user confirmation**
5. Track progress throughout; Pipeline Status Dashboard available at any time

---

## Trigger Conditions

### Trigger Keywords

**English**: academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow


### Non-Trigger Scenarios

| Scenario | Skill to Use |
|----------|-------------|
| Only need to search materials or do a literature review | `deep-research` |
| Only need to write a paper (no research phase needed) | `academic-paper` |
| Only need to review a paper | `academic-paper-reviewer` |
| Only need to check citation format | `academic-paper` (citation-check mode) |
| Only need to convert paper format | `academic-paper` (format-convert mode) |

### Trigger Exclusions

- If the user only needs a single function (just search materials, just check citations), no pipeline is needed — directly trigger the corresponding skill
- If the user is already using a specific mode of a skill, respect that entry point; the pipeline is opt-in
- The pipeline is optional, not mandatory

---

## Pipeline Stages (10 Stages)

| Stage | Name | Skill / Agent Called | Available Modes | Deliverables |
|-------|------|---------------------|----------------|-------------|
| 1 | RESEARCH | `deep-research` | socratic, full, quick | RQ Brief, Methodology, Bibliography, Synthesis |
| 2 | WRITE | `academic-paper` | plan, full | Paper Draft |
| **2.5** | **INTEGRITY** | **`integrity_verification_agent`** | **pre-review** | **Integrity verification report + corrected paper** |
| 3 | REVIEW | `academic-paper-reviewer` | full (incl. Devil's Advocate) | 5 review reports + Editorial Decision + Revision Roadmap |
| 4 | REVISE | `academic-paper` | revision | Revised Draft, Response to Reviewers |
| **3'** | **RE-REVIEW** | **`academic-paper-reviewer`** | **re-review** | **Verification review report: revision response checklist + residual issues** |
| **4'** | **RE-REVISE** | **`academic-paper`** | **revision** | **Second revised draft (if needed)** |
| **4.5** | **FINAL INTEGRITY** | **`integrity_verification_agent`** | **final-check** | **Final verification report (declared checks must PASS; registered denominators and unknown/out-of-scope states remain visible)** |
| 5 | FINALIZE | `academic-paper` | format-convert | Final Paper (default MD; DOCX via Pandoc when available, otherwise conversion instructions; ask about LaTeX; confirm correctness; PDF) |
| **6** | **PROCESS SUMMARY** | **orchestrator** | **auto** | **Paper creation process record MD + LaTeX to PDF (EN)** |

**Parallelization opportunity (v3.3)**: Within Stage 2, the `academic-paper` skill's Phase 1 (literature_strategist_agent) and the `visualization_agent` can operate in parallel after Phase 2 (structure_architect_agent) completes the outline. Specifically:
- Once the outline includes a visualization plan, `visualization_agent` can begin figure generation
- Simultaneously, `argument_builder_agent` can build CER chains
- `draft_writer_agent` waits for both to complete before beginning Phase 4

This mirrors PaperOrchestra's parallel execution of Plot Generation (Step 2) and Literature Review (Step 3) after Outline (Step 1), which reduces overall pipeline latency. The parallelization is optional — sequential execution remains the default for simplicity.

---

## Pipeline State Machine

1. **Stage 1 RESEARCH** -> user confirmation -> Stage 2
2. **Stage 2 WRITE** -> user confirmation -> Stage 2.5
3. **Stage 2.5 INTEGRITY** -> PASS -> Stage 3 (FAIL -> fix and re-verify, max 3 rounds; then Integrity Check FAIL Loop -> recorded user decision)
4. **Stage 3 REVIEW** -> Accept -> Stage 4.5 / Minor|Major -> Stage 4 / Reject -> Stage 2 or end
5. **Stage 4 REVISE** -> user confirmation -> Stage 3'
6. **Stage 3' RE-REVIEW** -> Accept|Minor -> Stage 4.5 / Major -> Stage 4'
7. **Stage 4' RE-REVISE** -> user confirmation -> Stage 4.5 (no return to review)
8. **Stage 4.5 FINAL INTEGRITY** -> PASS (zero issues) -> Stage 5 (FAIL -> fix and re-verify; after 3 unresolved rounds -> Integrity Check FAIL Loop -> recorded user decision)
9. **Stage 5 FINALIZE** -> MD -> DOCX via Pandoc when available (otherwise instructions) -> ask about LaTeX -> confirm -> PDF -> completion checkpoint (FULL) -> Stage 6 (user may decline Stage 6: marked `skipped`, pipeline goes directly to `completed`)
10. **Stage 6 PROCESS SUMMARY** -> ask language version -> generate process record MD -> LaTeX -> PDF -> terminal acknowledgement (`finish` / `end` / `done` / `confirm`, or an unambiguous natural-language equivalent) -> pipeline global state `completed`

See `references/pipeline_state_machine.md` for complete state transition definitions.

---

## Adaptive Checkpoint System

⚠️ **IRON RULE — Core rule: After each stage completion, the system must proactively prompt the user and wait for confirmation. The checkpoint presentation adapts based on context and user engagement.**

### Checkpoint Types

| Type | When Used | Content |
|------|-----------|---------|
| FULL | First checkpoint; after integrity boundaries; Stage 5 completion (final-deliverable acceptance) | Full deliverables list + decision dashboard + all options |
| SLIM | After 2+ consecutive "continue" responses on non-critical stages | One-line status + explicit continue/pause prompt |
| MANDATORY | Integrity FAIL; Review decision; Stage 5 entry gate (before finalization) | Cannot be skipped; requires explicit user input |

### Decision Dashboard (shown at FULL checkpoints)

```
━━━ Stage [X] [Name] Complete ━━━

Metrics:
- Word count: [N] (target: [T] +/-10%)    [OK/OVER/UNDER]
- References: [N] (min: [M])              [OK/LOW]
- Coverage: [N]/[T] sections drafted       [COMPLETE/PARTIAL]
- Criterion status: [named criterion + evidence-anchored categorical judgement, or `NOT_COMPARABLE`]

Deliverables:
- [Material 1]
- [Material 2]

Flagged: [any issues detected, or "None"]

Ready to proceed to Stage [Y]? You can also:
1. View progress (say "status")
2. Adjust settings
3. Pause pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Adaptive Rules

1. **First checkpoint**: always FULL
2. **After 2+ consecutive "continue" without review**: prompt user awareness ("You've continued [N] times in a row. Want to review progress?")
3. **Integrity boundaries (Stage 2.5, 4.5)**: always MANDATORY
4. **Review decisions (Stage 3, 3')**: always MANDATORY
5. **Before finalization (Stage 5 entry gate)**: always MANDATORY — this is the checkpoint between Stage 4.5 PASS and the Stage 5 dispatch, where the user explicitly confirms proceeding and makes the finalization-format decision (citation style); the in-stage LaTeX question and content confirmation stay inside Stage 5 execution. The Stage 5 completion checkpoint (Final Paper delivered, before Stage 6) is FULL — never SLIM. See `references/pipeline_state_machine.md` § Stage 5 boundary semantics
6. **All other stages**: start FULL, downgrade to SLIM if user says "just continue"

### Checkpoint Rules

1. ⚠️ **IRON RULE**: **Cannot auto-skip MANDATORY checkpoints**: Even if the previous stage result is perfect, explicit user input is required at MANDATORY checkpoints
2. **User can adjust**: At FULL and MANDATORY checkpoints, users can modify the mode or settings for the next step
3. **Pause-friendly**: Users can pause at any checkpoint and resume later
4. **SLIM mode**: If the user says "just continue" or "fully automatic," subsequent non-critical checkpoints switch to SLIM format (one-line status + explicit continue/pause prompt)
5. **Awareness guard**: After 4+ consecutive continue responses, the system inserts a FULL checkpoint regardless of stage type to ensure user remains engaged

### Self-Check Questions (at every FULL checkpoint)

Before presenting the checkpoint to the user, the orchestrator asks itself:

1. **Citation integrity**: Are there any unverified citations in the latest output?
2. **Sycophantic concession**: Did the latest stage uncritically accept all feedback without pushback?
3. **Criterion trajectory**: For each applicable named criterion, did the evidence-anchored status improve, remain unchanged, regress, or become non-comparable? Never reduce this to a hidden scalar or `latest >= previous`. Pause and flag any unresolved decision-bearing regression; use `NOT_COMPARABLE` when the criterion or evidence base changed.
4. **Scope discipline**: Did the latest stage add content not requested by the user or the revision roadmap?
5. **Completeness**: Are all required deliverables for this stage present?

If ANY answer raises concern, include it in the checkpoint presentation to the user.

---

## Agent Team (5 Agents)

| # | Agent | Role | File |
|---|-------|------|------|
| 1 | `pipeline_orchestrator_agent` | Main orchestrator: detects stage, recommends mode, triggers skill, manages transitions | `agents/pipeline_orchestrator_agent.md` |
| 2 | `state_tracker_agent` | State tracker: records completed stages, produced materials, revision loop count | `agents/state_tracker_agent.md` |
| 3 | `integrity_verification_agent` | Integrity checker: coverage-bounded reference, citation, registered-claim, and reported-data checks (blocking verdicts are explicit) | `agents/integrity_verification_agent.md` |
| 4 | `collaboration_depth_agent` | **Observer (advisory only — never blocks).** Reads dialogue log and scores user-AI collaboration pattern against `shared/collaboration_depth_rubric.md`. Invoked at FULL/SLIM checkpoints and during Stage 6 record compilation (whole-pipeline pass, before the Process Record is delivered). Based on Wang & Zhang (2026). | `agents/collaboration_depth_agent.md` |
| 5 | `claim_ref_alignment_audit_agent` | **Opt-in claim faithfulness auditor (v3.8 #103).** Audits sampled citations for claim ↔ reference alignment + negative-constraint compliance; emits per-claim `claim_audit_results[]`, `claim_drift[]`, `uncited_assertions[]`, `constraint_violations[]`. Dispatched via orchestrator §3.6 when claim_audit mode is requested. | `agents/claim_ref_alignment_audit_agent.md` |

---

## Reference Documentation

Detailed protocol sections live in `docs/` and load on demand - read a file only when its topic applies:

- [docs/orchestrator-workflow.md](docs/orchestrator-workflow.md) - Orchestrator Workflow, Phase-by-phase Invocation Contract (v3.9.2), Opt-in Inquiry Branch Ledger (#743 alpha) (+5 more)
- [docs/revision-loop-management.md](docs/revision-loop-management.md) - Revision Loop Management, Cross-run Adjudication Activity (#673; opt-in advisory side channel), Auditability and replay boundaries (+11 more)
- [docs/related-skills.md](docs/related-skills.md) - Related Skills, Model Tiering (#517, optional), Version Info (+1 more)
