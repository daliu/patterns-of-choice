# H-A2 — The consequential / real-stakes channel (the keystone validity probe)

**Status:** Design proposal, drafted 2026-06-16 (extension loop, iteration 6). Develops branch **A2** of [`measurement-avenues.md`](measurement-avenues.md) — an A-series *modality* (a new channel). Labeled **H-A2** alongside H-A1. **Phase-2 / opt-in**, and unlike every prior branch it is **not** an N=1 reveal read — it is a **cohort-level validity probe** (see §1.5). The lock is Dave's call.

**Provenance.** Branch A2, and the empirical hinge of the whole project. The instrument's **foundational empirical risk** (`concept.md` Premise; `validity-threats.md` EV-3/EV-4) is that low-stakes hypothetical choices may not predict real behavior at all (EV-3), or may be *categorically* different from behavior under real stakes (EV-4, the stakes/power discontinuity). EV-4 names exactly one in-instrument way to *detect* that rather than assume it: the **real-stakes nights** (`concept.md` — small real money / charity; module F costly-signaling). H-A2 formalizes that into a pre-registered channel. It is the branch that can **falsify the instrument's central claim** — and running it anyway is the project's intellectual-honesty core.

**Builds on the existing predictive-validity plan.** `concept.md`'s validation plan already lists "predictive validity against real-stakes behavior." H-A2 is its formalization into a named channel **plus** two genuinely new tests: the EV-4 *bend* (§1.3) and the convergence with H9c (§1.4).

---

## 1. The hypothesis statement

**H-A2 (proposed Phase-2 secondary).**

*The instrument's hypothetical revealed scores predict real-stakes behavior above chance (the project's central bet); but real-stakes behavior bends systematically away from the laddered low-stakes prediction, and the bend grows with stake size (the EV-4 discontinuity, made empirical); and the bend is largest for the participants whose self-prediction fails most at high stakes (H9c).*

### 1.1 The channel

