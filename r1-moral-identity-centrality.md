# R1 — Moral identity centrality (load-bearing or performative?)

**Status:** Design proposal, drafted 2026-06-24 (extension loop, iteration 13 — Round 2). Develops **R1** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 2". **MVP-1 (the measure is mostly re-analysis of the inventory's identity layer); the moderator validation is cohort.** Carded. The lock is Dave's.

**Provenance.** R1. The instrument already separates **identity-level** claims ("I am someone who…", sticky, behavior-driving) from **value-level** claims ("I value…", revisable) in the inventory (`concept.md` §"Identity-level vs. trait-level"), and Aquino & Reed 2002 is already a reference. R1 reads, from that split, **how central *being moral* is to a person's self-concept** — and, crucially, treats it as the **moderator** that predicts how strongly *every other signal* in the instrument fires: the meta-variable for "does morality actually drive this person, or just decorate them?"

---

## 1. The hypothesis statement

**R1 (proposed `pre-registration.md` §6, secondary).**

*Moral-identity centrality — how core being-moral is to the self-concept, in its internalized and symbolic facets — is reliably measurable and distinct from how highly a person ranks moral values; and it moderates value–behavior consistency (higher centrality ⇒ tighter coupling between stated and revealed morality).*

### 1.1 Measurement primitive (from the identity layer; two facets)
Centrality is read from the **identity-level** moral-trait claims in the inventory (`concept.md` §151), *independent of behavior* (so it can later predict behavior without circularity, §1.4):
```
central_i        = strength/centrality of moral traits in i's identity-level ("I am…") claims
internalize_i    = private facet — being moral is core to who I am          (Aquino & Reed: Internalization)
symbolize_i      = public facet — I express/signal being moral to others    (Aquino & Reed: Symbolization)
```
Two facets because Aquino & Reed 2002 show they behave differently — Internalization predicts behavior; Symbolization is more self-presentational (§1.5).

### 1.2 R1a — centrality is reliably measured
Split-window test–retest of `central_i` (and the two facets): lower 95% CI ≥ **0.40**. Bootstrap per §8.

### 1.3 R1b — centrality is distinct from value-importance
*Ranking* honesty #1 is not the same as honesty being *central to who you are*. Discriminant: `central_i` not recoverable from the inventory's value-importance ranking (§5) — model R² of [value-rank] predicting `central_i` upper CI < 0.50. Centrality is a second axis on the self (how identity-defining), beside importance.

### 1.4 R1c — centrality moderates value–behavior consistency (headline + validation)
The reason R1 matters: it predicts the *strength* of the instrument's other signals.
```
R1c:  higher central_i (esp. internalize_i) predicts — across participants —
        · a SMALLER stated–revealed gap (§6)
        · LESS cross-situational variability (H10)
        · a WIDER moral circle (H11)
        · LESS self–other hypocrisy (H12)
      lower 95% CI of these moderation associations in the predicted direction > 0.
```
**Non-circularity (load-bearing):** `central_i` is the *self-report identity* measure (§1.1), and the moderation targets are *behavioral* (the gap, variability, circle, hypocrisy) — measure and target are independent, so this is a real prediction, not a tautology. The mechanism is the repo's own self-efficacy link (Bandura; `concept.md` §171: identity drives behavior when paired with self-efficacy). Anchor: Hertz & Krettenauer 2016 meta (moral identity → moral behavior, r ≈ 0.31).

### 1.5 N=1, value-neutrality, the desirability caveat
- **N=1.** `central_i` and the two facets are within-person, reveal-eligible ("being good is highly central to your self-concept — and more internalized than symbolic"). R1c is cohort.
- **Value-neutrality.** High centrality is **not** simply better: it can be admirable integrity *or* moral grandiosity / self-righteousness / scrupulosity (morality so central it turns rigid and judgmental). Low centrality isn't worse — it can be a healthy non-moralizing stance. Descriptive. In particular **high symbolization + low internalization** is the *performative* pattern — the likely signature of grandstanding (H-A3) and hypocrisy (H12); **high internalization** is the load-bearing pattern. The reveal describes the facet profile; it never scores "more central = better person."
- **Desirability caveat.** Self-reported moral centrality is flattery-prone (almost everyone wants to say morality is core to them), and Symbolization especially so. The harder-to-fake validation is R1c — *does* the claimed centrality actually moderate behavioral consistency? A high claimed centrality that fails to moderate (no smaller gap, no less hypocrisy) is itself the diagnostic (claimed-but-not-load-bearing).

### 1.6 Falsification and exploratory
Combined R1 = **R1a ∧ R1b ∧ R1c** (reliable, distinct, and a genuine moderator). A null R1c (centrality doesn't predict consistency) is the important falsification — it would mean self-reported moral centrality is decorative, not load-bearing (still publishable, and itself a finding about moral self-report). **Exploratory:** R1 as the **person-level moderator of the whole instrument** (the analog of C1's channel-level integration — C1 asks "do the channels agree?", R1 asks "does morality drive this person at all?"); symbolization↔H-A3 grandstanding and ↔H12 hypocrisy (the performative cluster); internalization↔A5's felt-but-violated (does an internalized identity produce the guilt-that-seeds-change, B4 grower trajectory?).

