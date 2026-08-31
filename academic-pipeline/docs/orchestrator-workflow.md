## Orchestrator Workflow

### Step 1: INTAKE & DETECTION

```
pipeline_orchestrator_agent analyzes the user's input:

1. What materials does the user have?
   - No materials           --> Stage 1 (RESEARCH)
   - Has research data      --> Stage 2 (WRITE)
   - Has paper draft        --> Stage 2.5 (INTEGRITY)
   - Has verified paper     --> Stage 3 (REVIEW)
   - Has review comments    --> Stage 4 (REVISE)
   - Has revised draft      --> Stage 3' (RE-REVIEW)
   - Has final draft for formatting --> Stage 5 (FINALIZE)

2. What is the user's goal?
   - Full workflow (research to publication)
   - Partial workflow (only certain stages needed)

3. Determine entry point, confirm with user
```

### Step 2: MODE RECOMMENDATION

```
Based on entry point and user preferences, recommend modes for each stage:

User type determination:
- Novice / wants guidance --> socratic (Stage 1) + plan (Stage 2) + guided (Stage 3)
- Experienced / wants direct output --> full (Stage 1) + full (Stage 2) + full (Stage 3)
- Time-limited --> quick (Stage 1) + full (Stage 2) + quick (Stage 3)

Explain the differences between modes when recommending, letting the user choose
```

### Step 3: STAGE EXECUTION

```
Call the corresponding skill (does not do work itself, purely dispatching):

1. Inform the user which Stage is about to begin
2. Load the corresponding skill's SKILL.md
3. Launch the skill with the recommended mode
4. Monitor stage completion status

After completion:
1. Compile deliverables list
2. Update pipeline state (call state_tracker_agent)
3. [MANDATORY] Proactively prompt checkpoint, wait for user confirmation
```

### Step 4: TRANSITION

```
After user confirmation:

1. Pass the previous stage's deliverables as input to the next stage
2. Trigger handoff protocol (defined in each skill's SKILL.md):
   - Stage 1  --> 2: deep-research handoff (RQ Brief + Methodology Blueprint + Bibliography + Synthesis)
   - #672 cargo on every transition: exact builder-produced `preregistration-artifact/1.0` receipt and its named companion when provided; validate and carry byte-for-byte
   - Stage 2  --> 2.5: Pass complete paper to integrity_verification_agent
   - Stage 2.5 --> 3: Pass the Stage 2.5 paper to reviewer (verified, or carrying the recorded FAIL-loop partially-unverified warning)
   - Stage 3  --> 4: Pass Revision Roadmap to academic-paper revision mode
   - Stage 4  --> 3': Pass revised draft, the hard-required original pre-revision draft (#576 current 1.1 §3.1 Phase 2A comparison base), exact author-adjudication sidecar, fully replayed Revision-Evidence Bundle, Response to Reviewers, Editorial Decision Letter, Round-1 findings, the immutable Roadmap, the exact ordered patch/report pairs projected by the bundle, and Round-1 Reviewer Configuration Cards. Missing original/roadmap/author/bundle is `manifest_incomplete`; this is the default contract re-review transfer. A user-requested fresh full review at 3' remains a separate full-mode branch.
   - Stage 3' --> 4': Pass new Revision Roadmap + R&R Traceability Matrix (Schema 11) to academic-paper revision mode; the traceability sidecar (frozen `previously_missed`/`indeterminate` records, #576 §8) rides through 4' toward Stage 4.5
   - Stage 3' --> 4.5 (Accept/Minor direct path): Pass verified revised draft + the traceability sidecar's frozen records to integrity_verification_agent as gate input
   - Stage 4/4' --> 4.5: Pass revision-completed paper to integrity_verification_agent (final verification); on the Major-via-4' path the Stage 3' traceability sidecar travels along as gate input
   - Stage 4.5 --> 5: Pass the accepted final draft (verified, or carrying the recorded FAIL-loop partially-unverified warning) to the one mandatory Stage-5 entry checkpoint; run #660 then #672 against that same accepted artifact ID/SHA-256 before format-convert dispatch
   - Stage 5  --> 6: Pass final deliverables list + the Process-Summary projection of pipeline state history, omitting the #673 activity projection of terminal root `run_id`, pending/sealed activity fields, selected-store data, renderer output, and diagnostics (user may decline Stage 6 at the Stage 5 completion checkpoint)
3. Begin next stage
```

