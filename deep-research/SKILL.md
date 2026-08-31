---
name: deep-research
description:"Universal deep research agent team. 13-agent pipeline for rigorous academic research on any topic. 8 modes: full research, quick brief, paper review, lit-review, fact-check, three-way literature scan, Socratic guided research dialogue, and systematic review with optional meta-analysis. Covers research question formulation, Socratic mentoring, methodology design, systematic literature search, source verification, cross-source synthesis, risk of bias assessment, meta-analysis, APA 7.0 report compilation, editorial review, devil's advocate challenges, ethics review, and post-research literature monitoring. Triggers on: research, deep research, literature review, systematic review, meta-analysis, PRISMA, evidence synthesis, fact-check, WHY HOW WHAT papers, 3W literature scan, guide my research, help me think through."
metadata:
  version: "2.12.1"
  last_updated: "2026-08-15"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - academic-paper
    - academic-pipeline
---

# Deep Research — Universal Academic Research Agent Team

Universal deep research tool — a domain-agnostic 13-agent team for rigorous academic research on any topic.

**v2.4** adds writing quality improvements to the report compiler:
- **Style Profile consumption** (optional) — If a Style Profile is available from academic-paper intake, the report compiler applies it as a soft guide for the Executive Summary and Synthesis sections. Discipline conventions and report objectivity take priority.
- **Writing Quality Check** — The report compiler runs a writing quality checklist before finalizing: flags AI-typical overused terms, checks sentence/paragraph length variation, removes throat-clearing openers. See `academic-paper/references/writing_quality_check.md`.

> **Routing discipline (v3.9.2):** see `shared/references/intent_clarification_protocol.md` for cross-skill routing rules. This skill assumes routing has already settled — ambiguous cross-phase materials should have been clarified upstream.

## Quick Start

**Minimal command:**
```
Research the impact of AI on higher education quality assurance
```

**Socratic mode:**
```
Guide my research on the impact of declining birth rates on private universities
```

**Execution:**
1. Scoping — Research question + methodology blueprint
2. Investigation — Systematic literature search + source verification
3. Analysis — Cross-source synthesis + bias check
4. Composition — Full APA 7.0 report
5. Review — Editorial + ethics + vulnerability scan
6. Revision — Final polished report

---

## Trigger Conditions

### Trigger Keywords

**English**: research, deep research, literature review, systematic review, meta-analysis, PRISMA, evidence synthesis, fact-check, methodology, APA report, academic analysis, policy analysis, WHY HOW WHAT papers, 3W literature scan, guide my research, help me think through, monitor this topic, set up alerts

: , WHY HOW WHAT ,


### Socratic Mode Activation

Activate `socratic` mode when the user's **intent** matches any of the following patterns, **regardless of language**. Detect meaning, not exact keywords.

**Intent signals** (any one is sufficient):
1. User has no clear research question and wants guided thinking
2. User asks to be "led", "guided", or "mentored" through research
3. User expresses uncertainty about what to research or where to start
4. User wants to brainstorm, explore, or clarify a research direction
5. User describes a vague interest without a specific, answerable question

**Default rule**: When intent is ambiguous between `socratic` and `full`, **prefer `socratic`** — it is safer to guide first than to produce an unwanted report. The user can always switch to `full` later.

**Example triggers** (illustrative, not exhaustive):
"guide my research""help me think through", or equivalent in any language

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Writing a paper (not researching) | `academic-paper` |
| Reviewing a paper (structured review) | `academic-paper-reviewer` |
| Full research-to-paper pipeline | `academic-pipeline` |

### Quick Mode Selection Guide

| Your Situation | Recommended Mode | Spectrum |
|----------------|-----------------|----------|
| Vague idea, need guidance / | `socratic` | originality |
| Clear RQ, need comprehensive research / RQ | `full` | balanced |
| Need a quick brief (30 min) / | `quick` | fidelity |
| Have a paper to evaluate before citing / | `review` | balanced |
| Need literature review for a topic / | `lit-review` | fidelity |
| Need a fast paper-comparison scan / | `three-way-scan` | fidelity |
| Need to verify specific claims / | `fact-check` | fidelity |
| Need systematic review / meta-analysis / | `systematic-review` | fidelity |

**Spectrum** (v3.2): *fidelity* = template-heavy, predictable output; *balanced* = default; *originality* = exploratory, template-light. See `shared/mode_spectrum.md` for the full cross-skill spectrum table.

Not sure? Start with `socratic` — it will help you figure out what you need.
 `socratic` ——

---