---

## 2. Theoretical grounding
- **Aquino & Reed 2002 (The Self-Importance of Moral Identity, JPSP — already a repo reference).** The construct and its Internalization/Symbolization facets — the basis for R1a/R1b.
- **Hertz & Krettenauer 2016 (meta-analysis).** Moral identity → moral behavior at r ≈ 0.31 — the evidence for R1c's moderation, and the honest effect-size ceiling for its threshold.
- **Hardy & Carlo 2011.** Moral identity as a source of moral motivation — the why behind the moderation.
- **Oyserman identity-based motivation + Bandura self-efficacy (both already in-repo).** The mechanism linking an identity claim to action (and why identity without self-efficacy under-delivers) — R1c's mediator.

## 3. Instrument modification required
- **Already in place.** The inventory's identity-level vs. value-level split (`concept.md` §151) — `central_i` is mostly re-analysis of the identity-layer moral-trait claims.
- **A1 (light add).** A few identity-level items that cleanly separate Internalization from Symbolization (the current split may not fully distinguish the two facets) — small inventory additions, not scenarios.
- **A2.** Scoring `§27` (proposed): `central_i`, `internalize_i`, `symbolize_i`, R1a/b, and the R1c moderation tests (centrality × the gap/H10/H11/H12 scores). Parity-gated.
- No new scenarios; corpus untouched. R1c is computable once the other branches' per-person scores exist (cohort).

## 4. Implications for existing locked decisions
**MVP-1 measure (identity layer) + a cohort moderation analysis.** Reuses the inventory; R1c links to the other branches' outputs. **Carded** (the *load-bearing-vs-performative* framing, not a desirability-trivial "how moral are you"). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R1 (moral-identity centrality) as a secondary; `central_i`/internalization/symbolization from the inventory identity layer (scoring §27); R1c the moderator validation against the §6 gap / H10 / H11 / H12, measured independently of behavior; one design-stage card." Considered-and-rejected: bolting on the full Aquino-Reed scale verbatim (rejected — the inventory's identity layer already carries most of it; add only the facet-separating items); a "moral-identity score" headline (rejected — report the facet profile + whether it actually moderates).

## 5. Why this is a research contribution
R1 is the **person-level moderator** the instrument lacked: a single meta-variable for *how load-bearing morality is to this person*, which predicts the strength of every other signal — and which separates **internalized** moral identity (drives behavior) from **symbolic** (drives self-presentation), giving a principled handle on the grandstanding/hypocrisy cluster. It is to the *person* what C1 is to the *channels*: the integrating layer that says whether the parts cohere — here, whether morality actually governs the self or merely adorns it. And it makes the honest move of validating a flattery-prone self-report against behavior rather than trusting it.

## 6. Open design questions
- **Q1.** Internalization/Symbolization item coverage — does the existing identity layer separate them, or are a few items needed?
- **Q2.** Desirability mitigation on the self-report (indirect phrasing; lean on R1c as the real test).
- **Q3.** Non-circularity discipline in code — `central_i` must never be computed from the very behaviors R1c predicts.
- **Q4.** R1c is conditional on enough other-branch data per person — the staging.

## 7. Downstream changes this design unblocks
1. `scoring.md §27` — `central_i`/facets, R1a/b, the R1c moderation tests (independent measure → behavioral targets)
2. `pre-registration.md` §6 — R1 secondary, with R1c as the moderator hypothesis
3. inventory — a few Internalization/Symbolization-separating identity items (if needed)
4. `research-program.json` — the R1 card (design-stage)
5. `validity-threats.md` — a social-desirability row for self-reported centrality (and why R1c is the harder test)
6. `DECISIONS.md` — the R1 lock (Dave's call)

## 8. Relationship to the other branches
- **The moderator of everything.** R1c predicts the §6 gap, H10 variability, H11 circle, H12 hypocrisy — R1 is the person-level analog of C1 (channel-level integration).
- **The performative cluster.** Symbolization↔H-A3 grandstanding and ↔H12 hypocrisy (claim-without-conduct); Internalization↔A5 felt-but-violated and ↔B4 grower trajectory (identity that produces change).
- **The inventory.** Orthogonal to value-importance (R1b) — centrality is identity-defining-ness, beside ranking.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 2" R1; [`concept.md`](concept.md) §"Identity-level vs. trait-level" (the split R1 reads), §171 (the self-efficacy mediator), Aquino & Reed 2002 in references
- [`scoring.md`](scoring.md) §5 (inventory; value-ranking R1b is distinct from), §6 (the gap R1c moderates), §8 — where §27 lands
- [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md), [`h11-moral-circle-radius.md`](h11-moral-circle-radius.md), [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md), [`h-a3-moral-language.md`](h-a3-moral-language.md) (the signals R1 moderates / the performative cluster), [`c1-multimethod-convergence.md`](c1-multimethod-convergence.md) (the channel-level analog)
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`pre-registration.md`](pre-registration.md) §6
