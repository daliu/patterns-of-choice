# H10 — Cross-situational moral consistency (variability as a trait)

**Status:** Design proposal, drafted 2026-06-09 (extension loop, iteration 2). Develops branch **B1** of [`measurement-avenues.md`](measurement-avenues.md). Source document for downstream changes to `concept.md`, `pre-registration.md`, `scoring.md`, `DECISIONS.md`. Mirrors [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md) and [`h9-self-calibration.md`](h9-self-calibration.md). **The MVP-1 lock (proposed `DECISIONS.md` §20) is Dave's call** — this is the rigor-bar spec the loop produces, not a self-authorized pre-registration commitment.

**Provenance.** The corpus already varies surface context by design — workplace / family / public / anonymous (`concept.md` §"Anti-gaming"; the "observed vs. anonymous" behavioral signature) — but the instrument scores only a person's *mean* per construct and discards the *spread*. The spread is the signal H10 recovers: how much a person's revealed morality swings across social contexts is, per the person–situation literature, a stable individual difference — moral **context-sensitivity** as character. It costs nothing new to elicit; it is a re-analysis of choices already collected.

---

## 1. The hypothesis statement

**H10 (proposed addition to `pre-registration.md` §6, secondary).**

*The within-person, within-construct variability of revealed scores across surface contexts is a reliable, stable individual difference, distinct from revealed level and from the stated–revealed gap; and revealed scores are systematically more axis-positive in observed/public than in anonymous contexts.*

### 1.1 Measurement primitive

For participant *i*, construct *c* (a primary axis, §2.1), and surface context *k* ∈ {workplace, family, public, anonymous, …} (read from item `context:*` tags, §3), let `r_i(c,k)` be the participant's mean revealed item-score (§2.2) on construct *c* restricted to context-*k* items. Then:

```
mbar_i(c) = mean_k r_i(c,k)                                       # construct context-mean
sd_i(c)   = sqrt( (1/(K_i(c)-1)) * Σ_k ( r_i(c,k) - mbar_i(c) )^2 ) # cross-context SD (sample)
V_i       = mean_c sd_i(c)                                        # person-level variability index
```

All `r` and `sd` are on the same [−1,+1] axis, so `V_i` is unit-legal — but see §1.3 (ceiling/floor artifact). **`sd_i(c)` is the reveal-facing quantity; `V_i` is the cohort-statistic input.**

### 1.2 H10a — variability is reliable (a trait, not noise)

Variability is a trait only if it replicates within-person. Following Fleeson & Gallagher (2009), split each participant's sessions into odd/even halves, recompute the variability index on each, and correlate across participants:

```
H10a statistic:  lower 95% bootstrap-CI bound of  corr( V_i^(odd), V_i^(even) )  ≥ 0.40
```

If the cross-context spread were measurement error, the halves would not correlate; a positive split-half reliability is direct evidence that *how context-sensitive a person is* is itself stable. Threshold modest/secondary (a second-order quantity, as with H9b). Bootstrap: participant-level, 10,000 resamples, seed `20260510` (§8).

### 1.3 H10b — variability is distinct (discriminant)

`V_i` must not be a relabeling of how virtuous, or how self-consistent, a person is. Regress `V_i` on `[ level_i = mean_c mbar_i(c) , gap_i = mean_d |gap(i,d)| (§6) , cal_error_i (§14, where available) ]`; criterion: **upper** 95% CI of model R² **< 0.50**.

> **Range-restriction caveat (load-bearing).** A participant whose mean sits near an axis extreme (±1) has less room to vary, mechanically compressing `sd_i(c)` — which inflates the level↔variability association and risks a spurious "extremists are the consistent ones" reading. H10b is therefore paired with a pre-registered de-confounded analysis: regress `sd_i(c)` on `|mbar_i(c)|` and test whether reliable between-person variance survives in the *residual* (the ceiling-free variability signal). H10b counts as supported only if the discriminant-R² criterion **and** the residual-variability test agree.

