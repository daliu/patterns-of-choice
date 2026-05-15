# Reading the Analyzer Output

**Status:** Draft 0.1. Companion to `scoring.md` (the technical spec) and `concept.md` (the design rationale). Where scoring.md says *how* the numbers are computed, this doc says *what they mean* — for a user inspecting their own profile, for a researcher reading aggregated cohort data, for a future engineer interpreting outputs in tests.

This doc is intended to be read alongside an actual analyzer run. The examples reference the synthetic fixtures (`analysis/fixtures/sample-*.json`).

---

## What the analyzer outputs

`scripts/analyze.py` produces three or four tables, depending on what input was supplied:

1. **Revealed scores** (always, when a session log is supplied). One row per user × domain. Mean, n_sessions, SE.
2. **Probe break-points** (when `--probes` is supplied). One row per user × domain × probe. Log10 of stake at break; sign-flipped for inverted probes.
3. **Card-sort stated scores** (when `--card-sort` is supplied). One row per user × domain × layer. Fraction of in-domain values in the user's top-5.
4. **Gaps** (when both `--log` and `--card-sort` are supplied). One row per user × domain. Z-scored stated minus z-scored revealed, standardized within-domain across the sample.

Each section can be read on its own. The signal that the project is built around is the gap.

---

## Reading revealed scores

```
user_id                  domain                        mean  sess      se
-------------------------------------------------------------------------
user-alice               truth-telling               +0.875     1     nan
user-bob                 truth-telling               -0.396     2   0.329
```

**Range:** [−1, +1] per the clamp in scoring.md §2.2.

**Sign:** positive = ethical pole of the domain's primary axis. For truth-telling, positive = more honest choices. For resource-allocation, positive = more generosity-side. For in-group/out-group, positive = more loyalty-side. For reciprocity-cooperation, positive = more trust-side.

The "ethical pole" framing is deliberate but contested in the literature — the primary axis was chosen to point toward what *most* moral frameworks would call the more-ethical direction, but a moral particularist would object that there's no domain-general ethical direction. See `concept.md` §"Smuggled value claims" and `literature/ethical-frameworks.md` for the meta-ethical caveats.

**What individual values mean:**
- `+1.0` = user picked the ethical option on every item in the domain
- `0.0` = exact balance (or alternation)
- `−1.0` = user picked the unethical option on every item

**`sess`** = number of sessions contributing to this score. With small `sess`, the score is noisy; `se` (standard error) gets large.

**`nan` in `se`** = only one session contributed; standard error is undefined. The validation-cohort analyzer would use bootstrap CIs instead per scoring.md §8.

**What doesn't this measure?** Anything about a user's *stated* values. Honesty *in the choices* is observed; honesty *as a self-described value* is in the card-sort and pairwise sections. The whole project is built on these being separately measured.

---

## Reading probe break-points

```
user_id                  domain                     probe_id                log_score  inv
------------------------------------------------------------------------------------------
user-alice               truth-telling              cov-truth-001              +5.000    N
user-bob                 truth-telling              cov-truth-001              +1.000    N
user-alice               resource-allocation        cov-allocation-001         -1.000    Y
```

**`log_score`** = `log10` of the stake at the user's break-point.