## Agent Team (13 Agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `research_question_agent` | Transforms vague topics into precise, FINER-scored research questions with scope boundaries | Phase 1, Socratic Layer 1 |
| 2 | `research_architect_agent` | Designs methodology blueprint: paradigm, method, data strategy, analytical framework, validity criteria | Phase 1 |
| 3 | `bibliography_agent` | Systematic literature search, source screening, annotated bibliography in APA 7.0 | Phase 2 |
| 4 | `source_verification_agent` | Fact-checking, source grading (evidence hierarchy), predatory journal detection, conflict-of-interest flagging | Phase 2 |
| 5 | `synthesis_agent` | Cross-source integration, contradiction resolution, thematic synthesis, gap analysis | Phase 3 |
| 6 | `report_compiler_agent` | Drafts complete APA 7.0 report (Title -> Abstract -> Intro -> Method -> Findings -> Discussion -> References) | Phase 4, 6 |
| 7 | `editor_in_chief_agent` | Q1 journal editorial review: originality, rigor, evidence sufficiency, verdict (Accept/Revise/Reject) | Phase 5 |
| 8 | `devils_advocate_agent` | Challenges assumptions, tests for logical fallacies, finds alternative explanations, confirmation bias checks | Phase 1, 3, 5, Socratic Layer 2, 4 |
| 9 | `ethics_review_agent` | AI-assisted research ethics, attribution integrity, dual-use screening, fair representation | Phase 5 |
| 10 | `socratic_mentor_agent` | Q1 journal editor persona; guides research thinking through Socratic questioning across 5 layers | Socratic Mode (Layer 1-5) |
| 11 | `risk_of_bias_agent` | Assesses risk of bias using RoB 2 (RCTs) and ROBINS-I (non-randomized); traffic-light visualization | Systematic Review (Phase 2) |
| 12 | `meta_analysis_agent` | Designs and executes meta-analysis or narrative synthesis; effect sizes, heterogeneity, GRADE | Systematic Review (Phase 3) |
| 13 | `monitoring_agent` | Post-research literature monitoring: digests, retraction alerts, contradictory findings detection | Optional (post-pipeline) |

---

## Mode Selection Guide

See `references/mode_selection_guide.md` for the detailed guide.

```
User Input
    |
    +-- Already have a clear research question?
    |   +-- Yes --> Need PRISMA-compliant systematic review / meta-analysis?
    |   |           +-- Yes --> systematic-review mode
    |   |           +-- No --> Need a full report?
    |   |                      +-- Yes --> full mode
    |   |                      +-- No --> Only need literature?
    |   |                                 +-- Yes --> Need rapid paper comparison?
    |   |                                            +-- Yes --> three-way-scan mode
    |   |                                            +-- No --> lit-review mode
    |   |                                 +-- No --> quick mode
    |   +-- No --> Want to be guided through thinking?
    |              +-- Yes --> socratic mode
    |              +-- No --> full mode (Phase 1 will be interactive)
    |
    +-- Already have text to review? --> review mode
    +-- Only need fact-checking? --> fact-check mode
```

---

## Orchestration Workflow (6 Phases)

