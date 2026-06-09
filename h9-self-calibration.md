# H9 — Self-prediction calibration (do you know your own gap?)

**Status:** Design proposal, drafted 2026-06-08. Source document for downstream changes to `concept.md`, `pre-registration.md`, `scoring.md`, `DECISIONS.md`, and `validity-threats.md`. The hypothesis is being floated for pre-registration alongside H1–H8; this document is the proposal those downstream docs will draw from. Mirrors the structure of [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md).

**Provenance.** A June 2026 design conversation extending the project's revealed-vs-stated premise with two ideas from outside moral psychology: the *measurement-under-power* problem (you cannot observe how a person behaves with stakes/power until they have them, and acquiring them changes the person) and *calibration scored over a track record* (Tetlock's forecasting work — judgment measured by how well predictions match later outcomes). Pointed inward, those produce one observation the current instrument does not capture:

> The instrument measures the **size** of a person's stated–revealed gap. It does not measure their **awareness** of it. Two participants with an identical gap are different people if one foresaw their own slip and the other was blindsided — one has self-knowledge and a hard problem, the other has a self-deception problem, and the (MVP-2) intervention layer should treat them oppositely.

H9 adds that second axis: **self-prediction calibration** — how well a participant predicts their own revealed choices. It is a NOVEL measurement claim (longitudinal self-behavior calibration inside a values instrument), not an import from standard psychometrics. Drafted at Dave's direction.

---

## 1. The hypothesis statement

**H9 (proposed addition to `pre-registration.md` §6, secondary).**

*Participants systematically over-predict their own alignment with their stated values; this self-prediction error is a stable individual difference distinct from the stated–revealed gap and from revealed level; and it is largest where stakes are highest.*

### 1.1 Measurement primitive

For a designated **calibration probe** `p`, the participant first records a *non-binding prediction of their own choice* (the prediction beat, §3), then later makes the actual choice. Both resolve to the same primary-axis scale as any revealed item (`scoring.md` §2.2, range [−1,+1]); for cost-of-virtue probes both resolve to a predicted/actual break-point rung (`scoring.md` §4).

For participant *i* and probe *p*:

```
pred_i^p = predicted primary-axis score (or predicted break-point), elicited before resolution
rev_i^p  = actual revealed primary-axis score (§2) or revealed break-point (§4)
e_i^p    = pred_i^p − rev_i^p          # signed calibration error
```

`e_i^p > 0` means the participant predicted a more axis-positive (more honest / generous / trusting) choice than they made. The four MVP-1 primary axes are oriented with the consensually-prized pole positive for three domains (truth-telling→honesty, resource-allocation→generosity, reciprocity→trust); the in-group axis (loyalty +, universalism −) has a **value-contested** positive pole, so it is excluded from the signed H9a test and entered as exploratory only (see §1.6).

**Person-level indices** (both within-person; see §1.5 on N=1 validity):

```
cal_bias_i  = mean_p e_i^p       # signed self-enhancement bias
cal_error_i = mean_p |e_i^p|     # magnitude (inverse self-knowledge)
```

### 1.2 H9a — the self-enhancement prediction bias

Across participants, mean signed error is positive: people predict more value-aligned behavior than they reveal (the Epley & Dunning 2000 "holier-than-thou" prediction effect, replicated in this instrument and on socially-valued axes).

**Test statistic:** lower 95% bootstrap-CI bound of `mean_i cal_bias_i` ≥ **0.10** (axis units), computed over the three consensual-pole domains. Spearman-free; this is a mean, bootstrapped at participant level (10,000 resamples, seed `20260510`, identical to `scoring.md` §8).

### 1.3 H9b — calibration is a distinct, stable axis

Two parts, both required to claim "new axis, not a relabeling":

