# Validity Threats — adversarial audit

**Status:** Reference document. An adversarial stress-test of the MVP-1 design: what could break the instrument, and which design choices in `concept.md` / `mvp.md` / `scoring.md` / `pre-registration.md` are doing the work of mitigating each threat. Different from `pre-registration.md` §9 (a short list of acknowledged limitations) — this is a structured walk-through of validity-threat categories with mitigation traces.

**Audience.** A prospective co-PI evaluating whether to commit; a grant reviewer wanting to know what could fail; a future researcher running a replication or extension wanting to know what to watch for.

**Method.** Each threat states what could go wrong; names the design choice (or absence) that addresses it; rates residual risk (LOW / MEDIUM / HIGH); and names how the pilot or main study would detect if the mitigation failed.

---

## Construct validity

*Am I measuring what I think I'm measuring?*

### CV-1. The scenarios don't measure revealed values; they measure social-desirability response patterns.

**Threat.** Even in a private-feeling app context, participants may pick the option they think the researcher (or their future self) would approve of. The "revealed" framing is then a misnomer — the data is just another stated-values channel.

**Mitigations in design.**
- Forced-choice format with both options pre-validated as defensible (no "trick" wrong answer)
- Quick-fire timer (8 seconds per item) compresses deliberation, reducing self-presentation tuning
- The candor moment in onboarding explicitly says "this is unvalidated; you might step away" — primes honesty in the relational sense
- Cost-of-virtue probes structurally externalize the construct: response is a stake-ladder, not an opinion
- **Narrative immersion as active debiasing (H8a).** The narrative-embedding-with-attachment design is hypothesized to *reduce the impression-management component* of social-desirability responding: transportation lowers self-monitoring (Green & Brock 2000), and entertainment-overcoming-resistance theory names reduced self-presentation as a direct consequence of narrative engagement and parasocial bonding (Moyer-Gusé 2008). H8a makes this a falsifiable, pre-registered prediction rather than an assumption — see `literature/narrative-immersion.md` and `scoring.md` §9.2. **This mitigation is itself under test**, not assumed to work; if H8a fails, this row's residual risk does not improve.

**Residual risk: MEDIUM.** The timer helps but doesn't eliminate; the population using a paid panel still skews toward people who are explicitly performing for a researcher. Note the threat is specifically *impression management* (audience-facing editing), not *self-deceptive enhancement* (honest but inflated self-view, per Paulhus 1984) — narrative debiasing (H8a) can plausibly touch only the former, which bounds how much this residual risk can fall.

**Detection in pilot/main study.**
- Pilot exit interview Section 3 (honesty-of-self-reporting) directly asks participants whether they performed; transcript analysis is the primary signal
- Convergent validity test H2 against HEXACO honesty-humility: if H2 fails because revealed scores compress toward the ceiling (everyone scoring high on truth-telling), social-desirability is a leading hypothesis
- Discriminant test H7 against Big-5 neuroticism: if revealed scores correlate positively with N, the social-desirability hypothesis becomes more plausible (anxious users perform virtue more)
- H8a paired narrative-vs-abstract divergence (`scoring.md` §9.2): if narrative-framed responses shift toward stated values most for participants with the largest abstract-condition gap, that is direct positive evidence the narrative design reduces impression-management bias; if H8a's lower CI sits at/below zero, narrative is not debiasing and this threat stands undiminished

---

### CV-2. The tag-axis map encodes the researcher's values, not the participant's.

**Threat.** Every scenario item's tags are pre-assigned a contribution to a domain-axis by the authors. If "truth:partial" is coded as -0.5 on the truth axis, that's a normative claim — that partial truth-telling is partly dishonest. A participant who scores high on "truth:partial" choices has *revealed* something, but what we LABEL it is the researcher's frame.

**Mitigations in design.**
- The tag-axis map is versioned (currently v0.1) and locked at OSF filing; changes after lock require an ADR — protecting against post-hoc map-editing to fit a desired story
- The map is open-source and inspectable
- Each tag's contribution is documented with a one-line rationale (see `analysis/tag_axis_map_v0.1.csv` description column)
- Pre-registration commits to the map version that's locked at filing time

