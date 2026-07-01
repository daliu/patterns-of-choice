# Scoring Specification — MVP-1

**Status:** Draft 0.1. Defines how raw session-log data and inventory responses become the scores referenced by `pre-registration.md`. Locks before OSF pre-registration is filed.

This document does not specify an implementation; it specifies the math. Any analyzer (R, Python, TypeScript) that follows this spec is acceptable as long as the test suite matches.

---

## Scope

Specifies:
- Per-item revealed score from a single user choice
- Per-session and per-domain aggregation
- Cost-of-virtue probe scoring (including the inverted-probe convention)
- Inventory scoring (card-sort, pairwise via Bradley-Terry, story-prompt LLM coding)
- Per-domain gap computation
- Confidence-interval procedure
- Exclusion rules and edge cases

Does *not* specify:
- Recruitment / sampling procedure (see `pre-registration.md` §3)
- Storage / runtime implementation (see `mvp.md` tech-stack)
- Intervention-layer scoring (MVP-2)

---

## 1. Inputs

### 1.1 Session log entry (per choice)

```json
{
  "session_id": "uuid-v4",
  "user_id": "uuid-v4",
  "timestamp_iso": "2026-05-10T17:42:13.823Z",
  "scenario_id": "qf-truth-001",
  "scenario_type": "quick-fire-round",
  "domain": "truth-telling",
  "item_id": "qf-truth-001-i01",
  "option_id": "a",
  "tags": ["truth:commission", "counterparty:close", "stake:micro", "self-cost:apologize"],
  "response_time_ms": 4230,
  "presented_position": 3,
  "was_timeout": false
}
```

`tags` is denormalized at log-write time from the scenario JSON. This is intentional: it makes the analyzer independent of scenario-corpus state, and it pre-registers the tag set effective at the moment of choice.

### 1.2 Inventory entries

Card-sort, pairwise, and story-prompt entries each have their own schemas; see `inventory/SCHEMA.md`. The relevant fields the analyzer consumes:

- Card-sort: `(user_id, layer, value_id, selected: bool, sort_order)`
- Pairwise: `(user_id, layer, pair_id, left_id, right_id, choice: "left"|"right"|"skip", response_time_ms)`
- Story-prompt: `(user_id, prompt_id, text, llm_coded_tags: [{domain, value_id, confidence}])`

### 1.3 Cost-of-virtue probe entries

```json
{
  "user_id": "uuid",
  "session_id": "uuid",
  "probe_id": "cov-truth-001",
  "domain": "truth-telling",
  "value_slot": "honesty",
  "first_accept_rung": 3,            // ladder rung at which user first accepts (or "never")
  "first_accept_stake": 1000,        // dollar amount at first accept; null if "never"
  "is_inverted": false               // see §4
}
```

---

## 2. Per-item revealed score

Each scenario item has a *primary axis* — the value dimension the item most clearly bears on. The user's choice yields a signed contribution on that axis.

### 2.1 Tag-to-axis mapping (excerpt — full table in §11)

**Domain: truth-telling. Primary axis: `honesty` (range −1 to +1).**

| Tag | Contribution |
|---|---|
| `truth:commission`, `truth:confront-direct` | +1.0 |
| `truth:confront-mild`, `truth:state` | +0.7 |
| `truth:partial`, `truth:acknowledge`, `truth:soft-confront`, `truth:deferred-confront` | +0.5 |
| `truth:implicit` | +0.3 |
| `lie:white`, `lie:protective` | −0.5 |
| `lie:omission` | −0.7 |
| `lie:commission`, `truth:abandon` | −1.0 |

When a chosen option has multiple primary-axis tags, contributions are summed and clamped to [−1, +1].

### 2.2 Per-item primary-axis score

```
item_score = clamp(sum(tag_contribution for tag in chosen_option.tags), -1, +1)
```

Items where the chosen option carries *no* primary-axis tag are coded `NA` for that axis (not zero — zero is an explicit neutrality signal; NA is an authoring gap and is excluded from the domain mean).

### 2.3 Per-item secondary-axis scores

Two domains (in-group/out-group; reciprocity-cooperation) have meaningful *second* axes for cross-domain interpretation:

- **In-group/out-group secondary axis: `circle_radius`** (boundaries → hospitality). Same tag-table approach; full mapping in §11.
- **Reciprocity-cooperation secondary axis: `cooperation_orientation`** (independence → cooperation). Same.

Secondary axes are computed but not used in the primary CFA (§7); they're pre-registered as *exploratory* analyses.

---

## 3. Per-session and per-domain aggregation

### 3.1 Per-session revealed score (one domain)

For each session covering domain *d* and primary axis *a*:

```
session_score(user, session, d, a) = mean(item_score for item in session.items where item.domain == d)
```

NA items are excluded from the mean (case-wise exclusion). If fewer than 3 items in the session contribute to the axis, the session score is NA.

### 3.2 Per-user per-domain revealed score

```
revealed_score(user, d, a) = mean(session_score(user, session, d, a) for session in user.sessions where session.domain == d)
```

This is the primary user-level revealed score and the input to convergent-validity tests (`pre-registration.md` H2).

---

## 4. Cost-of-virtue probe scoring

### 4.1 Forward probes

For a forward probe (e.g., `cov-truth-001`): `break_point = first_accept_stake`.

If the user selected `never`: `break_point = +∞`.

Higher break points = more resistance to trading the stated value, i.e., a *stronger* virtue. The reported variable is `log10(break_point)` to compress the geometric ladder, with `+∞` recoded to `log10(max_rung) + 1` for analysis (i.e., one rung beyond the ladder top) — this is the pre-registered handling, not interpolation.

### 4.2 Inverted probes

For an inverted probe (e.g., `cov-allocation-001`, where the ladder asks at what overpayment the user *returns* the money rather than *keeps* it): the analyzer reads `analysis.break_point_field` and `analysis.no_break_point_handling` from the probe JSON. For inverted probes, `break_point = first_return_stake`, lower break points = *stronger* virtue (user returns earlier). The sign is flipped at the per-user-per-domain aggregation step so that all probe scores are directionally comparable across domains.

### 4.3 Probe trajectory (longitudinal)

Within-user trajectory of `log10(break_point)` across sessions is the primary longitudinal signal. Pre-registered analyses: trajectory slope per user, classified into *increasing* (virtue consolidation), *decreasing* (drift), or *stable* (within ±0.1 log-units per month). Exploratory: clustering of trajectory shapes.

---

## 5. Inventory (stated) scoring

### 5.1 Card-sort

Each layer (current / aspirational / admired-other) yields a top-5 set of `value_id`s. Each value's `card_sort_indicator` is `1` if selected, `0` otherwise. Aggregated to per-domain by mean over the values in that domain.

```
card_sort_stated(user, d, layer) = mean(card_sort_indicator(user, value_id, layer)
                                        for value_id in values_in_domain(d))
```

Range [0, 1]. Standardized within the sample at the analysis stage.

### 5.2 Pairwise (Bradley-Terry)

For each layer, fit a Bradley-Terry model on the user's pairwise choices to recover a latent utility *β_value* per value. Per-domain stated score:

```
pairwise_stated(user, d, layer) = mean(β_value for value_id in values_in_domain(d))
```

Implementation: `BradleyTerry2` package in R or equivalent. Posterior median is the point estimate; 90% credible interval is reported alongside.

### 5.3 Combined stated score

Per-domain stated score is the **mean of the within-domain standardized card-sort score and pairwise score**, per layer:

```
stated_score(user, d, layer) = mean(z(card_sort_stated), z(pairwise_stated))
```

Where `z()` is sample-level standardization. The mean is taken across the two sources; if one is missing (e.g., user skipped pairwise), the surviving source is used and a flag is logged.

### 5.4 Story-prompt contribution

Pre-registered as **exploratory only** for MVP-1: the LLM-coded story tags per user are summarized as a per-domain "spontaneous mention" frequency, reported descriptively. Not folded into the primary stated score because the coding pipeline is not yet validated at the κ ≥ 0.70 threshold the inventory README requires.

---

## 6. Gap computation

Primary gap (pre-registered):

```
gap(user, d) = stated_score(user, d, layer="aspirational") - revealed_score(user, d, primary_axis)
```

Both terms are sample-standardized before subtraction. Range typically [-3, +3] standard deviations.

Secondary gaps (exploratory):
- *Current→aspirational gap*: aspirational − current. Pure inventory; tests aspiration-inflation.
- *Aspirational→admired-other gap*: admired-other − aspirational. Honesty check on aspiration.

---

## 7. CFA strategy

For the construct-validity test (`pre-registration.md` H1), CFA cannot use one indicator per domain (under-identified). The pre-registered indicator scheme is **three indicators per domain**, computed per user:

1. *Quick-fire indicator*: mean of all quick-fire-round item scores in this domain across the protocol
2. *Narrative indicator*: mean of branching-narrative terminal-resolution scores in this domain across the protocol
3. *Cost-of-virtue indicator*: standardized cost-of-virtue probe break-point in this domain (sign-flipped for inverted probes)

That gives 12 indicators across 4 latent factors (domains) — adequate for a CFA. Implementation in `lavaan`.

If indicator (2) or (3) has too much missing data for a given domain at analysis time, the analyzer falls back to indicators (1) plus a secondary-axis aggregation, and the deviation is reported.

---

## 8. Confidence intervals

All point estimates report **95% bootstrap CIs** with 10,000 resamples at the participant level. Bootstrap is non-parametric and stratified by attention-check status (passed vs. flagged) when subgroup analyses are run. Random seed `20260510` (or update at pre-registration lock) is pre-committed for reproducibility.

---

## 9. H8 narrative-immersion scores (divergence and attachment)

This section operationalizes the H8 secondary hypothesis (`pre-registration.md` §6; design rationale in `h8-narrative-immersion-design.md`). H8 has two sub-hypotheses, each with its own derived score. All inputs are the standard revealed per-item scores of §2–§3; nothing here introduces a new scale.

**Status.** H8a (debiasing, §9.2) — the headline correlation `rho_8a`, its bootstrap CI, and the **conjoined de-coupled Frisch–Waugh–Lovell partial-association guard** — is BUILT (`analyze.py --h8-log --h8-manifest`, gated in `check_analyzer_thresholds.py` on `analysis/fixtures/sample-h8-log.json`). H8 is a **secondary, cohort-level** hypothesis (§9.5): it produces **no per-person reveal and no on-device surface**, so it adds nothing to the `poc-projection.js` ↔ `analyze.py` parity contract and **parity stays 9/9** (`poc-projection.js` untouched). H8b (attachment-laden shift, §9.4) is DEFERRED — it requires the per-character `attachment_strength` instrument (§9.3), which needs the NPC-cast + high-stakes attachment elicitation (surfaced to Dave). Three pre-registration reconciliations were resolved at build time and are **surfaced for Dave's lock, not auto-locked** (proposed as **DECISIONS §28**):

1. **Sign → positive.** The design doc §1 called the correlation "negative" under an assumed *revealed − stated* gap; under scoring.md §6's canonical *stated − revealed* convention the same prediction is **positive**. Implemented positive (the §9.2 Sign note is now resolved).
2. **Standardization is per-item, not pooled.** `r_narr` and `r_abs` are z-scored **per (pair, form) across users** (§2 per-item standardization); `stated_aspirational` is z-scored **per domain across users** (§6). Pearson `r` is invariant to per-variable affine scaling, so the self-checking generator can verify ground truth by running the real analyzer path.
3. **De-coupling guard uses the CI, not the point sign.** The spec framed the §9.2 de-coupled guard as "partial sign > 0." Under the §9.2 null the point sign is a coin-flip (non-deterministic, not falsifiable), so the guard was **tightened** to require the partial's **lower 95% bootstrap CI > 0** (reliably positive) — strictly stronger (CI_low > 0 ⟹ point > 0) and deterministically gate-able. See §9.2.

### 9.1 Paired-probe divergence score `D`

A *paired probe* is one construct presented to the same participant in two structurally-equivalent forms at well-separated sessions (order counterbalanced across participants):

- **narrative form** — embedded in an established arc, attachment-laden where applicable;
- **abstract form** — a structurally-equivalent quick-fire item.

**Which forms pair (input).** The narrative↔abstract pairing is *not* inferable from the scenarios themselves; it is declared in a manifest, `scenarios/h8-probe-pairs.json` (mirroring how `inventory/pairwise-pairs.json` declares pairwise comparisons). Each entry carries `pair_id`, `construct`, `domain`, `stakes_level` (`low` → H8a pool §9.2, `high` → H8b pool §9.4), a `narrative_ref` {scenario_id, signal}, an `abstract_ref` {scenario_id, item_id}, and — for high-stakes pairs — an `npc_ref` into `scenarios/npc-cast.json` so §9.4 can fetch the matching `attachment_strength`. The analyzer reads pairs from this manifest; a pair contributes only if the participant completed *both* referenced forms (§9.5 inclusion). Note `narrative_ref.signal` pins *which* scene/terminal is read, not *how* a narrative resolves to one scalar — that (terminal-based vs path-based) is the open question in §11 and must be resolved before lock.

Both forms are scored on the same primary-axis scale as any other revealed item (§2.2). For participant *i* and paired probe *p*:

```
r_narr(i,p) = primary-axis revealed score, narrative form
r_abs(i,p)  = primary-axis revealed score, abstract form
D_i^p       = r_narr(i,p) - r_abs(i,p)
```

`D_i^p > 0` means the narrative form elicited a more axis-positive response (e.g. more honest, more generous) than the abstract form. Both terms are sample-standardized (§2) before subtraction, so `D` is in standard-deviation units.

### 9.2 H8a — debiasing (low-stakes paired probes) (BUILT — conjoined headline + de-coupled guard)

H8a predicts that participants whose abstract-form behaviour falls furthest short of their *stated* values show the largest narrative-induced shift toward those values.

Using the canonical gap convention of §6 (stated − revealed; positive = states higher than acts), define the per-probe abstract gap, then aggregate to one pair of values per participant over their low-stakes complete pairs:

```
gap_abs(i,p) = s_i(domain of p, aspirational) - r_abs(i,p)
D_i^(low)    = mean_p D_i^p            over low-stakes pairs
gap_i^(abs)  = mean_p gap_abs(i,p)     over the same pairs
```

**H8a test statistic:** Pearson correlation across participants `rho_8a = corr(D_i^(low), gap_i^(abs))`; the H8a criterion is a **lower 95% bootstrap-CI bound ≥ 0.15** (positive). Spearman is reported as a distribution-free robustness check.

> **Sign note (RESOLVED at build).** The one-line statement in `h8-narrative-immersion-design.md` §1 calls this correlation "negative"; that phrasing assumed a *revealed − stated* gap. Under scoring.md §6's canonical *stated − revealed* convention the predicted sign is **positive**. scoring.md's convention is canonical for the OSF filing — the two statements describe the same prediction, differing only in the gap's sign convention. **Implemented positive** (`compute_h8a_debiasing`, `H8A_RHO_FLOOR = +0.15`); surfaced for Dave's DECISIONS §28 lock.

