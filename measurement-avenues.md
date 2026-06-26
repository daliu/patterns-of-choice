# Measurement Avenues — branching the instrument beyond scenario-choice

**Status:** Living research-directions map, opened 2026-06-09. Surveys measurement *modalities* and *constructs* beyond the current three-layer architecture (scenario-choice + stated inventory + intervention) and the H1–H9 set. Each entry is a candidate branch; the **roadmap** at the end is the working priority order and the backlog for the extension loop. Each loop iteration develops one branch into its own design doc / hypothesis spec at the repo's rigor bar, then checks it off here.

**Per-branch site sync (added 2026-06-16).** When a branch ships, also add its public card to [`research-program.json`](research-program.json) in the same commit — the daliu.github.io "research program" grid is generated from that manifest by `daliu.github.io/scripts/build_patterns_program.py` (run it, or `--check` to gate drift), so the public writeup no longer drifts as branches land. (Cards are accessible public copy, distinct from these technical specs; the H-A2 real-stakes keystone lives in the site's validity section, not the grid.)

**Provenance.** A self-paced extension loop (2026-06-09): "expand and branch out completely, exploring other avenues for tracking or evaluating morals / ethics." Framing inherited from the measurement-under-power / Goodhart / N≈2 thread that produced H9 (`h9-self-calibration.md`) and the Incentive-validity reframe (`validity-threats.md`).

**Framing — the current instrument is one modality.** PoC today measures revealed values from *elicited, hypothetical, low-stakes choices* (scenario layer), compares them to *stated* values (inventory layer) and to *self-predictions* (H9). That is one corner of a larger space. The foundational ecological-validity risk (EV-3) and the stakes discontinuity (EV-4) say the same thing: a single modality cannot carry the whole claim. The avenues below add channels and constructs whose errors are, by design, **uncorrelated** with the scenario layer's — which is the entire point (the multi-method logic, C1). None replaces the core; each is a triangulation leg. Every branch must still honor the load-bearing disciplines: **no composite score** (`concept.md`), **unit discipline / never pool across scales** (`scoring.md` §13.5), **censoring** (§13.2), **N=1 interpretability where it touches the reveal**, and **descriptive-never-prescriptive** (`DECISIONS.md` §6). And every new channel widens the **Incentive-validity** surface (`validity-threats.md` IN-1/IN-2) — each must be auditable for how it games.

---

## A. New measurement modalities (channels beyond elicited scenario-choice)

### A1. Informant / peer prediction — the "moral 360"
- *Construct.* Someone who knows the participant well predicts the participant's revealed choices; the **self-vs-informant prediction gap** is the signal.
- *Anchor.* Vazire 2010 SOKA (informants are *more* accurate than selves on observable evaluative traits — honesty especially); Connelly & Ones 2010 meta; Epley & Dunning 2000 (self-other prediction asymmetry). All three already cited in-repo.
- *Integration.* Reuses the existing scenario items as the prediction target; pairs directly with **H9** — H9 is *self*-predicts-self, A1 is *other*-predicts-self, and the asymmetry between them (informant beats self on the same items) is Epley–Dunning made live and within-instrument. Together they form a 2×2 self/other × predicts/acts calibration matrix.
- *New signal.* Who knows you better than you know yourself, and in which domains. Promotes the Phase-2 "informant validation" plan from a one-shot trait-rating check into a longitudinal measurement channel.
- *Validity risk.* Recruitment burden; informant motivation/accuracy; **privacy** — sharing a user's moral data with a third party is in direct tension with `DECISIONS.md` §7/§10 (must be participant-initiated, consented, local, and never a coercion surface; an informant must never see the participant's own answers, only make a blind prediction).
- *Priority.* **HIGH.** Deepest conversation tie (N≈2 high-bandwidth character-reading) and the credibility moat turned into a live channel. Likely spawns **H-A1**.