### Mid-Conversation Reinforcement Protocol

At every stage transition, the orchestrator MUST inject a brief core principles reminder. This prevents context rot in long conversations.

**Template** (adapt to the upcoming stage):

````
--- STAGE TRANSITION: [Current] → [Next] ---

🔄 Core Principles Reinforcement:
1. [Most relevant IRON RULE for the next stage]
2. [Most relevant Anti-Pattern to avoid in the next stage]
3. Quality check: Is the output of [Current Stage] at least as good as [Previous Stage]? If not, PAUSE.

Checkpoint: [MANDATORY/ADVISORY] — [What user needs to confirm]
---
````

**Stage-specific reinforcement content**: See `../references/reinforcement_content.md` for the full transition → reinforcement focus table.

---
## Phase-by-phase Invocation Contract (v3.9.2)

academic-pipeline is the orchestrator skill that coordinates the full ARS pipeline across 10 stages (delegating to deep-research, academic-paper, academic-paper-reviewer). Two invocation modes:

**Mode A — orchestrator-driven (default):** `pipeline_orchestrator_agent` runs all stages end-to-end with state tracking via Material Passport. `state_tracker_agent`, `integrity_verification_agent`, `collaboration_depth_agent`, and `claim_ref_alignment_audit_agent` are dispatched by the orchestrator at the appropriate checkpoints.

**Mode B — phase-by-phase (cross-session resume):** User invokes one phase agent at a time across sessions, typically via `ARS_PASSPORT_RESET=1` + `resume_from_passport=<hash>` (see `../references/passport_as_reset_boundary.md`).

In Mode B, **single-phase agents (Bucket A per `docs/design/2026-05-18-ars-v3.9.2-agent-phase-classification.md`) in the downstream skills (deep-research, academic-paper, academic-paper-reviewer) stay strictly within their assigned phase for writes**. The 5 agents in academic-pipeline itself are all cross-phase / meta by design (Bucket C/D) — they have no fence by design:

- `pipeline_orchestrator_agent` (D — orchestrator, full pipeline visibility)
- `state_tracker_agent` (D — meta state, all phases)
- `integrity_verification_agent` (C — Stage 2.5 / 4.5 cross-skill gate)
- `collaboration_depth_agent` (C — FULL/SLIM checkpoints + Stage 6 record compilation, advisory-only)
- `claim_ref_alignment_audit_agent` (C — opt-in claim audit, phase-orthogonal)