> **Mathematical-coupling caveat (BUILT — the load-bearing discipline).** `D_i^(low)` and `gap_i^(abs)` share the term `r_abs`, which inflates their correlation even under the null (a regression-to-the-mean artifact: under §2 z-scoring the artifact correlation is ≈ √(1 − ρ_na)/2, positive whenever the narrative and abstract forms are less than perfectly correlated). The confirmatory H8a test is therefore **conjoined** with a de-coupled analysis via **Frisch–Waugh–Lovell**: `partial_r = corr( resid(r_narr ~ r_abs), resid(stated ~ r_abs) )` (reusing `_ols_residuals` twice), which asks whether the narrative response is pulled toward the stated value *beyond* what the abstract response already predicts. Both arms are computed over the **same included cohort** — participants with ≥ 3 complete low-stakes pairs (§9.5); below-floor participants leak into neither arm. **H8a is SUPPORTED iff the headline lower-CI criterion (≥ 0.15) AND the de-coupled guard both hold.** The guard is the **lower 95% bootstrap CI of `partial_r` > 0**, not the point sign — under this null the point sign is a coin-flip, so a point-sign test is not falsifiable; the CI test is deterministic and strictly stronger (see §9-Status ¶3). `check_h8a_decoupling_lock` proves this is load-bearing: on an n=100 honest null the **headline** lower-CI clears 0.15 by the artifact alone (`headline_met` True) yet the partial CI straddles 0, so `supported` is **False**.

### 9.3 Attachment strength `attachment_strength`

Attachment is measured **per character** (resolving design-doc Q4) so it can be matched to the specific character featured in each high-stakes probe. This is mode-agnostic: it works whether the locked design is Mode A (central-buddy) or Mode B (flat-ensemble). For participant *i* and recurring character *c*:

```
selfreport(i,c) = mean over administrations (sessions 8/16/24) of the
                  z-scored PSR-PRD adaptation (Tukachinsky 2010) for c
latencygap(i,c) = z-scored slope, over sessions, of
                  RT(c-mentioning items) - RT(matched generic-role items)
attachment_strength(i,c) = mean( selfreport(i,c), latencygap(i,c) )
```

If the behavioural channel is too sparse for character *c* (pre-registered minimum: latency available in ≥ 3 sessions), `attachment_strength` falls back to `selfreport` alone and the substitution is logged. Both channels are z-scored within-sample before combination so neither dominates by scale.

### 9.4 H8b — attachment-laden shift (high-stakes paired probes) (DEFERRED — needs the §9.3 attachment instrument)

H8b predicts that, on high-stakes probes where a specific character's welfare is at stake, more-attached participants deviate more from their abstract-form response. Because the protective direction is not assumed in advance, H8b uses deviation **magnitude**. For each high-stakes attachment-laden pair *p* featuring character `c(p)`, aggregate per participant over their such pairs:

```
absD_i^(high) = mean_p | D_i^p |                     over high-stakes pairs
att_i         = mean_p attachment_strength(i, c(p))  over the same pairs
```

**H8b test statistic:** Pearson correlation `rho_8b = corr(absD_i^(high), att_i)`; criterion **lower 95% bootstrap-CI bound ≥ 0.20**. A directional companion analysis (signed `D` toward the protective option, on probes that define one) is reported as exploratory.

### 9.5 Estimation, inclusion, and power

- **CIs and seed.** Both `rho_8a` and `rho_8b` use participant-level non-parametric bootstrap, 10,000 resamples, seed `20260510` — identical to §8.
- **Per-participant inclusion.** A pair contributes only if **both** forms were completed (neither timed-out nor missing). A participant enters H8a with ≥ 3 complete low-stakes pairs; enters H8b with ≥ 2 complete high-stakes attachment-laden pairs **and** a valid `attachment_strength` for each featured character.
- **Order effects.** Presentation order (narrative-first vs abstract-first) is counterbalanced and entered as a covariate; a non-trivial order main-effect is reported, and if large the analysis is re-run within order strata.
- **Aggregation alternative.** Person-level aggregation (above) is the confirmatory specification, chosen for transparency. A probe-within-person mixed-effects model is pre-registered as a robustness check; material divergence between the two is reported.
- **Status and power.** H8 is *secondary*: reported with effect sizes and CIs, never a gate-criterion for instrument validation (contrast §7 / H1). At n=200 the lower-CI thresholds (0.15, 0.20) are deliberately modest — H8 is powered to detect a directional effect, not to bound it tightly.

---

## 10. Exclusion rules

Per `pre-registration.md` §5:

- Users with < 14 completed sessions are excluded from primary analyses (sensitivity-analyzed at < 7 and < 21).
- Sessions with quick-fire median response time < 2 s are dropped as inattentive.
- Probe responses with no choice (timed-out, not yet implemented; the no-option must be explicitly clicked) are coded as missing, *not* as the no-option default.
- Pairwise items where the user consistently chooses left or right > 90% of the time are flagged but retained; analyst inspects for bias.

---

## 11. Tag-to-axis tables (truncated)

The full mapping table per domain ships as a versioned data file `analysis/tag_axis_map_v0.1.csv` and is referenced (not re-defined) in any analyzer. Maintaining the mapping in a separate file makes the analyzer independent of the scenario corpus and lets pre-registered tag-mappings be locked at OSF filing time while scenarios continue to evolve.

Excerpts (the full file enumerates all currently-used tags across the scenario corpus):

```
domain,axis,tag,contribution
truth-telling,honesty,truth:commission,+1.0
truth-telling,honesty,truth:confront-direct,+1.0
truth-telling,honesty,truth:partial,+0.5
truth-telling,honesty,lie:white,-0.5
truth-telling,honesty,lie:commission,-1.0
resource-allocation,generosity,generosity,+1.0
resource-allocation,generosity,self_reliance,-0.7
in-group-out-group,loyalty,loyalty,+1.0
in-group-out-group,loyalty,universalism,-1.0
reciprocity-cooperation,trust,trust,+1.0
reciprocity-cooperation,trust,vigilance,-1.0
...
```

Authoring discipline: a new scenario item's tag set must be auditable against this mapping before merge. A CI hook (TODO) enforces this.

---

## 13. Per-person value weighting (ipsative; reference-free)

**Status:** Draft 0.1. Defines the "value-weighting" layer. Every quantity here is computed from **one person's own rows** and is interpretable for an N of 1. This section deliberately does **not** add any new scale and does **not** invoke the §6 gap or any sample z-score (those need ≥2 users; see §6 and interpretation.md "Single-user domains"). It is the self-against-self longitudinal case explicitly permitted by `DECISIONS.md` ("No leaderboards") — not a cross-person comparison.

A "weighting" is **a within-person ordering and a revealed price, never a composite and never a score-out-of-N** (`concept.md`: "refuse to ship a single 'ethics score'"). Three independent reads are produced; they are **never averaged together** (different units — averaging would manufacture a pseudo-quantity).

### 13.1 Ipsative domain ordering (behavioral)

For person *i*, take the per-domain revealed means `m_i(d) = revealed_score(user=i, d, primary_axis)` (§3.2, range [−1,+1]) over the domains `D_i` that clear §10 inclusion (≥14 sessions; sensitivity ≥7). Domains below inclusion are **omitted, not zero-filled**.

Self-anchor on the person's **own** unweighted cross-domain mean:

```
mbar_i   = mean_{d in D_i} m_i(d)
dev_i(d) = m_i(d) - mbar_i
```

The ordering is `rank(dev_i(d))` descending. **Deltas are gated by the person's own across-session noise, not a cohort SD.** For an adjacent pair `(d, d')`, assert "d above d'" only if

```
| m_i(d) - m_i(d') |  >  k * sqrt( se_i(d)^2 + se_i(d')^2 )
```

where `se_i(d)` is the §3.2/§8 within-person across-session SE (use `k = 1` for the descriptive readout; bootstrap per §8 if sessions allow). Pairs failing the gate are an explicit **TIE band**, not a rank.

A small **floor** is applied to each `se_i(d)` in quadrature — `se_eff = sqrt(se_i(d)^2 + se_floor^2)`, with `se_floor = 0.07` on the [−1,+1] axis — so that an implausibly small within-person SE (e.g. a domain with only 2 sessions that happened to land identically, giving `se = 0`) cannot collapse the gate to zero and manufacture a confident ordering from a trivial mean difference. At `se = 0` the floor sets the minimum orderable adjacent gap to `≈ k·se_floor·√2 ≈ 0.10`, matching the §13.4 fragility threshold (`|delta_revealed| < 0.1`). The floor is a tunable constant (`SE_FLOOR` in `runtime/poc-projection.js`).

**Hard preconditions (suppress the ordering entirely if unmet):**
- `se_i(d)` must be **computable** for the gated domains, i.e. ≥2 sessions/domain. With a single session (`se = nan`, see interpretation.md "Single-session users") the ordering is **suppressed**, not emitted as "provisional" — a "provisional rank" is read as a rank.
- Require **≥3 informative domains**. With 2 domains the "order" is a single sign and carries no representable uncertainty; it is suppressed.
- If the total spread `max_d dev_i(d) − min_d dev_i(d)` is itself within the pooled within-person SE, report **"no reliable ordering — your four values are roughly level for you,"** not a rank (this is the load-bearing defense against the ipsative zero-sum artifact, §13.4).

### 13.2 Cost-of-virtue revealed price (the per-person price atom)

The §4 break-point is read **directly as a revealed price in the person's own currency** — an absolute, self-anchored quantity, meaningful at N=1 because dollars are an external scale the person committed to. For person *i*, domain *d*, and a single probe *p*:

```
price_i(p) = log10( first_accept_stake )            # forward probe
price_i(p) = -log10( first_return_stake )           # inverted probe (axis-direction flip, §4.2)
```

**Censoring is explicit and load-bearing.** A `"never"` (or `always_keep`) response is **not a measured price**; it is `price > ladder top`. It is reported as right-censored ("at or above the $X ladder top — not measured higher") and **must never be turned into a finite number** for a gap (§13.3). The §4.1 `log10(max_rung)+1` recode is for the longitudinal-trajectory use (§4.3) only; it is **not** a price and is **not** admissible into a §13.3 delta.

Always retain the dollar form `10**price` and the modal break-rung for plain-language reporting.

**Per-domain price** is reported per-probe, not as one scalar, **unless** all of that domain's probes share one ladder (same rung-stake tuple) and one axis-direction. If a domain mixes ladders (e.g. reciprocity holds a `$0–$100k` forgiveness probe and a `$10k–$10M` cooperation probe) or mixes forward/inverted probes, each probe's price is reported separately; **no per-domain price average is taken.**

### 13.3 Within-person break-point gap (the pairwise readout)

The unit of meaning is the **gap between two of the person's own prices**:

```
delta_i(p1, p2) = price_i(p1) - price_i(p2)     # "~10**delta times more/fewer dollars before trading p1 vs p2"
```

A delta is computed **only if both probes share an identical rung-stake ladder AND the same ethical-axis direction**; otherwise emit **"not comparable — different stake ladders / opposite cost direction,"** not a number. (Verified necessity: a break at the floor of a `$5k–$5M` ladder vs the floor of a `$10–$10k` ladder yields `delta = log10(5000/10)` from *probe authoring*, not from a real price difference. In the current corpus the only large comparable family is the `$10–$10k` forward set.)

Axis-direction is **not** the §4 inverted flag (which is set only by `break_point_field == 'first_return_stake'` and does not encode true ethical direction). Read direction from each probe's `analysis.no_break_point_handling` ("lower break-point = more ethical" vs "higher = more ethical") and carry it through every comparison.

Each surviving delta is gated behind **both** the within-person across-session SD test (§4.3 trajectory machinery reused as a within-person error bar — a single-subject quantity) **and** the §10 minimum probe count, labeling sub-threshold pairs **"indistinguishable for you."** Any delta with a censored (`"never"`) endpoint is **suppressed** (you cannot subtract `price > top`).

**Invariant (enforced in code, not prose): prices are never summed or averaged across domains into any single figure.** A cross-domain total has no N=1 interpretation.

### 13.4 Stated-vs-revealed concordance (word-order vs deed-order)

This compares **two of the person's own orderings** of the same domains and is the only one of the three reads that touches the stated layer. It is **not** the §6 gap: it uses raw card-sort fractions and raw self-anchored means, never sample standardization.

Over the set `C` of domains for which **both** an aspirational card-sort `frac_in_top5` (§5.1) and a valid revealed per-domain mean (§3.2) exist (**require `|C| ≥ 3`**):

```
stated_i(d)   = card_sort_stated(i, d, layer = "aspirational")     # [0,1], 6 levels
revealed_i(d) = revealed_score(i, d, primary_axis)                 # [-1,+1]
```

Compute Kendall **tau-b** (tie-correcting; required because `frac_in_top5` is tie-dense) between the two vectors. For every unordered domain pair count concordant `nc`, discordant `nd`, and pairs tied on stated `t_s` / revealed `t_r`:

```
tau_b = (nc - nd) / sqrt( (nc + nd + t_s) * (nc + nd + t_r) )
```

**Output is the 3-band ordinal `{low / moderate / high divergence}` derived from `tau_b`, the two raw orderings, `|C|`, `nc`, `nd`, `t_s`, `t_r`, and the named domain-pair(s) that flip — never a bare scalar.** A continuous `D = 1 − tau_b` on `[0,2]` is **not** reported: with `|C| = 3` it can take only ~4 values, so a real-interval framing asserts precision the statistic cannot carry.

**Stability guards (both required):**
- **`|C| ≥ 3`**, else emit "concordance undefined — needs ≥3 domains with both stated and revealed data" and show the raw orderings only. (With 2 domains there is one pair, so tau-b is mechanically ±1 — a coin-flip dressed as a measurement.)
- Flag any flipped pair whose **revealed** means differ by less than a within-person noise threshold (the larger of the two per-domain SEs, or `|delta_revealed| < 0.1` on the [−1,+1] axis) as **"fragile"** rather than a confident flip. tau-b's exact-tie correction does nothing for near-ties on 3-item means.

Any uncertainty estimate shown alongside concordance must be derived **within-person** (e.g. leave-one-pair-out over the person's own domains), **never** from `analyze.py`'s cohort-relative bootstrap CIs.

### 13.5 What §13 deliberately does not compute

- **No cross-channel scalar.** The §13.1 ordering and the §13.2/.3 price are **not** correlated into a single self-consistency number (e.g. a Kendall tau between the behavioral order and a cost-of-virtue order). Such a tau is a forced single-subject statistic with no reference distribution (n=4, or n=2 where it is mechanically ±1). At most, report **directional agreement on individual same-ladder probes** as a plain concordant/discordant count, captioned "this is N of 1; it cannot be tested and is not a correlation," and only where both reads are independently valid.
- **No per-domain cost-of-virtue aggregate across mixed probe types** (interpretation.md L70: forward and inverted are not comparable without §7 CFA cohort standardization).
- **No composite "values score," no rank rendered as 1/2/3/4, no sorted bar chart, no cross-person comparison of anything.**

---

## 14. Self-prediction calibration scores (H9)

Operationalizes the H9 secondary hypothesis (`pre-registration.md` §6; design rationale in `h9-self-calibration.md`; locked in `DECISIONS.md` §19). H9 measures how well a participant predicts their own revealed choices. Like §9 it introduces **no new scale**: predictions resolve on the same primary axis (§2.2) and the same cost-of-virtue ladder (§4) as the choices they forecast. All *cohort* statistics use participant-level non-parametric bootstrap, 10,000 resamples, seed `20260510` (identical to §8/§9).

### 14.1 The calibration primitive

Before a designated calibration probe resolves, the participant records a non-binding self-prediction (the "prediction beat"; `h9-self-calibration.md` §3 A1), logged as a `prediction` event `{user_id, session_id, probe_id, predicted_option_id | predicted_rung, timestamp_iso}`. **Two channels, never pooled** (different units; §14.7):

**Axis channel (primary).** For a choice-based calibration probe `p` (quick-fire or H8-paired item), the predicted option is scored on the primary axis with the *same* tag-to-axis map (§2.1) as the actual choice:

```
pred_i^p = clamp( sum(tag_contribution for tag in predicted_option.tags), -1, +1 )
rev_i^p  = item_score of the actual choice (§2.2)
e_i^p    = pred_i^p - rev_i^p              # signed, axis units
```

`e_i^p > 0` = predicted a more axis-positive (more honest / generous / trusting) choice than was made.

**Cost-of-virtue channel (separate, price units).** For a CoV probe the participant predicts their own break-rung on the identical ladder. Using the §13.2 price atom:

```
pred_price_i^p = log10(predicted_break_stake)     # forward;  -log10(...) for inverted (§4.2 direction)
rev_price_i^p  = log10(first_accept_stake)         # the realized §4 break-point, same flip
e_price_i^p    = pred_price_i^p - rev_price_i^p    # log10-dollar units
```

**Censoring discipline (inherited from §13.2/§13.3, load-bearing).** If *either* the predicted or the realized break-point is `"never"` (right-censored, `price > ladder top`), `e_price` is **suppressed — never made finite.** The pair is reported only categorically: `{predicted-never & acted-never}`, `{predicted-never & acted-finite}` ("expected to hold out, didn't"), `{predicted-finite & acted-never}` ("expected to break, held"). A finite `e_price` is admissible only when both endpoints are measured prices on an identical rung ladder and shared axis direction — the same gate as a §13.3 delta.

### 14.2 Person-level indices (reveal-eligible, N=1)

On the axis channel, over a participant's completed calibration probes:

```
cal_bias_i  = mean_p e_i^p        # signed self-enhancement bias
cal_error_i = mean_p |e_i^p|      # magnitude; lower = better self-knowledge
```

**N=1 interpretability.** Because `pred` and `rev` sit on the *same* pre-defined axis (and the CoV channel on the same external dollar ladder), no cross-scale or cross-person standardization is needed — contrast the §6 gap (`interpretation.md` "Single-user domains"). `cal_bias_i` and `cal_error_i` are therefore meaningful for a single user and **eligible for the personal reveal without cohort norms** (relevant to `runtime-architecture.md` §10 #1). This is the §13 "self-against-self, N-of-1" case extended to a genuinely new quantity (self-knowledge). The reveal renders them descriptively ("you tend to predict yourself as more generous than you act, by about X, across N probes") — never a score-out-of-N (`concept.md`).

The H9a/H9b/H9c statistics below are *cohort* research tests (like §9's H8 statistics), separate from this within-person reveal read.

### 14.3 H9a — self-enhancement bias

Restricted to the **axis channel** and to the three domains with a consensual desirable pole (truth-telling, resource-allocation, reciprocity-cooperation); the in-group axis (loyalty +, universalism −) is value-contested and entered **exploratory only** (`h9-self-calibration.md` §1.1, §6 Q5).

```
H9a statistic:  lower 95% bootstrap-CI bound of  mean_i cal_bias_i  ≥ 0.10   (axis units)
```

**No mathematical-coupling inflation** (contrast §9.2): `pred` and `rev` are independent measurements, so `mean(pred − rev)` carries no shared-term artifact. The real confound is **reactivity** (the prediction beat changing the choice), netted in §14.6.

### 14.4 H9b — calibration is a distinct, stable axis

Two parts, both required to claim a new axis rather than a relabeling of the gap:

- **Stability.** Split-window test–retest of `cal_error_i` (first-half vs second-half sessions): lower 95% CI ≥ **0.40**. Deliberately below H3's 0.60 — a second-order derived quantity is noisier than a first-order score.
- **Discriminant.** Regress `cal_error_i` on `[ gap_i , revealed_level_i ]`, where `gap_i = mean_d |gap(i,d)|` (§6, absolute, over included domains) and `revealed_level_i = mean_d revealed_score(i,d,axis)` (§3.2). The model R² has **upper** 95% CI **< 0.50** — at least half the calibration variance is unexplained by how large the gap is or how virtuous the person acts.

**Status (BUILT, cohort-level — both halves now complete).** H9b-**stability** and H9b-**discriminant** are both implemented. Stability rides the `--predictions` / `--predictions-window-b` split-window path; the discriminant is `compute_h9b_discriminant` on `analyze.py --h9b-log` (a single combined `{session, card_sort, predictions}` corpus for one shared cohort, so H9b stays isolated from the main §3/§6 pipeline while exercising the *real* `user_domain_means` → `card_sort_scores[aspirational_self]` → `compute_gaps` sub-pipeline to form the two predictors). Seed `20260510 + 28`; `H9B_MIN_PARTICIPANTS = 8`, `H9B_R2_CEILING = 0.50`. Gated in `check_analyzer_thresholds.py` (H9 sub-expectation `H9b_discriminant` + a two-sided `check_h9b_discriminant_lock()`) on `analysis/fixtures/sample-h9b-log.json`. **With both halves built, H9b = stability ∧ discriminant is complete** (a calibration axis that is reliable *and* not a relabeling of the gap + virtue level).

**`cal_error` is the |e| MAGNITUDE from the SEPARATE prediction channel — load-bearing.** `cal_error_i = mean_p |pred − rev|` over axis probes, read from the independent prediction beat (§14.3), NOT a signed echo of `stated − revealed`. Were the outcome instead the *signed* `cal_bias` under predictions that merely parrot the card-sort aspiration (`pred ≡ stated`, `rev ≡ revealed`), then `cal_bias = stated − revealed = (μ_s − μ_r) + σ_s·gap + (σ_s − σ_r)·z_rev` is an **exact affine** function of `[gap, revealed_level]` (within-domain z is affine) → R² ≡ 1 → the discriminant would **always FAIL** regardless of the truth. Scoring the |e| magnitude from the decoupled prediction channel lets a genuinely dissociable self-knowledge axis score R² ≈ 0 and clear the ceiling. `check_h9b_discriminant_lock()` proves both arms on synthetic corpora with known ground truth: `cal_error ⊥ [gap, revealed]` → SUPPORTED; `cal_error` made a linear function of `[gap, revealed]` → NOT supported; plus the R² ≡ 1 signed-`cal_bias` mechanical-trap identity that motivates the magnitude/separate-channel design. **Cohort-level statistic** (an R² across participants), **never a per-person reveal**: no on-device surface changes (Python-only, parity stays green), and `cal_error_i` / gap_i / revealed_level_i stay separate facets, never pooled (§13.5).

### 14.5 H9c — the stakes-blindness signature

**Confirmatory test (axis channel only, for unit consistency).** Compare self-prediction error magnitude on the high- vs low-stakes H8 pools (both resolve to axis scores per §9.1):

```
blind_i = mean_p |e_i^p|  over H8b high-stakes attachment-laden pairs
        - mean_p |e_i^p|  over H8a low-stakes pairs