### A2. Consequential / real-stakes micro-decisions
- *Construct.* Actual small consequences — real money, real charity allocation, real time-cost, real social commitments — embedded as measurement, not hypotheticals.
- *Anchor.* Bostyn 2018 & FeldmanHall 2012 (hypothetical ≠ real); Abeler et al. 2019 (real-stakes honesty base rates); the EV-3/EV-4 threats name this as the gold standard the instrument otherwise lacks.
- *Integration.* Generalizes `concept.md`'s optional "real-stakes nights" into a first-class, sparsely-sampled channel. The single most direct probe of the **EV-4 stakes discontinuity**: compare a participant's real-stakes choice against their laddered low-stakes prediction (look for a *bend*, per EV-4 detection).
- *New signal.* A within-person low-stakes→real-stakes divergence — the empirical test of the instrument's own extrapolation boundary.
- *Validity risk.* Cost; ethics of inducing real consequences; can only be sampled rarely (so low statistical power); selection (who opts in).
- *Priority.* **HIGH** (attacks the foundational risk directly), but **expensive** — schedule after the cheap analytic branches.

### A3. Moral-language profile (free-text → moral content)
- *Construct.* LLM-coded analysis of the participant's own words (journaling, story prompts) for foundation-invocation, universalizing-vs-particularizing framing, and the gap between values *talked about* and values *acted on* — a **linguistic** stated-revealed gap distinct from the inventory's forced-choice one.
- *Anchor.* Moral Foundations Dictionary (Graham et al.) / LIWC (Pennebaker); narrative identity (McAdams). 
- *Integration.* Deepens the existing story-prompt channel (`inventory/story-prompts.json`, already LLM-coded). Subject to the same κ≥0.70 inter-rater gate before it touches primary analyses (`scoring.md` §5.4).
- *New signal.* What a person *spontaneously* moralizes vs. what they *choose* — a third vertex with the inventory and scenario layers.
- *Validity risk.* LLM-coding reliability; language ≠ value (people moralize fluently about things they don't act on — which is itself the signal, but must not be mistaken for the value); demographic/verbal-fluency confounds.
- *Priority.* **MEDIUM** (extends existing infrastructure).

### A4. Process / decision-dynamics signals
- *Construct.* Not the choice but the *deciding*: deliberation-time distributions, answer revisions/undos, hesitation, re-reads, attention order. Moral cognition as a process.
- *Anchor.* Value-based drift-diffusion models (Hutcherson; Crockett 2014, already cited); mouse-/process-tracing (Freeman & Ambady; Stillman et al. on response conflict). **Caution:** do NOT revive the Greene-style fast=deontological / slow=utilitarian mapping — it doesn't hold (Bago & De Neys 2019, already disclaimed in `concept.md`). Process signals describe *conflict and effort*, not which framework "won."
- *Integration.* Passive capture on existing items (the session log already records `response_time_ms`, `presented_position`, `was_timeout`). Mostly a scoring/analysis addition, little new content.
- *New signal.* *Felt conflict* — distinguishing an easy choice from a hard-won one, even when the choice is identical.
- *Validity risk.* Device/latency noise; over-interpretation; the timer construct (CV-1) interacts with any RT-based measure.
- *Priority.* **MEDIUM** (cheap data, but interpretively treacherous — needs a tight, pre-registered claim).

### A5. Moral-emotion / counterfactual-affect channel
- *Construct.* The affective pull of the *un*chosen option (residual guilt/tension), plus moral elevation and disgust. Distinguishes "chose well easily" from "chose well against a pull."
- *Anchor.* Haidt social-intuitionism; Tangney et al. (guilt vs. shame); counterfactual emotion (Cushman). Taps the **internalized-norms** leg of the conversation's triad — the thing that governs the unwatched solo actor.
- *Integration.* A short post-choice affect probe on a subset of items; resists gaming less than choice itself (you can fake a choice more easily than the report of a pull — though both are gameable).
- *New signal.* Internalization depth — whether a norm merely shapes behavior or is *felt*.
- *Validity risk.* Affect self-report is noisy and demand-prone; alexithymia/cultural display-rule variance; hardest of the modalities to validate.
- *Priority.* **MEDIUM-LOW** but **high novelty** — park until a cheaper branch proves the loop's cadence.

---

## B. New constructs computable from existing (or lightly-extended) data

### B1. Cross-situational moral consistency — variability as a meta-trait → **H10 (proposed)**
- *Construct.* The *variance* of a person's revealed score for one construct across contexts (workplace / family / public / anonymous — surface variation the corpus already enforces) is a **stable individual difference**: some people are principled-invariant, others highly context-driven.
- *Anchor.* The person–situation debate; Mischel & Shoda 1995 (CAPS — *if-then* behavioral signatures); Fleeson 2001 (density-distributions of personality states — people have stable *distributions*, not point traits).
- *Integration.* **Near-free** — pure re-analysis of existing scenario choices (no new elicitation). A new §-level statistic: within-person, within-construct variance across the corpus's surface-context tags, then test whether that variance is itself reliable across the protocol (test-retest of the variance).
- *New signal.* *Moral context-dependence* as a trait — orthogonal to both revealed level and the stated-revealed gap.
- *Validity risk.* Variance confounds measurement error with true variability (needs an error model to separate them — the within-person SE machinery in `scoring.md` §13.1 already exists); the "consistency = virtue" reading is itself a contested value claim (Dancy's particularism — flag, don't smuggle).
- *Priority.* **HIGH** — cheapest, cleanest, fully N=1-computable; the natural first loop branch. → **H10**.

### B2. Moral-circle radius / expansiveness → **H11 (proposed)**
- *Construct.* The radius of moral consideration (self → kin → friends → strangers → out-group → animals → future people), tracked longitudinally.
- *Anchor.* Crimston et al. 2016 Moral Expansiveness Scale (validated); Singer's expanding circle; Cikara/Bruneau parochial-empathy (already anchors the in-group domain).
- *Integration.* Deepens the in-group/out-group domain from a single loyalty axis into a graded *radius* by varying counterparty distance across items; the `circle_radius` secondary axis (`scoring.md` §2.3) is already a stub for this.
- *New signal.* *Where* a person draws the moral boundary, and whether it widens/narrows over time (the conversation's "circle-widening" arc, Marisol, made a measured construct).
- *Validity risk.* WEIRD framing of distance categories; measurement non-invariance across cultures (Atari 2023, already noted).
- *Priority.* **MEDIUM-HIGH** — validated construct; the longitudinal version is the novelty. → **H11**.

### B3. Moral hypocrisy / double-standard gap → **H12 (proposed)**
- *Construct.* The gap between the standard a person applies to *others* (judgment) and to *themselves* (behavior) on matched constructs.
- *Anchor.* Batson et al. 1997/1999 (moral hypocrisy); Valdesolo & DeSteno 2007 (Psych Science — people judge their own transgression more leniently than the identical other's).
- *Integration.* Add a judge-the-other framing to a subset of existing constructs (the act-yourself framing already exists); the gap pairs with H9 (self-prediction) and A1 (informant) to complete a judgment/behavior/prediction triangle.
- *New signal.* Self-leniency — a distinct failure mode from the stated-revealed gap (you can be accurate about your stated values yet hold others to a higher bar).
- *Validity risk.* Order/contamination between the judge-other and act-self items; needs careful separation in the session schedule.
- *Priority.* **MEDIUM-HIGH** — strong theory, pairs naturally with H9. → **H12**.

### B4. Value-change dynamics — rationalization vs. aspiration trajectory
- *Construct.* *How* stated values drift relative to behavior: toward behavior (dissonance-reduction / self-justification) vs. away (aspiration held in tension).
- *Anchor.* Festinger (dissonance); Bem (self-perception). `concept.md` already names the directional read ("stated moving toward revealed = rationalization; away = aspiration").
- *Integration.* Formalize the existing intuition as a trajectory typology over the longitudinal inventory + revealed series.
- *New signal.* The *direction* of value drift as a character signal, not just its magnitude.
- *Validity risk.* Requires long protocols to see drift; regression-to-the-mean artifacts in any two-wave change score.
- *Priority.* **MEDIUM** — depends on longitudinal data accruing.

---

## C. Integration / meta methods

### C1. Multi-method convergence (MTMM)
- *Construct.* Treat the channels (scenario-choice, inventory, calibration, language, peer, real-stakes, emotion) as a **multitrait–multimethod matrix**; *divergence across methods* is diagnostic, not noise.
- *Anchor.* Campbell & Fiske 1959.
- *Integration.* A meta-layer that becomes possible once ≥3 channels exist; reports per-construct convergent/discriminant patterns and flags which constructs are method-bound.
- *New signal.* Construct robustness — which moral signals survive method change and which are artifacts of elicited choice.
- *Validity risk.* Needs the channels built first; cross-method standardization must respect the unit discipline (no forced common scale).
- *Priority.* **MEDIUM** — sequencing-gated (build channels first), but it is the *payoff* that makes the whole branch-out worth more than the sum of channels.

### C2. Adversarial / stress conditions
- *Construct.* Time-pressure or cognitive-load variants to surface the "hot-state" self (the EV-4 discontinuity) within the instrument.
- *Anchor.* Greene et al. 2008 (cognitive load slows utilitarian judgment) — **but** treat dual-process claims cautiously (Bago & De Neys). **Do NOT** build on ego-depletion: the multilab RRR (Hagger et al. 2016) failed to replicate it; any load manipulation must not assume a depletion mechanism.
- *Integration.* A condition flag on existing items; pairs with H9c (stakes-blindness) and EV-4 as another route to the high-stakes self.
- *New signal.* Approximation of the under-pressure self without real stakes.
- *Validity risk.* Manipulation validity; the replication-fragility of the underlying theories; risk of inducing distress (scrupulosity guardrails apply).
- *Priority.* **MEDIUM-LOW** — theoretically fragile; needs a very tight claim.

---

## Roadmap (loop backlog — priority order)

Cheap-and-clean first, expensive-or-fragile last; sequence the meta-layer (C1) after enough channels exist.

1. **H10 — cross-situational moral consistency** (B1). No new elicitation; fully N=1; cleanest falsifiable hypothesis. ✓ **done** — [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md) (iteration 2).
2. **H-A1 — informant/peer prediction** (A1). Biggest true "branch out"; completes the self/other × predict/act matrix with H9. ✓ **done** — [`h-a1-informant-prediction.md`](h-a1-informant-prediction.md) (iteration 3).
3. **H12 — moral hypocrisy / double-standard** (B3). Pairs with H9; light authoring (add judge-other framings). ✓ **done** — [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md) (iteration 4).
4. **H11 — moral-circle radius** (B2). Validated construct; deepens the in-group domain; `circle_radius` stub already exists. ✓ **done** — [`h11-moral-circle-radius.md`](h11-moral-circle-radius.md) (iteration 5).
5. **A2 — consequential real-stakes channel.** Gold standard for EV-3/EV-4; expensive, so after the cheap branches. ✓ **done** — [`h-a2-real-stakes.md`](h-a2-real-stakes.md) (iteration 6, the keystone validity probe; Phase-2, cohort-level not N=1).
6. **A3 — moral-language profile.** Extends the story-prompt channel. ✓ **done** — [`h-a3-moral-language.md`](h-a3-moral-language.md) (iteration 7; MVP-1 exploratory, κ≥0.70-gated; unlocks C1 as the 3rd channel).
7. **C1 — multi-method convergence.** Gated on ≥3 channels existing — now unblocked (inventory + language + behavior). ✓ **done** — [`c1-multimethod-convergence.md`](c1-multimethod-convergence.md) (iteration 8, the MTMM capstone; cohort matrix + N=1 profile; no public card).
8. **A4 / A5 — process & emotion signals.** High novelty, high noise; need tight pre-registered claims. ✓ **done** — [`h-a4-a5-process-emotion.md`](h-a4-a5-process-emotion.md) (iteration 9; MVP-1 exploratory; A5 gets a design-stage card, A4 is a no-card analysis adjunct).
9. **B4 — value-change dynamics.** Gated on longitudinal data. ✓ **done** — [`b4-value-change-dynamics.md`](b4-value-change-dynamics.md) (iteration 10; Phase-2; RI-CLPM; design-stage card).
10. **C2 — adversarial/stress conditions.** Theoretically fragile; build last, carefully. ✓ **done** — [`c2-stress-conditions.md`](c2-stress-conditions.md) (iteration 11; Phase-2 exploratory, valid only on convergence with H-A2/H9c; no card). **← Round 1 complete (all 10 items).**

**Checked off:** B1 → **H10** (it. 2); A1 → **H-A1** (it. 3, Phase-2); B3 → **H12** — `h12-moral-hypocrisy.md` (it. 4, MVP-1 + §16-unlock); B2 → **H11** — `h11-moral-circle-radius.md` (it. 5, MVP-1 re-analysis); A2 → **H-A2** — `h-a2-real-stakes.md` (it. 6, Phase-2 keystone); A3 → **H-A3** — `h-a3-moral-language.md` (it. 7, MVP-1 exploratory, κ-gated); C1 → **MTMM capstone** — `c1-multimethod-convergence.md` (it. 8, analysis layer, no card); A4/A5 → **process + moral-emotion** — `h-a4-a5-process-emotion.md` (it. 9, A5 carded); B4 → **value-change dynamics** — `b4-value-change-dynamics.md` (it. 10, 2026-06-22, Phase-2, RI-CLPM, carded). Locks pending Dave's review. **Round 1 complete — all 10 items drafted (H10/H12/H11/H-A1 constructs · H-A2 real-stakes · H-A3 language · C1 MTMM capstone · A4/A5 process+emotion · B4 value-drift · C2 stress). The 15-min loop (cron `8819f3b8`) now extends the map (Round 2 below), one avenue per iteration, until genuinely dry — at which point the real constraint becomes build/validate (IRB, co-PI, runtime, κ-validation), not design.**

---

## Round 2 — candidate new avenues (beyond the original map)

Round 1 (the 10 items above) is complete. These are genuinely new, validated, ethics-measurement constructs **distinct from every Round-1 branch**, curated as the self-extending loop's next backlog (one per iteration, same rigor + disciplines + the facet-vs-method card judgment). Priority roughly by cheapness/cleanness.

- **R1. Moral identity centrality** ✓ **done** — [`r1-moral-identity-centrality.md`](r1-moral-identity-centrality.md) (iteration 13; the meta-moderator; internalization vs symbolization; R1c moderates the §6 gap / H10 / H11 / H12; carded). Aquino & Reed 2002 (already in references).
- **R2. Sacred / protected values** ✓ **done** — [`r2-sacred-protected-values.md`](r2-sacred-protected-values.md) (iteration 12; re-reads the censored cost-of-virtue `never`s as the protected-value set; R2b protected≠expensive via quantity-insensitivity + a taboo marker; carded). Baron & Spranca 1997; Tetlock taboo-tradeoffs.
- **R3. Moral disengagement** ✓ **done** — [`r3-moral-disengagement.md`](r3-moral-disengagement.md) (iteration 14; Bandura's 8 mechanisms; R3b decouples the gap from guilt — the A5 negative pole; the load-bearing justification-vs-disengagement discriminant; carded). Bandura 1999/2002; Moore et al. 2012.
- **R4. Moral attentiveness** — the chronic tendency to *perceive* the moral dimension of everyday life (Reynolds 2008, JAP). A perceptual front-end: do you even notice the ethical stakes? Measurable via what you spontaneously flag as moral (A3) + reaction to embedded moral content. ← *next*
- **R5. Moral typecasting / dyadic structure** — how you parse a situation into agent (doer) vs. patient (victim) (Gray & Wegner; Gray, Young & Waytz 2012). The *structure* you impose on moral scenes, not the choice — the most speculative of the five.

Each still owes the unit / N=1 / censoring / no-composite / value-neutral disciplines and the fraud/non-replication exclusions.

---

## Cross-references
- [`concept.md`](concept.md) — the three-layer architecture these branches extend; the anti-patterns and operating constraints they must honor
- [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md), [`h9-self-calibration.md`](h9-self-calibration.md) — the design-doc template each new branch follows; H9 pairs with A1/B3
- [`validity-threats.md`](validity-threats.md) — EV-3/EV-4 (why one modality is insufficient), IN-1/IN-2 (every new channel widens the gaming surface)
- [`scoring.md`](scoring.md) §2.3 (`circle_radius` stub → B2), §13 (N=1 within-person machinery → B1), §13.5 (unit discipline all branches obey)
- [`DECISIONS.md`](DECISIONS.md) §6/§7/§9/§10 (constraints), §16/§17 (corpus locks any new-content branch must respect)
- [`pre-registration.md`](pre-registration.md) — where H10–H12 land as they're drafted