**Residual risk: MEDIUM-HIGH.** This is a real and load-bearing threat. The instrument's interpretation depends on accepting the researcher's axis-coding.

**Detection in pilot/main study.**
- The exit interview re-narration test (have participants describe in their own words what each scenario was probing) is the headline signal — if participants' stated construct doesn't match the tag-axis map's construct, the map is encoding the wrong thing
- Inter-rater agreement on tag-axis assignments (have multiple ethics-research-experienced raters independently assign tags to a held-out item subset) would be a Phase-1 robustness check that's currently NOT scheduled — flag as a recommended addition

---

### CV-3. The four-domain factor structure is an empirical claim that may not hold.

**Threat.** `concept.md` and `pre-registration.md` H1 assume four domains (truth-telling, allocation, in-group, reciprocity) load on four distinct factors. If the factor analysis shows fewer factors (e.g., one general "moral conscientiousness" factor) or different factors (e.g., a self-other split orthogonal to domain), the entire interpretation framework is wrong.

**Mitigations in design.**
- H1 is pre-registered as a falsification target with explicit thresholds (RMSEA ≤ 0.08, CFI ≥ 0.90)
- H1 failure is named in `pre-registration.md` §6 as a "stop-on-failure status" for instrument validation — not a thing to explain away
- Negative-result publication commitment in DECISIONS §13 means a failed H1 gets published

**Residual risk: LOW (procedural) / MEDIUM (substantive).** The procedural protection against motivated reasoning is strong. The substantive risk that the 4-factor model is just wrong remains.

**Detection.** This IS the test. n≈200 cohort with item-level CFA is the validation step.

---

### CV-4. The "stated values" inventory and the "revealed values" scenarios are tapping the same underlying construct, just with different surface formats.

**Threat.** The stated-revealed *gap* depends on the two layers being genuinely distinct. If a participant's response to "rank these 20 values by importance" pulls from the same cognitive machinery as their response to a quick-fire scenario, the gap is psychometric noise, not signal.

**Mitigations in design.**
- Three-layer stated inventory (current self / aspirational self / admired other) deliberately invokes different framings
- Bradley-Terry forced-choice pairwise inventory uses a structurally different format than scenarios (paired comparisons rather than scenarios with options)
- HEXACO administration provides an external anchor independent of either layer
- H6 explicitly tests the stated-revealed correlation, with a *range* check (0.20 ≤ r ≤ 0.60) — too-high r supports this threat, too-low r supports separate construct (the desired case)

**Residual risk: MEDIUM.** The H6 range check is the most direct test, but it relies on the n=200 cohort behaving as expected.

**Detection.** H6 itself. If the observed r is >0.80, the two layers are not distinct constructs and the gap interpretation collapses.

---

## Internal validity

*Are the observed effects causally what I claim?*

### IV-1. Profile drift during the study could be participant artifact, not preference change.

**Threat.** If a participant's revealed score moves over 8 weeks, is it because their preferences shifted, because they got familiar with the format, because the scenarios got repetitive, or because of social-desirability adaptation?

**Mitigations in design.**
- Scenarios rotate across the corpus to minimize familiarity-driven scoring drift (the same item is rarely shown twice in close succession)
- Test-retest reliability H3 explicitly checks within-person score stability — if drift is large, H3 fails, and we know the instrument isn't reliable
- The pilot exit interview re-narration test surfaces whether participants are responding strategically vs. authentically
- Within-person trajectories are paired with within-person stated-inventory trajectories — divergent movement between them is meaningful; parallel movement is suspect

**Residual risk: MEDIUM.** MVP-1 is descriptive of correlation/stability; causal claims about preference change are reserved for MVP-2 with intervention conditions.

**Detection.** H3 failure (test-retest r < 0.60) is the signal. Pilot exit interviews ask about format-fatigue directly.

---

### IV-2. The longitudinal trajectory of cost-of-virtue probes may be artifact of stake-magnitude calibration drift in the participant's life.

**Threat.** A user whose break-point shifts from $1,000 to $100 might be revealing actual integrity drift, OR they might just have less money than they used to. The instrument can't distinguish.