H9c statistic:  lower 95% bootstrap-CI bound of  mean_i blind_i  > 0     (one-sided; directional)
```

A participant enters H9c with ≥ 1 valid axis-channel error in *each* pool.

**Convergent read (CoV channel, price units — reported, not pooled).** The cost-of-virtue break-point calibration `|e_price_i^p|` (§14.1, censoring-aware) is the high-stakes self-knowledge read in its own units; reported alongside H9c as convergent evidence but **not pooled** into `blind_i` (mixing axis and log-dollar units would manufacture a pseudo-quantity, §13.5). Directional CoV miscalibration — predicting a higher break-point than realized ("I thought I'd hold out longer") — is summarized descriptively over the uncensored CoV pairs.

> **Spec reconciliation — RESOLVED 2026-06-08.** Earlier `h9-self-calibration.md` §1.4 named cost-of-virtue *in* the high-stakes pool. Reconciled in favor of this section: the confirmatory `blind_i` uses the **axis-scale H8 pools only** (H8b high vs H8a low), with cost-of-virtue calibration as a **separate convergent read** in price units. Rationale: pooling axis units with log-dollar prices would require cross-channel standardization, which violates the §13.5 unit discipline and forfeits the N=1 property (§14.2). `h9-self-calibration.md` §1.4 has been updated to match; scoring.md remains canonical for the OSF filing.

### 14.6 Estimation, inclusion, and reactivity netting

- **Reactivity netting (load-bearing).** A counterbalanced subset of comparable probes carries **no** prediction beat (`h9-self-calibration.md` §3 A3). Let `Δreact` = mean revealed axis score on predicted items − mean on matched non-predicted items (between- or within-subject per the §6-Q2 locked allocation). If `Δreact`'s 95% CI excludes 0, the beat is altering behavior; H9a/H9c are then computed on **reactivity-adjusted** revealed scores (with the unadjusted values reported alongside), and a large `Δreact` is logged as an MVP-2 intervention signal (self-prediction increases consistency).
- **Per-participant inclusion.** Axis channel: a probe contributes only if both the prediction and the choice were recorded (neither timed-out/missing). H9a requires ≥ 3 valid consensual-domain probes; H9b requires `cal_error` computable in both windows (≥ 2 valid probes each); H9c requires ≥ 1 valid error in each H8 pool. CoV channel: only uncensored pairs (§14.1) yield a finite `e_price`.
- **Order effects.** Prediction-beat placement is counterbalanced; a beat-position main effect is reported and, if large, the analysis re-run within strata.
- **Status and power.** H9 is *secondary*: reported with effect sizes and CIs, never a gate-criterion (contrast §7/H1). At n=200 the thresholds are deliberately modest — powered to detect direction, not to bound it tightly.

### 14.7 What §14 deliberately does not compute

- **No cross-channel pooling.** The axis-channel indices and the CoV-channel price errors are never averaged or correlated into one "self-knowledge score" (different units; a forced single-subject correlation has no reference distribution — the §13.5 discipline).
- **No composite calibration score, no cross-person ranking of calibration in any user-facing surface.** The cohort H9a/b/c statistics live only in the research analysis; the reveal stays within-person and descriptive (§14.2).
- **No finite calibration error across a censored cost-of-virtue endpoint** (§14.1). "I'll never sell out" predicted, then a \$5M break observed, is a categorical mismatch, not a number.

---

## 15. H10 — cross-situational moral consistency (PROPOSED — pending DECISIONS §20 lock)

Design source: [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md). H10 asks whether the **variability** of a person's revealed scores across surface *contexts* is itself a stable individual-difference trait (Fleeson's density-distribution view; Mischel's if–then signatures; Doris situationism). It reuses the revealed axis scores already computed for §2–§3 — **no new elicitation** — and reads a `context:*` metadata tag off each item to bin it by setting. Contexts in the canonical corpus: `workplace`, `family`, `public`, `anonymous`.

**Status.** H10a + H10b + H10c + the per-construct `sd_i(c)` / `V_i` reveal quantities are BUILT — so **H10 = H10a ∧ H10b is now complete** (a reliable variability trait *and* one discriminable from the person's level / over-claim / self-insight, with a residual-variability de-confound). H10a/H10c on `analyze.py --context-log` (gated on `analysis/fixtures/sample-context-log.json`); H10b (the two-legged discriminant) on `analyze.py --h10b-log`, gated in `check_analyzer_thresholds.py` (H10 sub-expectation `H10b_discriminant` + a load-bearing `check_h10b_discriminant_lock()`) on `analysis/fixtures/sample-h10b-log.json`. All Python-only (H10b is a cohort-level R², no on-device reveal) so parity stays green. Only the **on-device `sd_i(c)` reveal** remains DEFERRED (§15.6).

### 15.1 Measurement primitive (§1.1 of the design doc)

For person `i`, construct (home domain) `c`, and context `k`, let `r_i(c, k)` be the mean revealed **primary-axis** item score (§2.1) over that person's items in that construct × context. Then:

    mbar_i(c) = mean_k r_i(c, k)                                        # construct context-mean
    sd_i(c)   = sqrt( (1 / (K_i(c) − 1)) · Σ_k ( r_i(c, k) − mbar_i(c) )² )   # cross-context SD (sample)
    V_i       = mean_c sd_i(c)                                          # person-level variability index

`sd_i(c)` is the within-person **cross-context** dispersion in one construct; `V_i` averages it over that person's qualifying constructs. Both are in axis units. `V_i` is a mean of facets reported **alongside** the per-construct `sd_i(c)` — it is **never** summed with any other branch's index into a composite (§13.5), and **never** pooled with the cost-of-virtue channel.

### 15.2 H10a — trait reliability (BUILT)

Split each participant's sessions into odd/even halves (1-indexed sorted order), recompute `V_i` on each, and correlate across participants:

    H10a supported  ⇔  lower 95% bootstrap CI of  corr( V_i^odd, V_i^even )  ≥ 0.40

(Fleeson & Gallagher 2009 report density-distribution parameters with split-half reliabilities in the .6–.9 band; 0.40 is a deliberately modest floor for n≈200.) Bootstrap: percentile method, pre-committed seed `20260510 + 13`. This is the reliability of the **variability trait itself** — orthogonal to the person's *level*; that de-confound is H10b.

### 15.3 H10b — discriminant validity (BUILT — two-legged)

`V_i` must not be a proxy for the person's mean level, their aspirational stated–revealed over-claim, or their self-prediction error, and the within-person variability must survive a range-restriction check. **Two legs, both required:**

    (1) MAIN — regress V_i on [ level_i = mean_c mbar_i(c),  gap_i (the §6 aspirational
        stated−revealed over-claim),  cal_error_i (the §14.2 self-prediction error magnitude) ]
        supported  ⇔  upper 95% CI of the model R²  < 0.50
    (2) DE-CONFOUND — regress each (user, construct) cell's sd_i(c) on |mbar_i(c)|
        supported  ⇔  upper 95% CI of THAT R²  < 0.50   (variability is not a mid-scale range artifact)

Supported iff **both** legs clear the ceiling. The main leg says consistency is not reducible to how high a person scores + how much they over-claim + how poorly they know themselves; the de-confound says the within-person variability is not merely a range artifact (a construct mean near 0 has more headroom to vary than one pinned at an axis extreme). The de-confound is **cell-level**, so it carries a pseudo-replication caveat (multiple cells per person) — documented, not gated; a descriptive check on the same 0.50 ceiling, never a per-person score.

**No algebraic trap.** `V_i` is measured on the context-**variance** channel (§15.1), never an affine echo of level/gap/cal_error (contrast H9b's signed `cal_bias = stated − revealed` identity or H11b's circle-mean identity), so the lock is honestly two-sided: `check_h10b_discriminant_lock()` exercises the main leg's supported **and** reducible directions, the de-confound's both directions, and confirms **both legs are load-bearing** (a cohort where the main leg passes but the de-confound fails → not supported, and vice-versa) on real-pipeline corpora. Bootstrap seeds `20260510 + 31` (main) / `+ 32` (de-confound). Cohort-level statistic — `V_i`, `level_i`, `gap_i`, `cal_error_i` and each `sd`/`|mbar|` cell stay separate facets, never pooled (§13.5).

### 15.4 H10c — observer-effect anchor (BUILT, directional)

A directional sanity anchor: revealed scores should shift between observed and anonymous settings (an expected sensitivity, not a failure of the trait). Per person, pooling axis items across constructs:

    obs_gap_i = mean( r_i over observed/public items ) − mean( r_i over anonymous items )
    H10c supported  ⇔  lower 95% CI of  mean_i obs_gap_i  > 0   (one-sided)

Seed `20260510 + 14`. Axis scores only — no cross-channel pooling.

### 15.5 Suppression, N=1 reveal, value-neutrality (§1.5–§1.6 of the design doc)

- **Suppression floors.** A context contributes `r_i(c, k)` only with **≥2 informative items**; a construct yields `sd_i(c)` only with **≥3 qualifying contexts**; `V_i` is formed only with **≥3 qualifying constructs** — else it is suppressed and the reveal reports the per-construct `sd_i(c)` alone. (Locked directly against the code by `check_h10_suppression()` — the H10 analog of the §14.1 censoring lock.)
- **N=1 interpretability.** `sd_i(c)` is a within-person quantity on the fixed primary axis, so it is reveal-eligible for a single user with **no cohort standardization** (contrast the cohort-only H10a/b statistics).
- **Value-neutrality (Dancy caveat).** Low variability is named **"steadiness"**, high variability **"responsiveness"** — descriptive poles, **never ranked**. Particularism holds that sensitivity-to-context can be a virtue, not a defect; the reveal must not imply that consistency is better than responsiveness.

### 15.6 What §15 deliberately does not compute

- **No composite / no cross-branch pooling.** `V_i` is a within-branch mean of `sd_i(c)` facets; it is never summed with a gap, a calibration index, or a CoV price into one "consistency score" (§13.5).
- **No ranking in any user-facing surface.** The cohort H10a/b/c statistics live only in the research analysis; the reveal stays within-person and descriptive (steadiness↔responsiveness).
- **No on-device projection yet.** The `sd_i(c)` reveal is NOT in `poc-projection.js` this increment (Python-only, parity stays green); when added it changes **both** scorers under the §13.5/parity locks.

---

## 16. H11 — moral-circle radius (PROPOSED — pending DECISIONS §21 lock)

Design source: [`h11-moral-circle-radius.md`](h11-moral-circle-radius.md). H11 asks how far a person's **concern reaches across recipient social/moral distance** — Singer's *expanding circle* made behavioral and within-person (Crimston et al. 2016 Moral Expansiveness Scale; Waytz et al. 2019 on the *shape* of the ideological circle; Cikara & Bruneau on parochial empathy). It reuses the **`circle_radius` secondary axis** already scored for the in-group domain (§2.3, hospitality **+1** / boundaries **−1**) — **no new elicitation** — and bins each item by its `counterparty:*` metadata tag through a **versioned distance-ordering map** (`analysis/counterparty_distance_map_v0.1.csv`, §16.5).

**Status.** H11a + H11b + H11c + the per-person `β_i` / `R_i` reveal quantities are BUILT — so **H11 = H11a ∧ H11b is now complete** (reliable shape *and* discriminable from generosity). H11a/H11c on `analyze.py --circle-log --distance-map`; H11b (the shape discriminant) on `analyze.py --h11b-log`, gated in `check_analyzer_thresholds.py` (H11 sub-expectation `H11b` + a two-sided `check_h11b_discriminant_lock()`) on `analysis/fixtures/sample-h11b-log.json`. All Python-only (H11b is a cohort-level R², no on-device reveal) so parity stays green. Only the **on-device `β_i`/`R_i` reveal** remains DEFERRED (§16.6). The scorer reads `circle_radius` **separately** from the primary `item_score`, so the parity secondary-axis-exclusion lock (hospitality **out** of the revealed score) is untouched.

### 16.1 Measurement primitive (§1.1 of the design doc)

For person `i` and distance bin `d`, let `concern_i(d)` be the mean **`circle_radius`-axis** item score (§16.5 scorer) over that person's in-group items whose `counterparty:*` tag falls in bin `d` (a bin enters only with **≥2 informative items**). Two within-person shape summaries:

    β_i        = OLS slope of concern_i(d) on the bin index d          # parochialism steepness (negative = concern declines with distance)
    midpoint_i = ½ · ( concern_i(nearest populated bin) + AXIS_FLOOR ) # AXIS_FLOOR = −1.0 (boundaries pole)
    R_i        = the first bin d (ascending) with concern_i(d) ≤ midpoint_i   # the reach of concern

`β_i` is the **robust** read — always finite. `R_i` is the **distance-axis analog of the cost-of-virtue break point**: it is **RIGHT-CENSORED** (`radius = None`, `censored = True`) when concern never crosses the midpoint (a wide/flat, impartial circle), and — inheriting §13.2 verbatim — a censored `R_i` is **NEVER made finite**. Both are on the fixed secondary axis + ordering; reported as facets, **never** summed into a composite (§13.5) and **never** pooled with the primary or cost-of-virtue channels.

### 16.2 H11a — shape reliability (BUILT)

Split each participant's sessions into odd/even halves (1-indexed sorted order), recompute `β_i` on each, and correlate across participants:

    H11a supported  ⇔  lower 95% bootstrap CI of  corr( β_i^odd, β_i^even )  ≥ 0.40

`β_i` (not `R_i`) carries the reliability precisely because it is always finite, whereas `R_i` right-censors whenever a participant's circle is flat (§6 Q3 of the design doc: the slope is the robust shape read when many participants are impartial). Bootstrap: percentile method, pre-committed seed `20260510 + 15`. This is the reliability of the **shape itself** — the de-confound from generosity level is H11b.

### 16.3 H11b — discriminant validity (BUILT, cohort-level)

The circle **shape** must not be a proxy for how generous the person is — "reach is not height" (a person can be lavish to kin then drop off a cliff — narrow — or modest but flat — wide; Crimston et al. 2016, the moral-expansiveness shape is dissociable from generosity level). Regress the shape slope on the near-bin concern **and a separate revealed generosity level**:

    regress β_i on [ near-bin concern_i,  resource-allocation generosity_i ]
    H11b (discriminant) supported  ⇔  upper 95% bootstrap CI of model R²  < 0.50

i.e. **at least half the circle-shape variance is NOT explained by how generous a person is**. Seed `20260510 + 27`; `compute_h11b_discriminant`, `--h11b-log`, `H11B_MIN_PARTICIPANTS = 8`. **H11 = H11a ∧ H11b** (reliable shape *and* dissociable from generosity) is now complete.

**Generosity is an EXTERNAL revealed measure, not the circle mean — load-bearing.** `generosity_i` is the §3.1 revealed-mean pipeline restricted to the **resource-allocation** domain (its `generosity` primary axis; `_resource_allocation_generosity`), scored by the SAME `item_score` + §10 inattentive drop + ≥3-items/session floor as every channel. Were generosity instead the *circle mean*, `β_i` (an OLS slope over the same bins) would be a **mechanical** function of the predictors: with concern linear in bin, `circle_mean = near + 2.5·β` (bins 0–5), so `β = (mean − near)/2.5` is an **exact** linear combo of `[near, mean]` and R² ≡ 1 — the discriminant would **always FAIL** regardless of the truth. Using a *separate* revealed axis decorrelates β from the predictors, so a genuinely dissociable shape scores R² ≈ 0 and clears the ceiling. `check_h11b_discriminant_lock()` proves both arms on synthetic corpora with known ground truth: β ⊥ [near, generosity] → SUPPORTED; β made a deterministic function of external generosity → NOT supported; and the R² ≡ 1 mechanical-trap identity that motivates the external-measure choice. **Cohort-level statistic** (an R² across participants), **never a per-person reveal**: no pooled circle score is emitted, and `β_i` / generosity_i stay separate facets (§13.5).

### 16.4 H11c — parochial-gradient anchor (BUILT, directional)

A directional sanity anchor validating that the researcher-imposed distance ordering is **behaviorally real** (Cikara & Bruneau): concern should, on average, decline from the nearest to the furthest bin. Per participant with a formed shape (≥4 populated bins):

    gradient_i = concern_i(nearest populated bin) − concern_i(furthest populated bin)
    H11c supported  ⇔  lower 95% CI of  mean_i gradient_i  > 0   (one-sided)

Seed `20260510 + 16`. `circle_radius` scores only — no cross-channel pooling. A wide/flat circle contributes `gradient_i ≈ 0` (it neither confirms nor breaks the ordering); the anchor is carried by the parochial majority.

### 16.5 Distance-ordering map, suppression, N=1, value-neutrality (§1.5 of the design doc)

- **The distance-ordering map (§3 A1).** `analysis/counterparty_distance_map_v0.1.csv` maps a bare `counterparty` tag → an ordered integer bin (0 = nearest). It is a **researcher-imposed ordering** (a CV-2 "smuggled values" risk, §1.5) and a **v0.1 DRAFT** whose **REL-2 inter-rater validation is human-gated** (see build-and-validate.md "Needs Dave / external"). The **§6 Q4 distance/power confound** is handled *in the map*: the power/role counterparties (`senior`, `subordinate`, `business`) and the within-item distance-*contrast* markers (`near-vs-far`, `local-vs-global`, `family-vs-stranger`, `close-distant`, `close-vs-peer`) are given a non-integer bin so the loader **excludes** them from the ladder while keeping them documented in the file.
- **Suppression floors.** A bin contributes `concern_i(d)` only with **≥2 informative items**; a participant yields `β_i` / `R_i` only with **≥4 populated ordered bins** — else suppressed, no shape reported. (Locked directly against the code by `check_h11_suppression()` — with the §13.2 censoring lock, the H11 analog of the §14.1 CoV-ceiling lock.)
- **N=1 interpretability.** `β_i` / `R_i` are within-person quantities on the fixed secondary axis + ordering, so they are reveal-eligible for a single user with **no cohort standardization** (contrast the cohort-only H11a/b statistics).
- **Value-neutrality (load-bearing).** A **wider circle is not scored as better** — Singer's impartialism is one defensible pole, Williams/MacIntyre/Confucian **partialism** (special obligations to the near) the other. The reveal **names the shape** (how far concern reaches, how steeply it falls) and **never ranks** it. This carries the same charge as R6's value-neutrality.

### 16.6 What §16 deliberately does not compute

- **No composite / no cross-branch pooling.** `β_i` and `R_i` are within-branch facets on the secondary axis; neither is summed with a gap, calibration index, variability index, or CoV price into one "circle score" (§13.5), nor pooled with the primary revealed score.
- **No ranking in any user-facing surface.** The cohort H11a/b/c statistics live only in the research analysis; the reveal stays within-person and descriptive (reach + steepness, impartial↔partial, never ranked).
- **No on-device projection yet.** The `β_i` / `R_i` reveal is NOT in `poc-projection.js` this increment (Python-only, parity stays green); when added it changes **both** scorers under the §13.5/parity locks.
- **No far-beings (non-human) bin in the MVP.** The map reserves bin 6 (`animal-dependent`) but the fixture exercises bins 0–5; the MVP-2 far-beings extension (design-doc §3 A3) is deferred.

---

## 17. R2 — sacred / protected values (PROPOSED — pending DECISIONS §22 lock)

Design source: [`r2-sacred-protected-values.md`](r2-sacred-protected-values.md). R2 asks which values a person **refuses to price at any stake** — protected/sacred values (Baron & Spranca 1997; Tetlock 2000 *taboo trade-offs*; Fiske & Tetlock 1997 *incommensurability*), where the resistance to trade-off is quantity-insensitive (Bartels & Medin 2007) and load-bearing in conflict (Ginges et al. 2007). It is a **pure re-read** of the cost-of-virtue channel (§4, §13.2): the **right-censored `never` tail** — the values a person won't sell at any rung in range — **is** their protected set. **No new break-point math**; the censoring discipline was already storing this construct.

**Status.** R2a + R2b + the per-person `P_i` reveal quantity are BUILT (`analyze.py --protected-log`, gated in `check_analyzer_thresholds.py` on `analysis/fixtures/sample-protected-values-log.json`, Python-only so parity stays green). R2c and the on-device protected-set reveal are DEFERRED (§17.4, §17.6). The `taboo` marker (§17.5) is a **new light data-contract field** scored here on synthetic fixtures; real collection + its exact phrasing are runtime/design-gated (surfaced to Dave). This re-reads the CoV break-point **primitive** (already parity-locked; the runtime emits per-slot `no_break_point` at `poc-projection.js:212`) **without changing it**.

### 17.1 Measurement primitive (§1.1 of the design doc)

For person `i`, the **professed protected set** is the set of value slots they mark `never` on the cost-of-virtue ladder:

    P_i = { v : response(i, v) is a censored `never` }     # categorical set membership, keyed by value_slot

A `never` is read **categorically** — it inherits §13.2 verbatim: right-censored (price above the ladder top), **NEVER finitized into a number**. `P_i` holds value-slot **strings**, never prices; it is a **set + a marker**, never summed into a "sacredness score" (§13.5 — §4 rejected exactly that scalar). A light companion marker rides each CoV probe:

    taboo_i(v) ∈ {0, 1}   # "was even being ASKED to price this wrong?" — a one-tap after the probe (§3 A1)

### 17.2 R2a — set reliability (BUILT)

Protected-value *set* membership must be stable across occasions. For each participant present in ≥2 waves, take the set-agreement (Jaccard) of their protected sets across the first and last wave:

    jaccard_i = | P_i^{w1} ∩ P_i^{w2} | / | P_i^{w1} ∪ P_i^{w2} |
    R2a supported  ⇔  lower 95% bootstrap CI of  mean_i jaccard_i  ≥ 0.40

Bootstrap: percentile method, pre-committed seed `20260510 + 17`. A participant whose protected union is **empty in both waves** (protects nothing either time) has an **undefined** Jaccard and is **EXCLUDED** — reported as `n_excluded_empty`, **never scored as perfect agreement** (which would spuriously inflate reliability from the majority who protect nothing).

### 17.3 R2b — protected ≠ EXPENSIVE (BUILT, directional — load-bearing)

The distinctness that makes protected values a real construct rather than a relabeling of "very expensive": among never-responders, being *asked* to price a genuinely protected value draws outrage (taboo) that pricing a merely high-but-finite value does not. Per participant with both a protected and a finite response carrying markers:

    contrast_i = mean( taboo_i(v) | v is a `never` )  −  mean( taboo_i(v) | v has a finite price )
    R2b supported  ⇔  lower 95% CI of  mean_i contrast_i  > 0   (one-sided)

Seed `20260510 + 18`. Without R2b a `never` is just "off the top of the ladder"; the taboo contrast is what separates a **sacred** value from a **very expensive** one. (The complementary *quantity-insensitivity* leg — a flat refusal that doesn't soften as the offer climbs — needs per-rung acceptance trajectories the single-break-point contract doesn't carry; bounded/deferred per §17.5 and design-doc §6 Q3. The taboo contrast is the primary distinctness test.)

### 17.4 R2c — discriminant validity (DEFERRED — cohort-coupled)

Protectedness must not be a proxy for how *important* a value is on the stated inventory (a merely top-ranked value):

    regress P_i-membership on [ inventory rank_v,  log-price_v ]
    R2c (discriminant) supported  ⇔  upper 95% CI of  R²  < 0.50

**DEFERRED** because it couples to the cohort inventory-rank + log-price pipeline, exactly as the H9b/H10b/H11b discriminant halves do — the current increment stays isolated on its own fixture.

### 17.5 Taboo marker, cheap-talk, N=1, value-neutrality (§1.5 of the design doc)

- **The `taboo` marker (§3 A1).** A new light data-contract field (0/1), a one-tap after a CoV probe. Scored here on synthetic fixtures; **real collection and its exact phrasing (Q1 — avoid a leading "was this offensive?") are runtime/design-gated** and surfaced to Dave (see build-and-validate.md "Needs Dave / external").
- **Cheap-talk caveat (load-bearing).** A hypothetical `never` is **costless** — anyone can *say* a value is sacred. `P_i` is therefore labelled **PROFESSED** protected values; the reveal never claims they'd survive a real offer. Real-stakes validation (which `never`s hold when the price is actual) rides **H-A2 → Phase-2** (IRB-gated; surfaced to Dave).
- **N=1 interpretability.** `P_i` is a within-person set on the fixed value slots — reveal-eligible for a single user with no cohort standardization ("honesty and loyalty are non-negotiable *for you*; generosity has a price"), contrast the cohort-only R2a/R2b statistics.
- **Value-neutrality (load-bearing).** A **large protected set is not scored as better** — many `never`s can be **integrity** OR rigid **dogmatism** (a value-monist who won't trade off anything is not more moral, just less flexible). The reveal **names the set** and **never ranks** it by size.

### 17.6 What §17 deliberately does not compute

- **No sacredness score / no pooling.** `P_i` is a set and `taboo` a marker; neither is summed with a gap, calibration index, variability index, circle radius, or CoV price into one scalar (§13.5), nor pooled across branches.
- **No finitized `never`.** The protected read **never** assigns a price to a `never` — it stays the right-censored categorical tail (§13.2), asserted directly against the code by `check_r2_censoring()` (the R2 analog of the §14.1 CoV-ceiling / |8.0| lock).
- **No real-stakes claim.** `P_i` is professed; the reveal carries the cheap-talk caveat and never asserts a value would survive a real offer (that is H-A2, Phase-2).
- **No on-device projection yet.** The `P_i` reveal is NOT in `poc-projection.js` this increment (Python-only, parity stays green); when added it changes **both** scorers under the §13.5/parity locks.

---

## 18. H12 — moral hypocrisy / self–other judgment asymmetry (PROPOSED — pending DECISIONS §23 lock)

H12 asks whether a person judges the **same act** more harshly when **another** commits it than when **they** do — the self–other asymmetry at the heart of moral hypocrisy. Grounding: Tappin & McKay 2017 (*The Illusion of Moral Superiority*); Epley & Dunning 2000 (*Feeling "holier than thou"*); the actor–observer asymmetry (Jones & Nisbett 1971; Malle 2006 meta-analysis); with Batson's *moral hypocrisy* (Batson et al. 1997, 1999) as the construct origin. It is a **paired within-person contrast on a common severity scale**: for each matched act, the person rates how wrong it is when *they* do it (`severity_self`) and when *another* does it (`severity_other`), both on the same 0–10 scale. **Deliberately avoided:** Valdesolo & DeSteno's manipulation-based induction (an experimenter-staged asymmetry, not a within-person read) and every excluded paradigm — no Stapel, Gino, Ariely-priming, or ego-depletion (see build-and-validate.md exclusions).

**Status.** H12a + H12c + H12b (discriminant, §18.5) + the per-person `H_i` reveal quantity are BUILT (`analyze.py --hypocrisy-log` / `--h12b-log`, gated in `check_analyzer_thresholds.py` on `analysis/fixtures/sample-hypocrisy-log.json` + `sample-h12b-log.json`, Python-only so parity stays green). H12 = reliability ∧ anchor ∧ discriminant is now complete; only the on-device `H_i` reveal remains DEFERRED (§18.6). The self–other judgment log is a **new light data-contract** (a matched pair of severity ratings per probe); real collection + its exact phrasing (avoid a leading "aren't others worse?") are runtime/design-gated and surfaced to Dave.

### 18.1 Measurement primitive

For person `i`, over their matched self–other judgment pairs, the **self–other asymmetry** is the mean signed gap:

    delta_i(act) = severity_other(i, act) − severity_self(i, act)     # signed, on a common 0–10 scale
    H_i = mean_act delta_i(act)          over acts with BOTH ratings present, ≥ 3 scorable pairs (§1.5 N=1)

`H_i > 0` = harsher on others than on self (the self-serving / moral-superiority direction); `H_i < 0` = harsher on self (self-critical). `H_i` is a **signed facet**, never summed with a gap, calibration index, variability index, circle radius, protected set, or CoV price into one scalar (§13.5), nor pooled across branches.

**Pairing / missing-data lock (the H12 analog of the §13.2 censoring lock).** A **declined judgment** — either side missing or non-numeric — makes `delta_i(act)` **undefined**, so the pair is **DROPPED**, never imputed to 0 (which would fabricate "no asymmetry"). The delta is the **signed** difference: harsher-on-self stays **NEGATIVE**, never clamped toward the self-serving direction. Asserted directly against the code by `check_h12_pairing_lock()`.

### 18.2 H12a — asymmetry reliability (BUILT)

The self–other asymmetry must be a stable trait, not occasion noise. Split each person's sessions odd/even, compute `H_i` on each half, and correlate across participants present in both halves:

    r = pearson_i( H_i^{odd}, H_i^{even} )    over shared participants (≥ 3)
    H12a supported  ⇔  lower 95% bootstrap CI of  r  ≥ 0.40

Bootstrap: percentile method over paired `(H_i^{odd}, H_i^{even})`, pre-committed seed `20260510 + 19`. This mirrors the H10a / H11a split-half reliability construction exactly (`_odd_even_sessions` + `_pearson_r` + `_bootstrap_ci_r`), not R2a's wave-Jaccard.

### 18.3 H12c — self-serving directional anchor (BUILT, directional — cohort validity check)

The construct's defining prediction is directional: on average the cohort tilts self-serving (harsher on others than on self), the "holier than thou" / illusion-of-moral-superiority signature:

    H12c supported  ⇔  lower 95% CI of  mean_i H_i  > 0   (one-sided)

Seed `20260510 + 20`. This is a **cohort validity anchor** (does the instrument recover the established direction?), **NOT a per-person verdict** — an individual with `H_i < 0` is harsher on themselves, described as such and never scored as more or less moral (§18.4).

### 18.4 Pairing lock, N=1, value-neutrality

- **Pairing lock (load-bearing).** Per §18.1: a declined judgment drops the pair (never imputed to 0); the sign is preserved. `check_h12_pairing_lock()` asserts this against the code so a regression that starts imputing declines, or clamps harsher-on-self toward 0, is caught even if the fixture changes.
- **N=1 interpretability.** `H_i` is a within-person mean over that person's ≥ 3 matched pairs — reveal-eligible for a single user with no cohort standardization ("you judge these acts about 1 point more harshly in others than in yourself"), contrast the cohort-only H12a / H12c statistics.
- **Value-neutrality (load-bearing).** Neither direction is scored as better. Harsher-on-others is **not** ranked above harsher-on-self, nor vice versa: a self-critical person (`H_i < 0`) is not "more honest," and a self-serving one is not "more confident" — both are **described, never ranked**. The reveal states the magnitude and direction of the asymmetry and stops there. (This is why H12c is walled off as a *cohort* anchor, not a per-person target.)
- **Cheap-talk / hypothetical caveat.** These are *judgments of hypothetical acts*, not behavior under stakes. `H_i` measures a **stated** judgment asymmetry; the reveal never claims the person would *act* on it. Behavioral validation (does a large `H_i` predict real self–other double standards?) is Phase-2 / IRB-gated and surfaced to Dave.

### 18.5 H12b — discriminant validity (BUILT 2026-07-01)

The self–other asymmetry must not be a proxy for a person's stated–revealed **gap** or their **calibration error** (a general "knows-self-poorly" factor):

    regress H_i on [ gap_i,  cal_error_i ]
    H12b (discriminant) supported  ⇔  upper 95% CI of  R²  < 0.50

**BUILT** — `compute_h12b_discriminant` on `analyze.py --h12b-log`, a combined `{session, card_sort, predictions, hypocrisy}` cohort fixture that runs the *real* §3/§6 gap sub-pipeline (`user_domain_means → card_sort_scores[aspirational_self] → compute_gaps`) and the §14.2 `cal_error_i` sub-pipeline internally to form the two predictors, so H12b stays isolated from the main H2–H7 cohort (the same isolation the H9b/H11b discriminants use). Reuses the `_ols_r_squared` / `_bootstrap_ci_r2` machinery; seed `20260510 + 29`, `H12B_MIN_PARTICIPANTS = 8`, `H12B_R2_CEILING = 0.50`. Gated by a two-sided `check_h12b_discriminant_lock()` on `analysis/fixtures/sample-h12b-log.json` (INDEPENDENT `H_i ⊥ [gap, cal_error]` → SUPPORTED; REDUCIBLE `H_i = f([gap, cal_error]) + noise` → NOT). **Unlike H9b/H11b there is deliberately NO manufactured mechanical-trap identity:** `H_i` rides an INDEPENDENT paired-severity channel (§18.1), not an affine echo of the predictors the way H9b's signed `cal_bias = stated − revealed` or H11b's circle-mean were — so the lock proves the *absence* of a forced identity by flipping the verdict True→False on IDENTICAL predictors via the severity channel alone (had an identity existed, even the ⊥ draw would pin R² ≡ 1; here it is ~0). Cohort-level R², **no on-device reveal → Python-only, parity stays 9/9. H12 = reliability ∧ anchor ∧ discriminant now complete.** The descriptive companions `h_gap_r` / `h_cal_error_r` (H_i's bare correlation with each predictor) localize any leakage without pooling per person.

### 18.6 What §18 deliberately does not compute

- **No hypocrisy score / no pooling.** `H_i` is a single signed asymmetry; it is not summed with a gap, calibration index, variability index, circle radius, protected set, or CoV price into one scalar (§13.5), nor pooled across branches.
- **No imputed declines.** A declined judgment is **dropped**, never scored 0 — asserted directly against the code by `check_h12_pairing_lock()` (the H12 analog of the §14.1 CoV-ceiling / |8.0| lock and `check_r2_censoring`).
- **No per-person moral ranking.** Neither harsher-on-others nor harsher-on-self is scored as better; H12c is a cohort validity anchor, not an individual verdict (§18.4).
- **No behavioral claim.** `H_i` is a stated judgment asymmetry; the reveal carries the hypothetical caveat and never asserts the person would act on the double standard (that is Phase-2).
- **No on-device projection yet.** The `H_i` reveal is NOT in `poc-projection.js` this increment (Python-only, parity stays green); when added it changes **both** scorers under the §13.5/parity locks.

---

## 19. R1 — moral identity centrality (PROPOSED — pending DECISIONS §24 lock)

R1 asks how **central a moral identity is to who a person is** — the *self-importance of moral identity*. Grounding: Aquino & Reed 2002 (*The Self-Importance of Moral Identity*), the canonical, well-replicated instrument. Its defining structure is **two disjoint facets**: **internalization** (private — how core moral traits like caring, fair, honest are to one's self-concept) and **symbolization** (public — the outward display of a moral identity through action and appearance). The two are **kept strictly separate and NEVER pooled** into one "moral-identity score" (§13.5 — the load-bearing discipline for this branch), because they dissociate: a person can internalize deeply while symbolizing little, and vice versa. Each facet is a **within-person mean of its own Likert items** (1–7). **Deliberately avoided:** any excluded paradigm — Aquino & Reed is not a fraud/non-replication case (see build-and-validate.md exclusions); no priming (contrast the excluded Macbeth/cleansing work).

**Status.** R1a + R1c + the two per-person facet means (`mean_internalization`, `mean_symbolization`) are BUILT (`analyze.py --identity-log`, gated in `check_analyzer_thresholds.py` on `analysis/fixtures/sample-identity-centrality-log.json`, Python-only so parity stays green). **R1b — the meta-moderation gap leg** (R1 moderating the §6 stated–revealed gap) is now BUILT too (`analyze.py --r1b-log`, gated on `sample-r1b-log.json` + `check_r1b_moderation_lock`, Python-only): R1 = **reliability (R1a) ∧ directional anchor (R1c) ∧ gap-moderation (R1b)**. The H10–H12 dampening legs of R1b, and the on-device facet reveal, remain DEFERRED (§19.5, §19.6). The moral-identity-centrality log is a **new light data-contract** (one Likert response per item, each carrying its `facet`); real collection + exact item phrasing (the Aquino & Reed stem "It would make me feel good to be a person who has these characteristics…") are runtime/design-gated and surfaced to Dave.

### 19.1 Measurement primitive

For person `i`, over their centrality items partitioned by facet, each facet is scored as its **own** within-person mean — the two facets are DISJOINT item sets, never combined:

    internalization_i = mean over i's internalization items    (≥ 3 scorable items, §1.5 N=1)
    symbolization_i   = mean over i's symbolization items      (≥ 3 scorable items, §1.5 N=1)
    # NO pooled (internalization_i + symbolization_i)/2 is ever formed (§13.5)

Both are **separate facets**, each never summed with the other — nor with a gap, calibration index, variability index, circle radius, protected set, CoV price, or self–other asymmetry into one scalar (§13.5), nor pooled across branches. The JSON `R1` block deliberately exposes `mean_internalization` and `mean_symbolization` as **separate keys with no pooled "centrality" key**.

**Facet-separation / missing-data lock (the R1 analog of the §13.2 censoring lock).** A **declined item** — response missing, non-numeric, or boolean — makes `_centrality_response` return `None`, so the item is **DROPPED** from its facet, never imputed to 0 (which would deflate the facet mean). A facet with **fewer than 3 scorable items** is **SUPPRESSED** (absent), never scored on thin data. And the two facets route to **disjoint** means — internalization never absorbs a symbolization response and vice versa. Asserted directly against the code by `check_r1_no_pool()`.

### 19.2 R1a — internalization-facet reliability (BUILT)

Moral-identity centrality must be a stable trait, not occasion noise. Split each person's sessions odd/even, compute the **internalization** facet mean on each half, and correlate across participants present in both halves:

    r = pearson_i( internalization_i^{odd}, internalization_i^{even} )    over shared participants (≥ 3)
    R1a supported  ⇔  lower 95% bootstrap CI of  r  ≥ 0.40

Bootstrap: percentile method over paired `(internalization_i^{odd}, internalization_i^{even})`, pre-committed seed `20260510 + 21`. This mirrors the H10a / H11a / H12a split-half reliability construction exactly (`_odd_even_sessions` + `_pearson_r` + `_bootstrap_ci_r`). Reliability is anchored on the **internalization** facet — the private, self-definitional dimension Aquino & Reed find the more trait-stable of the two; symbolization reliability is a natural R1-extension deferred with R1b.

### 19.3 R1c — internalization > symbolization directional anchor (BUILT, directional — cohort validity check)

The construct's defining prediction is directional: on average people endorse the **private** dimension of a moral identity **more** than its **public display** — the internalization-exceeds-symbolization signature Aquino & Reed 2002 report across samples:

    delta_i = internalization_i − symbolization_i     # within-scale (same 1–7 Likert), per person with BOTH facets
    R1c supported  ⇔  lower 95% CI of  mean_i delta_i  > 0   (one-sided)

Seed `20260510 + 22`. `delta_i` is a **within-scale within-subject contrast** (both facets on the identical 1–7 Likert), legitimate exactly as H12's `severity_other − severity_self` and H10c's `public − anonymous` — **NOT** cross-scale pooling. This is a **cohort validity anchor** (does the instrument recover the established direction?), **NOT a per-person verdict** — an individual with `delta_i < 0` symbolizes more than they internalize, described as such and never scored as more or less moral (§19.4).

### 19.4 Facet-separation lock, N=1, value-neutrality

- **Facet-separation lock (load-bearing).** Per §19.1: the two facets are disjoint item sets scored separately, never pooled into (I+S)/2; a declined item drops (never imputed 0); a below-floor facet is suppressed. `check_r1_no_pool()` asserts this against the code so a regression that starts pooling, imputing declines, or scoring a one-item facet is caught even if the fixture changes.
- **N=1 interpretability.** `internalization_i` and `symbolization_i` are within-person means over that person's ≥ 3 items each — reveal-eligible for a single user with no cohort standardization ("moral traits are highly core to how you see yourself; you place less weight on outwardly displaying them"), contrast the cohort-only R1a / R1c statistics. This reveal now **ships on-device** (§19.7): `centralityFacets()` in `poc-projection.js` computes the two facet means per person, JS↔Python parity-locked against `centrality_facet_by_user`.
- **Value-neutrality (load-bearing).** High centrality is **not** scored as better than low, and internalizing is **not** ranked above symbolizing. A strongly-internalized moral identity is integrity **or** rigid self-righteousness (the documented *dark side* of moral identity — moral licensing, out-group derogation); the reveal describes where a person sits on each facet and stops there. Neither facet is a virtue score, and the two are never collapsed to imply one number "how moral you are."
- **Cheap-talk / self-report caveat.** These are *self-reported* endorsements of how central moral traits are, not behavior under stakes. The facet means measure **stated** identity centrality; the reveal never claims the person would *act* on it. Behavioral validation (does high internalization predict a smaller stated–revealed gap?) is the **R1b moderation leg — now BUILT** as the gap leg (§19.5): the cohort-level regression of the §6 over-claim gap on internalization, supported iff the upper 95% CI of their correlation < 0.

### 19.5 R1b — meta-moderation, the gap leg (BUILT, directional — cohort validity check)

R1's headline role is as a **meta-moderator**: internalization should predict a **smaller** §6 stated–revealed gap and dampen the H10–H12 asymmetries (a more internalized moral identity → less over-claiming, less context-drift). The **gap leg** is now built (`analyze.py --r1b-log`, gated on `analysis/fixtures/sample-r1b-log.json`, Python-only so parity stays green):

    internalization_i = centrality_facet_by_user(identity, "internalization")   (§19.1)
    gap_i             = _h9b_person_predictors(session, card_sort)[i]["gap"]     (§6, signed over-claim)
    r                 = corr(internalization_i, gap_i)    (= the STANDARDIZED moderation slope, bivariate)
    R1b supported     ⇔  UPPER 95% bootstrap CI of r  <  0   (one-sided; seed 20260510 + 34)

Supported ⇔ a more internalized moral identity predicts a **significantly** smaller (more negative) over-claim — the Aquino & Reed 2002 identity→behavior-congruence prediction. **Directional** (a signed-slope test, not an R²-ceiling discriminant). The two channels are **INDEPENDENT** — internalization rides the identity log; the gap rides session + card_sort through the SAME parity-locked §3/§6 primitives H9b/H12b use — so there is no algebraic identity, and `check_r1b_moderation_lock()` holds ONE internalization profile FIXED and flips the verdict purely through the gap channel: NEGATIVE (gap = −z(internalization) + noise → supported), NULL (gap ⊥ internalization → not), POSITIVE (gap = +z(internalization) + noise → not — the WRONG direction is one-sided rejected). It is a **COHORT-level** construct-validity read, never a per-person verdict: a very negative gap is **modesty** (revealing more virtue than one states), not scored as "better," and neither internalization pole is ranked (§19.4).

**DEFERRED — the H10–H12 dampening legs.** Whether internalization *also* blunts the framing (H10) / anchor (H11) / decoy (H12) asymmetries is a natural R1b extension held for later: each adds two more cohort channels for descriptive-only companions, and each couples to its own §15/§16/§18 pipeline exactly as the H10b / H11b discriminant halves do. The current leg stays scoped to the §6 gap on its own {session, card_sort, identity} fixture.

### 19.6 What §19 deliberately does not compute

- **No moral-identity score / no pooling.** The two facets are scored separately; no `(internalization + symbolization)/2` and no pooled "centrality" scalar is ever formed (§13.5). The JSON block carries `mean_internalization` and `mean_symbolization` as separate keys and no pooled key — asserted by `check_r1` (rejects `centrality`/`moral_identity` keys) and `check_r1_no_pool`.
- **No imputed declines.** A declined item is **dropped**, never scored 0; a below-floor facet is suppressed — asserted directly against the code by `check_r1_no_pool()` (the R1 analog of the §14.1 CoV-ceiling / |8.0| lock and `check_r2_censoring`).
- **No per-person moral ranking.** Neither high centrality nor internalizing-over-symbolizing is scored as better; R1c is a cohort validity anchor, not an individual verdict (§19.4). The dark-side reading (self-righteousness, licensing) is held open.
- **No two-tailed / per-person moderation.** R1b's gap leg is one-sided (upper CI < 0 only — the wrong-direction POSITIVE cohort is rejected, proven by `check_r1b_moderation_lock`) and cohort-level; it is never a per-person "your identity moderates your gap" verdict, and a very negative gap is modesty, not scored better (§19.5). The H10–H12 dampening legs remain DEFERRED (cohort-coupled).
- **No cohort statistics on-device.** The N=1 facet reveal now ships in `poc-projection.js` (§19.7), but the R1a reliability, R1c directional anchor, and R1b moderation are **cohort-level** reads that deliberately stay OFF-device — they need the validation cohort, are not per-person, and would mislead if shown as an N=1 verdict. Only the two per-person facet means cross to the device.
- **No real centrality-log collection yet.** The on-device reveal runs on the instrument's centrality log, but the log's real item wording and collection flow (§19 item 6d) remain **Dave-gated** — synthetic fixtures only until the phrasing is authored and pre-registered.

### 19.7 On-device facet reveal (BUILT — the first shipped N=1 reveal for the H9–R6 family)

The N=1 facet reveal now runs **on-device** in `poc-projection.js`, breaking the reveal-deferral logjam that had held every H9–R6 branch's projection back:

    centralityFacets(records) -> { internalization, symbolization, n_internalization, n_symbolization, ok }
    # per-person, on-device; mirrors centrality_facet_by_user (§19.1) exactly

- **What it computes.** For one person's centrality records, `facetMean()` means each facet's ≥ 3 scorable items; `centralityFacets()` exposes the two facet means as **separate keys** — `internalization` and `symbolization`, each `null` below the ≥ 3-item floor — and never averages them into one scalar (§13.5). `centralityResponse()` uses `typeof v === "number"` so a declined (non-numeric / boolean) item is **dropped**, never imputed 0 (§1.5) — matching the analyzer's `_centrality_response`.
- **The parity lock.** `check_impl_parity.py` runs `centralityFacets()` under node on every fixture participant **plus** a synthetic below-floor user (2 internalization items, 0 symbolization) and asserts JS == Python on facet means, scorable-item counts, and the ≥ 3-floor suppression (`null` ⇔ absent). This takes the parity gate from 9/9 to **10/10**.
- **The analyzer companion.** `analyze.py` emits `R1.moral_identity_facet_reveal` — a per-user list of the two facet means with their item counts, `None` below floor — asserted by `check_r1` to carry no pooled key, suppress below-floor facets, and never suppress an at/above-floor facet.
- **Still off-device.** The reveal is the **only** R1 computation that crosses to the device; the cohort statistics (§19.2–§19.5) stay analyzer-side (§19.6), and the real centrality-log collection stays Dave-gated (§19.6).

---

## 20. R6 — moral conviction / metaethical objectivism (PROPOSED — pending DECISIONS §25 lock)

R6 asks a **meta-level** question about the values already scored elsewhere: does a person hold their moral claims as **objective facts** — true or false independent of anyone's opinion, true for everyone — or as **personal commitments** — deeply held, but ultimately their own stance? This is *metaethical objectivism* (Goodwin & Darley 2008, *The psychological and philosophical significance of ethical objectivism*), the cousin of Skitka's *moral conviction* (Skitka 2010) — the strength-and-metaphysics of how a value is held, orthogonal to *which* value it is. Its defining structure is a **two-part split held strictly apart** (§13.5 — the load-bearing discipline for this branch): the **stated objectivism probe** (a direct per-claim rating of how fact-like vs. opinion-like the claim is) and the **revealed signatures** (tolerance/compromise behavior + objectivist-vs-subjectivist language, κ-gated). The two are **NEVER pooled** into one "conviction score," because they dissociate — someone can *say* a claim is objective yet behave tolerantly, and vice versa. Within the stated probe, **moral** claims and **taste/preference** claims route to **disjoint reads**, never blended. **Deliberately avoided:** any excluded paradigm — Goodwin & Darley and Skitka are well-replicated, not fraud/non-replication cases (see build-and-validate.md exclusions); the branch is built with EXTRA value-neutral force (§20.4).

**Status.** R6a + R6d + R6b + the two per-person claim-type reads (`mean_moral_objectivism`, `mean_taste_objectivism`) are BUILT (`analyze.py --objectivism-log` / `--r6b-log`, gated in `check_analyzer_thresholds.py` on `analysis/fixtures/sample-objectivism-log.json` + `sample-r6b-log.json`, Python-only so parity stays green). With **R6b (the discriminant leg — objectivism is not reducible to R2 sacredness / R1 centrality / value-importance)** now built, R6 = **reliability (R6a) ∧ directional anchor (R6d) ∧ discriminant (R6b)**. Only R6c (the stated–revealed meta-gap — the revealed tolerance/compromise + objectivist-language signatures) remains DEFERRED (§20.5, κ-gated); the **on-device objectivism reveal is now BUILT** (§20.7, `poc-projection.js objectivismReads`, JS↔Python parity-locked). The metaethical-objectivism log is a **new light data-contract** (one Likert response per item, each carrying its `claim_type` ∈ {moral, taste}); real collection + exact item phrasing (the Goodwin & Darley stem "Is this claim true or false as a matter of objective fact, or is it a matter of opinion or preference?") are runtime/design-gated and surfaced to Dave.

### 20.1 Measurement primitive

For person `i`, over their objectivism-probe items partitioned by claim type, each claim type is scored as its **own** within-person mean on a 1–7 objectivism Likert (1 = purely a matter of opinion/preference … 7 = objectively true or false, a fact independent of anyone's view) — the two claim types are DISJOINT item sets, never combined:

    objectivism_moral_i = mean over i's MORAL-claim items    (≥ 3 scorable items, §1.5 N=1)   # the reveal quantity
    objectivism_taste_i = mean over i's TASTE-claim items    (≥ 3 scorable items, §1.5 N=1)   # the cohort baseline
    # NO pooled (moral + taste)/2 is ever formed, and the STATED probe is
    # NEVER pooled with the (deferred) REVEALED tolerance/language signatures (§13.5)

The moral read `objectivism_moral_i` is the reveal quantity; the taste read is the cohort-anchor baseline (§20.3). The JSON `R6` block deliberately exposes `mean_moral_objectivism` and `mean_taste_objectivism` as **separate keys with no pooled "objectivism"/"conviction" key**.

**No-pool / missing-data lock (the R6 analog of the §13.2 censoring lock).** A **declined item** — objectivism missing, non-numeric, or boolean — makes `_objectivism_response` return `None`, so the item is **DROPPED** from its claim type, never imputed to 0. A claim type with **fewer than 3 scorable items** is **SUPPRESSED** (absent), never scored on thin data. And the two claim types route to **disjoint** means — the moral read never absorbs a taste response and vice versa. Asserted directly against the code by `check_r6_no_pool()`.

### 20.2 R6a — objectivism reliability (BUILT)

Metaethical objectivism must be a stable individual difference, not occasion noise. Split each person's sessions odd/even, compute the **moral** read on each half, and correlate across participants present in both halves:

    r = pearson_i( objectivism_moral_i^{odd}, objectivism_moral_i^{even} )    over shared participants (≥ 3)
    R6a supported  ⇔  lower 95% bootstrap CI of  r  ≥ 0.50

Bootstrap: percentile method over paired `(objectivism_moral_i^{odd}, objectivism_moral_i^{even})`, pre-committed seed `20260510 + 23`. This mirrors the H10a / H11a / H12a / R1a split-half reliability construction exactly (`_odd_even_sessions` + `_pearson_r` + `_bootstrap_ci_r`). The reliability floor is the **higher 0.50 bar** (vs. 0.40 for the exploratory branches) because Goodwin & Darley and Skitka establish objectivism as a **stable trait-like individual difference**, not a labile state — a lower bar would under-hold a construct the literature says should be reliable.

### 20.3 R6d — moral > taste objectivism directional anchor (BUILT, directional — cohort validity check)

The construct's defining, replicated prediction is directional: on average people treat **moral** claims as **more fact-like** than **matters of taste** — the objectivism gradient Goodwin & Darley 2008 report across samples (ethical claims sit between unambiguous facts and pure preferences, but well above tastes):

    delta_i = objectivism_moral_i − objectivism_taste_i     # within-scale (same 1–7 objectivism Likert), per person with BOTH reads
    R6d supported  ⇔  lower 95% CI of  mean_i delta_i  > 0   (one-sided)

Seed `20260510 + 24`. `delta_i` is a **within-scale within-subject contrast** (both reads on the identical 1–7 objectivism Likert), legitimate exactly as R1c's `internalization − symbolization`, H12's `severity_other − severity_self`, and H10c's `public − anonymous` — **NOT** cross-scale pooling. This is a **cohort validity anchor** (does the instrument recover the established direction?), **NOT a per-person verdict** — an individual with `delta_i < 0` treats their tastes as more objective than their morals, described as such and never scored as more or less moral (§20.4). **Naming:** this second leg is labeled **R6d**, not R6c, deliberately — the design spec (r6-moral-conviction.md) reserves R6c for the stated–revealed meta-gap (DEFERRED, §20.5); the moral>taste anchor is a distinct directional check that would otherwise collide with that label.

### 20.4 No-pool lock, N=1, value-neutrality (EXTRA force)

- **No-pool lock (load-bearing).** Per §20.1: the STATED probe is never pooled with the (deferred) REVEALED signatures into one conviction score; the moral and taste reads are disjoint item sets scored separately, never pooled into (M+T)/2; a declined item drops (never imputed 0); a below-floor claim type is suppressed. `check_r6_no_pool()` asserts this against the code so a regression that starts pooling, imputing declines, or scoring a two-item read is caught even if the fixture changes.
- **N=1 interpretability.** `objectivism_moral_i` is a within-person mean over that person's ≥ 3 moral items — reveal-eligible for a single user with no cohort standardization ("you tend to treat moral claims as objective facts, true or false independent of opinion"), contrast the cohort-only R6a / R6d statistics. This reveal now **ships on-device** (§20.7): `objectivismReads()` in `poc-projection.js` computes the two claim-type reads per person, JS↔Python parity-locked against `objectivism_by_user`. Both reads are shown side by side **without** a per-person moral>taste verdict (that gradient is the cohort-only R6d, never an N=1 ranking).
- **Value-neutrality (load-bearing, EXTRA force — the branch is charged).** Holding morals as objective facts is **not** scored as better or worse than holding them as personal commitments. Each metaethical pole is **dual-read and never ranked**: objectivism reads as **moral clarity** *or* **rigid intolerance** (the documented risk — objectivists are less tolerant of moral disagreement, more willing to impose); subjectivism reads as **tolerant pluralism** *or* **standing for nothing**. The reveal describes where a person sits and stops there. The stance is **never** a virtue score, and the deliberately-NOT-built-in stance is that objectivism is neither more correct nor healthier (see build-and-validate.md / r6-moral-conviction.md §2 — the branch takes no side on the metaethics itself).
- **Cheap-talk / self-report caveat.** These are *self-reported* ratings of how fact-like a claim is, not behavior under disagreement. The claim-type reads measure **stated** objectivism; the reveal never claims the person would *act* intolerantly or refuse to compromise. Behavioral validation (does stated objectivism predict the revealed tolerance/compromise signature?) is the R6c meta-gap leg — Phase-2 / κ-gated and surfaced to Dave.

### 20.5 R6b — discriminant (BUILT) / R6c — meta-gap (DEFERRED)

- **R6b — discriminant (BUILT)** (metaethical objectivism is not just how-much-you-care): regress `objectivism_moral_i` on THREE "how much morality matters" constructs drawn from THREE DIFFERENT channels — `sacredness_i = |P_i|` (R2/§17.1, the size of the protected/`never` set), `centrality_i` (R1/§19.1 internalization), and `value_importance_i` (§5.1, aspirational card-sort selection breadth). Bootstrap the model R² CI (percentile method, pre-committed seed `20260510 + 30`), and

        R6b supported  ⇔  upper 95% CI of  R²( objectivism_moral ~ [sacredness, centrality, importance] )  < 0.50

  — objectivism carries variance those three miss, so it is a **distinct construct**, not reducible to how absolute / central / broad a person's values are (Goodwin & Darley 2008; the objectivism–conviction distinction). Built via `compute_r6b_discriminant` (`analyze.py --r6b-log`), gated by `check_r6b_discriminant_lock()` on `analysis/fixtures/sample-r6b-log.json`; Python-only (cohort-level, no on-device reveal) so parity stays green. **No manufactured trap** (the H12b pattern, deliberately): the outcome rides a genuinely INDEPENDENT fourth Likert channel — the four quantities come from four DIFFERENT logs (objectivism / protected / identity / card-sort), so there is **no algebraic identity** to force the R². The lock proves the *absence* of one by flipping the verdict **True→False on IDENTICAL predictors** via the objectivism channel alone (independent draw → R² ~ 0 → supported; a noisy linear echo of the predictors → R² high → not supported). Descriptive companions = bare Pearson r of objectivism vs each predictor. §13.5 no-pool: the R² is a **cohort-level** statistic, never a pooled per-person scalar. R6b reuses the R²-CI discriminant machinery of H9b / H10b / H11b / H12b exactly.
- **R6c — the stated–revealed meta-gap** (the headline): does stated objectivism match revealed behavior? The revealed signatures — refusal to compromise on the claim, intolerance of disagreement, and objectivist-vs-subjectivist *language* — are **κ-gated** (require a human-rater coding pipeline with inter-rater reliability, exactly as the §6 language-coding legs). **DEFERRED** — the current increment ships only the stated probe, isolated on its own fixture. The §13.2 CENSORING discipline attaches here: a **refusal to compromise** stays right-censored (a value one will not trade), never finitized into a price — the |8.0| lock pattern.

### 20.6 What §20 deliberately does not compute

- **No conviction score / no pooling.** The stated probe and the (deferred) revealed signatures are never pooled; the moral and taste reads are scored separately; no `(moral + taste)/2` and no pooled "objectivism"/"conviction" scalar is ever formed (§13.5). The JSON block carries `mean_moral_objectivism` and `mean_taste_objectivism` as separate keys and no pooled key — asserted by `check_r6` (rejects `conviction`/`objectivism_score` keys) and `check_r6_no_pool`.
- **No imputed declines.** A declined item is **dropped**, never scored 0; a below-floor claim type is suppressed — asserted directly against the code by `check_r6_no_pool()` (the R6 analog of the §14.1 CoV-ceiling / |8.0| lock and `check_r2_censoring`).
- **No metaethical ranking.** Neither objectivism nor subjectivism is scored as better or more correct; R6d is a cohort validity anchor, not an individual verdict, and each pole is dual-read (§20.4). The branch takes no side on the metaethics.
- **No behavioral / language claim yet.** R6's headline stated–revealed meta-gap (R6c) remains DEFERRED (κ-gated); the discriminant (R6b) is now BUILT. This branch ships the stated claim-type reads + reliability (R6a) + directional anchor (R6d) + discriminant (R6b), each isolated on its own fixture; only the revealed tolerance/compromise/language signatures await the human-rater pipeline.
- **No cohort statistics on-device.** The N=1 claim-type reveal now ships in `poc-projection.js` (§20.7), but the R6a reliability, R6d directional anchor, and R6b discriminant are **cohort-level** reads that deliberately stay OFF-device — they need the validation cohort, are not per-person, and would mislead if shown as an N=1 verdict. Only the two per-person claim-type reads cross to the device.
- **No real objectivism-log collection yet.** The on-device reveal runs on the instrument's objectivism log, but the log's real item wording and collection flow (the Goodwin & Darley probe stems) remain **Dave-gated** — synthetic fixtures only until the phrasing is authored and pre-registered.

### 20.7 On-device claim-type reveal (BUILT — the second shipped N=1 reveal for the H9–R6 family)

The N=1 claim-type reveal now runs **on-device** in `poc-projection.js`, the second family reveal to ship (after R1's facet reveal, §19.7) and the pattern's confirmation that the deterministic two-mean reveals port cleanly:

    objectivismReads(records) -> { moral, taste, n_moral, n_taste, ok }
    # per-person, on-device; mirrors objectivism_by_user (§20.1) exactly

- **What it computes.** For one person's objectivism records, `claimTypeMean()` means each claim type's ≥ 3 scorable items; `objectivismReads()` exposes the two reads as **separate keys** — `moral` and `taste`, each `null` below the ≥ 3-item floor — and never averages them into one scalar, nor fuses the stated probe with the deferred revealed signatures (§13.5, the load-bearing R6 discipline). `objectivismResponse()` uses `typeof v === "number"` so a declined (non-numeric / boolean) item is **dropped**, never imputed 0 (§1.5) — matching the analyzer's `_objectivism_response`. The two reads are shown side by side with **no per-person moral>taste verdict** (that gradient is the cohort-only R6d).
- **The parity lock.** `check_impl_parity.py` runs `objectivismReads()` under node on every fixture participant **plus** a synthetic below-floor user (2 moral items, 0 taste) and asserts JS == Python on claim-type means, scorable-item counts, and the ≥ 3-floor suppression (`null` ⇔ absent). This takes the parity gate from 10/10 to **11/11**.
- **The analyzer companion.** `analyze.py` emits `R6.objectivism_claim_reveal` — a per-user list of the two claim-type reads with their item counts, `None` below floor — asserted by `check_r6` to carry no pooled key, suppress below-floor reads, and never suppress an at/above-floor read.
- **Value-neutral, EXTRA force.** The reveal describes where a person sits on each claim type and stops — objectivism reads as moral clarity **or** rigid intolerance, subjectivism as tolerant pluralism **or** standing for nothing; neither pole ranked, the branch takes no side on the metaethics (§20.4).
- **Still off-device.** The reveal is the **only** R6 computation that crosses to the device; the cohort statistics (§20.2–§20.5) stay analyzer-side (§20.6), and the real objectivism-log collection stays Dave-gated (§20.6).

---

## 21. A3 — the moral-language channel: the coder + the κ gate (PROPOSED — pending DECISIONS §26 lock)

> **Numbering.** This is **sequential §21** in scoring.md (the running build order §14 H9 … §20 R6, §21 A3). The design doc `h-a3-moral-language.md` refers to a *notional* §20 for this channel; that collides with sequential §20 = R6, so A3 takes the next sequential slot. The DECISIONS lock is proposed as **§26** (R6 was §25).

A3 opens a **third channel on values**, orthogonal to the two the instrument already reads. Channel one is the **elicited/stated** inventory (what a person says they value when asked — the probes, card-sort, R1/R6 self-reports). Channel two is the **revealed** signature (what their choices, prices, and censoring behavior show — the ladders, H10–H12, R2). A3 is the **spontaneous** channel: *what a person moralizes about unprompted, and in what moral vocabulary* — which of the six Moral Foundations (Haidt & Graham; care / fairness / loyalty / authority / sanctity / liberty) their free-text language actually invokes. It is **foundational infrastructure**: the deferred R3/R4/R5 branches all draw on this same coded corpus, so the coder + its reliability gate are built first.

**The binding discipline is the κ gate (§21.2), not parity.** Language/LLM coding is **non-deterministic** by nature, so A3 is — **deliberately, as the first branch to do so** (`h-a3-moral-language.md` §1.5/§3/Q4) — placed **OUTSIDE** the `poc-projection.js` ↔ `analyze.py` parity contract. There is no on-device language reveal; A3 is Python-only and parity stays trivially green. In parity's place stands a stricter gate: **inter-rater reliability** (Cohen's κ) against gold-standard manual coding. The coder shipped this increment is a **byte-deterministic MFD-lexicon v0.1 DRAFT** stand-in (like H11's distance map): its *known* over- and under-matching is not a bug to hide but the honest **illustration of why the κ gate exists** — the real coder is an LLM pinned at temperature 0, and neither coder is trusted at scale until it clears κ ≥ 0.70 against **human** gold.

### 21.1 Measurement primitive

A **moral-language log**: each record is one free-text utterance `{user, session, prompt_id, text, gold_foundations}`. The coder reads `text` → a **set** of invoked foundations:

    tokens        = _tokenize(text)                # pure-stdlib, lowercased alphanumeric runs, no regex
    code(text)    = { f ∈ FOUNDATIONS : some token PREFIX-matches some stem of f }   # the MFD `word*` wildcard

`code_foundations` is **multi-label** (an utterance may invoke zero, one, or several foundations) and **byte-deterministic** (same text → same set, always). `gold_foundations` is the **gold-standard reference coding** — in the fixture, a SYNTHETIC stand-in for the ~200 human manual codes the real κ needs (§21.2). `foundation_i(f)` is a per-user, volume-normalized **rate** (§21.3), never a count that rewards verbosity.

**The κ operationalization.** Cohen's κ is computed over the binary **(utterance × 6-foundation)** present/absent cells:

    p_o = agree_cells / n_cells
    p_e = p_a1·p_b1 + (1 − p_a1)·(1 − p_b1)          # p_a1, p_b1 = coder/gold marginal present-rates
    κ   = (p_o − p_e) / (1 − p_e)                     # None if 1 − p_e == 0 (a rater never varies — undefined, not a fake 1.0)

This is the standard multi-label MFD reliability approach. `compute_a3_coding_kappa` carries κ **with its integer marginals** (`n_utterances`, `coder_present`, `gold_present`, `agree_cells`) so κ is never a bare scalar dressed up as reliability. `check_a3_kappa_lock()` pins the math against the code: perfect → 1.0, a hand TP9/TN9/FP1/FN1 → 0.8, TP8/TN8/FP2/FN2 → 0.6, a no-variance corpus → None.

**Missing-data (§1.5).** `_utterance_text` maps blank / whitespace-only / `None` / absent text → `None` = **missing data, DROPPED** from both the κ corpus and the profile denominator. This is held strictly apart from a **non-blank zero-foundation** utterance — someone who *writes* but doesn't moralize — which **COUNTS** in the denominator: the particularist is described as using less moral language, never treated as missing and never scored deficient (§21.4).

### 21.2 The binding κ gate — the descriptive-only WALL (BUILT: machinery only)

    A3 machinery certified  ⇔  synthetic κ ≥ A3_KAPPA_GATE (0.70)     # kappa_met_synthetic
    A3 channel promotable   ⇔  κ ≥ 0.70 vs. REAL HUMAN gold           # ALWAYS False this increment

On the synthetic fixture the coder clears the gate (κ ≈ 0.90 ≥ 0.70), which certifies **the machinery only** — that the coder, the κ computation, the marginals, and the missing-data handling are correct. It does **not** promote the channel. `promotable` is **ALWAYS False** and `descriptive_only` is **ALWAYS True**, because real promotion requires κ ≥ 0.70 against **gold-standard manual coding by human raters** (~200 codes, 50/domain × 2 raters — the §12 open question, Dave/human-gated). **Until that human-κ is met, the entire A3 channel is descriptive / exploratory-only.** The gate is **two-sided** — `check_a3_kappa_lock()` asserts a high-agreement corpus clears 0.70 *and* a low-agreement one does not, and that neither is ever `promotable`. This wall is the A3 analog of the §13.2 censoring lock and the |8.0| pattern: a structural invariant asserted against the code, not a fixture convenience.

### 21.3 foundation_i(f) — the value-neutral rate profile (BUILT)

`foundation_profile_by_user` returns, per user, a **rate vector** over all six foundations — `rate_i(f) = (# of that user's utterances invoking f) / (that user's scorable utterances)` — plus a cohort mean-rate vector. It is exposed in the JSON `A3` block as six **separate** foundation keys under `foundation_profile.cohort_mean_rates`, **never** collapsed into a scalar and **never** sorted by rate (the renderer emits canonical MFD order deliberately, so no ranking is implied). `check_a3` rejects any pooled `moral_language_score` / `foundation_score` / `mft_score` / `moralization_score` key and requires all six foundations present separately.

### 21.4 The κ-is-not-a-score wall, N=1, value-neutrality (EXTRA force)

- **κ is a coder-PAIR statistic, NEVER a person score (§13.5).** κ measures whether two *coders* agree, not anything about a *participant*. It is structurally impossible to attach κ to a user — it lives only in the coding-validation block, never in `foundation_profile`. `check_a3` and `check_a3_kappa_lock` assert this.
- **More moral language is NOT better.** Fluent moralizing is as consistent with **grandstanding** as with engagement (Tosi & Warmke, *Moral Grandstanding* 2016); moral-language **fluency ≠ virtue**. The coder assigns foundation **labels**, never ranks them, never emits a scalar "how moral" reading.
- **Declining to moralize is a stance, not a deficit.** A person who writes in **concrete, relational, particular** terms without invoking abstract foundations is making a recognizable **Dancy particularist** move — not registering a deficient "zero." A non-blank zero-foundation utterance is counted and described as such (§21.1), never scored down.
- **N=1 interpretability.** `foundation_i(f)` is reveal-eligible for a single user with no cohort standardization ("your written responses most often invoke *care* and *fairness* language") — but only descriptively, and only once the human-κ gate is met; the synthetic-certified machinery makes no person-level claim.

### 21.5 DEFERRED — the cohort-coupled halves

Built this increment: the coder + the κ gate + `foundation_i(f)` + the synthetic reliability fixture. **Deferred** (each couples to the cohort or awaits the human-κ gate, exactly as the H9b/H10b/H11b/R2c/R1b/R6b discriminant halves do):

- **Framing ratio** (individualizing care+fairness vs. binding loyalty+authority+sanctity language balance) — a within-person contrast over `foundation_i`, cohort-anchored.
- **The third ordering L_i + the S/R/L concordances** (§13.4 extension): a *language-derived* value ordering to sit beside the Stated and Revealed orderings, with three pairwise concordances (S↔R, S↔L, R↔L). Cohort-coupled and κ-gated.
- **H-A3a** (language-coding reliability as a hypothesis), **H-A3b** (the language channel is distinct from stated + revealed — discriminant), **H-A3c** (grandstanding signature) — all cohort- and/or human-κ-gated.

### 21.6 What §21 deliberately does not compute

- **No moral-language score / no pooling.** The coder emits foundation **labels** and per-foundation **rates**; no `(care + fairness + …)` sum, no pooled "moral-language"/"moralization" scalar, and κ is never blended with the stated (§20/R1) or revealed (R2/H10–12) channels (§13.5). Asserted by `check_a3` (rejects pooled keys) and `check_a3_kappa_lock`.
- **No promotion on synthetic κ.** Synthetic κ certifies the machinery; `promotable` stays False until human-gold κ ≥ 0.70. The channel is descriptive/exploratory-only until then — asserted two-sided against the code.
- **No ranking of foundations, no fluency = virtue.** Foundations are labeled, never ordered by worth; more moral language is neither better nor worse (§21.4).
- **Not parity-gated, by design.** LLM/language coding is non-deterministic, so A3 is deliberately the first branch **outside** the `poc-projection.js` ↔ `analyze.py` parity contract (`h-a3-moral-language.md` §1.5/§3/Q4). There is no on-device language reveal; the reliability gate (§21.2) stands in parity's place. The v0.1-DRAFT deterministic lexicon, the real-κ-needs-human-gold requirement, and the LLM-vs-deterministic coder choice are surfaced to Dave, not auto-locked.

---

## 22. A4 — the decision-conflict channel: the RT-derived effort signal (PROPOSED — pending DECISIONS §27 lock)

> **Numbering.** This is **sequential §22** in scoring.md (the running build order §14 H9 … §21 A3, §22 A4). The design doc is `h-a4-a5-process-emotion.md` (A4 = the process channel; A5 = the emotion channel, not built this increment). The DECISIONS lock is proposed as **§27** (A3 was §26).

A4 opens a **fourth channel**, orthogonal to the three on *values* — but A4 is not a channel on *which* values a person holds at all. The stated (§20/R1 probes), revealed (R2/H10–H12 choices), and spontaneous-language (§21 A3) channels all read **what** a person moralizes about. A4 reads the **process**: *how effortfully a choice was reached* — the response-time signature of hesitation, ambivalence, and cognitive load behind a moral judgment, independent of which way it went. It is the instrument's first **process** measure, and it is exploratory / high-noise by nature, so it ships behind a **tight reliability gate** and with the strongest value-neutrality wall in the project.

**The load-bearing discipline: conflict is EFFORT, never a framework read.** The single most important constraint on A4 is what it must **not** claim. A slow, effortful response is **not** evidence of deontological (vs. utilitarian) processing — the dual-process "hard cases are slow" story does not survive replication (Bago & De Neys, *Fast logic?* 2019; the instrument's `concept.md` already disclaims the Greene fast/slow mapping). So A4's read is **effort/ambivalence only**: `conflict(i, ·)` says *this choice was harder for this person than their baseline*, and nothing about **which moral framework** produced it. `check_a4` structurally rejects any `deliberation` / `utilitarian` / `deontological` / `framework` key; `check_a4_conflict_lock` asserts the render frames the signal as EFFORT and never a framework label.

### 22.1 Measurement primitive

A **decision-process log**: each record is one item response `{user, session, domain, item, response_time_ms, prompt_chars, presented_position}`. The conflict primitive is a **within-person, confound-residualized** z of response time:

    exclude       was_timeout ∨ timed ∨ scenario_type startswith "quick-fire"        # CV-1: quick-fire / timed items are not free-RT
    resid_i       = OLS residuals of response_time_ms on [prompt_chars, presented_position]   # strip reading-load + order
    conflict(i,item) = within-person z-score of resid_i                              # people read at different speeds
    conflict(i,domain) = mean over person i's domain items of conflict(i,item)

`_ols_residuals` residualizes RT on **reading-load** (`prompt_chars`) and **order** (`presented_position`) via the normal equations (intercept + 2 predictors) so a **slow-because-the-prompt-was-long** response is not misread as high conflict; if a person's within-person design is rank-deficient (no length/position variance) it falls back to plain within-person mean-centering. The `was_timeout` and the **timed quick-fire** set (CV-1) are **excluded** — a timed item's RT is an artifact of the clock, not of deliberation. `check_a4_conflict_lock` pins the residualizer exact on a hand case and proves the length-confound removal directly: a 10×-longer item with **median** effort is a large *naive*-RT outlier (z ≈ +2) but lands **mid-pack** after residualization (|z| < 0.3).

**Why the unit is per-DOMAIN, not per-person.** `conflict(i, item)` is z-scored **within each person**, so a person's conflict values have mean ≈ 0 **by construction** — a single pooled "person conflict score" would be degenerate (every participant would sit at ~0). The interpretable unit is therefore the **within-person relative effort per domain**: is this person more ambivalent about *harm* items than *truth* items than *fairness* items? `conflict_by_user_domain` returns `{(user, domain): mean_rt_z}`; `check_a4_conflict_lock` asserts the within-person mean is ≈ 0 (so a person-pool is degenerate) and that the cell key is `(user, domain)`.

### 22.2 The binding A4a reliability gate (BUILT: machinery only)

    A4a machinery certified  ⇔  per-domain split-half test–retest, lower 95% CI ≥ A4A_RELIABILITY_FLOOR (0.40)   # any_met

`compute_a4a_conflict_reliability` splits each person's sessions **odd/even**, computes `conflict(i, domain)` in each half, and correlates the two halves **across people, per domain** (participant-level non-parametric bootstrap, reusing `_domain_test_retest_r` and the project bootstrap seed). The gate is the **exploratory** bar — the *lower* 95% CI of the per-domain test–retest r ≥ **0.40** (deliberately below the 0.40–0.50 confirmatory bars of H10a–R6a, because a process channel is noisier). `any_met` is True iff **at least one** domain clears it. On the synthetic fixture all three domains clear (r ≈ 0.98–1.00). This certifies **the machinery only** — that the residualizer, the exclusions, the within-person z, the per-domain averaging, and the bootstrap are correct — never that a *real* cohort's decision conflict is reliable. The gate is **two-sided**: `check_a4_conflict_lock` asserts a corpus with a stable per-domain effort tilt clears the bar (`any_met` True) while the **same** corpus with the tilt flipped at retest does **not** (`any_met` False) — reliability is earned, not structural.

### 22.3 No pooled score, no framework label, value-neutrality (EXTRA force)

- **No pooled conflict scalar (§13.5).** A4 emits per-`(user, domain)` relative-effort cells and a per-domain reliability vector — **never** a summed "conflict score," and conflict is never blended with the stated / revealed / language channels. `check_a4` rejects any `conflict_score` / `a4_score` / `process_score` / `effort_score` key.
- **No moral-framework label — the load-bearing wall (§22 intro).** conflict is **effort**, not a read on utilitarian-vs-deontological processing (slow ≠ deontological; Bago & De Neys 2019). `check_a4` rejects `deliberation` / `utilitarian` / `deontological` / `framework` keys; the lock asserts the render never attaches a framework label.
- **Value-neutral: effortful virtue is not worse than easy virtue.** High conflict is **not** a deficit. Finding a virtuous choice **hard** — feeling the pull of the cost and choosing well anyway — is arguably the *stronger* character signal (the effortful-virtue cell), not the weaker one. A4 **describes** where the effort sits; it never ranks low-conflict above high-conflict or vice-versa.
- **N=1 interpretability.** `conflict(i, domain)` is reveal-eligible for a single user with no cohort standardization ("your *harm* choices took more deliberation than your *fairness* choices") — but descriptively, and only as effort, never as a framework diagnosis.

### 22.4 A4b — the discriminant half (BUILT); revision capture + the on-device reveal (DEFERRED)

Built earlier: the conflict primitive + the A4a reliability gate + the synthetic reliability fixture. Built this increment: **H-A4b, the discriminant half**. Still **deferred:**

- **H-A4b — does conflict add information beyond the choice? (discriminant) — BUILT.** A **WITHIN-PERSON (fixed-effects)** test of whether `conflict(i, domain)` — A4's RT-derived effort — is a distinct channel or merely a shadow of *what* was chosen. On the (user × domain) cell it regresses conflict on the choice **level** `z_revealed` (§3.2) and the aspirational-departure magnitude `|gap|` (§6), each **person-centered before pooling**, and calls conflict **DISTINCT ⇔ the UPPER 95% bootstrap CI of the model R² < A4B_R2_CEILING (0.50)** (seed `BOOTSTRAP_SEED + 33`). Person-centering is **load-bearing** (the A4b analog of H11b's external-generosity / H9b's magnitude-channel choice): conflict is a within-person z (~zero between-person variance under the per-person sum constraint) while `z_revealed`/`|gap|` carry mostly *between*-person variance, so a raw-score regression would cap R² below the ceiling and make the gate a one-sided rubber stamp — centering both sides makes it honestly two-sided. **No manufactured trap** (the H12b/R6b property): conflict rides the **independent RT channel** (residualized `response_time_ms`, §1.1), not an affine echo of the choice columns, so on a *fixed* session/card-sort corpus the verdict flips True→False through the RT channel alone — an RT profile drawn ⊥ the choice profile gives R² ≈ 0, one built to track `[level, |gap|]` gives R² high. **Descriptive companions** (within-person `conflict·level r`, `conflict·|gap| r`) localize any leakage without pooling. **Caveat:** the bootstrap resamples cells, so its CI understates repeated-user dependence (pseudo-replication) — but a distinctness claim must clear a *ceiling*, so understated width only makes "distinct" harder to earn (conservative). `compute_a4b_discriminant` + `--a4b-log` (`{process, session, card_sort}` bundle); locked two-sidedly by `check_a4b_discriminant_lock` (INDEPENDENT / REDUCIBLE / tiny cohorts through the real pipeline); fixture `sample-a4b-log.json` (SUPPORTED cohort only). Python-only, no on-device reveal → **parity stays green (9/9)**.
- **Answer-revision capture (Q1, Dave/runtime-gated) — DEFERRED.** RT is one process signal; **answer changes** (a participant selecting, then switching) are a second, arguably cleaner ambivalence signal. Whether the runtime captures revision events — and how — is an **open runtime question** (`h-a4-a5-process-emotion.md` §4 Q1), surfaced to Dave, not guessed. A4 is **RT-only** for now.
- **The on-device reveal + its parity lock — DEFERRED.** A4 is **parity-gated in principle** (unlike A3, whose non-determinism put it permanently outside parity — conflict is a deterministic arithmetic transform of logged RT, so it *belongs* in parity once revealed). But both A4a's per-domain reliability and A4b's cohort discriminant are **cohort-level analyses with no per-person on-device output**, so the `conflict(i, domain)` reveal in `poc-projection.js` stays **deferred** (the H9–R6 Python-only precedent) and A4 adds **nothing** to the parity contract. When the reveal ships, it changes **both** `analyze.py` and `poc-projection.js` together.

### 22.5 What §22 deliberately does not compute

- **No conflict score / no pooling.** Per-domain effort cells + a per-domain reliability vector + a cohort-level discriminant R²; no summed "conflict"/"process"/"effort" scalar, never blended across channels, and A4b person-centers → pools within-person deviations for a single cohort R² rather than ranking anyone (§13.5). Asserted by `check_a4` + `check_a4_conflict_lock` + `check_a4b_discriminant_lock`.
- **No moral-framework read.** conflict is EFFORT/ambivalence, never utilitarian-vs-deontological (Bago & De Neys 2019). The render carries the disclaimer; both the A4a and A4b locks assert it (and scan the A4b payload for banned framework keys).
- **No promotion on synthetic reliability.** Synthetic `any_met` certifies the machinery; a *real* cohort's process reliability is unproven until real data. Exploratory-only.
- **No public card (§1.4).** A4 is an **analysis adjunct** — context for the reveal, never a headline card in `research-program.json`. This also sidesteps the site-sync seam (no card to sync). A4 gets **no** public card, by design.

---

## 12. What's not yet specified (open questions)

- **Narrative-indicator scoring detail.** Each branching-narrative terminal scene has `resolution:*` tags. Whether to map each terminal directly to a primary-axis score (1:1) or compute the score from the *path* (sequence of decisions) is unresolved. Defer to a pilot read on whether path-based scoring adds discriminating signal beyond terminal-based.
- **Inter-rater reliability target for LLM story-coding.** README claims κ ≥ 0.70 before LLM coding is trusted at scale. The reference labels need to come from somewhere; gold-standard manual coding of ~50 stories per domain (~200 total) by 2 raters is the obvious approach but is real labor.
- **Within-user trajectory model.** Should the trajectory be linear, monotone-isotonic, or unconstrained? Strong priors weakly held; defer to pilot.
- **Handling of users who pass on the profile reveal (per `onboarding.md`).** No design difference for measurement, but the analyzer should log this so MVP-2's intervention-engagement modeling can use it.
- **`analyze.py` "never"-recode ceiling — RESOLVED 2026-06-08.** §4.1 recodes a `never` break-point to `log10(max_rung)+1`. The analyzer previously hardcoded a single ceiling (`LADDER_CEIL_LOG10 = 4.0`, a $10k top) for *all* probes, so a `never` on a high-ceiling probe was mis-scored identically to a `never` on a $10k one. Fixed via `analyze.load_probe_ceiling_map()` (per-probe `log10(real ladder top) + 1`) and locked by `check_analyzer_thresholds.py`'s probe-ceiling assertions; §13.3 still keeps `never` censored (never a finite number). Still open as a nicety: a structured `analysis.axis_direction: "forward"|"inverted"` field on the probe schema (instead of string-matching `no_break_point_handling` prose) would let §13.3 and `validate.py` stop parsing free text.