**Sign convention** is direction-aware:
- For **forward probes** (`inv = N`, e.g. `cov-truth-001`): the user accepts the unethical action at some stake. Higher score = stronger virtue (won't break until higher stakes).
  - `+1.0` = breaks at $10 (very low integrity)
  - `+5.0` = "never" (full integrity ceiling)
- For **inverted probes** (`inv = Y`, e.g. `cov-allocation-001` returning a found overpayment): the user does the ethical action at some stake. Sign-flipped so within the inverted range, higher score = stronger virtue.
  - `−1.0` = returns at $10 (returns at low stakes — strongest virtue within range)
  - `−5.0` = "never" returns (weakest virtue within range)

**Forward and inverted scores are NOT directly comparable** across probe types. The cross-probe-type normalization happens at the per-domain CFA aggregation step in `scoring.md §7`, which the validation-cohort analyzer would implement.

For the synthetic fixture: Alice never accepts paid review (+5.0) and returns overpayment at $10 (−1.0) — internally consistent high-integrity profile across both forward and inverted probes. Bob accepts at $10 (+1.0) and never returns (−5.0) — internally consistent low-integrity profile.

**The single-number summary for a user × domain across multiple probes is what the CFA would produce.** This analyzer doesn't aggregate; it shows the raw per-probe break-points for inspection.

---

## Reading card-sort stated scores

```
user_id     domain         layer                frac_in_top5
user-alice  truth-telling  current_self                0.600
user-alice  truth-telling  aspirational_self           0.600
user-alice  truth-telling  admired_other               0.400
```

**`frac_in_top5`** = fraction of in-domain values that appear in the user's top-5 selection for that layer.

There are 5 values in each MVP-1 domain. So:
- `0.0` = no in-domain values in user's top-5
- `0.2` = 1 in-domain value in top-5
- `0.4` = 2 in-domain values in top-5
- `0.6` = 3 in-domain values in top-5
- `0.8` = 4 in-domain values in top-5
- `1.0` = all 5 in-domain values in top-5 (only one user × layer × domain can hit this, since each user picks only 5 of the 20-value pool)

**Three layers per user.** The triple `(current_self, aspirational_self, admired_other)` gives three views of the same construct:
- **current_self**: how the user actually describes themselves
- **aspirational_self**: who they want to become
- **admired_other**: traits they identify in someone they respect (dodges self-flattery)

**Common patterns to look for:**
- `current_self ≈ aspirational_self` → user is satisfied with their stated identity on this dimension
- `aspirational_self > current_self` → user wants to grow toward this domain
- `admired_other > aspirational_self` → user identifies the value in others but doesn't aspire to it themselves (interesting signal — maybe they think it's not their job, or maybe they're underselling their aspiration)
- All three layers low → this domain isn't part of the user's stated value system at all

**Don't read too much into a single layer's value.** The signal is in the relationships across layers.

---

## Reading the gap

This is the central output.

```
user_id     domain         z_revealed  z_stated     gap
-------------------------------------------------------
user-alice  truth-telling      +1.020    +1.000  -0.020
user-carla  truth-telling      -0.042    +0.000  +0.042
```

**`z_revealed`** = the user's revealed score in this domain, z-scored against the sample distribution.

**`z_stated`** = the user's aspirational-layer card-sort score, z-scored against the sample distribution.

**`gap`** = `z_stated − z_revealed`. Both terms standardized.

### What positive vs negative gap means

- **Positive gap** (z_stated > z_revealed): the user *aspires* to be more virtuous on this dimension than their *choices* actually reveal them to be. The standard interpretation: this is the user's growth direction.
- **Negative gap** (z_stated < z_revealed): the user reveals more virtue than they claim to value. Two possible readings:
  - Modesty / self-deprecation (user undersells their stated values)
  - The user actively prioritizes this less than their behavior suggests; they just behave consistently with it for other reasons

- **Gap ≈ 0**: stated and revealed are aligned. The user lives the value they claim, or doesn't live the value they don't claim. Not necessarily "good" — alignment around an unstated value the user *should* care about is its own kind of gap.

### Sample-relative interpretation

**Z-scores are within-sample**: standardization is done across the users in the cohort, per-domain. So `z_revealed = +1.0` means "this user is one standard deviation above the mean of the sample on revealed truth-telling," not "this user is in the 84th percentile of all humans."

With small samples (the synthetic fixtures have 3 users), the standardization is noisy — scores cluster tightly around 0 except for the extreme users. In a real validation cohort (n = 200 per the pre-registration), the distribution would be much richer.

### What the gap doesn't tell you

- **The absolute level of virtue**: a user can have a small gap while being uniformly low. The gap is *relative*, not absolute.
- **Why the gap exists**: gap-analysis is descriptive, not explanatory. The user might have a gap because they aspire to growth (positive direction), or because they're inflating in self-report (a different process producing the same number).
- **The direction of causation between stated and revealed**: the analyzer can't say whether stated values pull revealed behavior (intention-driven) or vice versa (rationalization).

---

## Edge cases and warnings

### Single-session users
A user with only one session in a domain has `nan` standard error. Their revealed score might be entirely shaped by that one session's particular scenario sample. Treat as provisional.

### Single-user domains
If only one user in the sample has revealed data for a domain (as with `user-alice` and `resource-allocation` in the fixtures), the gap is **not computed** for that domain. Per scoring.md §6, sample standardization requires ≥2 users per domain.

### Cross-domain comparison
Z-scores are within-domain. A user's `z_revealed = +1.0` in truth-telling and `z_revealed = −0.5` in resource-allocation does NOT mean they're more honest than they are generous in any absolute sense — it means their position relative to the sample differs between the two domains.

### Tag drift
If new scenarios introduce tags not in `analysis/tag_axis_map_v0.1.csv`, the analyzer will silently exclude those tags from scoring (they're treated as if absent). The `validate.py` tooling catches unknown tags as errors. **Run validate.py before trusting analyzer output.**

### Per-scenario-domain scoring
Cross-domain `value:X` tags (e.g., `value:loyalty` appearing in a truth-telling scenario) are deliberately not scored on the loyalty axis. See `DECISIONS.md §15` for the rationale and the pre-registration consequence.

---

## How findings connect to the validation hypotheses

The pre-registration's primary hypotheses are:

- **H1: Construct validity (4-factor CFA fit).** Revealed-score table feeds the CFA per scoring.md §7. The analyzer doesn't run the CFA (needs `lavaan` / `statsmodels`); the table here is the raw input.
- **H2: HEXACO honesty-humility convergent validity (r ≥ 0.25, lower-95-CI ≥ 0.15).** The revealed truth-telling column is what would be correlated with HEXACO H scores in the validation cohort. Synthetic fixtures here don't include HEXACO data; that's collected separately per the MVP-1 protocol.
- **H3: Test-retest reliability (r ≥ 0.60 per domain across weeks 1-2 vs. 3-4).** Computed from session-log time-stamps in a longer-running cohort; this analyzer would produce the inputs but doesn't compute the split-half correlation itself.

**The gap signal is exploratory, not pre-registered as a primary hypothesis.** Per the pre-reg, the gap is reported as a finding once measurement validity (H1-H3) is established. Treating gap results as primary before that would be over-interpretation.

---

## Open interpretation questions

- **Identity-claim weighting**: scoring.md §5 distinguishes "I am X" identity-level from "I value X" trait-level claims. The current card-sort scoring conflates them. The validation analyzer should separate.
- **Reliability of the per-domain mean**: the analyzer reports `se` as a one-step standard error. For longitudinal users, a within-user variance component (across-sessions) is more meaningful than the cross-sample SE; the validation analyzer should compute this.
- **Probe trajectory direction**: a user whose log10 break-point increases over sessions is consolidating; decreasing is drifting. The longitudinal interpretation (scoring.md §4.3) is reserved for the validation analyzer.

---

## Cross-references

- `scoring.md` — technical spec for how each number is computed
- `concept.md` §"Core insight" — the design rationale for the gap as the central signal
- `pre-registration.md` — which numbers are pre-specified validation hypotheses vs. exploratory
- `scripts/analyze.py` — the analyzer implementing the spec
- `scripts/README.md` — how to run the analyzer
- `DECISIONS.md §15` — per-scenario-domain scoring (why cross-domain value tags are metadata)
