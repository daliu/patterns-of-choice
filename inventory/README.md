# inventory/

The stated-values inventory module. Captures what users *say* they value, in three formats — card sort, forced-choice pairwise comparison, and free-text story prompts — across three layers: current self, aspirational self, admired other.

The inventory and the scenarios share a 1:1 domain taxonomy (`truth-telling`, `resource-allocation`, `in-group-out-group`, `reciprocity-cooperation` for MVP-1), so per-domain gap analysis is a direct subtraction.

## Files

| File | Purpose |
|---|---|
| [`values-deck.json`](values-deck.json) | 20 behaviorally-anchored values for the card-sort protocol — 5 per MVP-1 domain |
| [`pairwise-pairs.json`](pairwise-pairs.json) | 30 forced-choice pairs for Bradley-Terry ranking: 16 within-domain (internal tensions) + 14 cross-domain |
| [`three-layer-prompts.json`](three-layer-prompts.json) | Phrasing templates for current / aspirational / admired-other framings |
| [`story-prompts.json`](story-prompts.json) | Free-text prompts for the qualitative layer; LLM-coded back to taxonomy post-hoc |
| [`relational-variant.json`](relational-variant.json) | Opt-in role-anchored framing variant ("as a daughter/colleague/friend, I am someone who...") — addresses the MacIntyre/Confucian role-ethics critique that personal-trait anchoring is itself a value commitment. Content authored, MVP-1 deferred. |
| [`SCHEMA.md`](SCHEMA.md) | Full field definitions for the JSON files |

## Design choices and why

**20 values, not 50.** Card-sort fatigue rises sharply past ~25 items. Twenty gives 190 possible pairs (sample 30) and is comfortably navigable on mobile.

**5 per domain, deliberate internal tensions.** Each domain includes values that pull against each other (e.g. `honesty` vs `tact`, `generosity` vs `self-reliance`). Without internal tension, the within-domain card-sort and pairwise data carry no signal.

**Behavioral anchors over abstractions.** Every card carries one sentence describing the value as a behavior, not as a virtue-word. "Saying what's true even when it's costly" beats "honesty is important." Forces the user to imagine the cost.

**Three layers separately captured.** Current self ("I am a person who..."), aspirational self ("I want to be a person who..."), admired other ("someone I respect is..."). The current↔aspirational gap is the user-chosen growth direction; the admired-other layer dodges the self-flattery instinct and often surfaces traits a user won't claim for themselves.

**Forced-choice, not Likert.** Likert lets people max all values; pairwise forces real tradeoff. Bradley-Terry posterior gives ranked utilities per value with usable confidence intervals.

**Story prompts as the qualitative anchor.** What users surface unprompted, in their own words, is more predictive than what they check from a list. Coded back to taxonomy post-hoc by LLM, then human-verified for the validation cohort.

## When each protocol fires

| Protocol | When | Duration |
|---|---|---|
| Card sort (top 5 of 20) | Session 1 — onboarding | ~3 min |
| Pairwise comparison (30 pairs) | Sessions 1–2 — split across two sessions to avoid fatigue | ~4 min each |
| Three-layer framing | Sessions 2–3 — each layer captured separately | ~2 min each |
| Story prompts (2 free-text items at onboarding) | Session 3 | ~5 min |
| Ongoing drift items | 1–2 items per session thereafter, rotating | ~30 sec |

Total onboarding inventory load: ~25 minutes across sessions 1–3. After that, the inventory is *passively maintained* through ongoing drift items rather than re-administered.

## MVP-1 coverage tracker

- [x] 20-value deck across 4 domains, 5 per domain
- [x] 30 pairwise pairs (16 within-domain, 14 cross-domain)
- [x] Three-layer prompt templates
- [x] Story prompts (5 templates)
- [ ] Validation against existing instruments (HEXACO-60 honesty-humility is the primary external anchor — done in analysis, not in this module)
- [ ] Drift-item rotation logic — engineering, deferred