**Mitigations in design.**
- Ladder is in "user-local currency" but the magnitudes are absolute USD-equivalents
- The cost-of-virtue scoring spec (scoring.md §4) flags this as a known confound and lists it as a stratifier the analyzer should report
- Within-user trajectory is interpreted *alongside* changes in self-reported financial situation (collected at exit interview)

**Residual risk: HIGH for the cost-of-virtue domain specifically.** This is named in `pre-registration.md` §9 and `literature/ecological-validity-positive.md`.

**Detection.** Exit interview asks about financial-situation changes during the study; analyzer should be extended (post-MVP-1) to estimate sensitivity to declared financial-situation as a moderator.

---

## External validity

*Do the findings generalize?*

### EV-1. The pilot and main-study cohorts are recruited via Prolific.

**Threat.** Prolific participants are systematically not the general population — they tend to be younger, more educated, more comfortable with self-reflection-as-paid-task, and have prior survey-study exposure.

**Mitigations in design.**
- Acknowledged explicitly in `pre-registration.md` §9
- Pilot demographics are collected and published
- The instrument's "ethical preferences" claim is bounded to "this population" in published results, not generalized

**Residual risk: MEDIUM.** Real but well-known to the field.

**Detection.** Pilot demographics published; if the population is skewed in ways that affect the instrument's psychometrics, that's a Phase-2 question (recruit from a different frame).

---

### EV-2. The English-language, WEIRD-cultural framing of the scenarios may not transfer.

**Threat.** Items like "a colleague repeats an inaccurate story about an absent person" assume a workplace culture, a moral universe of personal-truth norms, a notion of "absent person" agency. None of these are universal.

**Mitigations in design.**
- Pre-registration §7 explicitly names cross-cultural generalization as "out of scope for this pre-registration" and "Phase-3+ question"
- Concept doc operating constraint: no claim about non-WEIRD generalizability

**Residual risk: HIGH for any future cross-cultural claim; LOW for MVP-1's narrow scope.**

**Detection.** Future replications in non-WEIRD populations would be the actual test; nothing in MVP-1 attempts this.

---

### EV-3. App-based decisions don't predict real-world decisions.

**Threat.** This is the headline ecological-validity threat. Lab-to-field meta-analyses (Galizzi & Navarro-Martinez 2019) show median r ≈ 0.14 between behavioral-economic lab measures and real-world cooperation behavior. The instrument may produce reliable, internally-coherent revealed scores that simply don't predict anything outside the app.

**Mitigations in design.**
- Convergent-validity tests H2 (HEXACO H) and H4 (informant HEXACO H) are designed to be the field-anchor — HEXACO H has documented field-prediction at modest effect sizes
- Cost-of-virtue probes are framed as field-relevant decisions, not lab tasks
- The instrument is positioned in `concept.md` as a "long-form mirror" for self-understanding — its value claim does NOT depend on field-prediction. Self-reflective use does not require behavioral-prediction accuracy.
- `literature/ecological-validity-positive.md` documents this as the headline threat and the cost-of-virtue probe as the one specifically lacking direct lab→field validation

**Residual risk: HIGH for the field-prediction claim; LOWER for the self-reflective-utility claim.**

**Detection.** H4 (informant) is the closest field-anchor test in MVP-1. A formal field-criterion measure (paired with a real-world decision opportunity) would be MVP-2 or later. MVP-1 deliberately does not claim field-prediction.

---

### EV-4. The stakes/power discontinuity: low-stakes choices may be categorically different from high-stakes behavior, not merely noisier predictors of it.

**Threat.** EV-3 frames the lab→field gap as *attenuation* — a low but positive correlation. There is a stronger, worse version. Stakes are not a scaling parameter applied to a stable preference; they are a **treatment that changes the decision-maker.** Under real stakes or real power, the person choosing is a different system — visceral/hot-state, loss-facing, socially exposed — than the one who laddered through hypothetical rungs in a calm app session. If so, the cost-of-virtue curve can be *locally* valid (orderly within the probed range) and *globally* non-extrapolable: a phase transition exists at real stakes that no amount of low-stakes laddering reveals. This is the "measurement-under-power" problem — you cannot sample how someone behaves with power until they have it, and acquiring it changes them. It subsumes the cost-of-virtue confound in IV-2 but is more fundamental: even with perfect within-range measurement, the *shape* may not continue.