- **Stability.** Split-window test–retest of `cal_error_i` (first-half vs second-half sessions) has lower 95% CI ≥ **0.40**. (Deliberately modest: a second-order derived quantity is noisier than a first-order score; contrast `scoring.md` H3's 0.60.)
- **Discriminant.** `cal_error_i` is not redundant with the §6 gap or revealed level: in a regression of `cal_error_i` on [`gap_i`, `revealed_level_i`], the model R² has **upper** 95% CI < **0.50** — i.e. at least half the calibration variance is not explained by how big the gap is or how virtuous the person acts.

### 1.4 H9c — the stakes-blindness signature (the load-bearing one)

Within-person, self-prediction error magnitude is **larger on high-stakes probes than low-stakes probes**:

```
blind_i = mean|e_i^p| over high-stakes probes  −  mean|e_i^p| over low-stakes probes
```

**Test statistic:** lower 95% bootstrap-CI bound of `mean_i blind_i` > **0** (one-sided; no fixed magnitude floor — the directional claim is the prediction). High-stakes pool = cost-of-virtue probes + the H8b attachment-laden pairs; low-stakes pool = H8a low-stakes pairs + matched quick-fire. A participant enters H9c only with ≥1 valid error in each pool.

This is the behavioral fingerprint of the measurement-under-power problem: people mispredict themselves *most* precisely where the high-stakes self diverges from the low-stakes self. **H9c confirming is direct evidence for `validity-threats.md` EV-4** (the stakes/power discontinuity) — the instrument measures its own most dangerous extrapolation boundary. See §8.

### 1.5 Why these are N=1-interpretable (a design win)

Unlike the §6 gap — which crosses the card-sort [0,1] scale and the revealed [−1,+1] scale and therefore needs sample-level z-standardization (≥2 users; see `interpretation.md` "Single-user domains") — calibration compares **predicted-axis vs revealed-axis on the *same* pre-defined scale**, and the cost-of-virtue version compares **predicted vs actual dollars** on an external absolute scale. No cross-scale or cross-person standardization is required. `cal_bias_i` and `cal_error_i` are therefore meaningful for a single user, like the `scoring.md` §13 ipsative reads — but unlike §13 (which only re-orders signals the user already produced) calibration adds genuinely *new* information: self-knowledge. This makes it a rare signal eligible for the personal reveal **without cohort norms** (relevant to `runtime-architecture.md` §10 decision #1, the "reveal needs cohort computation" constraint — calibration sidesteps it).

### 1.6 Falsification and partial results

The combined H9 claim requires **H9a ∧ H9b ∧ H9c**. Partial results are reported and published (as with H8): "people over-predict their virtue but calibration is not separable from the gap" (H9a∧¬H9b), "calibration is a stable trait but unbiased" (¬H9a∧H9b), "blindness concentrates at high stakes but the global bias is null" (H9c∧¬H9a), etc. The in-group domain's signed-bias result and the **exploratory H9d** below are reported descriptively regardless.

**Exploratory H9d (MVP-2 hook, not tested confirmatorily in MVP-1).** Self-prediction error shrinks with use — the longitudinal slope of `|e_i^p|` over sessions is negative (the mirror teaches self-insight). MVP-1 is measurement-only (`DECISIONS.md` §2) and cannot separate practice from a genuine self-knowledge gain, so H9d is exploratory here and becomes a candidate **primary intervention outcome** for MVP-2.

---

## 2. Theoretical grounding

### 2.1 Self–other prediction asymmetry (Epley & Dunning 2000)

"Feeling holier than thou": people robustly over-predict the morality/generosity of *their own* future behavior while predicting *others'* behavior accurately, because they forecast the self from an idealized self-concept and others from base rates. This is the direct anchor for H9a — and it predicts the asymmetry should be *largest* on the value-laden choices PoC is built from. Carlson 2013 (self-knowledge review) and Vazire 2010 SOKA (already cited in `validity-threats.md` EV-3 / Phase-2 informant rationale) place the same self-insight limit at the center of the field; H9 is the within-instrument operationalization of it.

### 2.2 Projection bias and the hot–cold empathy gap (Loewenstein 1996, 2005; Loewenstein, O'Donoghue & Rabin 2003)

People predicting in a "cold" (low-arousal, low-stakes) state systematically fail to anticipate "hot"-state behavior, because they project the current state onto the future self. This is the mechanism behind H9c: the cold, deliberative ladder-prediction cannot reach the hot, stakes-laden actual choice — so error grows with stakes. It also makes H9c's prediction *directional and a priori*, not post-hoc.

### 2.3 Calibration over a track record (forecasting / Tetlock)

The forecasting literature scores judgment not by a single guess but by calibration across many resolved predictions. H9 imports that move, pointed at the self: a participant's `cal_error_i` is a calibration score over their own resolved self-predictions accumulated longitudinally. This is also why H9 is naturally a PoC hypothesis and not a one-shot survey item — calibration *needs* the repeated-measures spine the instrument already has.

### 2.4 What this is a threat to, and what it strengthens

H9 does not replace any existing construct; it sits orthogonal to the gap. But it bears on two existing rows of `validity-threats.md`: it supplies a behavioral test for **EV-4** (stakes discontinuity; §8), and it gives **IN-2** (self-gaming) a detector — anomalously *perfect* calibration is a self-gaming flag (a user performing their ideal predicts and produces the ideal), see `validity-threats.md` IN-2.

---

## 3. Instrument modification required to test H9

The design is deliberately economical: H9 piggybacks on corpus that already exists or is already planned, and adds one runtime beat plus a scoring section. No new domain content is required.

### Already in place
- **Cost-of-virtue probes** (`scoring.md` §4; 3 per domain × 4 = 12). The single highest-value calibration site: the ladder structure lets a *predicted* break-point be elicited on the identical rungs as the *actual* one.
- **H8 paired narrative-vs-abstract probes** (`scenarios/h8-probe-pairs.json`, ~8–12 pairs, low- and high-stakes pools). These already separate low- vs high-stakes constructs within-subject — exactly the contrast H9c needs. H9 reuses the same manifest and pools.
- **Append-only session log** (`scoring.md` §1.1) — a new event type for the prediction beat slots in without disturbing existing projections (`runtime-architecture.md` §18 event-sourcing).

### What needs to be added

**A1. The prediction beat.** Before a calibration probe resolves, a one-screen *non-binding self-prediction* on the same response surface as the eventual choice:
- *Cost-of-virtue form (primary):* "Before you start — at what amount do you think you'll switch?" on the identical rung ladder. Yields `predicted_breakpoint` directly comparable to the revealed break-point (`scoring.md` §4).
- *Choice form (for H8-paired and quick-fire calibration items):* "Which do you think you'll choose?" on the same options, recorded as a predicted primary-axis score.

The beat is **counterbalanced and not universal** — see A3 (reactivity control). Logged as a new `prediction` event `{user_id, session_id, probe_id, predicted_option_id | predicted_rung, timestamp_iso}`.

**A2. Calibration scoring spec.** New `scoring.md §14` operationalizing `e_i^p`, `cal_bias_i`, `cal_error_i`, the H9a/H9b/H9c statistics, and — critically — the **censoring discipline** inherited from §13.2/§13.3: if either the predicted or the actual cost-of-virtue endpoint is `"never"` (right-censored), the signed error is **suppressed, never made finite**; the pair is reported categorically (predicted-never/acted-never/mismatch-direction) only. A finite `e` is admissible solely when both endpoints are measured prices on an identical rung ladder and shared axis direction (same gate as a §13.3 delta).

**A3. Reactivity control (load-bearing — see §6).** Eliciting a prediction can change the subsequent choice (question–behavior / mere-measurement effect; Sherman 1980; Spangenberg & Greenwald 1999). A counterbalanced subset of comparable probes receives **no** prediction beat. Revealed behavior on predicted vs non-predicted items is contrasted (between-subject on matched probes, or within-subject across matched probes) to estimate and remove the reactivity component before H9 scoring. If prediction shifts behavior toward stated values, that is both a confound to net out *and* an MVP-2 intervention candidate (predicting yourself increases consistency) — the same dual framing as H8.

---

## 4. Implications for existing locked decisions

**`DECISIONS.md` §16 / §17 corpus.** H9 adds **no new scenarios** — it adds a prediction beat to existing cost-of-virtue and H8 probes. The §16 corpus lock is therefore *not* touched by H9 (contrast §17, which unlocked it for H8's paired probes). Only the runtime, scoring, and pre-registration change.

**`DECISIONS.md` §19 — LOCKED 2026-06-08.** "Add H9 (self-prediction calibration) to MVP-1 as a secondary hypothesis; reuse the cost-of-virtue + H8 paired-probe corpus via a counterbalanced prediction beat; no corpus expansion." Rationale parallels §17's "one cohort, one publication" logic, plus H9's near-zero authoring cost and N=1-computability. See `DECISIONS.md` §19 for the full ADR (including the unit-consistency reconciliation that routes cost-of-virtue calibration to a separate convergent read, `scoring.md §14.5`).

**Pre-registration.** H9 becomes the 9th hypothesis, **secondary** (reported with effect sizes/CIs; never a gate-criterion — the H1/H2/H3 primary gate is unchanged). H9a/H9b/H9c thresholds lock at OSF filing.

**Reveal (`runtime-architecture.md` §10).** Because calibration is N=1-computable (§1.5), it can enter the personal reveal without the cohort-norms artifact the §6 gap requires. This is a genuine simplification for the pilot reveal and worth noting in the runtime open-decisions list.

**Statistical multiplicity (`validity-threats.md` SV-1).** Three new secondary statistics; folded into the Holm-Bonferroni secondary-set reporting already specified.

---

## 5. Why this is a research contribution, not just a feature

Self-insight limits are well-documented as a *one-shot* laboratory phenomenon (Epley & Dunning 2000; Vazire 2010). What is not in the literature is a **longitudinal, within-person calibration of self-predicted vs revealed ethical behavior** that (a) tracks whether self-knowledge is a stable trait, (b) localizes mispredict-yourself error to high-stakes contexts as a signature of the hot–cold gap, and (c) can test whether the error shrinks with sustained reflective practice (H9d, MVP-2). If H9a–c hold, PoC reports something no existing instrument does: not just *who you are vs who you say you are*, but *how well you know the difference* — and where your self-knowledge fails worst. That third number is, for the user, often the most actionable one, and for the field a new individual-difference construct with a pre-registered measurement model.

---

## 6. Open design questions

**Q1. Prediction placement — RESOLVED (provisional): immediately-before, same-session, for cost-of-virtue; cross-session for the future-self variant deferred.** The cleanest comparable prediction is on the identical cost-of-virtue ladder immediately before laddering (no item-matching problem). A *future-self* prediction ("next time you face this, what will you do?") matched to a later session's item is higher-validity for projection bias but introduces an item-matching burden; deferred to a possible H9-extension, not MVP-1.

**Q2. Reactivity-control allocation — OPEN.** Between-subject (cleanest causal estimate of reactivity, costs power) vs within-subject matched (more power, risks carryover). Provisional: within-subject matched pairs for cost-of-virtue, between-subject split for the quick-fire calibration set. Resolve before lock; pilot informs.

**Q3. Prediction response surface granularity — OPEN.** Predict an exact rung/option, or a coarser band ("early / middle / hold out")? Exact maximizes resolution; bands reduce noise and may better match how people actually represent their own future choices. Reserved for `scoring.md` §14 iteration; pilot exit interview asks which felt answerable.

**Q4. Does the prediction beat threaten the quick-fire timer construct?** The 8-second quick-fire timer (`validity-threats.md` CV-1) compresses deliberation; adding a prediction beat to quick-fire items could break that. Provisional: prediction beats attach to cost-of-virtue and narrative probes (untimed) only; quick-fire calibration, if any, uses a separate untimed prediction administered apart from the timed item. Resolve before lock.

**Q5. In-group domain signed bias.** Because the loyalty/universalism axis lacks a consensual desirable pole, H9a excludes it (§1.1). Open whether a *participant-anchored* orientation (sign the axis toward each participant's own stated pole) rescues a signed test for that domain without smuggling the researcher's value-direction. Reserved; exploratory for now.

---

## 7. Downstream changes this design unblocks

When the H9 framework is confirmed (next iteration), the following become actionable — applied iteration-by-iteration, not in this doc:

1. `pre-registration.md` §6 — add H9 (H9a/H9b/H9c) to the secondary hypotheses table; §5 — add the prediction-beat analysis plan and the reactivity-control contrast
2. `scoring.md` §14 — operationalize `e`, `cal_bias`, `cal_error`, the three statistics, and the censoring discipline
3. `DECISIONS.md` §19 — lock the H9-in-MVP-1 decision and the no-corpus-expansion note
4. `concept.md` — add a "Self-prediction calibration" subsection under the measurement layer; note the N=1-reveal property
5. `validity-threats.md` — EV-4 and IN-2 already cross-reference H9 (added in the same iteration as this doc); add a CV-style row for prediction reactivity once §14 lands
6. `scenarios/` + runtime — the `prediction` event type, the beat UI, and the counterbalancing schedule
7. `pilot-protocol.md` — exit-interview items for Q3 (band vs exact) and Q4 (timer interaction); calibration-beat realness check
8. `types.ts` — `PredictionLogEntry` event type (append-only, user-keyed, timestamped — conforms to `runtime-architecture.md` §18)

---

## 8. Relationship to H8 and to validity-threats EV-4

- **Shared corpus with H8.** H9 reads the same `scenarios/h8-probe-pairs.json` pools (low-stakes → H9c low pool; high-stakes attachment-laden → H9c high pool). The marginal authoring cost of H9 over H8 is essentially zero; the marginal runtime cost is the prediction beat. Where a participant has both an H8 divergence `D_i^p` and a self-prediction `pred_i^p` on the same pair, the two **decompose** the narrative shift into a *foreseen* component (the participant predicted it) and a *surprised-me* component (`D` not anticipated by `pred`) — a finer reading than either hypothesis alone, reported as exploratory.
- **Evidence for EV-4.** `validity-threats.md` EV-4 (the stakes/power discontinuity) predicts that low-stakes choices are not merely noisy predictors of high-stakes behavior but categorically different. H9c is its behavioral fingerprint: if self-prediction error concentrates at high stakes, the high-stakes self is demonstrably not reachable from the low-stakes self by extrapolation — which is what EV-4 asserts. H9c confirming raises the residual risk attached to any high-stakes claim; H9c null *lowers* it. Either way the instrument measures its own extrapolation boundary, which is the honest thing for it to do.
- **Detector for IN-2.** Self-gaming (performing one's ideal) produces predicted≈actual≈ideal, i.e. anomalously low `cal_error`. H9 thus gives the Incentive-validity audit a quantitative flag it otherwise lacks.

---

## Cross-references

- [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md) — sibling design doc; shared paired-probe corpus
- [`validity-threats.md`](validity-threats.md) EV-4 (stakes discontinuity), IN-1/IN-2 (incentive validity) — the rows H9 tests / detects
- [`scoring.md`](scoring.md) §4 (cost-of-virtue), §6 (gap convention), §13.2–§13.3 (censoring discipline H9 inherits) — where §14 will be added
- [`concept.md`](concept.md) — measurement layer; cost-of-virtue as "the single most useful signal"
- [`DECISIONS.md`](DECISIONS.md) §2 (measurement-only MVP-1, hence H9d exploratory), §16/§17 (corpus; untouched by H9), §19 (proposed)
- [`runtime-architecture.md`](runtime-architecture.md) §10 (reveal cohort-norms constraint H9 sidesteps), §18 (event-sourcing the prediction beat conforms to)
