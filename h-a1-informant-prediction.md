# H-A1 — Informant prediction (the "moral 360")

**Status:** Design proposal, drafted 2026-06-10 (extension loop, iteration 3). Develops branch **A1** of [`measurement-avenues.md`](measurement-avenues.md) — the first *modality* branch (a new channel, not a re-analysis of the scenario layer). Labeled **H-A1** to mark it as the A-series (modality) line, distinct from the B-series construct hypotheses (H10–H12) that ride the main integer sequence. **Phase-2 / MVP-2 scope** (informant recruitment is a Phase-2 burden; see §4). The lock is Dave's call — this is the rigor-bar spec the loop produces.

**Provenance.** Branch A1, and the deepest tie to the moral-systems conversation that seeded this project: **character-reading works at N≈2** — high-bandwidth, repeated, contextual observation by someone who knows you. PoC is otherwise solipsistic (a single user judging themselves). H-A1 adds the *other* who knows the participant well, as a live measurement channel, and asks the question H9 set up but could not answer alone: **does someone who knows you predict your moral choices better than you predict yourself?** (Vazire's self–other knowledge asymmetry says: for observable, evaluative traits — honesty above all — *yes*.)

**Not the existing informant-convergence check.** `pre-registration.md` already has a Phase-2 "informant convergence" secondary: an informant *rates the participant's traits* (HEXACO/values) to **validate the instrument**. H-A1 is orthogonal and additive: an informant *predicts the participant's specific revealed choices*, item by item, as a **new measurement channel**, and the **self–informant asymmetry** is a new construct. Trait-rating validates; choice-prediction measures.

---

## 1. The hypothesis statement

**H-A1 (proposed Phase-2 secondary).**

*Someone who knows the participant well predicts the participant's revealed choices with above-chance distinctive accuracy; for observable, evaluative domains this informant accuracy exceeds the participant's own self-prediction accuracy (the SOKA asymmetry); and informant accuracy scales with relational bandwidth.*

### 1.1 Measurement primitive and the self/other × predict/act matrix

For participant *i*, informant *j* (one of i's recruited informants), and item *p*: the informant makes a **blind prediction** `pred_{j→i}^p` of i's choice — seeing only the scenario, never i's actual answer — scored on the same primary axis (§2.2) as any revealed item. i's realized choice is `rev_i^p`. The participant's own self-prediction `pred_{i→i}^p` is the H9 prediction beat (`scoring.md` §14).

This completes the matrix H9 opened:

|                         | predicts SELF (target = i)        | acts (i's revealed)     |
|-------------------------|-----------------------------------|-------------------------|
| **SELF** is the predictor  | `pred_{i→i}^p` — H9 self-calibration | `rev_i^p`               |
| **OTHER** (informant) predicts | `pred_{j→i}^p` — **H-A1**          | `rev_i^p`               |

The cell of interest is the *difference* between the two predictors of the same behavior.

### 1.2 Distinctive vs. normative accuracy (the load-bearing decomposition)

"Accuracy" must not be the base rate in disguise. An informant who simply predicts "most people are honest" scores well on honesty items without knowing *this person* at all (Cronbach 1955; Funder 1995, Realistic Accuracy Model). So every accuracy below is **distinctive** — predicting the participant's *deviations from the norm*, with the normative component partialled out and reported separately, never conflated.

Let `norm^p = mean_i rev_i^p` (the cohort-average revealed score on item *p*). Then:

```
rev_i^p*       = rev_i^p       − norm^p          # i's deviation from the norm
pred_{j→i}^p*  = pred_{j→i}^p  − norm^p          # informant's predicted deviation
dacc(j→i)      = corr_p( pred_{j→i}^p* , rev_i^p* )   # DISTINCTIVE accuracy (per informant–target pair)
nacc(j→i)      = corr_p( pred_{j→i}^p  , norm^p )     # normative accuracy — reported, never pooled with dacc
```

The same decomposition applied to H9 yields distinctive self-accuracy `dacc(i→i) = corr_p(pred_{i→i}^p*, rev_i^p*)`.

> **Cohort dependency (honest scope note).** Unlike H9 and H10, distinctive accuracy is **not N=1** — `norm^p` requires the cohort. What *is* N=1 is informant **consensus** (§1.4: do my informants agree with each other?), which needs no norm. So H-A1's reveal offers an N=1 consensus read plus a cohort-anchored distinctive-accuracy read; the SOKA statistics (§1.3) are cohort-level. This is an intrinsic property of cross-person accuracy constructs, not a design shortfall.

### 1.3 H-A1a — informant validity; H-A1b — the SOKA asymmetry (core)

**H-A1a (the channel carries distinctive signal).** Informants predict participants' idiosyncratic deviations above zero, and above the participant's *stated* values used as a predictor (an informant who beats the participant's own questionnaire is reading behavior, not parroting reputation):
```
H-A1a:  lower 95% bootstrap-CI bound of  mean_{i,j} dacc(j→i)  > 0      (and a reported margin over a stated-values baseline)
```

**H-A1b (others know your morality better than you do — the headline).** For observable, evaluative domains (truth-telling/honesty foremost; SOKA's strongest case), informant distinctive accuracy exceeds self distinctive accuracy:
```
Δ_SOKA(i) = mean_j dacc(j→i) − dacc(i→i)
H-A1b:  lower 95% bootstrap-CI bound of  mean_i Δ_SOKA(i)  > 0,  concentrated in high-observability/high-evaluativeness domains
```
Predicted gradient (pre-registered direction, not just sign): `Δ_SOKA` largest for truth-telling (highly observable + highly evaluative), smaller for domains whose construct is more internal/less evaluative. A *uniform* `Δ_SOKA` across domains would point to a global self-deprecation or informant-halo artifact rather than the SOKA structure — so the **gradient is itself a test**, as the H8a domain-gradient is for bandwidth-restoration. Bootstrap per `scoring.md` §8, seed `20260510`.

### 1.4 H-A1c — consensus vs. self-insight (the blind-spot signature)

With ≥2 informants, **consensus** is the agreement among informants about what i would do (Kenny 1994, Social Relations Model: target variance). Per participant–domain, contrast informant `consensus_i(d)` against the participant's own self-prediction accuracy `self_acc_i(d)` (H9). The reveal-facing construct is the **blind-spot map**: domains where consensus is *high* but self-accuracy is *low* are **legible-to-others, opaque-to-self**.
```
H-A1c:  across participants, consensus and self-accuracy are dissociable — corr( consensus_i , self_acc_i ) upper 95% CI < 0.50
```
(If they were redundant, "others see what you see"; the dissociation is what makes a blind spot a blind spot.) The within-person ranking of `(consensus_i(d) − self_acc_i(d))` names the participant's blind-spot domains.

### 1.5 N=1, value-neutrality, and the wellbeing constraint

- **N=1 vs cohort.** Informant *consensus* is N=1 (within-person, ≥2 informants, no cohort). *Distinctive accuracy* and *SOKA* need the cohort norm (§1.2). The reveal renders consensus and the blind-spot map descriptively; no composite "self-awareness score" (`concept.md`).
- **Value-neutrality.** Being more legible to others than to yourself is **described, not graded** — it is not framed as a deficiency. (Some opacity-to-others is privacy, not pathology.)
- **Wellbeing (load-bearing).** "Others see your morality more clearly than you do" is a heavy reveal. It is strictly opt-in, contemplatively framed, behind the scrupulosity guardrails (`concept.md` §"Risks to vulnerable users"), and never delivered as a verdict.

### 1.6 Falsification and exploratory H-A1d

Combined H-A1 = **H-A1a ∧ H-A1b** (the channel works *and* shows the asymmetry). H-A1c is the reveal-construct (dissociation reported either way). Partial results published, as with H8/H9/H10.

**Exploratory H-A1d — accuracy scales with relational bandwidth (the direct N≈2 test).** The moral-systems conversation's central empirical claim was that character-reading is reliable *in proportion to bandwidth* — duration, closeness, shared context, the shadow of the future. H-A1d tests it head-on:
```
H-A1d:  over informant–target pairs,  corr( dacc(j→i) , relational_bandwidth_{j,i} )  > 0
```
with `relational_bandwidth` from informant-reported closeness/duration/co-residence/contexts-shared (IOS scale, Aron et al. 1992, already in the repo's references). If accuracy does *not* rise with bandwidth, the N≈2 thesis is wrong for *moral* prediction specifically — a publishable null. Exploratory in Phase-2 (pair-level, non-independent).

---

## 2. Theoretical grounding

- **Self–other knowledge asymmetry (Vazire 2010 SOKA; Carlson 2013).** Others are *more* accurate than the self on traits that are both **observable** and **evaluative** — honesty-humility is the canonical example, and it is exactly PoC's flagship domain. This is the engine of H-A1b and predicts its domain gradient. Already cited in-repo (EV-3, Phase-2 rationale).
- **Self–other prediction asymmetry (Epley & Dunning 2000).** People over-predict their own virtue (this is H9a); the corollary is that a third party, forecasting from the base rate rather than an idealized self-image, can do better. H-A1 is the other half of the Epley–Dunning effect that H9 only half-measured.
- **Realistic Accuracy Model + the Cronbach components (Funder 1995; Cronbach 1955).** Accuracy decomposes; distinctive ≠ normative. §1.2 is non-negotiable because of this literature — it is the single most common way "informants are accurate" claims are inflated.
- **Informant validity for behavior (Connelly & Ones 2010).** Multi-informant ratings predict consequential behavior better than self-report for honest/conscientious/agreeable conduct — the empirical license to treat informant prediction as a *measurement*, not just a check. **Caveat (honest):** that meta is about *trait ratings* predicting *aggregated behavior*; predicting *specific item-level choices* is a thinner literature, so H-A1a is genuinely exploratory at the item grain.
- **Social Relations Model (Kenny 1994).** The round-robin decomposition that lets §1.4 separate consensus (target variance) from informant bias (perceiver variance) — needed to read consensus cleanly with ≥2 informants.

---

## 3. Instrument modification required

### Already in place
- The full scenario corpus (the prediction targets) and the per-item axis scoring (§2) — informants predict on the *same* items, scored the *same* way.
- The H9 prediction beat and `scoring.md` §14 — supplies `pred_{i→i}` and `dacc(i→i)` for the SOKA contrast; the reactivity control (§14.6) matters here (see §6).
- The Aron IOS closeness scale (repo references) for `relational_bandwidth` (H-A1d).

### What needs to be added
- **A1. The informant module + blind-prediction flow.** A participant-initiated invite; the informant completes a bounded set of the participant's items in "predict what they'd do" mode, seeing only the scenario. A new event `InformantPredictionLogEntry {informant_id (pseudonymous), target_user_id, item_id, predicted_option_id, relationship_meta, timestamp}` — append-only, conforming to `runtime-architecture.md` §18.
- **A2. Distinctive-accuracy scoring (`scoring.md §16`, proposed).** `norm^p`, `dacc`/`nacc`, `Δ_SOKA`, consensus (SRM), the §1.4 dissociation, H-A1d — **parity-gated** like the rest (must agree across `poc-projection.js` and `analyze.py` via `make check`; consensus/raw reads can be on-device, the norm-dependent reads are analyzer-side).
- **A3. The privacy & consent architecture (§7)** — the gating requirement; without it the module must not ship.

No new scenarios; the corpus is untouched (§16/§17 locks hold).

---

## 4. Implications for existing locked decisions

**Phase-2 / MVP-2, not MVP-1.** Informant recruitment is a separate burden the MVP-1 cohort can't carry at power; the repo already slots informant work in Phase-2. H-A1 is **piloted opt-in in MVP-1** (a handful of participants recruit informants to calibrate the flow and the item-budget) and **powered in Phase-2**. This differs from H9/H10 (MVP-1) and is the honest call.

**Corpus untouched.** No new scenarios (contrast §17). Only a module, scoring §16, and pre-registration change.

**Proposed `DECISIONS.md` entry (pending Dave's lock).** "Add H-A1 (informant choice-prediction channel) as a Phase-2 secondary; participant-initiated, blind, local-first informant module; distinctive-accuracy + SOKA-asymmetry + consensus scoring (§16); no corpus expansion." Considered-and-rejected: fold into the existing informant-convergence check (rejected — that is trait-rating for instrument validation, a different construct); MVP-1 inclusion (rejected — recruitment burden, underpowered). **Not written into `DECISIONS.md` by the loop** — the lock is Dave's.

**Relationship to `DECISIONS.md` §7/§10.** This modality lives or dies on those constraints — see §7.

---

## 5. Why this is a research contribution

SOKA is established for *trait ratings*; H-A1 makes it a **live, item-level, longitudinal measurement channel inside a values instrument**, and turns the self/other asymmetry into a reveal-facing **blind-spot map** — the domains where the people who know you predict your moral choices better than you do. No instrument reports that. And H-A1d gives the moral-systems conversation's "N≈2 high-bandwidth character-reading" thesis a **direct, falsifiable test on moral prediction specifically** — does knowing someone better actually let you predict their ethics, or is moral behavior the one domain where closeness doesn't buy accuracy? Either answer is worth publishing.

---

## 6. Open design questions

**Q1. Item budget per informant.** Distinctive accuracy needs enough items for a stable within-pair correlation (≥ ~20?), but informant burden is the binding constraint. Resolve against pilot completion rates; possibly a fixed high-signal subset (the cost-of-virtue + truth-telling items where SOKA is strongest).

**Q2. Reactivity asymmetry.** The self-prediction (H9 beat) can change the participant's own choice (the §14.6 question–behavior effect); the informant's prediction cannot. So the SOKA contrast (§1.3) must compare `dacc(j→i)` against `dacc(i→i)` computed on the **no-prediction-beat control items**, or reactivity-adjust `rev` first — else the asymmetry is confounded by reactivity. Pre-register the control-item version as confirmatory.

**Q3. Halo / charitable-informant bias.** Informants close to the participant may predict charitably (toward the virtuous pole). This *depresses distinctive accuracy* (biases toward the norm) and is testable as a positive `nacc` with near-zero `dacc`; report it, don't assume it away. Anonymity of the informant's predictions from the participant reduces (not eliminates) the incentive.

**Q4. Incentivizing accuracy without creating a gaming surface.** Paying informants for accuracy improves effort but invites collusion/coaching (IN-2). Provisional: no accuracy payment; attention checks + blind prediction + distinctive scoring (coaching toward the norm doesn't raise `dacc`). Revisit.

**Q5. How much to show the participant.** Aggregate blind-spot map only, or per-informant? Per-informant is more informative but relationally hazardous (and a leakage/coercion risk, §7). Provisional: aggregate-only by default; per-informant solely under explicit mutual consent.

---

## 7. Privacy & misuse architecture (make-or-break)

An informant channel is the single most dangerous modality in the instrument: it is, structurally, "a record of what your intimates think you would do." The `concept.md` meta-risk ("the product attracts exactly the actors who would corrupt it") and the `validity-threats.md` Incentive-validity rows (IN-1/IN-2) apply with doubled force. Non-negotiable constraints — the module must not ship without all of them:

1. **Participant-initiated only.** The participant invites informants. No informant-, employer-, partner-, or platform-initiated flow — ever. Nobody can cause someone to be informed-upon. (A controlling partner using this to probe someone is the canonical abuse to design out.)
2. **Blind in both directions.** The informant sees only the scenario and "predict what *[name]* would do"; never the participant's actual answers. The participant sees only the aggregate blind-spot map; individual attributable predictions only under explicit mutual consent (Q5). No flow leaks one party's data to weaponize against the other.
3. **Never gating (IN-1, doubled).** Informant data must *never* feed any selection/screening/eligibility decision. A gated "moral 360" is a surveillance instrument; per the Incentive-validity principle, gating it also *destroys its validity* (informants would be coached, IN-2). The `DECISIONS.md §7` "no enterprise/screening ever" lock is the enforcement.
4. **Local-first, encrypted, deletable (DECISIONS §10).** Informant predictions live under the participant's local-first, E2E-encrypted store and **delete with the participant's profile**. No central plaintext honey-pot; informants are pseudonymous to the system.
5. **Consent + wellbeing on both sides.** Informed consent for the informant (their predictions are data); contemplative, opt-in, scrupulosity-guarded delivery for the participant (§1.5).

These are the same constraints that make the module *ethical* and the constraints that make its measurement *valid* — the Incentive-validity equivalence, exactly as `validity-threats.md` frames it. If any cannot be guaranteed by architecture (not just policy), H-A1 should remain a design, not a build.

---

## 8. Downstream changes this design unblocks
1. `scoring.md §16` — distinctive/normative accuracy, `Δ_SOKA`, SRM consensus, the §1.4 dissociation, H-A1d; parity-gated (`make check`)
2. `pre-registration.md` §6 — H-A1a/b/c (+ exploratory H-A1d) as Phase-2 secondaries; §5 — the informant analysis plan + the reactivity-control contrast (Q2)
3. `types.ts` `InformantPredictionLogEntry`; the informant invite/blind-prediction runtime flow
4. `concept.md` — an "informant channel" subsection under the measurement layer; the §7 constraints surfaced in the operating-constraints list
5. `validity-threats.md` — a CV-style row for informant halo/normative-accuracy confound (Q3) and an IN row for the informant-coercion surface (§7)
6. `DECISIONS.md` — the Phase-2 lock (Dave's call)

---

## 9. Relationship to H9, H10, EV-3, and the existing informant-convergence check
- **Completes H9's matrix.** H9 measured self-predicts-self; H-A1 adds other-predicts-self; `Δ_SOKA` is the asymmetry between them — the thing neither hypothesis can see alone.
- **H10 link.** High cross-context variability (H10) should *lower* informant distinctive accuracy too (a situation-driven person is hard for *anyone* to predict) — an exploratory cross-test: `corr(V_i, mean_j dacc(j→i)) < 0`.
- **EV-3 (ecological validity).** Informant prediction is a method whose errors are uncorrelated with the scenario layer's — a genuine triangulation leg (the multi-method payoff, `measurement-avenues.md` C1), and a partial answer to "do app choices mean anything" that doesn't require real-stakes (A2).
- **Distinct from informant-convergence.** That check = informant *trait ratings* validating the instrument; H-A1 = informant *choice predictions* as a channel + the SOKA construct. Run together, they cross-validate (an informant accurate at prediction should also rate traits convergently).

---

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) A1 — the branch this develops; C1 (MTMM) it feeds
- [`h9-self-calibration.md`](h9-self-calibration.md) — the self half of the matrix; `scoring.md` §14 supplies `dacc(i→i)`
- [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md) — §9 cross-test (variability vs informant accuracy)
- [`validity-threats.md`](validity-threats.md) — EV-3 (triangulation), IN-1/IN-2 (the §7 coercion/gaming surface)
- [`concept.md`](concept.md) — Vazire/Connelly Phase-2 informant rationale (the trait-rating check H-A1 is distinct from); scrupulosity guardrails
- [`DECISIONS.md`](DECISIONS.md) §7/§10 (the privacy constraints §7 depends on); §16/§17 (corpus untouched)
- [`pre-registration.md`](pre-registration.md) — the existing "informant convergence" secondary; where H-A1 lands as a Phase-2 hypothesis