Routing into Mode B requires explicit user signal — `/ars-<mode>` slash command or `[direct-mode]` prefix. Ambiguous cross-phase input defaults to clarification per `../shared/references/intent_clarification_protocol.md`. **Critically:** if `pipeline_orchestrator_agent` is dispatched on ambiguous cross-phase materials, the orchestrator itself currently cannot reconcile (this is the v3.10 conductor #134 work) — v3.9.2 routes such cases to clarification BEFORE the orchestrator runs.

**Enforcement (v3.9.2):** Phase Boundary blocks on downstream Bucket A agents + advisory verifier (`scripts/check_pipeline_integrity.py`) + a deterministic PreToolUse write-scope guard in hook-enabled runtimes (#134 rescope, PR #294). Multi-phase envelope + orchestrator structured intake remain forward-scope (#134 Slices 3-5).

---
## Opt-in Inquiry Branch Ledger (#743 alpha)

`ARS_INQUIRY_LEDGER=1` enables the bounded
`inquiry-branch-ledger/1.0` memory surface. Unset or `0` emits no ledger
artifact, pointer, prompt, or summary. Even when enabled, one linear branch
does not materialize a ledger; the second recorded branch is the first lawful
publication point.

The orchestrator owns the interaction surface and the deterministic runtime
`scripts/inquiry_branch_ledger.py` owns validation, replay, append,
profile-budget checks, pointer binding, and crash recovery. Replay receives the
exact profile file for every ledger binding; it never substitutes a current
fallback for missing historical bytes. AI facets enter `parked` and can become
author-owned only through an explicit origin-bound adoption receipt. Reopening
marks only author-recorded first-degree artifacts stale and never rewrites
them.

Render the runtime's compact summary only at the Stage 1 design-freeze
checkpoint, the Stage 2.5 and 4.5 MANDATORY checkpoints, or immediately after
a recorded reopen-condition signal. With the flag off or at most one branch,
omit the block completely. Every shown interaction offers `skip`, `off`, and
reset-to-simple-path; these hide future surfaces without deleting the ledger.
The summary is advisory state memory and never changes an integrity verdict or
checkpoint requirement. Full protocol and crash semantics:
`docs/design/2026-08-17-743-inquiry-branch-ledger-design.md`.

---
## Integrity Review Protocol

Stage 2.5 (pre-review) and Stage 4.5 (post-revision) verification. 5-phase protocol: references → citation context → statistical data → originality → claims.

⚠️ **IRON RULE**: Stage 4.5 must reach a recorded terminal resolution before Stage 5: PASS, or — after the 3-round integrity FAIL loop is exhausted — an explicit, recorded user decision on the listed unresolved items (rationale requirements escalate on repeated overrides; see `../shared/compliance_checkpoint_protocol.md`). Unresolved items are never silently dropped. Stage 4.5 performs a fresh from-scratch pass without relying on Stage 2.5 conclusions; this is not a claim of independent error processes.

⚠️ **IRON RULE (v3.2)**: Both Stage 2.5 and Stage 4.5 must also run the **AI Research Failure Mode Checklist** — a 7-mode taxonomy extending the citation hallucination checks into implementation bugs, hallucinated results, shortcut reliance, bug-as-insight, methodology fabrication, and pipeline-level frame-lock. If any of the 7 modes is `SUSPECTED`, or if Modes 1/3/5/6 are `INSUFFICIENT EVIDENCE`, the pipeline **blocks** and the user must acknowledge (confirm / override with reasoning / revise) before the pipeline proceeds. No configuration flag silences this block; the only path past it is the recorded user acknowledgment above — a trust-based control with an audit trail. Stage 6 PROCESS SUMMARY then reports the full failure-mode audit log as part of the AI Self-Reflection Report.

> See `../references/integrity_review_protocol.md` for the 5-phase citation/claim verification procedures.
> See `../references/ai_research_failure_modes.md` for the 7-mode AI research failure checklist and block/override logic.

- [v3.4.0] `compliance_agent` runs mode-aware PRISMA-trAIce + RAISE compliance check; tier-based block semantics. See `../shared/compliance_checkpoint_protocol.md`.

### Tortured-phrase advisory (#660)

After the exact Stage 4.5 pass and immediately before Stage 5 formatting, the orchestrator runs the deterministic #660 checker over the exact accepted working draft using an explicit user-supplied or synthetic-fixture snapshot and detached manifest bound to the raw snapshot SHA-256; omitted supply produces an explicit `not_checked` artifact. The path ships no native PPS content/importer/fetcher or redistributed phrase list and uses no live model, external API, human or model judge, or ambient clock; timestamps are explicit inputs. Its own-draft result is `HEURISTIC-ADVISORY` / `UNMEASURED`, never changes the Stage 4.5 PASS or Stage 5 gate, never rewrites prose, and must be re-run only after a revision has re-entered the existing integrity/screen sequence.

For the literature corpus, a non-in-place producer emits one current v1.2 advisory row per `cited_title` and `cited_abstract`; a missing abstract remains explicitly `not_checked` / `unresolved` with `ABSTRACT_MISSING`. Downstream consumers are read-only and compose every row into the one existing `Bibliographic Integrity Advisories` section. The advisory mints no marker, triggers no terminal policy, gate, finalizer promotion, ranking, citation rewrite, or replacement text, and supports no clean-draft, origin, papermill, contextual-validity, publisher-acceptance, or matcher-accuracy claim.

### Cross-document consistency advisory (#672)

The Stage-1 shell-capable dispatcher is the only consumer that may invoke
`scripts/build_cross_document_consistency_advisory.py
build-preregistration-artifact`. The non-shell research architect supplies only
the caller declaration and named companion handle. The resulting exact sidecar
and provided companion are replay-validated and carried byte-for-byte through
every handoff. Omission, silent substitution, template replacement, or digest
repair is invalid.

After the same exact Stage 4.5 PASS, the single mandatory Stage-5 entry
checkpoint runs #660 first and #672 second. Both bind the identical accepted
draft; #660 `input_binding.artifact.artifact_id/artifact_sha256` must equal #672
`input_binding.accepted_draft_artifact_id/accepted_draft_sha256`. They remain
separate carriers with separate failure semantics: preserve a schema-valid #660
degraded artifact on exit 1; a #672 contract/runtime failure writes no artifact
and records only bounded `ADVISORY_UNAVAILABLE:<CODE>`.

#672 is always `LLM-ADVISORY` / `UNMEASURED`. It has no score, pass/fail, gate,
readiness, authorization, ClaimIntent, rewrite, consent/protocol duplicate, or
clean/agreement meaning. It cannot change Stage 4.5, block or delay the existing
checkpoint, or alter Stage-5 routing after user confirmation. A manuscript
revision stales both advisories and must re-enter integrity before #660 and #672
rerun, in that order, against the new accepted bytes.

---
## Two-Stage Review Protocol

Stage 3 (full review, 5 reviewers) → Revision Coaching → Stage 4 → Stage 3' (re-review) → optional Residual Coaching → Stage 4'.

Stage 3' runs under the #576 three-gate evidence-before-persuasion contract by default: the orchestrator emits a hash-bound input manifest, dispatches Phase 1 (criteria commitment, revision-blind) → Phase 2A (evidence verdict, persuasion-blind) → Phase 2B (claim matching, letter revealed), and invokes `scripts/check_re_review_synthesis.py` as a MANDATORY step before any decision surfaces — outcomes are Accept / Minor / Major, a `user_review_required` deferral, or a fail-closed abort (never Reject). The sidecar's frozen `previously_missed`/`indeterminate` new-issue records forward to Stage 4.5 on both routes. Legacy single-pass re-review requires the explicit `ARS_RE_REVIEW_LEGACY=1` flag and is marked `[LEGACY-NO-CONTRACT]`. Authority: `pipeline_orchestrator_agent.md` § Stage 3' Re-Review Contract Dispatch + `../academic-paper-reviewer/references/re_review_mode_protocol.md`.

> See `../references/two_stage_review_protocol.md` for detailed stage flows and coaching dialogue limits.

---
## Mid-Entry Protocol

Users can enter from any stage. The orchestrator will:

1. **Detect materials**: Analyze the content provided by the user to determine what is available
2. **Identify gaps**: Check what prerequisite materials are needed for the target stage
3. **Suggest backfilling**: If critical materials are missing, suggest whether to return to earlier stages
4. **Direct entry**: If materials are sufficient, directly start the specified stage

**Important: mid-entry cannot skip Stage 2.5**
- If the user brings a paper and enters directly, go through Stage 2.5 (INTEGRITY) first before Stage 3 (REVIEW)
- Only exception: User can provide a previous integrity verification report and content has not been modified

---
## External Review Protocol

Handles external (human) reviewer feedback integration. 4-step workflow: Intake & Structuring → Strategic Revision Coaching → Revision & Response → Self-Verification.

> See `../references/external_review_protocol.md` for the complete 4-step workflow, coaching dialogue patterns, and capability boundaries.

---
## Progress Dashboard

ASCII dashboard shown at FULL checkpoints to display pipeline progress.

> See `../references/progress_dashboard_template.md` for the dashboard template.

---
