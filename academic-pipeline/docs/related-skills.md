## Related Skills

| Skill | Relationship |
|-------|-------------|
| `deep-research` | Dispatched (Stage 1 research phase) |
| `academic-paper` | Dispatched (Stage 2 writing, Stage 4/4' revision, Stage 5 formatting) |
| `academic-paper-reviewer` | Dispatched (Stage 3 first review, Stage 3' verification review) |

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
| Skill Version | 3.21.1 |
| Last Updated | 2026-08-24 |
| Maintainer | Cheng-I Wu |
| Dependent Skills | deep-research v2.0+, academic-paper v2.0+, academic-paper-reviewer v1.1+ |
| Role | Full academic research workflow orchestrator |

---
## Changelog

> See `../references/changelog.md` for full version history.
