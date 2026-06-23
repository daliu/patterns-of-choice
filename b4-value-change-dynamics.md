# B4 — Value-change dynamics (rationalization vs. growth)

**Status:** Design proposal, drafted 2026-06-22 (extension loop, iteration 10). Develops branch **B4** of [`measurement-avenues.md`](measurement-avenues.md). Formalizes a read `concept.md` already names (§"Longitudinal capture": "stated values moving *toward* revealed behavior is rationalization; moving *away* is aspiration"). **Phase-2 / MVP-2** — it is gated on enough longitudinal waves to model a trajectory (see §1.5). The lock is Dave's.

**Provenance.** Branch B4. The instrument collects two series over weeks — *stated* values (the longitudinal inventory, "one or two items per session") and *revealed* behavior — and the §6 gap is their difference at one time. B4 asks the **dynamic** question the static gap can't: when stated and revealed disagree, *which one moves to close it, and in which direction?* That direction distinguishes **rationalization** (you quietly lower the professed bar to match how you act) from **growth** (you hold the bar and pull your behavior up to it) — and, per person, it adjudicates the classic dissonance/self-perception-vs-self-regulation question.

---

## 1. The hypothesis statement

**B4 (proposed `pre-registration.md` §6, secondary; Phase-2).**

*The stated and revealed value-series each drift in a person-stable way; and the cross-lagged direction of their coupling — whether behavior leads the stated value (rationalization / self-perception) or the stated value leads behavior (growth / aspiration) — is a meaningful, reliable individual difference, not regression to the mean.*

### 1.1 Measurement primitive (two coupled series)
For person *i*, construct *d*, wave *t*:
```
stated_i(d,t)    = longitudinal inventory score for d at wave t  (concept.md §"Longitudinal capture")
revealed_i(d,t)  = revealed behavioral score for d at wave t      (§2–3, windowed)
gap_i(d,t)       = stated_i − revealed_i                          (§6 at a single time)
```
B4 models the *joint dynamics* of the two series, not the snapshot gap. The signal is the **cross-lag**: does `revealed(t)` predict `stated(t+1)` (behavior leads the professed value — rationalization/self-perception) or does `stated(t)` predict `revealed(t+1)` (the professed value leads behavior — growth/aspiration)?

### 1.2 B4a — the two series have reliable, separable trajectories
Each series drifts person-stably (a reliable within-person slope/dynamic), and the two are separable (not one series in two guises — the §6/H6 distinctness, longitudinally). Requires **≥3 waves** (a two-wave slope is just a difference score, §1.5). Reliability of the per-person dynamic estimated by split-half over waves or model-based SE.