```
User: "Research [topic]"
     |
=== Phase 1: SCOPING (Interactive) ===
     |
     |-> [research_question_agent] -> RQ Brief
     |   - FINER criteria scoring (Feasible, Interesting, Novel, Ethical, Relevant)
     |   - Scope boundaries (in-scope / out-of-scope)
     |   - 2-3 sub-questions
     |
     |-> [research_architect_agent] -> Methodology Blueprint
     |   - Research paradigm (positivist / interpretivist / pragmatist)
     |   - Method selection (qualitative / quantitative / mixed)
     |   - Data strategy (primary / secondary / both)
     |   - Analytical framework
     |   - Validity & reliability criteria
     |
     +-> [devils_advocate_agent] -- CHECKPOINT 1
         - RQ clarity and answerable?
         - Method appropriate for question?
         - Scope too broad or too narrow?
         - Verdict: PASS / REVISE (with specific feedback)
     |
     ** User confirmation before Phase 2 **
     |
=== Phase 2: INVESTIGATION ===
     |
     |-> [bibliography_agent] -> Source Corpus + Annotated Bibliography
     |   - Systematic search strategy (databases, keywords, Boolean)
     |   - Inclusion/exclusion criteria
     |   - PRISMA-style flow (if applicable)
     |   - Annotated bibliography (APA 7.0)
     |
     +-> [source_verification_agent] -> Verified & Graded Sources
         - Evidence hierarchy grading (Level I-VII)
         - Predatory journal screening
         - Conflict-of-interest flagging
         - Currency assessment (publication date relevance)
         - Source quality matrix
     |
=== Phase 3: ANALYSIS ===
     |
     |-> [synthesis_agent] -> Synthesis Narrative + Gap Analysis
     |   - Thematic synthesis across sources
     |   - Contradiction identification & resolution
     |   - Evidence convergence/divergence mapping
     |   - Knowledge gap analysis
     |   - Theoretical framework integration
     |
     +-> [devils_advocate_agent] -- CHECKPOINT 2
         - Cherry-picking check
         - Confirmation bias detection
         - Logic chain validation
         - Alternative explanations explored?
         - Verdict: PASS / REVISE
     |
=== Phase 4: COMPOSITION ===
     |
     +-> [report_compiler_agent] -> Full APA 7.0 Draft
         - Title Page
         - Abstract (150-250 words)
         - Introduction (context, problem, purpose, RQ)
         - Literature Review / Theoretical Framework
         - Methodology
         - Findings / Results
         - Discussion (interpretation, implications, limitations)
         - Conclusion & Recommendations
         - References (APA 7.0)
         - Appendices (if applicable)
     |
=== Phase 5: REVIEW (Parallel) ===
     |
     |-> [editor_in_chief_agent] -> Editorial Verdict + Line Feedback
     |   - Originality assessment
     |   - Methodological rigor
     |   - Evidence sufficiency
     |   - Argument coherence
     |   - Writing quality (clarity, conciseness, flow)
     |   - Verdict: ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT
     |
     |-> [ethics_review_agent] -> Research-Integrity Review + Human-Subjects Administrative Status
     |   - AI disclosure compliance
     |   - Attribution integrity
     |   - Dual-use screening
     |   - Fair representation check
     |   - Integrity verdict only: CLEARED / CONDITIONAL / BLOCKED
     |   - Human subjects: readiness and authorization reported separately; institutional determination required
     |   - Authority-bound planning: exact requirement IDs + actor/consumer scope only after the #666 replay-validated resolved-context gate
     |   - Candidate rule trace: display only a replay-validated and surface-linted #669 artifact; never use it as a pathway result or workflow input
     |   - Packet structure: consume only a replay-validated #667 manifest; deterministic status never becomes authorization or content adequacy
     |   - Content coverage: consume only a replay-validated #681 `LLM-ADVISORY`; preserve deterministic status and report efficacy as `UNMEASURED`
     |
     +-> [devils_advocate_agent] -- CHECKPOINT 3
         - Final vulnerability scan
         - Strongest counter-argument test
         - "So what?" significance check
         - Verdict: PASS / REVISE
     |
=== Phase 6: REVISION ===
     |
     +-> [report_compiler_agent] -> Final Report
         - Address editorial feedback
         - Resolve ethics conditions
         - Incorporate devil's advocate insights
         - Max 2 revision loops
         - Remaining issues -> "Acknowledged Limitations" section
```

### Checkpoint Rules

1. ⚠️ **IRON RULE**: **Devil's Advocate** has 3 mandatory checkpoints; **Critical-severity** issues block progression
2. Revision loops capped at **2 iterations**; remaining issues become "acknowledged limitations"
3. ⚠️ **IRON RULE**: **Ethics Review** stops the user once to confirm a Critical **integrity** concern (fabrication / plagiarism / missing AI disclosure / source misrepresentation / concrete harm-enabling specifics). Overridable with recorded reasoning — it confirms, it does not veto. Subject matter alone never blocks; dual-use is advisory (Responsible Use Statement), not a block.
4. User confirmation required after Phase 1 before proceeding

---

## Phase-by-phase Invocation Contract (v3.9.2)

ARS pipeline runs in 6 phases. Two invocation modes:

**Mode A — orchestrator-driven (default):** `pipeline_orchestrator_agent` (in `academic-pipeline` skill) runs all phases end-to-end with state tracking via Material Passport.

**Mode B — phase-by-phase (cross-session resume):** User invokes one agent per phase across sessions for long-running projects. Common pattern via `ARS_PASSPORT_RESET=1` + `resume_from_passport=<hash>` (see `academic-pipeline/references/passport_as_reset_boundary.md`).

In Mode B, **single-phase agents (Bucket A per `docs/design/2026-05-18-ars-v3.9.2-agent-phase-classification.md`) stay strictly within their assigned phase for writes**. Reads from upstream phases are allowed. Multi-phase agents (Bucket B: `devils_advocate_agent`, `report_compiler_agent`) do exactly the work specified by the caller's invocation for that phase — no extension to other phases in the same call.

Routing into Mode B requires explicit user signal — `/ars-<mode>` slash command or `[direct-mode]` prefix. Ambiguous cross-phase input defaults to clarification per `shared/references/intent_clarification_protocol.md`.

**Enforcement (v3.9.2):** Phase Boundary blocks on Bucket A agents + advisory verifier (`scripts/check_pipeline_integrity.py`) + a deterministic PreToolUse write-scope guard in hook-enabled runtimes (#134 rescope, PR #294). Multi-phase envelope remains forward-scope (#134 Slices 3-5).

---

## Reference Documentation

Detailed protocol sections live in `docs/` and load on demand - read a file only when its topic applies:

- [docs/socratic-mode-guided-research-dialogue.md](docs/socratic-mode-guided-research-dialogue.md) - Socratic Mode: Guided Research Dialogue, Systematic Review Mode, Operational Modes (+11 more)
- [docs/quality-standards.md](docs/quality-standards.md) - Quality Standards, Cross-Agent Quality Alignment, Integration with Other Skills (+3 more)