**Mitigations in design.**
- MVP-1's claim is bounded to the low-stakes self-mirror; `concept.md` positions the instrument as a "long-form mirror," explicitly not a predictor of high-stakes conduct
- `scoring.md` §13.2 reads the cost-of-virtue break-point as a within-person *revealed price*, a local quantity, not a global integrity constant — the spec already refuses the extrapolation this threat warns against
- The optional **real-stakes nights** (`concept.md` — small real money / charity) are the one in-instrument probe that can *detect* a discontinuity rather than assume its absence

**Residual risk: HIGH for any extrapolation to high-stakes / under-power conduct; LOW for the bounded low-stakes self-mirror claim MVP-1 actually makes.** The danger is not in the measurement but in a reader (or a future product surface) treating the low-stakes curve as a prediction of conduct under real pressure.

**Detection.**
- Real-stakes-night choices analyzed as a *bend* away from the laddered prediction (systematic sign), not merely added variance — a bend is the discontinuity's signature
- **Cross-link to H9c** (`h9-self-calibration.md` §1.4; `scoring.md` §14, proposed): if participants' self-prediction error concentrates at high stakes, the high-stakes self is demonstrably not reachable from the low-stakes self by extrapolation — the behavioral fingerprint of this discontinuity. H9c confirming is evidence *for* EV-4; H9c null lowers the residual risk. Either way the instrument measures its own most dangerous extrapolation boundary, which is the honest thing for it to do.

---

## Reliability

*Would re-running produce similar results?*

### REL-1. Test-retest reliability may be confounded by genuine preference change.

**Threat.** H3 expects test-retest r ≥ 0.60. But 8 weeks is long enough that genuine preference change is possible — the instrument might be MORE valid (catching real change) precisely when test-retest r is LOWER.

**Mitigations in design.**
- Test-retest window is 2 weeks vs. 2 weeks within an 8-week protocol, not full-protocol-length
- The threshold (r ≥ 0.60) is set lower than typical psychometric standards (r ≥ 0.80) precisely to allow for genuine change
- H3 failure threshold (r < 0.60) triggers a NO-GO classification not because the instrument failed but because it failed the stability assumption *for the construct it claims to measure*

**Residual risk: LOW-MEDIUM.** The threshold is well-calibrated.

**Detection.** H3 itself. The exit interview also asks "Has anything about your ethics changed during the study?" — a signal for the genuine-change interpretation.

---

### REL-2. Inter-rater reliability of tag-axis assignments is unmeasured.

**Threat.** Different ethics researchers might disagree on whether "truth:partial" should contribute -0.5 or 0.0 to the truth axis. The instrument's interpretation rests on a single set of judgments.

**Mitigations in design.**
- The map is open-source and inspectable
- A future contributor can fork the map and re-run the analyzer against the alternative coding

**Residual risk: MEDIUM.** Currently UNMITIGATED at the design level.

**Detection.** Recommend a pre-pilot inter-rater agreement check: have 3 ethics-research-experienced raters independently assign tags to a held-out subset of items, compute Cohen's kappa per tag. *This is not currently in the pilot-protocol or pre-launch checklist*; flag as a recommended addition to Phase 4.

---

## Statistical validity

*Am I using the right tests?*

### SV-1. Multiple-hypothesis testing across H1–H7 inflates Type-I error.

**Threat.** Seven hypotheses without familywise correction increase the chance that at least one passes by chance alone.

**Mitigations in design.**
- Pre-registration with thresholds locked before data collection eliminates the worst form (post-hoc cherry-picking)
- Primary hypotheses (H1, H2, H3) are pre-specified separately from secondary; only the primary set is gate-criterion
- The negative-result publication commitment removes the file-drawer dimension

**Residual risk: LOW for the gate-criterion primary set; MEDIUM for the secondary set.**

