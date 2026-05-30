# H8 — Narrative-immersion as measure-debiasing

**Status:** Design proposal, drafted 2026-05-30. Source document for downstream changes to `concept.md`, `pre-registration.md`, `scoring.md`, and `DECISIONS.md`. The hypothesis is being floated for pre-registration alongside the existing seven; this document is the proposal that those downstream docs will draw from.

**Provenance.** Dave's project-direction statement, 2026-05-29:

> "by lulling people into a story, it's easier to gauge their choices over time, especially under fabricated moments of stress. It's easy to say you'll save a handful of humans over a dog, but when the dog is your imaginary buddy of several storied adventures, the tradeoff becomes more grounded in reality with life-like consequences."

This is a NOVEL methodological claim, not an import from standard psychometrics. If pre-registered and confirmed, it would be a contribution to moral psychology: narrative-embedding-with-recurring-character-attachment as a measurable debiasing mechanism against social-desirability response in ethical decision-making instruments.

---

## 1. The hypothesis statement

**H8 (proposed addition to `pre-registration.md` §6, secondary).**

*For a within-subject pair of probes — one embedded in a narrative arc featuring a recurring character the participant has come to know across prior sessions, the other a structurally-equivalent abstract / one-shot framing — the participant's response in the narrative condition will differ from their response in the abstract condition in the direction of (a) closer alignment with their stated values for low-stakes choices, and (b) farther deviation from their stated values for high-stakes attachment-laden choices.*

**Pre-registered formal statement (operational form):**

For each participant *i* completing a paired narrative-vs-abstract probe pair *p*:

Let `D_i^p = revealed(narrative) - revealed(abstract)` (the within-person, within-pair divergence score).

Then:
- **H8a (debiasing):** For low-stakes paired probes, `D_i^p` is negatively correlated with `gap_i^p` (the participant's stated-revealed gap on the abstract condition). That is: participants with the largest gap on the abstract probe show the LARGEST narrative-induced shift TOWARD their stated values. Threshold: lower 95% bootstrap CI of correlation ≥ 0.15.
- **H8b (attachment-laden shift):** For high-stakes attachment-laden paired probes (where the narrative invests the participant in a specific character whose welfare is at stake), `D_i^p` is positively correlated with `attachment_strength_i` (a measured immersion construct). That is: more-immersed participants show LARGER deviations from abstract-condition responses on the attachment-laden items. Threshold: lower 95% bootstrap CI of correlation ≥ 0.20.

Both sub-hypotheses are needed: H8a tests narrative-as-debiasing; H8b tests narrative-as-attachment-grounding. The combined finding would be that narrative immersion does NOT uniformly bias responses — it shifts them in *predictable construct-aware directions*, which is the methodological claim.

**Falsification thresholds.** H8 as a whole is falsified if EITHER:
- H8a fails (lower CI < 0.15), meaning narratives don't reduce social-desirability-driven deviation from stated values
- H8b fails (lower CI < 0.20), meaning narrative attachment doesn't add measurable stake-grounding

A mixed result (H8a passes, H8b fails) would be reported as "narratives debias but do not add attachment-grounding"; the reverse as "attachment grounds but does not debias." Both partial findings would be informative and published.

---

## 2. Theoretical grounding

Three converging literatures support the proposal:

### 2.1 Narrative transportation theory (Green & Brock 2000)

Green & Brock's Transportation-Imagery Model establishes that narrative engagement reduces critical processing and increases acceptance of in-story propositions. The mechanism is partly attention (transport monopolizes attention away from the source-monitoring that powers social-desirability responding) and partly identification (the participant sees the situation through a character's eyes rather than through their own performed-public-self perspective).

This is the strongest theoretical anchor for H8a (debiasing). The prediction follows directly: choices embedded in transported narrative should show reduced social-desirability bias.

### 2.2 Parasocial attachment (Horton & Wohl 1956; Tukachinsky 2010)

Decades of media-psychology research show that audiences form genuine emotional bonds with fictional or media-portrayed characters. These bonds exhibit measurable correlates: the participant's response to character welfare changes is correlated with self-reported attachment strength and behaviorally correlated (e.g., physiological arousal during character peril). Tukachinsky 2010's PSR-PRD measures parasocial relationship strength with established psychometric properties.

This is the anchor for H8b (attachment-laden shift). The prediction is that participants who have developed measurable parasocial attachment to a recurring character will weight that character's welfare in ethical decisions more heavily than they would in an equivalent abstract framing.