### 1.4 H10c — the observer-effect anchor (directional)

A specific, established, directional slice — the observer effect (Rotella et al. 2025, marked "verified" in `concept.md`'s observed-vs-anonymous signature). Within-person:

```
obs_gap_i = mean(r_i over public/observed items) − mean(r_i over anonymous items)
H10c statistic:  lower 95% bootstrap-CI bound of  mean_i obs_gap_i  > 0   (one-sided; directional)
```

H10c grounds H10 in a confirmable directional anchor (variance alone is sign-agnostic) and folds the observed↔anonymous contrast — one dimension of context — into the broader variability construct.

> **Scope note (MVP-1 vs MVP-2).** "Public/observed" here means the scenario's **depicted** setting (items where the portrayed situation is witnessed/public vs. anonymous-online) — a surface-context dimension already present in the MVP-1 corpus (`concept.md` §"Anti-gaming"). It is **distinct** from a participant-level **observer mode** (informing participants that their *own* session answers are watched), which `pre-registration.md` defers to MVP-2 ("no observer mode in MVP-1"). H10c uses the former and does **not** require the latter; an MVP-2 observer mode would add a second, stronger test of the same effect.

### 1.5 N=1 interpretability and value-neutrality

**N=1.** `sd_i(c)` is a within-person quantity on a fixed axis — no cohort standardization — so each participant's per-construct context-sensitivity is reveal-eligible (descriptive: "your honesty is steady across settings; your generosity swings between public and anonymous"). The split-half reliability (H10a) and the discriminant test (H10b) are *cohort* statistics, separate from the reveal — as §14 separated cohort H9 statistics from the N=1 reveal read.

**Suppression (inherits §13).** A construct contributes `sd_i(c)` only with ≥3 distinct contexts each holding ≥2 informative items; below that, suppress (a 2-context SD is a single signed difference dressed as a spread). If a participant clears the threshold on <3 constructs, suppress `V_i` for the reveal and report per-construct only.

**Value-neutrality (the Dancy caveat — load-bearing).** H10 measures context-*sensitivity* and takes no stance on whether consistency is a virtue. Moral particularism (Dancy 2004, already in `concept.md`) holds that responsiveness to context can be the morally *correct* posture, not a failure; the situationist tradition (Doris 2002) treats cross-situational variability as the human default, not a defect. The reveal must not valorize either pole — framing is strictly descriptive (`DECISIONS.md` §6). "Low variability" is reported as *steadiness*, "high" as *responsiveness*, with no ranking.

### 1.6 Falsification and exploratory H10d

Combined H10 = **H10a ∧ H10b** (variability is a reliable, distinct trait). H10c is a standalone directional anchor (confirm/null reported either way). Partial results are published, as with H8/H9.

**Exploratory H10d (cross-link to H9).** Context-driven participants should predict themselves worse: `corr(V_i, cal_error_i) > 0` — high cross-context variability predicts larger H9 self-prediction error (you cannot forecast a self the situation keeps rewriting). Exploratory in MVP-1 (same cohort, but a derived-on-derived correlation); a clean MVP-2 confirmatory target.

---

## 2. Theoretical grounding

### 2.1 The person–situation debate and its resolution (Mischel; Fleeson)
Mischel (1968) showed cross-situational behavioral consistency is lower than trait theory assumed (the "0.30 ceiling"). The resolution is not "no traits" but a richer object: Mischel & Shoda (1995, CAPS) showed people have stable *if-then* signatures (consistent *patterns* of variation), and Fleeson (2001) showed each person's behavior is a **density distribution of states** whose *mean and SD are both stable individual differences*. H10 imports Fleeson's object directly into the moral domain: the SD of a person's revealed morality across contexts is a trait, and Fleeson & Gallagher (2009)'s split-half-of-the-SD is the method (H10a).

### 2.2 The situationist challenge to virtue ethics (Doris)
Doris (2002, *Lack of Character*) argues the empirical variability of moral behavior across situations undercuts the classical notion of robust, cross-situational virtue. H10 makes the live empirical version of that argument *measurable per person*: it neither assumes robust character (trait theory) nor denies it (radical situationism), but estimates, for each individual, how situation-bound their morality actually is.

### 2.3 The value-neutrality constraint (Dancy; particularism)
Treating low variability as "principled/good" is a normative claim H10 must not smuggle. Dancy (2004) and care-ethics traditions hold that the morally mature response is often *context-sensitive*, not invariant. H10 is descriptive; §1.5 fixes the framing.

### 2.4 The directional anchor (observer effect)
The observed↔anonymous gap is the best-replicated single dimension of moral context-sensitivity (Rotella et al. 2025; robust in die-roll and dictator-game literatures, per `concept.md`'s signature table). H10c uses it to give an otherwise sign-agnostic variance construct a confirmable directional prediction. Hofmann et al. (2014)'s experience-sampling finding — everyday morality is heavily context-dependent — is the ecological backdrop that makes context-variance worth measuring at all.

---

## 3. Instrument modification required

### Already in place
- **Surface-context variation** across workplace / family / public / anonymous (`concept.md` §"Anti-gaming"; "aggressive surface variation; same logical structure across settings").
- **The observed-vs-anonymous signature** (`concept.md`) — H10c's contrast is already a named design element.
- **Within-person SE machinery** (`scoring.md` §13.1, `se_i(d)`) — reused to gate `sd_i(c)` against the within-context noise floor.
- **The per-item revealed score and aggregation** (§2–§3) — the inputs; nothing new to elicit.

### What needs to be added
- **A1. Context-tag pass (metadata, NO new scenarios).** Each existing item needs an explicit `context:<setting>` tag (and the observed/anonymous flag) so the analyzer can group within-construct-across-context. The contexts already vary by design; this makes them machine-legible. A small authoring/tagging task, audited for tag validity (which contexts are genuinely comparable for a construct — REL-2-style inter-rater check recommended).
- **A2. Balanced context sampling.** The rotation must ensure each participant sees each construct in ≥3 contexts with ≥2 items each (the §1.5 inclusion floor); otherwise `sd_i(c)` is biased by uneven context coverage. A scheduling constraint, not new content.
- **A3. Scoring spec `§15` (proposed).** Operationalizes `r_i(c,k)`, `sd_i(c)`, `V_i`, the H10a split-half, the H10b discriminant + residual-variability de-confound, H10c, and the §1.5 suppression rules.

This is **pure re-analysis + a tagging/scheduling pass** — the corpus itself does not grow.

---

## 4. Implications for existing locked decisions

**`DECISIONS.md` §16/§17 corpus — untouched.** H10 adds no scenarios. (Contrast §17, which expanded the corpus for H8.) Only tags, scheduling, scoring, and pre-registration change.

**Proposed `DECISIONS.md` §20 (pending Dave's lock).** "Add H10 (cross-situational moral consistency) to MVP-1 as a secondary hypothesis; no new scenarios (requires a `context:*` tag pass + balanced-context scheduling on existing items); scoring `§15`." Rationale: near-zero authoring cost, fully N=1-computable, operationalizes the situationist debate as a moral trait, and reuses an already-designed surface-variation feature. Considered-and-rejected: defer to MVP-2 (loses the shared cohort; the data is already being collected, so deferral wastes it); pool variability into a single "consistency score" (rejected — a composite, forbidden by `concept.md`, and it would mask the construct-level signal). **Not written into `DECISIONS.md` by the loop** — the lock is Dave's, per the h8/h9 precedent.

**Relationship to the "consistency under reframing" signature.** `concept.md` lists "consistency under reframing" as a behavioral signature (with the Dancy caveat already attached). H10 is its formalization and generalization: from a per-item reframing check into a reliable, person-level, cross-context variability trait.

**Reveal.** Per-construct `sd_i(c)` is N=1-computable, so it enters the personal reveal without cohort norms (like H9's calibration, unlike the §6 gap).

---

## 5. Why this is a research contribution

The person–situation debate is one of psychology's oldest, and Fleeson's density-distribution resolution is well-established for personality *states* — but not operationalized as a **moral** trait, and not longitudinally inside an instrument that already separates stated from revealed values. H10 reports something no existing instrument does: not just *what* a person's values are or *whether* they match their stated ones, but *how situation-bound* they are — and (H10d) whether that situation-boundness is what makes them opaque to themselves. It also lets the instrument speak to the Doris situationist challenge with per-person data rather than group averages. All of it falls out of choices already being collected.

---

## 6. Open design questions

**Q1. Context taxonomy granularity.** Four settings (workplace/family/public/anonymous) × observed/anonymous, or a finer grid? Finer = more contexts per construct (better SD estimate) but more items needed for balance. Provisional: the existing four settings + the observed/anonymous flag; resolve against corpus coverage.

**Q2. Ceiling/floor handling.** §1.3 names the residual-variability de-confound; open whether to additionally restrict the confirmatory V_i to mid-range constructs, or model the mean–SD relationship explicitly (Fleeson's approach). Reserved for `scoring.md §15`.

**Q3. Construct weighting in V_i.** Equal-weight constructs, or weight by item count / reliability? Provisional equal-weight (transparent); pilot informs.

**Q4. Is "context" confounded with "stakes"?** Some settings co-vary with stakes (workplace decisions may be higher-stakes than anonymous-online). H10 must hold stakes roughly constant within a construct's context set, or the variance conflates context with the cost-of-virtue dimension (which is H9c / §4's job). Requires the context-tag pass to record stakes alongside setting so the analyzer can check/stratify.

---

## 7. Downstream changes this design unblocks

1. `scoring.md §15` — the variability math, suppression rules, H10a/b/c statistics
2. `pre-registration.md` §6 (H10 secondary) + §5 (the cross-context analysis plan + the residual-variability de-confound)
3. `concept.md` — promote "consistency under reframing" to its H10 formalization; note the N=1-reveal property
4. `scenarios/` — the `context:*` tag pass (+ stakes co-tag per Q4); balanced-context scheduling
5. `DECISIONS.md §20` — the lock (Dave's call)
6. `validity-threats.md` — a CV-style row for context-tag validity (which contexts are truly comparable for a construct) and the range-restriction artifact
7. `analysis/tag_axis_map` — register `context:*` as intentional metadata tags (cf. the §15/DECISIONS cross-domain-tag handling)

---

## 8. Relationship to H9, EV-4, and the observed-vs-anonymous signature

- **H10d ↔ H9.** Cross-context variability predicting self-prediction error links the two: the context-driven self is the hard-to-forecast self.
- **H10 vs. H9c / cost-of-virtue.** H10 is variability across *social context* (who's watching, which relationship) holding stakes roughly constant; H9c and the cost-of-virtue curve are variability across *stakes*. Distinct axes — Q4 keeps them from contaminating each other.
- **Generalizes the observed-vs-anonymous signature.** That signature is one context dimension; H10c confirms it directionally and H10a/b embed it in a full context-variance trait.
- **EV-4 tie.** Both EV-4 (stakes discontinuity) and H10 say a single-context measurement under-describes a person; H10 is the social-context analogue of EV-4's stakes-context point.

---

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) B1 — the branch this develops; roadmap
- [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md), [`h9-self-calibration.md`](h9-self-calibration.md) — sibling design docs; H10d pairs with H9
- [`scoring.md`](scoring.md) §2–§3 (revealed scores), §13.1 (within-person SE), §13 (N=1 discipline), §6 (gap for H10b) — where §15 will be added
- [`concept.md`](concept.md) — surface-variation / observed-vs-anonymous design; "consistency under reframing" signature; Dancy caveat
- [`DECISIONS.md`](DECISIONS.md) §6 (descriptive-only), §16/§17 (corpus, untouched), §20 (proposed)
- [`validity-threats.md`](validity-threats.md) — context-tag validity + range-restriction rows (proposed)
