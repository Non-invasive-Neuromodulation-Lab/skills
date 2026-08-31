## Socratic Mode: Guided Research Dialogue

5-layer dialogue guiding users from vague ideas to concrete research questions. Core principle while non-generation Socratic mode is active: ⚠️ **IRON RULE**: Never give direct answers. The explicit candidate-generation exit below leaves that mode before any candidate is shown.

**Layers**: Clarification -> Assumption Probing -> Evidence/Reasoning -> Viewpoint/Perspective -> Implication/Consequence

**Research-question authorship boundary:** Socratic mode is non-generation by
default. Non-convergence may produce only a summary of directions the user has
already expressed plus focused questions or a `lit-review` suggestion; it never
produces candidate RQs automatically. If the user explicitly asks the system to
propose candidates, announce the exit from non-generation Socratic mode and
emit `[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]` on a standalone
line before any clearly labeled AI-generated candidate. Never switch silently.

> See `../references/socratic_mode_protocol.md` for the full 5-layer dialogue flow, management rules, and auto-end conditions.

### Opt-in Reading Probe (v3.5.1)

Setting `ARS_SOCRATIC_READING_PROBE=1` enables a one-time honesty probe during **goal-oriented** Socratic sessions. When the user cites a specific paper, the Mentor asks them to paraphrase one passage. Decline is logged without penalty. Default OFF. See `../agents/socratic_mentor_agent.md` §"Optional Reading Probe Layer".

---
## Systematic Review Mode

PRISMA 2020-compliant systematic review with optional meta-analysis. Follows 5-phase protocol: Protocol Registration -> Systematic Search -> Screening & Selection -> Data Extraction & RoB -> Synthesis & Reporting.

> **v3.4.0 compliance:** `systematic-review` mode triggers `compliance_agent` at Stage 2.5 (Methods items) and Stage 4.5 (remaining items + RAISE 8-role matrix). PRISMA-trAIce Mandatory failures block the pipeline. See `../shared/compliance_checkpoint_protocol.md`.

> See `../references/systematic_review_protocol.md` for full PRISMA pipeline, checkpoint rules, and meta-analysis procedures.

---
## Operational Modes

| Mode | Agents Active | Output | Word Count |
|------|---------------|--------|------------|
| `full` (default) | All 9 core (excluding socratic_mentor, RoB, meta-analysis) | Full APA 7.0 report | 3,000-8,000 |
| `quick` | RQ + Biblio + Verification + Report | Research brief | 500-1,500 |
| `review` | Editor + Devil's Advocate + Ethics | Reviewer report on provided text | N/A |
| `lit-review` | Biblio + Verification + Synthesis | Annotated bibliography + synthesis | 1,500-4,000 |
| `three-way-scan` | Biblio + Verification (retrieval + WHY/HOW/WHAT extract) | Paper shortlist compared by WHY/HOW/WHAT + cross-paper synthesis | 800-2,000 |
| `fact-check` | Source Verification only | Verification report | 300-800 |
| `socratic` | Socratic Mentor + RQ + Devil's Advocate | Research Plan Summary (INSIGHT collection) | N/A (iterative) |
| `systematic-review` | RQ + Architect + Biblio + Verification + RoB + Meta-Analysis + Synthesis + Report + Editor + Ethics + DA | Full PRISMA 2020 report + forest plot data + GRADE table | 5,000-15,000 |

---
## Three-Way Scan Mode (WHY / HOW / WHAT)

Use `three-way-scan` when the user needs a disciplined shortlist of papers compared in a stable frame, but does **not** yet need a full literature review report.

- **WHY**: what problem or bottleneck the paper addresses and why it matters
- **HOW**: what strategy, method, or technical route the paper uses
- **WHAT**: what the paper found, built, or still leaves unresolved

This mode is intentionally lighter than `lit-review`. It prioritizes:

1. candidate retrieval
2. deduplication
3. compact per-paper extraction
4. cross-paper synthesis of shared WHY, divergent HOW, and remaining gaps

Recommended per-paper output:

```markdown
## <paper title>
Source: <provider> | Year: <year> | Link: <url>

- WHY: ...
- HOW: ...
- WHAT: ...
```

