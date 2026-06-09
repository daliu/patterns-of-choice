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

### 9.2 H8a — debiasing (low-stakes paired probes)

H8a predicts that participants whose abstract-form behaviour falls furthest short of their *stated* values show the largest narrative-induced shift toward those values.

Using the canonical gap convention of §6 (stated − revealed; positive = states higher than acts), define the per-probe abstract gap, then aggregate to one pair of values per participant over their low-stakes complete pairs:

```
gap_abs(i,p) = s_i(domain of p, aspirational) - r_abs(i,p)
D_i^(low)    = mean_p D_i^p            over low-stakes pairs
gap_i^(abs)  = mean_p gap_abs(i,p)     over the same pairs
```

**H8a test statistic:** Pearson correlation across participants `rho_8a = corr(D_i^(low), gap_i^(abs))`; the H8a criterion is a **lower 95% bootstrap-CI bound ≥ 0.15** (positive). Spearman is reported as a distribution-free robustness check.

> **Sign note (pre-registration-critical).** The one-line statement in `h8-narrative-immersion-design.md` §1 calls this correlation "negative"; that phrasing assumed a *revealed − stated* gap. Under scoring.md §6's canonical *stated − revealed* convention the predicted sign is **positive**. scoring.md's convention is canonical for the OSF filing — the two statements describe the same prediction, differing only in the gap's sign convention. This must be reconciled to one sign before lock.

> **Mathematical-coupling caveat.** `D_i^(low)` and `gap_i^(abs)` share the term `r_abs`, which inflates their correlation even under the null (a regression-to-the-mean artifact). The confirmatory H8a test is therefore paired with a **pre-registered de-coupled analysis**: regress `r_narr` jointly on `s_i` and `r_abs`, and test whether the partial association of `r_narr` with `s_i` is positive controlling for `r_abs` — i.e. the narrative response is pulled toward the stated value beyond what the abstract response already predicts. H8a is counted as supported only if the headline correlation criterion **and** the de-coupled partial-association sign agree.

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

### 9.4 H8b — attachment-laden shift (high-stakes paired probes)

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

## 12. What's not yet specified (open questions)

- **Narrative-indicator scoring detail.** Each branching-narrative terminal scene has `resolution:*` tags. Whether to map each terminal directly to a primary-axis score (1:1) or compute the score from the *path* (sequence of decisions) is unresolved. Defer to a pilot read on whether path-based scoring adds discriminating signal beyond terminal-based.
- **Inter-rater reliability target for LLM story-coding.** README claims κ ≥ 0.70 before LLM coding is trusted at scale. The reference labels need to come from somewhere; gold-standard manual coding of ~50 stories per domain (~200 total) by 2 raters is the obvious approach but is real labor.
- **Within-user trajectory model.** Should the trajectory be linear, monotone-isotonic, or unconstrained? Strong priors weakly held; defer to pilot.
- **Handling of users who pass on the profile reveal (per `onboarding.md`).** No design difference for measurement, but the analyzer should log this so MVP-2's intervention-engagement modeling can use it.
- **`analyze.py` "never"-recode ceiling — RESOLVED 2026-06-08.** §4.1 recodes a `never` break-point to `log10(max_rung)+1`. The analyzer previously hardcoded a single ceiling (`LADDER_CEIL_LOG10 = 4.0`, a $10k top) for *all* probes, so a `never` on a high-ceiling probe was mis-scored identically to a `never` on a $10k one. Fixed via `analyze.load_probe_ceiling_map()` (per-probe `log10(real ladder top) + 1`) and locked by `check_analyzer_thresholds.py`'s probe-ceiling assertions; §13.3 still keeps `never` censored (never a finite number). Still open as a nicety: a structured `analysis.axis_direction: "forward"|"inverted"` field on the probe schema (instead of string-matching `no_break_point_handling` prose) would let §13.3 and `validate.py` stop parsing free text.