Real consequential micro-decisions — **sparsely sampled, opt-in, consented, debriefed** — embedded as occasional "real-stakes episodes" alongside the hypothetical daily practice. Paradigms, all IRB-standard and chosen so no third party can be harmed (the stakes are the participant's own small bonus, time, or a charity donation):

- **Real charitable allocation** (a real-money dictator/giving decision: keep a bonus vs. donate to a vetted charity) → matches the resource-allocation domain. *Identifiable* (per-person).
- **Real lost-wallet / overpayment return**, **real verifiable promise-keeping**, **real time/effort donation** → matched to truth-telling / reciprocity. *Identifiable.*
- **Fischbacher die-roll** (privately report a roll for real money) → a *cohort* honesty base rate only. Its individual **un**identifiability is what protects the participant — and therefore precludes a per-person score (§1.4).

Explicitly **not** the Mazar/Ariely matrix-priming paradigm — non-replicating (Verschuere et al. 2018 RRR) and entangled with the Ariely/Gino fraud, per `concept.md` and the repo's post-Gino discipline. Die-roll (Fischbacher) and Abeler et al. 2019 are the well-replicated honesty paradigms.

### 1.2 H-A2a — convergent ecological validity (the central bet)

The hypothetical instrument's per-person revealed scores predict real-stakes behavior on matched constructs:
```
H-A2a:  lower 95% bootstrap-CI bound of  corr( revealed_score_instrument(i, domain) , real_stakes_behavior(i, domain) )  > 0
```
The threshold is **honestly low**: the lab→field meta-analytic ceiling is r ≈ 0.14 (Galizzi & Navarro-Martinez 2019; `validity-threats.md` EV-3), so — exactly as H2's HEXACO threshold was calibrated down to Thielmann's ρ ≈ 0.20 ceiling (`DECISIONS.md` §11) — a lower-CI-above-zero criterion is the defensible bar, with the point estimate reported against the meta-analytic ceiling. **This is the test the entire predictive-validity claim rides on.** If H-A2a fails, EV-3 wins: the instrument measures something reliable and internally coherent that does not predict real conduct, and the predictive-validity claim is a documented NO-GO (reported per the negative-result commitment, `DECISIONS.md` §13).

### 1.3 H-A2b — the stakes bend (EV-4, made empirical)

Real-stakes behavior is systematically shifted from the laddered low-stakes prediction, and the shift grows with stake size:
```
bend_i      = real_stakes_choice(i) − hypothetical_prediction(i, at the matched stake)   # on the matched axis
H-A2b:  (i)  lower 95% CI of  |mean_i bend_i|  > 0  with a pre-registered sign (less virtuous under real stakes);
        (ii) |bend| increases with stake magnitude — the cost-of-virtue ladder's extrapolation curves.
```
This is EV-4's detection criterion — *a bend, not mere attenuation/noise.* The hypothetical cost-of-virtue break point vs. the **real** one. A null bend (real ≈ laddered) is itself a strong, reassuring result: the low-stakes curve extrapolates.

### 1.4 H-A2c — convergence with H9c (two measurements of one discontinuity)

H9c says self-prediction error concentrates at high stakes (a *self-report*-derived fingerprint of the discontinuity). H-A2b says real behavior bends at high stakes (a *real-behavior*-derived fingerprint). If both are real, they should agree:
```
H-A2c:  corr( blind_i [H9c stakes-blindness] , |bend_i| [H-A2b] )  > 0,  lower 95% CI > 0
```
Their agreement is triangulated evidence the EV-4 discontinuity is real (two independent methods, uncorrelated errors); their *disagreement* is diagnostic (e.g., people bend but *see it coming* → the discontinuity is real but not a self-knowledge failure). Either way it ties the real-stakes channel to the self-calibration channel.

### 1.5 Why this is a cohort probe, not an N=1 reveal — and the hard limits

- **Not N=1.** Real-stakes episodes are rare (cost, fatigue, non-repeatable) → far too sparse per person for a within-person reveal. H-A2 is a **cohort-level validity statistic**, the sharpest contrast with H9/H10/H11/H12 (all N=1 reveal-eligible). It does not appear in the personal reveal; it appears in the validation paper.
- **The identifiability tradeoff.** The die-roll protects participants by being individually unidentifiable — which kills per-person correlation. So per-person H-A2a uses *identifiable* paradigms (charity allocation, return, promise); die-roll contributes only a cohort honesty base rate against which the instrument's aggregate is calibrated.
- **Ethics.** Real consequences require IRB, consent, and debrief; stakes are the participant's own bonus/time or a charity donation — **never** a paradigm where the participant can harm a third party. Bounded and opt-in.
- **Selection.** Opt-in to real stakes → a self-selected subsample (likely the more confident / engaged). The opt-in rate is reported; the real-stakes subsample's representativeness is a named limit, not papered over.
- **The deepest limit (honest).** The EV-4 discontinuity may live at stakes *beyond what is ethical to induce* — you cannot ethically grant someone real power or life-altering stakes. So an in-instrument real-stakes channel can probe only the **low end** of the real-stakes range: it can *detect* a bend that begins within ethical stakes, but it **cannot rule out** a discontinuity at higher stakes. A2 sharpens EV-4; it cannot fully resolve it. (The measurement-under-power problem is partly unsolvable in-instrument, by construction.)

### 1.6 Falsification and exploratory tests

**H-A2a is load-bearing** — its failure is a documented falsification of the predictive-validity claim (not of the instrument's *reflective* utility, which `concept.md` is careful never to predicate on field-prediction). H-A2b/c sharpen the discontinuity. Partial results published.

**Exploratory.** H-A2 × H-A1 (do informants predict real-stakes behavior *better than the self* — SOKA extended to real conduct?); H-A2 × H11 (does the moral-circle radius predict real charitable allocation as recipient distance varies?); H-A2 × cost-of-virtue (the real break point vs. the laddered one, per construct).

---

## 2. Theoretical grounding

- **Bostyn et al. 2018; FeldmanHall et al. 2012.** Hypothetical ≠ real in trolley/dictator paradigms — the threat H-A2 confronts head-on (already the repo's foundational-risk anchors).
- **Abeler, Nosenzo & Raymond 2019 (N ≈ 44,000); Fischbacher & Föllmi-Heusi 2013.** The well-replicated real-stakes *honesty* paradigms (die-roll, sender–receiver) — the safe alternatives to Mazar/Ariely.
- **Galizzi & Navarro-Martinez 2019.** Lab→field correspondence median r ≈ 0.14 — the meta-analytic ceiling that sets H-A2a's honest threshold.
- **Pletzer 2019.** HEXACO honesty-humility predicts real workplace deviance ρ ≈ −0.48 — evidence the lab→field bridge is not zero for the trait PoC targets, licensing a non-trivial H-A2a expectation.
- **Levitt & List 2007.** What lab measures do and don't reveal about field behavior — scrutiny, selection, and stakes as the moderators H-A2's limits (§1.5) come from.

---

## 3. Instrument modification required

### Already in place
- `concept.md` "optional real-stakes nights" (§Rotation) and **module F** ("optional costly signaling — charity allocation, public commitments; strictly opt-in").
- The existing predictive-validity plan item and the EV-3/EV-4 rows that name real-stakes as the detection method (and the H9c cross-link in EV-4).
- The cost-of-virtue probes — whose hypothetical break points are exactly what H-A2b compares the real break point against.

### What needs to be added (the heaviest of any branch — real infrastructure, not authoring)
- **A1. Real-stakes episode infrastructure.** Charity integration + a vetted charity list, real-bonus payment rails, the consent/debrief flow, and the matched-construct map (which real decision pairs with which instrument axis). This is engineering + operations + IRB, not scenario authoring.
- **A2. Scoring `§19` (proposed).** `real_stakes_behavior(i, domain)`, `bend_i`, the H-A2a/b/c statistics, the identifiability handling (per-person identifiable paradigms vs. cohort-only die-roll), opt-in/selection reporting. Parity-gated where it touches the analyzer.
- **A3. IRB + ethics.** Real consequences move this from "app" to "human-subjects study with real payoffs" — a different consent and review tier.

No new scenarios; the channel uses *real decisions*, so the §16/§17 scenario corpus is untouched.

---

## 4. Implications for existing locked decisions

**Phase-2, opt-in, cohort-level.** Not MVP-1 — real-stakes is sparse, expensive, IRB-heavy, and underpowered at the MVP-1 cohort. Aligns with `concept.md` (real-stakes is "optional," module F) and the Phase-2/3 validation plan (real-stakes follow-up).

**Formalizes, not duplicates, the predictive-validity plan.** The existing plan names real-stakes predictive validity; H-A2 turns it into a pre-registered channel and adds the bend (§1.3) and the H9c convergence (§1.4).

**Corpus untouched** (real decisions, not scenarios). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add H-A2 (real-stakes channel) as a Phase-2 secondary; opt-in, consented, identifiable-paradigm per-person convergent test + die-roll cohort base rate; scoring §19; the keystone ecological-validity probe." Considered-and-rejected: MVP-1 inclusion (rejected — cost/power/IRB); harm-to-others paradigms (rejected — §1.5 ethics); the Mazar/Ariely task (rejected — non-replicating, fraud-adjacent).

**Updates EV-3/EV-4.** Those rows currently *name* real-stakes nights as the detection method; once H-A2 is locked they cite it as the operationalized probe (and H-A2's own §1.5 limit — the un-inducible high-stakes range — should be folded back into EV-4 as the residual that even A2 can't close).

---

## 5. Why this is a research contribution

H-A2 is the **keystone**: it operationalizes the project's foundational empirical risk into a falsifiable channel, rather than leaving "does a daily puzzle capture real character?" as a caveat. It adds the **bend test** (real vs. laddered — EV-4 made measurable) and the **H9c convergence** (a self-report fingerprint of the discontinuity and a real-behavior fingerprint, which should agree) — a multi-method case for or against the discontinuity that neither channel makes alone. And it states its own ceiling honestly (§1.5): the un-inducible high-stakes range that no ethical in-instrument probe can reach. A project that builds the test most able to sink it is the credible kind.

---

## 6. Open design questions
- **Q1. Paradigm set.** Charity allocation is the cleanest/most-ethical identifiable per-person measure; how many paradigms, matched to which domains, at what frequency (one real episode per ~N sessions)?
- **Q2. Stake magnitude.** How high can real stakes ethically go? The bend may only appear above the inducible ceiling (§1.5) — pilot the largest defensible stake and report the range probed.
- **Q3. Identifiability vs. protection.** Per-person convergent tests need identifiable behavior, but identifiability raises social-desirability and privacy stakes. Resolve per paradigm; die-roll stays cohort-only.
- **Q4. Construct matching.** Mapping a real decision (donate $X?) to an instrument axis (generosity) is itself an inferential step — pre-register the mapping like the tag-axis map.
- **Q5. Debrief.** Real moral choices can be self-revealing in distressing ways; the debrief and the scrupulosity guardrails (`concept.md`) apply with extra force.

---

## 7. Downstream changes this design unblocks
1. `scoring.md §19` — `real_stakes_behavior`, `bend_i`, H-A2a/b/c, identifiability + selection handling; parity-gated
2. `pre-registration.md` — formalize real-stakes predictive validity + the bend + the H9c-convergence test as Phase-2 hypotheses
3. real-stakes infrastructure (charity rails, payment, consent/debrief), and an IRB amendment
4. `validity-threats.md` — EV-3/EV-4 cite H-A2 as the operationalized detector; add H-A2's §1.5 un-inducible-range limit as the EV-4 residual; a selection-bias row for the opt-in subsample
5. `concept.md` — promote "real-stakes nights" / module F from optional aside to the named keystone validity channel
6. `DECISIONS.md` — the H-A2 lock (Dave's call)

---

## 8. Relationship to EV-3/EV-4, H9c, cost-of-virtue, H-A1, H11
- **EV-3/EV-4.** H-A2 *is* the detection method those rows name — and the only branch that can confirm or falsify the instrument's predictive premise.
- **H9c.** The convergence (§1.4) — real-behavior bend vs. self-report stakes-blindness, two measurements of one discontinuity.
- **Cost-of-virtue.** H-A2b compares the *real* break point to the *laddered* one — the cost-of-virtue probe's hypothetical made consequential.
- **H-A1.** Exploratory: do informants predict *real-stakes* behavior better than the self (SOKA extended from hypothetical to real conduct)?
- **H11.** Exploratory: does the moral-circle radius predict *real* charitable allocation as recipient distance varies (the circle made consequential)?

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) A2 (and C1, which H-A2 feeds as the real-behavior method); [`validity-threats.md`](validity-threats.md) EV-3, EV-4 (the rows this operationalizes), IN-1 (real-stakes data must never gate)
- [`concept.md`](concept.md) (foundational empirical risk; real-stakes nights; module F; the Mazar/Ariely exclusion), [`h9-self-calibration.md`](h9-self-calibration.md) §1.4 (H9c — the convergence)
- [`scoring.md`](scoring.md) §4 (cost-of-virtue break point vs. the real one) — where §19 lands; [`DECISIONS.md`](DECISIONS.md) §11 (the meta-analytic-ceiling threshold precedent), §13 (negative-result commitment), §16/§17 (corpus untouched)
- [`pre-registration.md`](pre-registration.md) (the predictive-validity plan H-A2 formalizes)