Then add:

- common `WHY`
- divergent `HOW`
- strongest `WHAT`
- unresolved global gap

If the user later wants a broader evidence matrix, thematic synthesis, or PRISMA-like coverage, escalate from `three-way-scan` to `lit-review` or `systematic-review`.

---
## Failure Paths

See `../references/failure_paths.md` for all failure scenarios, trigger conditions, and recovery strategies across all modes.

Key failure path summary:

| Failure Scenario | Trigger Condition | Recovery Strategy |
|---------|---------|---------|
| RQ cannot converge | Phase 1 / Layer 1 exceeds multiple rounds while still vague | Full mode may use its candidate workflow; Socratic mode summarizes user-expressed directions or suggests `lit-review`, with no candidate generation unless the user explicitly exits non-generation mode |
| Insufficient literature | bibliography_agent finds < 5 sources | Expand search strategy, alternative keywords |
| Methodology mismatch | RQ type misaligned with method capability | Return to Phase 1, suggest 3 alternative methods |
| Devil's Advocate CRITICAL | Fatal logical flaw discovered | STOP, explain the issue, require correction |
| Ethics BLOCKED | Critical integrity issue (not subject matter) | Stop the user once to confirm; list issues + remediation path; overridable with recorded reasoning |
| Socratic non-convergence | > 10 rounds without convergence | Suggest switching to full mode |
| User abandons mid-process | Explicitly states they don't want to continue | Save progress, provide re-entry path |
| Only literature in other languages | English search returns empty | Switch to regional academic databases |

---
## Literature Monitoring (Optional Post-Pipeline)

Optional post-research monitoring for new publications in the research area.

> See `../references/literature_monitoring_strategies.md` for setup instructions across academic databases.

---
## Handoff Protocol: deep-research → academic-paper

After research is complete, the following materials can be handed off to `academic-paper`:

1. **Research Question Brief** (from research_question_agent)
2. **Methodology Blueprint** (from research_architect_agent)
3. **Annotated Bibliography** (from bibliography_agent)
4. **Synthesis Report** (from synthesis_agent)
5. **[If socratic mode] INSIGHT Collection and Research Plan Summary**
6. **Preregistration handoff** — exactly one builder-produced
   `preregistration-artifact/1.0` sidecar (including an unavailable receipt) and,
   when `status=provided`, its explicitly named companion bytes

**Trigger**: User says "now help me write a paper" or "write a paper based on this"

`academic-paper`'s `intake_agent` will automatically detect available materials and skip redundant steps:
- Has RQ Brief -> skip topic scoping
- Has Bibliography -> skip literature search
- Has Synthesis -> accelerate findings / discussion writing
- Has preregistration sidecar -> strict-validate it and its named companion,
  then carry both byte-for-byte; never rebuild it from prose or a template

The non-shell `research_architect_agent` supplies only the explicit caller
declaration and companion handle. Before handoff, a shell-capable dispatcher
must run the named deterministic `build-preregistration-artifact` subcommand in
`scripts/build_cross_document_consistency_advisory.py`, with caller-held RFC3339
`declared_at`. Only that builder may create or update the sidecar. A later
explicit user supply creates a new builder-produced sidecar; omission or silent
substitution is invalid.

See `../examples/handoff_to_paper.md` for a detailed handoff example.

---
## Full Academic Pipeline

See `../academic-pipeline/SKILL.md` for the complete workflow.

---
## Agent File References

| Agent | Definition File |
|-------|----------------|
| research_question_agent | `../agents/research_question_agent.md` |
| research_architect_agent | `../agents/research_architect_agent.md` |
| bibliography_agent | `../agents/bibliography_agent.md` |
| source_verification_agent | `../agents/source_verification_agent.md` |
| synthesis_agent | `../agents/synthesis_agent.md` |
| report_compiler_agent | `../agents/report_compiler_agent.md` |
| editor_in_chief_agent | `../agents/editor_in_chief_agent.md` |
| devils_advocate_agent | `../agents/devils_advocate_agent.md` |
| ethics_review_agent | `../agents/ethics_review_agent.md` |
| socratic_mentor_agent | `../agents/socratic_mentor_agent.md` |
| risk_of_bias_agent | `../agents/risk_of_bias_agent.md` |
| meta_analysis_agent | `../agents/meta_analysis_agent.md` |
| monitoring_agent | `../agents/monitoring_agent.md` |

