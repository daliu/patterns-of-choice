# R6 — Moral conviction / metaethical objectivism (facts, or your own?)

**Status:** Design proposal, drafted 2026-06-28 (extension loop, iteration 17 — Round 3's first, and the **design phase's last** per Dave's 2026-06-28 redirect to build-and-validate). Develops **R6** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 3". MVP-1, **design-stage** (a well-validated construct with a clean *stated* anchor; the *revealed* signatures lean on the κ-gated language channel + tolerance-behavior coding — §1.1). The lock is Dave's.

**Provenance.** R6, and the one branch that measures not *what* you value or *how much*, but **how you hold it** — as an objective fact, or as your own. Two literatures converge: **moral conviction** (Skitka 2010) — the degree to which an attitude is experienced as a matter of moral right-and-wrong rather than preference or convention — and **metaethical objectivism** (Goodwin & Darley 2008) — whether a person treats a moral claim as objectively true (a fact, true independent of any opinion) or as a matter of opinion (like taste). It is the **meta-stance toward one's own values**, and it carries a heavy, well-replicated behavioral payload: conviction predicts intolerance of those who disagree, preferred distance from them, refusal to compromise or negotiate, outcome-based (not procedure-based) judgments of legitimacy, and greater acceptance of any-means-including-force to reach a morally-convicted end.

---

## 1. The hypothesis statement

**R6 (proposed `pre-registration.md` §6, secondary).**

*The metaethical stance a person takes toward their own moral positions — treating them as objective facts (true for everyone) vs. as personal commitments (true for me) — is a reliable individual difference, distinct from which values they hold (the inventory), from how non-tradeable those values are (R2 sacred values), and from how central morality is to their identity (R1); and its revealed signature (intolerance of divergent others, refusal to compromise, objectivist moral language) can diverge from its stated form — a gap on the meta-layer.*

### 1.1 Measurement primitive (a stated anchor + revealed signatures)
For person *i*, two related quantities:
```
objectivism_i = treats moral claims as objectively true/false (fact) vs. as matters of opinion (preference)
conviction_i  = the degree an attitude is experienced as moral right/wrong vs. preference/convention
```
Unusually for this instrument, R6 has **both a clean stated anchor and revealed signatures**, and the discipline is to hold them apart (**never pool** — §13.5):
- **Stated anchor (the objectivism probe).** Goodwin & Darley's paradigm: present moral statements and ask whether each is objectively true/false or a matter of opinion, with the disagreement-resolution follow-up (if two people disagree, can one be *wrong*?). The direct, validated metaethical measure.
- **Revealed — tolerance/compromise behavior.** In scenarios where another agent chooses differently on a moral dimension, does *i*'s choice sanction/distance the divergent other and refuse the offered middle (high conviction), or live-and-let-live and compromise (low conviction)? A behavioral tolerance read.
- **Revealed — objectivist vs. subjectivist language (A3 / `scoring.md §20`).** Does spontaneous moral talk assert fact ("X is just wrong," "everyone should") or mark preference ("for me," "I feel," "I wouldn't, but")? κ-gated.

### 1.2 R6a — the metaethical stance is a reliable individual difference
Split-window test–retest of `objectivism_i` (and the conviction read): lower 95% CI ≥ **0.50** (both Skitka's conviction and Goodwin & Darley's objectivism are reliable, stable individual differences — the bar is set higher than the exploratory branches' 0.40). Bootstrap per §8.

### 1.3 R6b — the meta-stance is discriminant (not value-content, not sacredness, not centrality)
The load-bearing claim — that *how* you hold a value is not reducible to the value itself, its tradeability, or its centrality:
- **vs. the inventory.** Two people who equally value honesty differ if one holds it as a universal fact and the other as a personal commitment. `objectivism_i` is discriminant from value-importance.
- **vs. R2 (sacred values) — the cleanest discriminant pair, and the one R6 most owes.** **Sacredness = resistance to tradeoff; objectivism = perceived epistemic status.** They dissociate: "I personally won't eat meat, but I don't think it's objectively wrong for others" (sacred-to-me, non-objectivist); "lying is objectively wrong for everyone, yet I'd trade a small lie to save a life" (objectivist, tradeable). Model R² of [R2 sacredness, R1 centrality, value-importance] predicting `objectivism_i` has upper CI < 0.50.
- **vs. R1 (centrality).** Centrality = how much morality defines who you are; objectivism = whether you treat it as fact. A person can have morality central yet hold it as their own commitment (central, non-objectivist), or peripheral yet believe in objective moral facts.

### 1.4 R6c — the stated–revealed meta-gap (the instrument's distinctive contribution)
The instrument's whole logic is stated-vs-revealed; R6 lifts it to the meta-layer. The stated objectivism probe (§1.1) and the revealed signature (tolerance/compromise behavior + objectivist language) should converge — but the **divergence** is the signal: the person who *says* "morality is subjective, to each their own" yet *behaves* with high conviction (sanctions and distances those who choose differently), or the reverse — the professed objectivist who is in practice tolerant and compromising. That meta-gap (stated metaethics vs. revealed metaethics) is a genuine new quantity no other branch touches.

### 1.5 N=1, value-neutrality (with extra force), censoring
- **N=1.** `objectivism_i` is within-person, reveal-eligible (descriptive: "you tend to hold your moral positions as objective facts that hold for everyone" vs. "...as personal commitments you don't impose on others"). R6a/b/c are cohort.
- **Value-neutrality (load-bearing, and unusually charged here).** **Neither pole is better.** Objectivism can be moral clarity and the courage to stand for something, *or* rigid intolerance of dissent; subjectivism can be tolerant pluralism, *or* a relativism that won't stand for anything. Each pole has a virtuous and a vicious reading; the reveal names where you sit and **never ranks**. This branch touches charged territory (conviction predicts refusal to compromise and acceptance of force), so the descriptive-never-prescriptive discipline binds with extra force: R6 reports the *structure* — that you hold morals as facts, and that this co-occurs with low tolerance of dissent — without endorsing or condemning it.
- **Censoring (§13.2).** The compromise-refusal signature connects to R2's right-censored cost-of-virtue `never`s; those stay censored — a refusal to compromise is read as conviction, never converted to a finite tradeoff price.

### 1.6 Falsification and exploratory cross-links
Combined R6 = **R6a ∧ R6b** (a reliable metaethical stance, discriminant from sacredness/centrality/content). R6c (the stated–revealed meta-gap) is the distinctive extension. A null R6b — `objectivism_i` collapses onto R2 sacredness or R1 centrality — is the falsification (the meta-stance would then be nothing over what those already measure). **Exploratory cross-links:** R6 ↔ **R2** (epistemic status vs. tradeoff resistance — the key discriminant); R6 ↔ R1 (stance vs. centrality); R6 ↔ A3 (objectivist vs. subjectivist language is the linguistic detector); R6 ↔ H11 (does objectivism narrow the circle through out-group intolerance, or widen it through universalized concern? — conviction drives both); R6 ↔ R3 (conviction can *license* disengagement — "any means" for a convicted end is the moral-justification mechanism, R3's darkest move).

---

## 2. Theoretical grounding
- **Skitka 2010 (and Skitka, Bauman & Sargis 2005; Skitka & Morgan 2014) — moral conviction.** Attitudes held with moral conviction function differently: they predict intolerance of and distancing from the attitudinally dissimilar, outcome-based legitimacy, resistance to authority and compromise, and greater acceptance of any-means including violence. (Skitka already enters the repo via Hofmann et al. 2014 everyday-morality; this adds her conviction program.) — R6a/b's behavioral anchor.
- **Goodwin & Darley 2008 ("The psychology of meta-ethics: Exploring objectivism", *Cognition*).** The individual-difference paradigm for metaethical objectivism — whether people treat ethical claims as objectively true vs. matters of opinion, with reliable between-person variation and a clean elicitation. — R6's stated-anchor method.
- **Deliberately *not* built on:** any claim that objectivism is the *correct* metaethics, or that more conviction is healthier — value-neutrality forbids both. R6 measures the stance descriptively; it takes **no** position on moral realism.

## 3. Instrument modification required
- **A1 (light add).** A **metaethical objectivism probe** (Goodwin & Darley paradigm — moral statements rated objective-fact vs. opinion, with the disagreement-resolution follow-up) as the stated anchor; plus **divergent-other framings** in existing tradeoff scenarios (does *i* sanction/distance the other who chooses differently, and refuse the offered middle?) for the revealed tolerance/compromise read. No new domains required.
- **A2.** Scoring **§31** (proposed): `objectivism_i`/`conviction_i`, R6a/b/c, the discriminant from R1/R2/value-importance, and the stated–revealed meta-gap. Inherits A3's κ gate for the language-derived part; **never pools** the stated probe with the revealed signatures (§13.5).
- **A3 corpus.** Read for objectivist-vs-subjectivist linguistic markers (a new feature over A3's foundation-content read).

## 4. Implications for existing locked decisions
**MVP-1 design-stage; a clean stated anchor + revealed signatures, the κ gate binding the language part.** **Carded** (the facts-or-your-own facet). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R6 (moral conviction / metaethical objectivism) as a secondary; `objectivism_i` from the Goodwin & Darley probe + revealed tolerance/compromise behavior + objectivist language (scoring §31); R6b discriminant from R2 sacredness, R1 centrality, value-importance; R6c the stated–revealed meta-gap; value-neutral with extra-force descriptive-only guardrails (the branch is charged); one design-stage card." Considered-and-rejected: scoring objectivism as healthier conviction or as worse intolerance (rejected — value-neutrality, both poles dual-read); folding R6 into R2 (rejected — epistemic status ≠ tradeoff resistance, R6b); taking any position on moral realism (rejected — the instrument measures the *stance*, not its correctness); making the stated probe the sole measure (rejected — the revealed signature and the meta-gap are the instrument's value-add).

## 5. Why this is a research contribution
R6 measures the one thing upstream of every value the instrument already reads: **how you hold it.** Not which morals, not how much, not how non-tradeable — but whether you take them as facts true for everyone or as commitments that are yours. It is the metaethical layer, with a heavy real-world payload (conviction is among the strongest predictors of intolerance, refusal to compromise, and acceptance of force). And because the instrument is built on the stated–revealed gap, R6 can do what a survey cannot: catch the professed relativist who behaves with absolute conviction, and the professed absolutist who lives and lets live — the meta-gap between the metaethics you *state* and the one you *enact*.

## 6. Open design questions
- **Q1.** The revealed tolerance/compromise read — designing divergent-other scenarios that surface sanctioning/distancing without leading the participant or moralizing the disagreement for them.
- **Q2.** The R6–R2 discriminant in practice — can `objectivism_i` (epistemic status) be cleanly factored from R2 sacredness (tradeoff resistance) when the two so often co-occur? (The dissociation cases in §1.3 are the validation targets.)
- **Q3.** The charged-content guardrail — keeping the reveal descriptive when the construct predicts intolerance and force; the threshold past which the reveal routes to neutral framing rather than anything that reads as endorsement or diagnosis.

## 7. Downstream changes this design unblocks
1. `scoring.md §31` — `objectivism_i`/`conviction_i`, R6a/b/c, the discriminant, the meta-gap
2. `pre-registration.md §6` — R6 secondary; R6b the discriminant, R6c the stated–revealed meta-gap
3. `scenarios/` — the objectivism probe + divergent-other framings (light add to existing items)
4. `research-program.json` — the R6 card (design-stage)
5. `validity-threats.md` — the charged-content row (descriptive-only under extra force) + the stated-probe reactivity note
6. `DECISIONS.md` — the R6 lock (Dave's call)

## 8. Relationship to the other branches
- **R2 (the key pair).** Epistemic status (fact vs. opinion) vs. tradeoff resistance (sells at no price) — they co-occur but dissociate (§1.3); R6's main discriminant burden.
- **R1.** Holding morals as facts (R6) ≠ morality being central to the self (R1) — meta-stance vs. centrality.
- **A3.** Objectivist vs. subjectivist *language* is R6's linguistic detector (a new feature over A3's foundation content).
- **R3.** Moral conviction can *license* disengagement — "any means" for a convicted end is the moral-justification mechanism; R6 is the upstream stance, R3 the downstream exculpation.
- **H11.** Conviction drives both universalized concern (wider circle) and out-group intolerance (sharper boundary) — an exploratory moderation.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 3" R6 (the map's first Round-3 item); [`r2-sacred-protected-values.md`](r2-sacred-protected-values.md) (the key discriminant — epistemic status vs. tradeoff resistance), [`r1-moral-identity-centrality.md`](r1-moral-identity-centrality.md) (stance vs. centrality), [`h-a3-moral-language.md`](h-a3-moral-language.md) (the objectivist/subjectivist-language detector + the shared κ gate), [`r3-moral-disengagement.md`](r3-moral-disengagement.md) (conviction licenses the "any means" justification)
- [`concept.md`](concept.md) (Skitka via Hofmann 2014 in references; this adds the conviction + objectivism anchors), [`scoring.md`](scoring.md) §20 (language channel), §13.2 (censoring — compromise-refusal stays censored), §13.5 (unit discipline — never pool stated probe with revealed signatures), §8 — where §31 lands
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus; the objectivism probe is a light add), §19 (the H9 lock pattern R6's lock follows), [`validity-threats.md`](validity-threats.md) (the charged-content + reactivity rows), [`pre-registration.md`](pre-registration.md) §6