**Detection.** Reported with effect sizes and CIs; familywise correction (Holm-Bonferroni) can be applied at analysis time and reported alongside uncorrected values.

---

### SV-2. The bootstrap CI implementation depends on a single seed.

**Threat.** Per `scoring.md` §8 and `scripts/analyze.py`, bootstrap CIs use a pre-committed seed (BOOTSTRAP_SEED = 20260510). If a downstream replication uses a different seed, CIs will differ slightly — though this is the correct behavior for bootstrap.

**Mitigations in design.**
- Seed is explicitly committed in the analyzer and in the locked OSF documents at filing time
- The seed value is publicly known, not hidden

**Residual risk: LOW (this is correctly handled per psychometric standards).**

**Detection.** Replication by a third party using the seed should reproduce CIs exactly; any deviation is investigable.

---

### SV-3. The 4-factor CFA may have insufficient power at n=200.

**Threat.** n=200 is on the small side for an 8-factor CFA. Item-level loadings are noisy at this n; the RMSEA / CFI thresholds may be met or missed by sampling variation alone.

**Mitigations in design.**
- The factor model is small (4 factors, ~12 indicators per factor)
- Threshold values (RMSEA ≤ 0.08, CFI ≥ 0.90) are lenient by current SEM-fit standards
- A second n=200 replication is held as a contingent recommendation if H1 is mixed

**Residual risk: MEDIUM.** Could go either way.

**Detection.** RMSEA and CFI confidence intervals reported alongside point estimates; if CIs are wide and the threshold falls within them, the result is "indeterminate" not "passed/failed" and a second n=200 replication is recommended.

---

## Incentive validity

*Under what use does the instrument measure values at all?*

**Framing principle — validity and misuse-resistance are the same property.** Every threat above asks "is the number measuring values?" This category asks the prior question: *under what conditions does it measure values in the first place?* The answer is sharp. PoC measures values only in the **non-instrumental regime** — where the participant gains nothing by scoring a particular way. The instant a PoC score *pays* — gates a job, a date, a loan, a reputation, or even serves the user's own self-image as a target to beat — Goodhart's law applies: the measure becomes a target, and a targeted measure of virtue stops measuring virtue and starts measuring performance-under-incentive. The most skilled impression-managers then produce the cleanest profiles, exactly *inverting* the signal.

This reframes the operating constraints in `DECISIONS.md` §6 (descriptive-never-prescriptive), §7 (no enterprise/screening ever; no engagement monetization), §9 (no social comparison), and §10 (local-first, user-owned, deletable). They are usually presented as *ethical* commitments. They are equally **measurement-validity boundary conditions** — the envelope within which the instrument's numbers mean anything. An ethics violation here is simultaneously a validity collapse, and that equivalence is the strongest available defense against the most probable future pressures (a B2B screening product, a shareable score, a leaderboard): each would not merely be wrong, it would *void the measurement*. The `concept.md` meta-risk section ("the product attracts exactly the actors who would corrupt it") is this same threat seen from the ethics side.

### IN-1. If the instrument's output ever gates a decision, revealed scores invert into a measure of gaming-ability.

**Threat.** The moment any third party (employer, partner, court, government, platform) or the product itself uses a PoC profile to *select* or *rank*, the measured population shifts from "people revealing values" to "people optimizing a visible target." Per Goodhart, the scores stop tracking values; per the leaders-discussion provenance, this is the "valid as a compass, not as a selector" boundary — a compass that starts steering gets gamed. The failure is not gradual degradation; it is a discontinuous inversion (the best gamers float to the top).

**Mitigations in design.**
- `DECISIONS.md` §7 ("no enterprise/employer-screening product ever") and §10 (local-first, no central plaintext honey-pot, user-deletable) make gating *architecturally* hard, not merely discouraged
- §6 (no verdict) and §9 (no comparison) remove the in-product targets a user could optimize toward
- `runtime-architecture.md` §18 has *no schema slot* for social comparison or streaks on values — the data model itself refuses the surface

**Residual risk: LOW while the operating constraints hold; CATASTROPHIC and discontinuous if any is ever relaxed.** This is not a statistic to monitor but an invariant to preserve.