---
## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `../references/apa7_style_guide.md` | APA 7th edition quick reference | report_compiler, editor_in_chief |
| `../references/source_quality_hierarchy.md` | Evidence pyramid + grading rubric | source_verification, bibliography |
| `../references/methodology_patterns.md` | Research design templates | research_architect |
| `../references/logical_fallacies.md` | 30+ fallacies catalog | devils_advocate |
| `../references/ethics_checklist.md` | AI disclosure, attribution, dual-use | ethics_review |
| `../references/interdisciplinary_bridges.md` | Cross-discipline connection patterns | synthesis, research_architect |
| `../references/socratic_questioning_framework.md` | 6 types of Socratic questions + 30+ prompt patterns | socratic_mentor |
| `../references/failure_paths.md` | 12 failure scenarios with triggers and recovery paths | all agents |
| `../references/mode_selection_guide.md` | Mode selection flowchart and comparison table | orchestrator |
| `../references/irb_decision_tree.md` | Portable human-subjects navigation aid; not an authority, universal taxonomy, or pathway determination | ethics_review, research_architect |
| `../shared/references/human_subjects_authority_protocol.md` | Exact authority selection, replay validation, actor/consumer filtering, and fail-closed resolved-context gate | ethics_review, research_architect |
| `../shared/human_subjects_authority_registry.json` | Bounded jurisdiction profiles with exact requirement IDs, authority anchors, obligated actors, and consumer scopes | ethics_review, research_architect |
| `../shared/contracts/human_subjects/resolved_authority_context.schema.json` | Pointer-only resolved-context shape; consumers still require deterministic replay validation | ethics_review, research_architect |
| `../shared/references/review_pathway_rule_trace_protocol.md` | Candidate-name ownership, exact selected-profile predicate partition, replay, render, surface lint, and non-consumer boundary (#669) | ethics_review, research_architect |
| `../shared/contracts/human_subjects/review_pathway_trace_request.schema.json` | Closed caller-owned candidate mapping; every selected-profile `pathway_trace` requirement is accounted for exactly once | dispatching layer |
| `../shared/contracts/human_subjects/review_pathway_rule_trace.schema.json` | Closed candidate-only predicate trace; replay and surface lint remain mandatory | ethics_review, research_architect |
| `../shared/references/submission_packet_manifest_protocol.md` | Deterministic packet inventory, authority replay, status, and non-authorization boundary (#667) | ethics_review, research_architect |
| `../shared/contracts/human_subjects/submission_packet_manifest.schema.json` | Pointer-only deterministic packet-manifest shape; consumers still require exact replay validation | ethics_review, research_architect |
| `../shared/references/authority_content_coverage_advisory_protocol.md` | Replay-bound authority-profile content observations, evidence-row/1.1 provenance, and noninterference boundary (#681) | ethics_review, research_architect |
| `../shared/contracts/human_subjects/content_coverage_advisory.schema.json` | Closed `LLM-ADVISORY` carrier; consumers still require finalizer replay validation | ethics_review, research_architect |
| `../shared/contracts/evidence/evidence_row_v1_1.schema.json` | Requirement/expectation/artifact-bound bounded excerpt rows for the #681 advisory surface | ethics_review |
| `../references/equator_reporting_guidelines.md` | EQUATOR reporting guideline mapping | research_architect, report_compiler |
| `../references/preregistration_guide.md` | Preregistration decision tree + platforms + checklist | research_architect |
| `../shared/references/cross_document_consistency_advisory_protocol.md` | Exact preregistration sidecar ownership/replay plus #672 advisory and #660 coexistence boundaries | research_architect, academic-paper intake, pipeline orchestrator |
| `../shared/contracts/passport/preregistration_artifact.schema.json` | Closed persistent preregistration handoff receipt; companion bytes remain separately named | dispatching layer, intake, pipeline orchestrator |
| `../references/systematic_review_toolkit.md` | Cochrane v6.4, PRISMA 2020, RoB 2, ROBINS-I, I² guide, GRADE, protocol registration | risk_of_bias, meta_analysis, bibliography, report_compiler |
| `../references/literature_monitoring_strategies.md` | Google Scholar alerts, PubMed alerts, RSS feeds, Retraction Watch, citation tracking, monitoring cadence | monitoring_agent |
| `../references/argumentation_reasoning_framework.md` | Cognitive framework for evaluating argument strength: Toulmin model, causal reasoning (Bradford Hill), inference to best explanation, epistemic status classification | synthesis, devils_advocate, source_verification, socratic_mentor, research_architect |
| `../references/socratic_mode_protocol.md` | Full 5-layer Socratic dialogue flow, management rules, auto-end conditions | socratic_mentor, research_question |
| `../references/systematic_review_protocol.md` | Full PRISMA pipeline, checkpoint rules, meta-analysis procedures | risk_of_bias, meta_analysis, bibliography, report_compiler |
| `../references/cross_agent_quality_definitions.md` | Peer-reviewed source tiers, currency standards, severity definitions | all agents |
| `../references/changelog.md` | Full version history | — |

---
## Templates

| Template | Purpose |
|----------|---------|
| `../templates/research_brief_template.md` | Quick mode output format |
| `../templates/literature_matrix_template.md` | Source x Theme analysis matrix |
| `../templates/evidence_assessment_template.md` | Per-source quality assessment card |
| `../templates/preregistration_template.md` | OSF standard 21-item preregistration template |
| `../templates/prisma_protocol_template.md` | PRISMA-P 2015 systematic review protocol template |
| `../templates/prisma_report_template.md` | PRISMA 2020 systematic review report template (27 items) |

---
## Examples

| Example | Demonstrates |
|---------|-------------|
| `../examples/exploratory_research.md` | Full 6-phase pipeline walkthrough |
| `../examples/systematic_review.md` | PRISMA-style literature review |
| `../examples/policy_analysis.md` | Applied comparative policy research |
| `../examples/socratic_guided_research.md` | Complete Socratic mode multi-turn dialogue (12 rounds) |
| `../examples/handoff_to_paper.md` | deep-research full mode handoff to academic-paper |
| `../examples/review_mode.md` | Review mode: 3-agent review pipeline for policy recommendation text |
| `../examples/fact_check_mode.md` | Fact-check mode: source verification of HEI claims with per-claim verdicts |
| `../examples/idea_diversity_coverage_gap_advisory.md` | #257 Socratic wording-pattern + lit-review distributional-skew advisories |

---
## Output Language

Follows the user's language. Academic terminology kept in English. Socratic mode uses natural conversational style.

---
## Anti-Patterns

Explicit prohibitions to prevent common failure modes:

| # | Anti-Pattern | Why It Fails | Correct Behavior |
|---|-------------|-------------|-----------------|
| 1 | **Confirmation bias in source selection** | Only finding sources that support the hypothesis | Devil's Advocate checkpoint must include counter-evidence search |
| 2 | **Cherry-picking evidence** | Citing one supportive study while ignoring three contradicting ones | Report the full evidence landscape including conflicting findings |
| 3 | **Vibe citing** | Mixing elements from 2-3 real papers into a fabricated reference | Every reference must be verified independently; mashup fabrication is the hardest to detect |
| 4 | **⚠️ IRON RULE: Treating "difficult to verify" as acceptable** | Marking a reference as "uncertain" instead of FAIL | Gray zone = FAIL. If you cannot confirm it exists, it does not go in the report |
| 5 | **Skipping phases** | Jumping to synthesis before completing source verification | Complete each phase fully; Phase N output is Phase N+1 input |
| 6 | **Shallow Socratic mode** | Giving answers disguised as questions ("Wouldn't you say X is true?") | Ask genuine questions that expose assumptions; never lead to predetermined conclusions |
| 7 | **Source tier inflation** | Treating a blog post as equivalent to a peer-reviewed journal | Apply evidence hierarchy strictly: Tier 1 (peer-reviewed) > Tier 2 (preprint) > Tier 3 (gray lit) |
