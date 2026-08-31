## Quality Standards

### Writing Quality
1. **Every claim must have a citation** or be supported by the paper's own data — or, for #548 absence/novelty claims, carry documented-search provenance plus the named nearest prior work where one exists (the explicit absence-of-adjacent-work statement suffices otherwise; no source can cite an absence)
2. **Zero citation orphans** — in-text citations <-> reference list must perfectly match
3. **Consistent register** — academic tone appropriate for the discipline
4. **Logical flow** — clear transitions between paragraphs and sections
5. **Word count compliance** — within +/-10% of target

### Abstract Quality
6. **Grounded writing** — the abstract reflects the draft's actual content, never invented
7. **Component coverage** — Background, Purpose, Method, Findings, Implications all present
8. **Keywords** — 5-7, reflecting the paper's core concepts
9. **Word count** — 150-300 words

### Citation Quality
10. **Format compliance** — 100% adherence to selected citation style
11. ⚠️ IRON RULE: **DOI inclusion** — every source with a DOI must include it; every citation must be verified via DOI or WebSearch
12. **Currency** — flag sources older than 10 years (unless seminal works)
13. **Self-citation ratio** — flag if >15%

### Peer Review
14. **Five criterion-bound dimensions** — Originality, Methodological Rigor, Evidence Sufficiency, Argument Coherence, and Writing Quality; report categorical judgements with evidence and no numerical aggregation
15. **Actionable feedback** — every criticism must include a specific suggestion
16. **Max 2 revision rounds** — unresolved items become Acknowledged Limitations

### Mandatory Inclusions
⚠️ **IRON RULE**: Every paper MUST include: Data Availability Statement, Ethics Declaration, Author Contributions (CRediT), Conflict of Interest Statement, Funding Acknowledgment.
17. **AI-use reporting** — normal `full` / `format-convert` flows include the existing generic AI tool-usage statement; standalone `disclosure` mode instead follows the selected venue applicability/status or policy-anchor rendering contract
18. **Limitations section** — explicitly discuss study limitations
19. **Ethics statement** — when applicable (human subjects, sensitive data)

---
## Output Language

Follows the user's language for discussion. Academic terminology is kept in English. All evaluated and generated text is English-only.

---
## Integration with Other Skills

```
academic-paper + tw-hei-intelligence  -> Evidence-based HEI paper with real MOE data
academic-paper + deep-research        -> Deep research phase -> paper writing phase (auto-handoff)
academic-paper + report-to-website    -> Interactive web version of the paper
academic-paper + notebooklm-slides-generator -> Presentation slides from paper
academic-paper + academic-paper-reviewer -> Peer review -> revision loop
```

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
| Skill Version | 3.3.1 |
| Last Updated | 2026-08-15 |
| Maintainer | Cheng-I Wu |
| Dependent Skills | deep-research v1.0+ (upstream), academic-paper-reviewer v1.0+ (downstream) |

---
## Version History

> See `../references/changelog.md` for full version history.
