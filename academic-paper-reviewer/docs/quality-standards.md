## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Perspective differentiation | Each reviewer reviews from their assigned angle (config-time assignment diversity); overlapping findings may corroborate one another, but role/persona separation is not evidence of independent errors — deduplication happens at synthesis, never by reviewers self-censoring (#574 P0-3/#740) |
| Evidence-based | The Journal-Fit Reviewer's recommendation signal and the synthesizer's decision must be based on specific reviewer comments; no fabrication |
| Specificity | Every finding carries a typed evidence anchor (`../templates/peer_review_report_template.md` § Evidence Anchor Types); no vague comments (#574 A2) |
| Evidence-driven balance | Findings follow the evidence in both directions — genuine merits acknowledged, no manufactured balance and no finding quotas (#574 A1/B1) |
| Professional tone | Review tone must be professional and constructive; avoid personal attacks or demeaning language |
| Actionability | Each weakness must include specific improvement suggestions |
| Format consistency | All reports must follow the template structure; no freestyle |
| **Devil's Advocate completeness** | **Devil's Advocate must produce the strongest counter-argument; cannot be omitted** |
| **CRITICAL threshold** | **⚠️ IRON RULE: Devil's Advocate CRITICAL issues cannot be ignored by the Editorial Decision — every one is adjudicated visibly (validated/unresolved blocks Accept; adjudicated-and-rejected is recorded with rationale, never silently bypassed — #574 B1)** |

---
## Output Language

All reviews are written in English. Academic terms remain in English.

---
## Related Skills

| Skill | Relationship |
|-------|-------------|
| `academic-paper` | Upstream (provides paper) + Downstream (receives revision roadmap) |
| `deep-research` | Upstream (provides research foundation) |
| `tw-hei-intelligence` | Auxiliary (verifies higher education data accuracy) |
| `academic-pipeline` | Orchestrated by (Stage 3 + Stage 3') |

---
## v3.6.2 Sprint Contract Hard Gate

- **Reviewer hard gate.** All reviewer modes that ship with contracts (`reviewer_full`, `reviewer_methodology_focus`) now run two-call Phase 1 (paper-content-blind) + Phase 2 (paper-visible) orchestration. See `../references/sprint_contract_protocol.md`.
- **Schema 13.2 sprint contract.** Each dimension carries `eligible_roles` and `owner_role`; reviewer Phase 1 commits only eligible scoring plans, while Phase 2 marks ineligible dimensions `not_assessed`. Mandatory dimensions pre-commit `what_triggers_fatal`; fatality is never synthesized post hoc. Validator: `scripts/check_sprint_contract.py`. Schema: `../shared/sprint_contract.schema.json`.
- **Executable conformance + panel checkers.** Before synthesis, `scripts/check_phase_conformance.py` verifies role binding, plan grammar, manuscript blindness, trigger binding, dissent cap, and evidence anchors. After synthesis, `scripts/check_panel_synthesis.py` recomputes role-scoped two-stage arithmetic, verifies `dimension_verdicts`, and enforces the DA-CRITICAL terminal gate.
- **Synthesizer three-step mechanical protocol.** Build per-dimension eligible-seat matrix → apply each condition's quantifier per dimension, then its dimension quantifier → resolve precedence by severity. Majority with one assessed eligible seat means that seat decides. Forbidden operations are explicit in `../agents/editorial_synthesizer_agent.md`.
- **methodology_focus reduced panel.** `reviewer_methodology_focus` mode runs a 2-reviewer panel (Journal-Fit Reviewer, internal role `eic`, + methodology only) instead of the default 5.
- **Templates:** `../shared/contracts/reviewer/full.json` (panel 5) and `../shared/contracts/reviewer/methodology_focus.json` (panel 2). Reserved modes (`reviewer_calibration`, `reviewer_guided`) keep pre-v3.6.2 behaviour until follow-up patch templates land; `reviewer_re_review` left the Schema 13 enum with #576 Spec B and is governed by the dedicated contract family `../shared/contracts/re_review/`.

---
## Model Tiering (#517, optional)

When `ARS_MODEL_TIERING` is set, the dispatching session routes this skill's agents per `../shared/model_tiering.md` (canonical: the full 39-agent judgment/execution table + rules). Compact rule:

- **Unset (default):** every agent inherits the session model — byte-equivalent pre-#517 behavior.
- **`economy`** (frontier-tier session): execution-type agents dispatch ONE tier below the session model — floor Opus-class, never lower; judgment-type agents stay on the session model. No-op at or below the floor (announce once).
- **`quality-boost`** (below-frontier session): judgment-type agents at the checkpoint surfaces (Stage 2.5/4.5 gates; the opt-in Stage 4→5 claim–ref audit; final review) jump UP to the frontier tier (however many tiers away — not a single increment); nothing is ever downgraded. No-op at the frontier (announce once).
- Unknown values → warn once, behave as unset. Tiers are relative positions, never hard-pinned model ids. When a direction is active, route repeated same-stage calls to the SAME worker so its prompt cache accumulates; unset means dispatch shapes stay byte-equivalent too.

---
## Version Info

| Item | Content |
|------|---------|
| Skill Version | 1.11.1 |
| Last Updated | 2026-08-15 |
| Maintainer | Cheng-I Wu |
| Dependent Skills | academic-paper v1.0+ (upstream/downstream integration) |
| Role | Multi-perspective academic paper review simulator |

---
## Changelog

> See `../references/changelog.md` for full version history.
