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

### 2.1 Tag-to-axis mapping (excerpt — full table in §10)

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

- **In-group/out-group secondary axis: `circle_radius`** (boundaries → hospitality). Same tag-table approach; full mapping in §10.
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

## 9. Exclusion rules

Per `pre-registration.md` §5:

- Users with < 14 completed sessions are excluded from primary analyses (sensitivity-analyzed at < 7 and < 21).
- Sessions with quick-fire median response time < 2 s are dropped as inattentive.
- Probe responses with no choice (timed-out, not yet implemented; the no-option must be explicitly clicked) are coded as missing, *not* as the no-option default.
- Pairwise items where the user consistently chooses left or right > 90% of the time are flagged but retained; analyst inspects for bias.

---

## 10. Tag-to-axis tables (truncated)

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

## 11. What's not yet specified (open questions)

- **Narrative-indicator scoring detail.** Each branching-narrative terminal scene has `resolution:*` tags. Whether to map each terminal directly to a primary-axis score (1:1) or compute the score from the *path* (sequence of decisions) is unresolved. Defer to a pilot read on whether path-based scoring adds discriminating signal beyond terminal-based.
- **Inter-rater reliability target for LLM story-coding.** README claims κ ≥ 0.70 before LLM coding is trusted at scale. The reference labels need to come from somewhere; gold-standard manual coding of ~50 stories per domain (~200 total) by 2 raters is the obvious approach but is real labor.
- **Within-user trajectory model.** Should the trajectory be linear, monotone-isotonic, or unconstrained? Strong priors weakly held; defer to pilot.
- **Handling of users who pass on the profile reveal (per `onboarding.md`).** No design difference for measurement, but the analyzer should log this so MVP-2's intervention-engagement modeling can use it.