**Detection.** Governance/architecture invariant, not a study test: the §7 "no enterprise ever" lock and the §10 data architecture are the enforcement. Any proposal that would let a third party require the test, or attach a stake to the output, is the tripwire.

### IN-2. Self-gaming: once a solo user infers what is measured, they can perform to it.

**Threat.** Even with no external gate, a user can turn the instrument into a target for their *self-image* — choosing the option they want to be true of themselves rather than the one that is. This degrades the revealed channel toward a second stated channel (the CV-1 threat, self-initiated).

**Mitigations in design.**
- §6's descriptive-never-prescriptive stance removes the score-to-beat: there is deliberately no number to optimize, which removes most of the motive
- Anti-gaming design in `concept.md` (noise filler items, full profile withheld ~10–15 sessions, aggressive surface variation across workplace/family/public/anonymous settings)
- H8 narrative immersion lowers self-monitoring (CV-1 mitigation; `scoring.md` §9.2), which also lowers self-gameability
- **H9 supplies a detector** (`h9-self-calibration.md` §8): a user performing their ideal predicts and produces that ideal, yielding anomalously *low* self-prediction error — so near-perfect calibration is a self-gaming flag rather than a success.

**Residual risk: MEDIUM.** A determined self-gamer cannot be fully stopped; the absence of any payoff (no score, no comparison, local-only) removes most of the incentive, and H9 makes the residue partly detectable.

**Detection.** The CV-1 convergent/discriminant signals (ceiling compression on revealed scores; positive correlation with neuroticism) plus the H9 calibration flag above.

---

## Recommended additions surfaced by this audit

Items this audit found are **NOT currently in the pre-registration, pilot-protocol, or pre-launch checklist** that should be added before OSF filing:

1. **Inter-rater agreement check on tag-axis assignments** (CV-2, REL-2 mitigation). Add to Phase 4 of pre-launch checklist: "Independent inter-rater coding of a 12-item subset by 3 ethics-research-experienced raters; report Cohen's kappa per tag."
2. **Sensitivity-to-financial-situation analysis on CoV probes** (IV-2 mitigation). Extend the analyzer post-MVP-1 to stratify CoV trajectories by self-reported financial-situation change.
3. **Familywise-corrected reporting of H1–H7** (SV-1). Specify in pre-registration that Holm-Bonferroni-corrected p-values will be reported alongside uncorrected effect-size estimates.
4. **CI-aware reporting of H1 RMSEA / CFI** (SV-3). Specify in pre-registration that point estimates AND 95% CIs of the SEM-fit indices will be reported; the H1 decision rule should account for CI width.
5. **Self-prediction reactivity control** (IN-2 / H9). Counterbalanced no-prediction control items, so the calibration beat's question–behavior effect on the subsequent choice can be estimated and removed before H9 scoring; pre-specify the predicted-vs-non-predicted contrast (also an MVP-2 intervention candidate if prediction increases stated–revealed consistency). See `h9-self-calibration.md` §3 A3.

These are not blockers for the current MVP-1 plan but are concrete additions a co-PI would likely require before signing off.

---

## Cross-references

- [`pre-registration.md`](pre-registration.md) §9 — short list of acknowledged limitations
- [`concept.md`](concept.md) — design rationale for the choices that mitigate these threats
- [`mvp.md`](mvp.md) — MVP-1 scope; the bounded thing this audit applies to
- [`scoring.md`](scoring.md) §8 — bootstrap CI seed
- [`literature/ecological-validity-positive.md`](literature/ecological-validity-positive.md) — the headline ecological-validity discussion (EV-3)
- [`DECISIONS.md`](DECISIONS.md) — the design-choice ADRs each threat references
- [`pilot-pre-launch-checklist.md`](pilot-pre-launch-checklist.md) Phase 4 — where the recommended additions belong
- [`h9-self-calibration.md`](h9-self-calibration.md) — H9 (self-prediction calibration); EV-4 and IN-2 cross-link to its scoring (§14, proposed) and its self-gaming detector
- Originating design conversation (June 2026 "measurement-under-power / calibration" thread) — provenance for EV-4's discontinuity framing and the Incentive-validity reframe