### 1.3 B4b — the cross-lagged direction is a meaningful individual difference (RI-CLPM)
**Method (load-bearing).** The standard cross-lagged panel model conflates between-person and within-person variance and would mis-assign the direction; B4 uses the **random-intercept CLPM** (Hamaker, Kuiper & Grasman 2015), which separates the stable between-person trait (the chronic gap) from the within-person dynamics (who-pulls-whom over time). The within-person cross-lags are the signal:
```
B4b:  the within-person cross-lag asymmetry  (stated→revealed)  −  (revealed→stated)
      is a reliable individual difference (per person×construct), with a non-degenerate
      between-person distribution; lower 95% CI of its split-window test–retest ≥ 0.40.
```
A positive asymmetry = **growth/aspiration leads** (stated→revealed dominant); negative = **rationalization/self-perception leads** (revealed→stated dominant). (Festinger and Bem both predict behavior→stated; B4 doesn't separate dissonance from self-perception — both are the "behavior-leads" pole.)

### 1.4 B4c — the trajectory typology (the reveal-facing read)
Classify each person×construct trajectory (N=1, descriptive, wave-count-gated):
- **Grower** — stated→revealed dominant; the gap closes by behavior rising to the bar.
- **Rationalizer** — revealed→stated dominant; the gap closes by the bar dropping to behavior.
- **Aspirer** — stated rising while the gap holds/widens; the bar raised, behavior not (yet) following.
- **Entrenched** — stable gap, negligible cross-lags.

### 1.5 Caveats (B4 is methodologically treacherous — the rigor is here)
- **Regression to the mean.** Any two-wave change score is RTM-contaminated (the map's named risk). B4 therefore *requires* ≥3 (preferably many) waves and model-based dynamics (RI-CLPM / latent change), and **never raw difference scores**.
- **CLPM → RI-CLPM.** The naive CLPM has been heavily critiqued for confounding trait and dynamics; RI-CLPM (Hamaker 2015) is mandatory, not optional — without it, the chronic between-person gap masquerades as a within-person direction.
- **Sparse, noisy waves.** The inventory is one-or-two-items-per-session, so each wave's `stated` is a noisy estimate; trajectory on noisy series needs many waves + measurement-error modeling (a latent-variable RI-CLPM if identifiable, §6 Q). Under-powered waves → B4 stays descriptive.
- **Protocol length.** The MVP-1 8-week protocol likely yields too few clean waves for a stable RI-CLPM, so B4 is realistically **Phase-2/MVP-2** (longer protocols); an MVP-1 read is tentative/exploratory at best.
- **Value-neutrality (beyond `concept.md` §153's labels).** Rationalization is **not** inherently bad — lowering a genuinely unrealistic standard can be healthy acceptance, not self-deception; and a chronically widening aspirational gap held *without* behavior change can be scrupulosity (`concept.md` risk section), not virtue. The typology is descriptive; the reveal must not shame the "rationalizer" or valorize the "aspirer."

### 1.6 Falsification and exploratory
Combined B4 = **B4a ∧ B4b** (reliable separable trajectories with a reliable directional asymmetry). A null B4b (no stable direction, or pure RTM) is the falsification — value-change is then idiosyncratic noise, not a trait. Partial results published.

**Exploratory.** (a) **B4 ↔ H-A5 (the leading indicator):** A5's *felt-but-violated* cell (feeling the pull of a virtue you didn't enact) should predict a **grower** trajectory — the felt norm is the seed of the behavior-leading dynamic. If so, the moral-emotion channel (iteration 9) is the early signal of the growth direction (iteration 10). (b) **B4 ↔ the intervention layer:** growers respond to scaffolding; rationalizers need the gap *surfaced* first; aspirers need self-efficacy — the typology matches interventions (the MVP-2 hook). (c) **B4 ↔ H10:** is a person's drift-*direction* itself context-stable, or do they grow in one domain and rationalize in another?

---

## 2. Theoretical grounding
- **Festinger 1957 (cognitive dissonance).** Acting against a stated value creates dissonance, reduced by moving the stated value toward the behavior — the rationalization pole's mechanism. Already cited in `concept.md`.
- **Bem 1972 (self-perception).** You infer attitudes from behavior — same behavior→stated direction, different mechanism. B4 measures the direction, not which mechanism; both are the "behavior-leads" pole.
- **Hamaker, Kuiper & Grasman 2015 (RI-CLPM).** The method that makes B4b honest — separating the chronic between-person gap from within-person who-leads-whom dynamics. The single most important methodological choice here.
- **Latent change-score models (McArdle 2009).** The broader family for modeling coupled change over many waves; the path if waves and identification permit.

---

## 3. Instrument modification required
### Already in place
- The two longitudinal series — `stated` (the longitudinal inventory, `concept.md` §"Longitudinal capture") and `revealed` (§2–3) — are collected by design. B4 introduces **no new collection**; it is an analysis layer.

### What needs to be added
- **A1. Enough waves.** The binding requirement — a protocol long enough (and an inventory cadence dense enough) for ≥3 clean waves per construct, realistically Phase-2/MVP-2.
- **A2. Scoring `§24` (proposed).** The RI-CLPM (or latent change) specification per construct, the cross-lag-asymmetry statistic, the typology classification with wave-count gates, the RTM guards. Cohort-level for the model; the N=1 typology for the reveal (suppressed below the wave threshold).

No new scenarios; corpus untouched.

---

## 4. Implications for existing locked decisions
**Phase-2/MVP-2, analysis layer.** Reuses the existing series; gated on longitudinal waves (the MVP-1 protocol is likely too short for a robust model). **Formalizes `concept.md` §153** ("drift toward = rationalization; away = aspiration") into a model-based directional construct, and adds the value-neutrality nuance §153 lacks.

**Public card: yes.** Unlike the meta-method (C1) and the analysis adjunct (A4), B4 is a genuinely compelling, accessible self-knowledge facet — *which way are your values moving — up to meet your behavior, or down?* — so it gets a `research-program.json` card, design-stage labeled (and honest that it needs a long run to see).

**Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add B4 (value-change dynamics) as a Phase-2 secondary; RI-CLPM over the longitudinal stated/revealed series (scoring §24); the rationalizer/grower/aspirer/entrenched typology, wave-count-gated, value-neutral; one design-stage card; no new collection." Considered-and-rejected: two-wave difference scores (rejected — RTM); naive CLPM (rejected — Hamaker; trait/dynamics confound); MVP-1 confirmatory inclusion (rejected — too few waves).

---

## 5. Why this is a research contribution
The instrument already has a static gap; B4 makes its **dynamics** a construct: the *direction* of value-change (rationalize vs. grow), per person, per domain — and it lets the instrument **adjudicate, within a person, the dissonance/self-perception-vs-self-regulation question** (does your value follow your behavior, or lead it?) that the attitude literature usually answers only at the group level. It supplies the intervention layer its matching variable (typology→intervention) and links the moral-emotion channel (A5) to behavior change as its leading indicator.

---

## 6. Open design questions
- **Q1. Waves for a stable RI-CLPM.** How many clean waves per construct are needed; what inventory cadence delivers them without fatiguing the practice? Pilot.
- **Q2. Noisy-wave handling.** Latent-variable RI-CLPM (modeling each wave's measurement error) vs. manifest RI-CLPM — identifiability at realistic n and wave counts.
- **Q3. Reveal framing.** "Rationalizer" must be delivered without shaming (the value-neutrality of §1.5); pilot the language.
- **Q4. Domain aggregation.** Per-construct trajectories vs. a person-level drift style — and whether the latter is even coherent (H10 says context-sensitivity is itself a trait).

---

## 7. Downstream changes this design unblocks
1. `scoring.md §24` — RI-CLPM / latent-change spec, the cross-lag asymmetry, the typology + wave-gates + RTM guards
2. `pre-registration.md` §6 — B4 as a Phase-2 secondary
3. `research-program.json` — the B4 card (design-stage)
4. `concept.md` — formalize the §153 drift read; add the value-neutrality nuance
5. `validity-threats.md` — rows for RTM in change scores and the CLPM-vs-RI-CLPM trait/dynamics confound
6. `DECISIONS.md` — the B4 lock (Dave's call)

---

## 8. Relationship to the other branches
- **The §6 gap, in motion.** B4 is the *dynamics* of the static stated–revealed gap — how it moves, not how big it is.
- **A5 → B4.** The felt-but-violated cell (A5) is the hypothesized leading indicator of the grower trajectory (B4) — moral emotion as the seed of change.
- **The intervention layer.** The typology is the MVP-2 intervention-matching variable.
- **H10.** Is the drift-*direction* itself context-stable, or domain-specific?
- **Feeds C1.** The trajectory direction is another channel/feature for the multi-method picture.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) B4; [`concept.md`](concept.md) §"Longitudinal capture" (the §153 read this formalizes; Festinger/Bem; the scrupulosity risk for the value-neutrality caveat)
- [`scoring.md`](scoring.md) §6 (the static gap B4 sets in motion), §8 (bootstrap) — where §24 lands; [`h-a4-a5-process-emotion.md`](h-a4-a5-process-emotion.md) (A5 → B4 leading indicator)
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`validity-threats.md`](validity-threats.md) (RTM + CLPM/RI-CLPM rows), [`pre-registration.md`](pre-registration.md) §6, [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md) (is drift-direction context-stable?)