### 2.3 Social-desirability response as the threat being addressed

This is the existing `validity-threats.md` §CV-1 entry. The instrument's revealed-vs-stated framing assumes the revealed channel is less socially-desirability-shaped than the stated channel; CV-1 acknowledges this assumption is only partly satisfied by the timer + private-app design. H8 proposes a SECOND mitigation mechanism (narrative transportation) and pre-registers a test of whether it works.

If H8a confirms, the instrument has a documented second debiasing channel. If H8a fails, the instrument is still useful but the field-prediction claim (validity-threats §EV-3) becomes correspondingly less defensible.

---

## 3. Instrument modification required to test H8

The current MVP-1 instrument supports H8 *almost* but not fully. What's there, what's missing:

### Already in place

- **12 narrative scenarios** (3 per domain × 4 = 12). These are multi-decision-point arcs that span the protocol duration.
- **Recurring character mention** is flagged in `concept.md` §"Mechanics worth borrowing" as a design idea but is NOT currently implemented in the narrative authoring as a load-bearing element. Narratives use roles ("a colleague", "your aging parent") rather than named recurring characters.
- **48 scenarios with full domain coverage** — provides ample paired-probe candidates.

### What needs to be added

**A1. Recurring named characters.** A small recurring cast (~5-7 named NPCs with backstory continuity across sessions) needs to be authored and threaded through the existing narratives. The cast should span:
- One close-friend NPC who appears in truth-telling and reciprocity scenarios across multiple sessions
- One family-member NPC who appears in resource-allocation and in-group scenarios
- One out-group / new-arrival NPC whose circle-membership status evolves across sessions
- One adversary-but-with-redemption-arc NPC for reciprocity tests
- One animal companion / dependent NPC for the attachment-laden high-stakes probes (Dave's "imaginary buddy dog" example)

These would be added to scenario authoring as a metadata layer: each narrative scenario opt-in references one or more `recurring_npc:<id>` tags. The runtime renders consistent names and personality across sessions. Backwards-compatible with the existing 48-scenario corpus — existing scenarios can be retrofitted with NPC references where appropriate, or left in their current generic-role form.

**A2. Paired narrative-vs-abstract probes.** A subset (~8-12) of constructs need to be probed in BOTH formats:
- Narrative form: embedded in an established arc, attachment-laden where applicable
- Abstract form: structurally-equivalent quick-fire item

Within-subject design: the participant sees BOTH formats but at well-separated session times. Counterbalance order across participants.

This is the headline new authorial work for H8. ~8-12 paired probes is a meaningful corpus expansion.

**A3. Immersion / attachment measurement.** Two channels:
- Self-report: at sessions 8, 16, 24, administer a short adaptation of Tukachinsky 2010's PSR-PRD scale for each recurring NPC ("How attached do you feel to [name]?", "How much does [name] feel like a real person?", etc.). ~3-5 items per NPC × 5-7 NPCs = ~15-35 items total per administration; manageable in 5 min.
- Behavioral: response-latency on NPC-mentioning items vs. equivalent generic-role items. Increasing latency-gap over sessions is a proxy for attachment-investment.

**A4. Updated scoring spec.** A new section `scoring.md §9` operationalizing the H8 divergence score `D_i^p`, the attachment-strength score `attachment_strength_i`, and the H8a / H8b test statistics.

---

## 4. Implications for existing locked decisions

**DECISIONS §16 corpus lock.** The 48-scenario lock was set on the assumption that further additions require explicit construct-gap motivation. H8 itself IS a construct-gap motivation. The ~8-12 paired-probe additions would unlock §16 with a documented rationale, increasing the corpus to ~56-60.

**Pre-registration.** H8 becomes the 8th hypothesis. Secondary status (reported with effect sizes, not gate-criterion for instrument validation). The OSF filing would lock the H8 spec at filing time.

**Concept doc.** The "Mechanics worth borrowing" section's recurring-NPC mention gets promoted from "idea" to "load-bearing methodological mechanism." A new section ("Narrative immersion as measure-debiasing") is added.

**Pilot protocol.** The n=10 pilot would NOT formally test H8 (sample too small for the within-subject divergence statistics). Pilot's role is to:
- Verify the recurring NPCs feel real to participants in exit interviews
- Calibrate the attachment-measurement instrument
- Confirm the paired-probe pairing doesn't feel artificial to participants

**Pre-launch checklist.** Phase 4 (content finalization) gains: "Author ~8-12 paired narrative-vs-abstract probes"; "Design and author recurring-NPC cast"; "Implement attachment-measurement instrument."

---

## 5. Why this is a research contribution, not just an instrument feature

Standard psychometric instruments treat narrative-embedding as either (a) cosmetic (just a way to make items more interesting) or (b) a confounding source of variance to be minimized. The Implicit Association Test, the trolley problem, the dictator game, the dilemma vignettes literature — all treat the framing as instrument noise to be controlled away.

H8 inverts this: it claims narrative-embedding-with-recurring-character-attachment is a FEATURE that improves the instrument's measurement quality on a specific, named, falsifiable dimension (social-desirability debiasing). If confirmed, this gives the methodological literature a paradigm where narrative is INSTRUMENTAL rather than ornamental.

The closest existing literature is narrative transportation in PERSUASION (Green & Brock 2000) and in HEALTH-EDUCATION outcomes (Hinyard & Kreuter 2007). H8 is the first attempt I'm aware of to apply transportation-theory mechanisms to a MEASUREMENT context rather than an intervention context.

If H8a passes, the instrument's social-desirability concerns are demonstrably mitigated by the design. If H8b passes, the instrument has a measured mechanism for stake-grounding that abstract framings can't replicate. Both findings would be publishable independently of whether the larger MVP-1 validation succeeds.

---

## 6. Open design questions reserved for next iterations

These are not blocking the H8 framework, but will need decisions before H8 can be pre-registered:

**Q1. How many recurring NPCs in the cast?** Trade-off: more NPCs = richer attachment opportunities, but harder for the participant to track and remember. Suggestion: start with 5-7, calibrate from pilot exit interview.

**Q2. Should the imaginary-buddy NPC (Dave's example) be specifically a dog, or a more abstract dependent figure?** Dog has the highest-affect-anchor in pop-cultural memory; but a non-anthropomorphic figure may be more cross-culturally legible. Defer to pilot calibration.

**Q3. How are paired probes designed to be structurally equivalent across narrative/abstract?** The construct must be identical; only the framing differs. This is a significant authoring constraint and may reduce the number of paired probes that are cleanly possible.

**Q4. Is attachment-strength measured per-NPC or globally?** Per-NPC gives finer-grained data but more measurement burden. Suggestion: per-NPC for the high-attachment cast (the buddy figure especially); global for the wider cast.

**Q5. Should H8 be tested only in MVP-1, or held for a dedicated MVP-1.5 study after MVP-1's primary validation?** Argument for MVP-1: tests the design while the cohort is already engaged. Argument for separate study: H8 has its own design requirements that may not align cleanly with the existing MVP-1 protocol. Defer to co-PI consultation.

---

## 7. Downstream changes this design unblocks

When the H8 framework is approved (next iteration), the following downstream changes become actionable:

1. `concept.md` — add a "Narrative immersion as measure-debiasing" section; promote recurring-NPC from idea to mechanism
2. `pre-registration.md` §6 — add H8 (H8a + H8b sub-hypotheses) to the secondary hypotheses table
3. `pre-registration.md` §5 — add the within-subject paired-probe analysis plan
4. `scoring.md` — new §9 operationalizing divergence + attachment scores + H8 test statistics
5. `DECISIONS.md` — §17 unlocking the corpus from 48 → ~56-60 with H8 as the rationale
6. `pilot-protocol.md` — add the pilot's H8-supporting tasks (NPC-realness exit-interview question; attachment-instrument calibration)
7. `pilot-pre-launch-checklist.md` — Phase 4 additions for paired-probe authoring + NPC cast + attachment instrument
8. `validity-threats.md` §CV-1 — update mitigation list to include "narrative-immersion-as-debiasing per H8 (if confirmed)"
9. `literature/narrative-immersion.md` — new literature doc grounding the theoretical claim
10. `scenarios/` — author recurring-NPC layer + paired probe scenarios

This is multi-iteration work. The framework here is the proposal; downstream changes happen iteration-by-iteration once Dave confirms the framework is the direction he wants.

---

## Cross-references

- [`validity-threats.md`](validity-threats.md) §CV-1 — the social-desirability threat H8 proposes to mitigate
- [`concept.md`](concept.md) — recurring-NPC mention to be promoted
- [`pre-registration.md`](pre-registration.md) §6 — where H8 would be added
- [`scoring.md`](scoring.md) — where §9 would be added
- [`DECISIONS.md`](DECISIONS.md) §16 — corpus lock H8 would unlock
- [`pilot-protocol.md`](pilot-protocol.md) — pilot's calibration role for H8
