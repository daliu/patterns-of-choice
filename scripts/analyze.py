#!/usr/bin/env python3
"""
Minimal analyzer implementing the scoring-spec subset that doesn't require
external statistical libraries.

Implemented here:
- Per-item revealed score from tags via the tag-axis map (§2.1, §2.2)
- Per-session aggregation (§3.1)
- Per-user-per-domain aggregation (§3.2)
- Cost-of-virtue probe break-point scoring (§4) when --probes is supplied
- Card-sort inventory scoring per domain × layer (§5.1) when --card-sort
  is supplied
- Bradley-Terry pairwise inventory scoring (§5.2) via Hunter 2004 MM
  algorithm when --pairwise is supplied
- Combined card-sort + pairwise per §5.3 when both inventory inputs are
  present: stated_score(user, d, layer) = mean(z(card_sort), z(pairwise))
  per-domain standardized within sample
- Primary gap computation (§6) when both --log and inventory data are
  present: z(stated_aspirational) - z(revealed), standardized per-domain
- Bootstrap 95% CIs (§8) on revealed scores, gaps, and the H2 convergent-
  validity correlation, with the pre-committed random seed (20260510)
- H2 convergent validity (pre-registration.md): Pearson r between revealed
  truth-telling and HEXACO-60 honesty-humility, when --hexaco is supplied,
  with bootstrap 95% CI
- H4 informant convergent validity (pre-registration.md): same correlation
  but with averaged informant ratings instead of self-report; when
  --informant-hexaco is supplied
- H6 stated-revealed correlation range check (pre-registration.md):
  per-user (stated_aspirational, revealed) Pearson r should fall in
  [0.20, 0.60]; computed from the existing gap pipeline when both
  --log and inventory inputs are present
- H7 Big-5 neuroticism discriminant (pre-registration.md): Pearson r
  between revealed truth-telling and Big-5 neuroticism should be ≤ 0.40
  (an inverted threshold — measuring discriminant validity not
  convergent); when --big5 is supplied
- H3 revealed test-retest (pre-registration.md, primary): per-domain
  Pearson r between weeks 1-2 and weeks 3-4 revealed scores should be
  ≥ 0.60 (lower 95% CI). When --log-window-b is supplied alongside
  the primary --log.
- H5 cost-of-virtue probe test-retest (pre-registration.md,
  secondary): per-domain r ≥ 0.50 between the two windows of probe
  break-points. When --probes-window-b is supplied.
- H9a/H9b/H9c self-prediction calibration (§14 of scoring.md, 9th
  pre-reg hypothesis, DECISIONS §19). When --predictions is supplied
  (and --predictions-window-b for the H9b test-retest split): the
  per-person cal_bias / cal_error indices, H9a self-enhancement
  (mean signed error > 0 over consensual-pole domains), H9b-stability
  (split-window test-retest of cal_error), H9c stakes-blindness (the
  load-bearing signature — self-prediction error larger under high
  stakes), and the cost-of-virtue channel with the §14.1 censoring
  lock. Axis and cost-of-virtue channels are NEVER pooled (§14.7).
  The H9b DISCRIMINANT half (R² of cal_error on [gap, revealed_level])
  is deferred — it couples to the H2-H7 cohort pipeline; see
  build-and-validate.md.
- H10a/H10c cross-situational moral consistency (§15 of scoring.md,
  10th pre-reg branch). When --context-log is supplied (a session log
  whose items carry context:* setting tags): the per-construct
  within-person cross-context SD sd_i(c) and the person-level
  variability index V_i (N=1 reveal-eligible, value-neutral — steadiness
  vs responsiveness, never ranked), H10a trait reliability (split-half
  odd/even sessions, lower CI ≥ 0.40), and H10c the observer-effect
  anchor (public − anonymous > 0, directional). The H10b DISCRIMINANT
  half (V_i regressed on level/gap/cal_error + the residual-variability
  de-confound) is deferred — it couples to the cohort pipeline, like the
  H9b discriminant; see build-and-validate.md. sd_i(c) is never summed
  into a composite (§13.5) and never pooled across the CoV channel.
- H11a/H11c moral-circle radius (§16 of scoring.md, 11th pre-reg branch).
  When --circle-log is supplied (in-group items carrying circle_radius
  hospitality/boundaries tags + counterparty:* distance tags): concern_i(d)
  = mean circle_radius-axis score per distance bin (via the versioned
  counterparty→bin ordering map, --distance-map), and the two within-person
  shape summaries β_i (OLS slope = parochialism steepness) and R_i (the
  radius = first bin where concern crosses the person's midpoint,
  RIGHT-CENSORED and never made finite when concern never declines — the
  distance-axis analog of the cost-of-virtue break point, §13.2). H11a shape
  reliability (β_i split-window odd/even, lower CI ≥ 0.40) and H11c the
  parochial-gradient anchor (near − far concern > 0, directional). The H11b
  DISCRIMINANT half (shape regressed on generosity level + near-bin concern)
  is deferred — cohort-coupled, like H9b/H10b. Value-neutral (§1.5): a wider
  circle is never scored as better; β_i/R_i are reported as facets, never
  summed (§13.5) and never pooled with the primary or CoV channels.
- R2a/R2b sacred / protected values (§17 of scoring.md, 12th pre-reg branch).
  When --protected-log is supplied (cost-of-virtue responses carrying
  value_slot + wave, and a light taboo 0/1 marker): P_i = the SET of
  value_slots a person marks `never` — the right-censored CoV tail (§4,
  §13.2) re-read as their PROFESSED protected set, categorical and never
  finitized into a price. R2a set reliability (protected-set test-retest
  Jaccard across waves, lower CI ≥ 0.40) and R2b protected ≠ EXPENSIVE (the
  load-bearing distinctness: taboo higher on protected than on high-but-finite
  values, lower CI of the contrast > 0, directional). Value-neutral (§17.5):
  a large protected set is integrity OR dogmatism, never ranked; cheap-talk
  caveat — professed, real-stakes validation (H-A2) is Phase-2. R2c
  discriminant (vs importance rank) deferred — cohort-coupled. P_i is a SET +
  a marker, never summed into a sacredness score (§13.5).
- H12a/H12c moral hypocrisy / self–other judgment asymmetry (§18 of
  scoring.md, 13th pre-reg branch). When --hypocrisy-log is supplied (matched
  severity_self + severity_other judgments of the SAME acts): H_i =
  mean(severity_other − severity_self) is the person's self–other asymmetry, a
  paired within-person contrast on a common scale. H12a reliability (split-half
  odd/even correlation of H_i, lower CI ≥ 0.40) and H12c the self-serving anchor
  (mean_i H_i > 0, directional — others judged more harshly than self; Tappin &
  McKay 2017, Epley & Dunning 2000). Value-neutral (§18.4): harsher-on-others and
  harsher-on-self are both described, never ranked. A declined judgment drops the
  pair, never imputed to 0 (the pairing lock). H12b discriminant (vs gap /
  calibration) deferred — cohort-coupled. Signed facet, never summed (§13.5).
- R1a/R1c moral identity centrality (§19 of scoring.md, 14th pre-reg branch). When
  --identity-log is supplied (per-item internalization + symbolization centrality
  responses, Aquino & Reed 2002): the two DISJOINT facets are read SEPARATELY and
  NEVER pooled into one moral-identity score (§13.5, load-bearing here). R1a
  reliability (split-half odd/even correlation of the internalization facet, lower
  CI ≥ 0.40) and R1c the internalization > symbolization anchor (mean_i of the
  within-scale delta > 0, directional — the private dimension endorsed more than the
  public). Value-neutral (§19.4): high centrality is not scored as better than low
  (integrity OR rigid self-righteousness), and internalizing is not ranked above
  symbolizing. A declined item drops, never imputed; a facet below the item floor is
  suppressed. R1b — whether centrality MODERATES the §6 gap / H10–H12 — deferred,
  cohort-coupled (like the H9b/H10b/H11b/R2c discriminant halves).
- R6a/R6d moral conviction / metaethical objectivism (§20 of scoring.md, 15th pre-reg
  branch). When --objectivism-log is supplied (per-item objectivism ratings across
  moral + taste claim types, Goodwin & Darley 2008): the STATED objectivism probe is
  read as a standalone quantity and NEVER pooled with the (deferred, κ-gated) REVEALED
  tolerance/compromise/language signatures (§13.5, load-bearing here). R6a reliability
  (split-half odd/even correlation of the moral read, lower CI ≥ 0.50 — the higher bar)
  and R6d the moral > taste anchor (mean_i of the within-scale delta > 0, directional —
  moral claims treated as more fact-like than tastes). Value-neutral with EXTRA FORCE
  (§20.4): holding morals as objective facts is not ranked above holding them as your
  own (moral clarity OR rigid intolerance; each pole dual-read). A declined item drops,
  never imputed; a read below the item floor is suppressed. R6b (discriminant) and R6c
  (the stated–revealed meta-gap) deferred — cohort-coupled / κ-gated.

Reserved for the future validation-cohort analyzer:
- CFA on item-level loadings (§7 of scoring.md, H1 of pre-reg) —
  legitimately needs lavaan or statsmodels.sem; not implementable
  with stdlib-only constraint
- Per-domain probe aggregation as a CFA indicator (§7)
- Longitudinal cost-of-virtue probe trajectories (§4.3) — needs
  > 2 time windows of probe data
- H8a / H8b narrative-immersion divergence + attachment (§9 of
  scoring.md, 8th pre-reg hypothesis). The statistics themselves
  (two Pearson correlations with bootstrap CIs) are stdlib-tractable
  and would reuse the _domain_test_retest_r / bootstrap_ci machinery
  below. It is reserved NOT for a library reason but because it still
  has unresolved INPUT preconditions that are design decisions, not code:
  (a) RESOLVED — scenarios/h8-probe-pairs.json now declares 9 paired
      probes (plus 5 recurring-character arcs in scenarios/arcs/), so
      there is content to compute on;
  (b) how a narrative resolves to one scalar r_narr — terminal-based
      vs path-based — is the open question in scoring.md §11 and must
      be resolved before the divergence score is well-defined;
  (c) the H8a sign convention is flagged in scoring.md §9.2 as
      reconcile-before-OSF-lock.
  With (b)-(c) settled this is a natural next analyzer addition with a
  check_analyzer_thresholds gate alongside H2-H7.

Usage:
    python scripts/analyze.py --log analysis/fixtures/sample-session-log.json
    python scripts/analyze.py --log <path> --probes <path>     # + probes
    python scripts/analyze.py --log <path> --card-sort <path>  # + card-sort
    python scripts/analyze.py --log <path> --tag-map <path>
    python scripts/analyze.py --log <path> --json              # JSON output

Inputs:
- The session log is a JSON file: array of SessionLogEntry per types.ts.
- The probes file is a JSON file: array of ProbeResponse per types.ts.
- The card-sort file is a compact format: array of
    { user_id, layer, selected_value_ids[] }
  Production CardSortResponse data (one entry per value) is also accepted.
- The tag-axis map is `analysis/tag_axis_map_v*.csv` (defaults to v0.1).
"""

import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Pre-committed random seed per scoring.md §8. Lock this before OSF filing.
BOOTSTRAP_SEED = 20260510
BOOTSTRAP_N = 10000
BOOTSTRAP_CI = 0.95

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TAG_MAP = REPO_ROOT / "analysis" / "tag_axis_map_v0.1.csv"
DEFAULT_DISTANCE_MAP = REPO_ROOT / "analysis" / "counterparty_distance_map_v0.1.csv"
SCENARIOS_DIR = REPO_ROOT / "scenarios" / "sample"
INVENTORY_DIR = REPO_ROOT / "inventory"


def load_tag_axis_map(path: Path) -> dict[tuple[str, str], tuple[str, float]]:
    """
    Returns dict keyed by (domain, tag) → (axis, contribution).
    Rows with axis == 'metadata' are skipped.
    Rows with domain == '*' are reserved for metadata; not scoring-relevant.
    """
    m: dict[tuple[str, str], tuple[str, float]] = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            axis = row.get("axis", "").strip()
            if axis == "metadata":
                continue
            domain = row.get("domain", "").strip()
            tag = row.get("tag", "").strip()
            contrib_str = row.get("contribution", "").strip()
            if not contrib_str:
                continue
            try:
                contrib = float(contrib_str)
            except ValueError:
                continue
            m[(domain, tag)] = (axis, contrib)
    return m


# Per scoring.md §2.2 the per-item revealed score is computed on the domain's
# PRIMARY axis only. These names match runtime/tag-axis-map.v0.1.json `primary_axis`;
# the cross-impl parity test guards against drift from the on-device projection.
PRIMARY_AXIS = {
    "truth-telling": "honesty",
    "resource-allocation": "generosity",
    "in-group-out-group": "loyalty",
    "reciprocity-cooperation": "trust",
}

# §10: a session×domain whose MEDIAN item response time is below this is dropped
# as inattentive (matches poc-projection.js revealedScores).
INATTENTIVE_RT_MS = 2000


def _median(xs: list[float]) -> float:
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return float("nan")
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def item_score(entry: dict, tag_map: dict[tuple[str, str], tuple[str, float]]) -> tuple[float, int]:
    """
    Sum scoring contributions for the entry's tags **on the domain's primary
    axis** (scoring.md §2.2); clamped to [-1, +1]. Tags on a secondary axis
    (e.g. in-group's circle_radius) are excluded, exactly as the on-device
    projection does — so the two implementations agree on the revealed score.

    Returns (score, contributing_tag_count). If no tag contributes, returns
    (0.0, 0); the caller treats this as NA-for-score-purposes.
    """
    domain = entry.get("domain", "")
    primary = PRIMARY_AXIS.get(domain)
    total = 0.0
    n = 0
    for tag in entry.get("tags", []):
        hit = tag_map.get((domain, tag))
        if hit and hit[0] == primary:
            total += hit[1]
            n += 1
    return (max(-1.0, min(1.0, total)), n)


def session_aggregates(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[tuple[str, str, str], list[float]]:
    """
    Group per-item scores by (user_id, session_id, domain). Returns raw lists of
    scores; caller can compute mean / variance / count.

    Items where no tag matched the domain's primary axis are excluded. A whole
    session×domain group is dropped when its MEDIAN item response time is below
    INATTENTIVE_RT_MS (§10), matching poc-projection.js. The gate fails open when
    response times are absent/non-numeric (e.g. synthetic fixtures), like the
    projection's NaN-median behavior.
    """
    raw: dict[tuple[str, str, str], dict[str, list]] = defaultdict(lambda: {"scores": [], "rts": []})
    for entry in entries:
        score, n = item_score(entry, tag_map)
        if n == 0:
            continue
        key = (entry["user_id"], entry["session_id"], entry["domain"])
        raw[key]["scores"].append(score)
        raw[key]["rts"].append(entry.get("response_time_ms"))
    grouped: dict[tuple[str, str, str], list[float]] = {}
    for key, g in raw.items():
        rts = g["rts"]
        if all(isinstance(r, (int, float)) for r in rts) and _median(rts) < INATTENTIVE_RT_MS:
            continue  # §10 inattentive drop
        grouped[key] = g["scores"]
    return grouped


def session_means(
    grouped: dict[tuple[str, str, str], list[float]],
    min_items_per_session: int = 3,
) -> dict[tuple[str, str, str], float]:
    """Per scoring.md §3.1: session score = mean of item scores in session×domain."""
    return {
        k: sum(v) / len(v)
        for k, v in grouped.items()
        if len(v) >= min_items_per_session
    }


def _bootstrap_ci_mean(
    values: list[float],
    rng: random.Random,
    n_iter: int = BOOTSTRAP_N,
    ci: float = BOOTSTRAP_CI,
) -> tuple[float, float]:
    """
    Non-parametric bootstrap CI for the mean. Returns (lower, upper) per
    the percentile method per scoring.md §8. Random sample with replacement;
    deterministic per the pre-committed seed in the caller.

    Degenerate cases:
    - n=1: CI undefined; return (nan, nan)
    - n<1: same
    """
    n = len(values)
    if n < 2:
        return (float("nan"), float("nan"))

    means = []
    for _ in range(n_iter):
        sample = [rng.choice(values) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    alpha = (1 - ci) / 2
    lower_idx = int(n_iter * alpha)
    upper_idx = int(n_iter * (1 - alpha))
    return (means[lower_idx], means[min(upper_idx, n_iter - 1)])


def user_domain_means(
    session_score_map: dict[tuple[str, str, str], float],
) -> dict[tuple[str, str], dict[str, Any]]:
    """
    Per scoring.md §3.2: revealed_score(user, d) = mean of session scores.
    Returns dict keyed by (user, domain) → {mean, n_sessions, se, ci_low,
    ci_high}. Bootstrap CI per §8 with pre-committed seed.
    """
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (user, _session, domain), score in session_score_map.items():
        grouped[(user, domain)].append(score)

    # Deterministic RNG keyed by the pre-committed seed
    rng = random.Random(BOOTSTRAP_SEED)

    out: dict[tuple[str, str], dict[str, Any]] = {}
    for key in sorted(grouped.keys()):
        scores = grouped[key]
        n = len(scores)
        mean = sum(scores) / n
        if n > 1:
            var = sum((s - mean) ** 2 for s in scores) / (n - 1)
            se = (var / n) ** 0.5
            ci_low, ci_high = _bootstrap_ci_mean(scores, rng)
        else:
            se = float("nan")
            ci_low = float("nan")
            ci_high = float("nan")
        out[key] = {
            "mean": mean,
            "n_sessions": n,
            "se": se,
            "ci_low": ci_low,
            "ci_high": ci_high,
        }
    return out


def render_table(scores: dict[tuple[str, str], dict[str, Any]]) -> str:
    """Tabular text output for human inspection."""
    rows = sorted(scores.items())
    if not rows:
        return "(no scores computed)"

    header = (
        f"{'user_id':<24} {'domain':<26} {'mean':>7} {'sess':>5} "
        f"{'95% CI':>16}"
    )
    out = [header, "-" * len(header)]
    for (user, domain), s in rows:
        mean = f"{s['mean']:+.3f}"
        if s["ci_low"] != s["ci_low"]:
            ci_str = "         nan"
        else:
            ci_str = f"[{s['ci_low']:+.2f}, {s['ci_high']:+.2f}]"
        out.append(
            f"{user:<24} {domain:<26} {mean:>7} {s['n_sessions']:>5} {ci_str:>16}"
        )
    return "\n".join(out)


def load_probe_inversion_map() -> dict[str, bool]:
    """
    Read each cov-*.json scenario; return {probe_id: is_inverted} where
    is_inverted is True iff break_point_field == 'first_return_stake'.
    """
    out: dict[str, bool] = {}
    for path in sorted(SCENARIOS_DIR.glob("cov-*.json")):
        try:
            with path.open() as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        analysis = data.get("analysis") or {}
        out[data["id"]] = analysis.get("break_point_field") == "first_return_stake"
    return out


def load_probe_ceiling_map() -> dict[str, float]:
    """
    Read each cov-*.json; return {probe_id: log10(max ladder-rung stake)} — each
    probe's OWN ceiling, used to anchor the out-of-range "never"/"always" pole.

    Replaces a previously-hardcoded $10K ceiling that collapsed a refusal on a
    high-ceiling probe (e.g. cov-ingroup-002's $100K ladder — a stronger virtue
    signal) to the same score as a refusal on a $10K probe.
    """
    out: dict[str, float] = {}
    for path in sorted(SCENARIOS_DIR.glob("cov-*.json")):
        try:
            with path.open() as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        stakes = [
            r.get("stake")
            for r in (data.get("ladder") or [])
            if isinstance(r.get("stake"), (int, float)) and r.get("stake") > 0
        ]
        if stakes:
            out[data["id"]] = math.log10(max(stakes))
    return out


def probe_break_point_score(
    response: dict,
    inversion_map: dict[str, bool],
    ceiling_map: dict[str, float] | None = None,
) -> tuple[float, bool] | None:
    """
    Compute log10 of the break-point per scoring.md §4. Returns (score, inverted)
    or None if the response can't be scored.

    For forward probes (e.g. cov-truth-001):
      - first_accept_stake numeric → log10(stake)
      - "never" → log10(max ladder rung) + 1 (per spec §4.1)
    For inverted probes (e.g. cov-allocation-001 — ladder asks at what stake
    the user does the ETHICAL action, so smaller break-point = stronger virtue):
      - first_return_stake numeric → -log10(stake) (sign-flipped at aggregation)
      - "always_return" (rung 0 conceptually) → 0 ethical-pole anchor
      - "always_keep" / never returns → -log10(max ladder rung) - 1
    """
    # The app/runtime emit 'scenario_id'; older fixtures/synthetic data use
    # 'probe_id'. Accept either as the probe identifier.
    probe_id = response.get("probe_id") or response.get("scenario_id")
    if not probe_id:
        return None
    inverted = inversion_map.get(probe_id, response.get("is_inverted", False))
    stake = response.get("first_accept_stake")
    rung = response.get("first_accept_rung")

    # Per-probe ladder ceiling = log10 of the probe's OWN top rung (so a refusal on a
    # $100K probe scores above a refusal on a $10K one). Falls back to $10K only when
    # the probe definition is unavailable. Fixes the prior hardcoded 4.0.
    ladder_ceil_log10 = (ceiling_map or {}).get(probe_id, 4.0)

    # Refusal pole: the app writes the boolean 'no_break_point'; fixtures use the
    # sentinel rung == "never". Either means "wouldn't, at any stake in range".
    if response.get("no_break_point") is True or rung == "never":
        # refused at all rungs → one decade above the probe's own ceiling (spec §4.1)
        if inverted:
            return (-ladder_ceil_log10 - 1.0, True)  # would never do the ethical thing
        return (ladder_ceil_log10 + 1.0, False)  # would never do the unethical thing

    if isinstance(stake, (int, float)) and stake > 0:
        log_score = math.log10(stake)
        if inverted:
            # Smaller stake = stronger virtue; sign-flip so higher = more virtuous
            return (-log_score, True)
        return (log_score, False)

    if isinstance(stake, (int, float)) and stake == 0:
        # Forgiveness-style probe rung 1 ($0 additional restitution = strongest forgiveness)
        if inverted:
            return (0.0, True)  # strongest ethical pole
        return (0.0, False)

    return None


def probe_scores_by_user_domain(
    responses: list[dict],
    inversion_map: dict[str, bool],
    ceiling_map: dict[str, float] | None = None,
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """
    Per-user per-domain bucketing. Each item in the list is one probe response
    with its computed score and metadata for downstream aggregation or display.
    """
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in responses:
        score = probe_break_point_score(r, inversion_map, ceiling_map)
        if score is None:
            continue
        log_score, inverted = score
        grouped[(r["user_id"], r["domain"])].append({
            "probe_id": r.get("probe_id") or r.get("scenario_id"),
            "value_slot": r.get("value_slot"),
            "log_score": log_score,
            "inverted": inverted,
            "first_accept_stake": r.get("first_accept_stake"),
            "first_accept_rung": r.get("first_accept_rung") or r.get("break_point_rung"),
        })
    return grouped


def load_values_deck_domains() -> dict[str, str]:
    """Return {value_id: domain} from inventory/values-deck.json."""
    deck_path = INVENTORY_DIR / "values-deck.json"
    with deck_path.open() as f:
        deck = json.load(f)
    return {v["id"]: v["domain"] for v in deck.get("values", [])}


def card_sort_scores(
    responses: list[dict],
    value_domain: dict[str, str],
) -> dict[tuple[str, str, str], float]:
    """
    Per scoring.md §5.1:
        card_sort_stated(user, d, layer) = mean(card_sort_indicator(value)
                                                for value in values_in_domain(d))

    Accepts either the compact fixture format (one entry per user×layer
    with selected_value_ids[]) or production CardSortResponse format
    (one entry per user×layer×value with selected boolean).

    Returns dict keyed by (user_id, domain, layer) → score in [0, 1].
    """
    # Pivot to {(user, layer): set_of_selected_value_ids}
    selected: dict[tuple[str, str], set[str]] = defaultdict(set)
    for r in responses:
        user = r.get("user_id")
        layer = r.get("layer")
        if not user or not layer:
            continue
        if "selected_value_ids" in r:
            for vid in r["selected_value_ids"]:
                selected[(user, layer)].add(vid)
        elif "value_id" in r and r.get("selected") is True:
            selected[(user, layer)].add(r["value_id"])

    # Aggregate per (user, domain, layer)
    out: dict[tuple[str, str, str], float] = {}
    domain_values: dict[str, list[str]] = defaultdict(list)
    for vid, dom in value_domain.items():
        domain_values[dom].append(vid)

    for (user, layer), picked in selected.items():
        for domain, vids in domain_values.items():
            if not vids:
                continue
            n_in_domain = sum(1 for v in vids if v in picked)
            out[(user, domain, layer)] = n_in_domain / len(vids)
    return out


def fit_bradley_terry(
    comparisons: list[tuple[str, str]],
    value_pool: list[str],
    max_iter: int = 200,
    tol: float = 1e-6,
) -> dict[str, float]:
    """
    MM algorithm for Bradley-Terry latent utility (Hunter 2004).
    comparisons: list of (winner, loser) tuples
    value_pool: list of value IDs

    Returns dict[value_id, β] where β > 0 is the latent utility.
    Normalization: Σβ = n (number of values).

    Values that never win get β = 0; values not in any comparison stay
    at their initial β = 1.0 (i.e., the prior).

    The MM algorithm guarantees monotone convergence to the maximum-
    likelihood estimate; standard convergence is fast for moderately
    dense comparison sets. For the synthetic fixture (15 pairs over
    20 values), convergence typically in <50 iterations.
    """
    n = len(value_pool)
    idx = {v: i for i, v in enumerate(value_pool)}

    # Count wins
    wins = [0] * n
    for w, l in comparisons:
        if w in idx:
            wins[idx[w]] += 1

    # Pair-comparison count matrix
    pair_count = [[0] * n for _ in range(n)]
    for w, l in comparisons:
        if w in idx and l in idx and w != l:
            i, j = idx[w], idx[l]
            pair_count[i][j] += 1
            pair_count[j][i] += 1

    # Initialize
    beta = [1.0] * n

    for _ in range(max_iter):
        new_beta = [0.0] * n
        for i in range(n):
            if wins[i] == 0:
                new_beta[i] = 0.0
                continue
            denom = 0.0
            for j in range(n):
                if i == j or pair_count[i][j] == 0:
                    continue
                denom += pair_count[i][j] / (beta[i] + beta[j])
            if denom > 0:
                new_beta[i] = wins[i] / denom
            else:
                new_beta[i] = 0.0

        # Normalize Σβ = n
        s = sum(new_beta)
        if s > 0:
            new_beta = [b * n / s for b in new_beta]

        # Convergence check
        diff = max(abs(new_beta[i] - beta[i]) for i in range(n))
        beta = new_beta
        if diff < tol:
            break

    return {value_pool[i]: beta[i] for i in range(n)}


def pairwise_scores(
    responses: list[dict],
    value_domain: dict[str, str],
) -> dict[tuple[str, str, str], float]:
    """
    Per scoring.md §5.2: fit Bradley-Terry per (user, layer) on pairwise
    comparisons; aggregate per-domain via mean of β across in-domain values.

    Accepts compact fixture format ({user_id, layer, choices: [[w, l]...]}).

    Returns dict[(user_id, domain, layer)] → per-domain mean β.
    """
    out: dict[tuple[str, str, str], float] = {}
    value_pool = sorted(value_domain.keys())

    # Group choices per (user, layer)
    by_user_layer: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for r in responses:
        user = r.get("user_id")
        layer = r.get("layer")
        if not user or not layer:
            continue
        for pair in r.get("choices", []):
            if isinstance(pair, list) and len(pair) == 2:
                by_user_layer[(user, layer)].append((pair[0], pair[1]))

    for (user, layer), comparisons in by_user_layer.items():
        if not comparisons:
            continue
        betas = fit_bradley_terry(comparisons, value_pool)

        # Aggregate per-domain
        domain_betas: dict[str, list[float]] = defaultdict(list)
        for vid, beta in betas.items():
            domain = value_domain.get(vid)
            if domain:
                domain_betas[domain].append(beta)
        for domain, beta_list in domain_betas.items():
            out[(user, domain, layer)] = sum(beta_list) / len(beta_list)
    return out


def render_pairwise_table(scores: dict[tuple[str, str, str], float]) -> str:
    rows = sorted(scores.items())
    if not rows:
        return "(no pairwise responses)"
    header = (
        f"{'user_id':<24} {'domain':<26} {'layer':<20} "
        f"{'mean_beta':>10}"
    )
    out = [header, "-" * len(header)]
    for (user, domain, layer), beta in rows:
        out.append(f"{user:<24} {domain:<26} {layer:<20} {beta:>10.3f}")
    return "\n".join(out)


def render_card_sort_table(scores: dict[tuple[str, str, str], float]) -> str:
    """One row per (user, domain, layer)."""
    rows = sorted(scores.items())
    if not rows:
        return "(no card-sort responses)"
    header = f"{'user_id':<24} {'domain':<26} {'layer':<20} {'frac_in_top5':>12}"
    out = [header, "-" * len(header)]
    for (user, domain, layer), score in rows:
        out.append(f"{user:<24} {domain:<26} {layer:<20} {score:>12.3f}")
    return "\n".join(out)


def _standardize_per_domain(
    domain_user_values: dict[str, list[tuple[str, float]]],
) -> dict[tuple[str, str], float]:
    """
    Per-domain sample z-score: for each domain, compute mean and SD across
    users, then z-score each user's value. Returns {(user, domain): z}.
    Degenerate samples (< 2 users) are skipped (no z-score computable).
    """
    out: dict[tuple[str, str], float] = {}
    for domain, user_values in domain_user_values.items():
        if len(user_values) < 2:
            continue
        vals = [v for _, v in user_values]
        n = len(vals)
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / (n - 1)
        sd = var ** 0.5
        if sd == 0:
            continue
        for user, v in user_values:
            out[(user, domain)] = (v - mean) / sd
    return out


def combined_stated_score(
    card_sort: dict[tuple[str, str, str], float],
    pairwise: dict[tuple[str, str, str], float],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    """
    Per scoring.md §5.3: combined stated score is the mean of the within-
    sample standardized card-sort and pairwise scores, per-domain per-layer.

    Standardization is per-(domain, layer) — z-scores computed across users
    who have both scores in that (domain, layer) slice.

    Returns dict[(user, domain, layer)] → {z_card, z_pair, combined, source}.
    source is "combined" when both are present, "card_sort_only" or
    "pairwise_only" when only one is.
    """
    out: dict[tuple[str, str, str], dict[str, Any]] = {}

    # Find (domain, layer) slices with both inputs
    cs_keys = set(card_sort.keys())
    pw_keys = set(pairwise.keys())

    # For each (domain, layer), pull users with both
    by_dom_layer: dict[tuple[str, str], list[tuple[str, float, float]]] = defaultdict(list)
    for (user, domain, layer) in cs_keys & pw_keys:
        by_dom_layer[(domain, layer)].append(
            (user, card_sort[(user, domain, layer)], pairwise[(user, domain, layer)])
        )

    # Standardize per (domain, layer)
    for (domain, layer), rows in by_dom_layer.items():
        if len(rows) < 2:
            continue
        cs_vals = [cs for _, cs, _ in rows]
        pw_vals = [pw for _, _, pw in rows]
        cs_z = _z(cs_vals)
        pw_z = _z(pw_vals)
        if cs_z is None or pw_z is None:
            continue
        for (user, _, _), cz, pz in zip(rows, cs_z, pw_z):
            out[(user, domain, layer)] = {
                "z_card_sort": cz,
                "z_pairwise": pz,
                "combined": (cz + pz) / 2,
                "source": "combined",
            }

    # Users with only one source per (domain, layer): include without combining
    for key in cs_keys - pw_keys:
        out.setdefault(key, {
            "z_card_sort": float("nan"),
            "z_pairwise": float("nan"),
            "combined": card_sort[key],
            "source": "card_sort_only",
        })
    for key in pw_keys - cs_keys:
        out.setdefault(key, {
            "z_card_sort": float("nan"),
            "z_pairwise": float("nan"),
            "combined": pairwise[key],
            "source": "pairwise_only",
        })

    return out


def _z(values: list[float]) -> list[float] | None:
    """Sample z-score helper. Returns None on degenerate samples."""
    if len(values) < 2:
        return None
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    sd = var ** 0.5
    if sd == 0:
        return None
    return [(v - mean) / sd for v in values]


def compute_gaps(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    stated_layer: dict[tuple[str, str], float],
    stated_source: str = "card_sort",
) -> dict[tuple[str, str], dict[str, float]]:
    """
    Primary gap per scoring.md §6:
      gap(user, d) = z(stated_aspirational(user, d)) - z(revealed(user, d))

    Both terms standardized per-domain across users in the sample. Positive
    gap = user aspires higher than their revealed behavior; negative = user
    reveals more virtue than they claim.

    `stated_layer` is the aspirational-layer stated score per (user, domain),
    pre-filtered. `stated_source` is metadata describing which feeder produced
    the stated value ('card_sort', 'pairwise', or 'combined').

    Requires ≥ 2 users per domain to compute a within-domain z-score.
    """
    # Find (user, domain) pairs that have BOTH revealed and stated
    revealed_keys = set(revealed_means.keys())
    stated_keys = set(stated_layer.keys())
    common = sorted(revealed_keys & stated_keys)
    if not common:
        return {}

    # Group by domain for standardization
    revealed_by_domain: dict[str, list[tuple[str, float]]] = defaultdict(list)
    stated_by_domain: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for user, domain in common:
        revealed_by_domain[domain].append((user, revealed_means[(user, domain)]["mean"]))
        stated_by_domain[domain].append((user, stated_layer[(user, domain)]))

    z_revealed = _standardize_per_domain(revealed_by_domain)
    z_stated = _standardize_per_domain(stated_by_domain)

    out: dict[tuple[str, str], dict[str, float]] = {}
    for key in common:
        if key not in z_revealed or key not in z_stated:
            continue
        out[key] = {
            "z_revealed": z_revealed[key],
            "z_stated_aspirational": z_stated[key],
            "gap": z_stated[key] - z_revealed[key],
            "stated_source": stated_source,
        }
    return out


def _pearson_r(xs: list[float], ys: list[float]) -> float | None:
    """Sample Pearson correlation. Returns None on degenerate inputs."""
    n = len(xs)
    if n != len(ys) or n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    var_x = sum((xs[i] - mx) ** 2 for i in range(n))
    var_y = sum((ys[i] - my) ** 2 for i in range(n))
    if var_x == 0 or var_y == 0:
        return None
    return cov / (var_x * var_y) ** 0.5


def _bootstrap_ci_r(
    xs: list[float],
    ys: list[float],
    rng: random.Random,
    n_iter: int = BOOTSTRAP_N,
    ci: float = BOOTSTRAP_CI,
) -> tuple[float, float]:
    """
    Bootstrap CI for Pearson r per scoring.md §8: resample (x, y) pairs
    with replacement, recompute r, percentile method. Pre-registered
    seed in the caller.
    """
    n = len(xs)
    if n < 3:
        return (float("nan"), float("nan"))
    rs: list[float] = []
    for _ in range(n_iter):
        indices = [rng.randrange(n) for _ in range(n)]
        sx = [xs[i] for i in indices]
        sy = [ys[i] for i in indices]
        r = _pearson_r(sx, sy)
        if r is not None:
            rs.append(r)
    if len(rs) < 10:
        return (float("nan"), float("nan"))
    rs.sort()
    alpha = (1 - ci) / 2
    lower_idx = int(len(rs) * alpha)
    upper_idx = int(len(rs) * (1 - alpha))
    return (rs[lower_idx], rs[min(upper_idx, len(rs) - 1)])


def _correlate_revealed_with_external(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    external_by_user: dict[str, float],
    domain: str,
    seed_offset: int,
    threshold_low: float | None = None,
    threshold_high: float | None = None,
) -> dict[str, Any] | None:
    """
    Generic Pearson r computation between revealed score in a domain
    and an external per-user value, with bootstrap CI.

    threshold_low: H is "met" if r CI is ABOVE this (convergent validity)
    threshold_high: H is "met" if r CI is BELOW this (discriminant validity)

    Used for H2/H4 (convergent, threshold_low) and H7 (discriminant,
    threshold_high).
    """
    xs: list[float] = []
    ys: list[float] = []
    for (user, d), s in revealed_means.items():
        if d == domain and user in external_by_user:
            xs.append(s["mean"])
            ys.append(external_by_user[user])

    if len(xs) < 3:
        return None

    r = _pearson_r(xs, ys)
    if r is None:
        return None

    rng = random.Random(BOOTSTRAP_SEED + seed_offset)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)

    threshold_met = None
    if ci_low == ci_low:  # NaN check
        if threshold_low is not None:
            threshold_met = ci_low >= threshold_low
        elif threshold_high is not None and ci_high == ci_high:
            threshold_met = ci_high <= threshold_high

    return {
        "r": r,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n": len(xs),
        "pre_registered_threshold_met": threshold_met,
        "threshold_low": threshold_low,
        "threshold_high": threshold_high,
    }


def compute_h2_convergent_validity(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    hexaco_data: list[dict],
    domain: str = "truth-telling",
) -> dict[str, Any] | None:
    """
    Per pre-registration.md H2: Pearson r between revealed truth-telling
    and HEXACO honesty-humility self-report (total score). Pre-registered
    threshold: lower 95% bootstrap CI ≥ 0.15.

    Note: with synthetic n=3 fixture data, the result is purely
    demonstrative. The validation-cohort analyzer on n≈200 is where the
    pre-registered threshold becomes a meaningful test.
    """
    hex_by_user: dict[str, float] = {}
    for entry in hexaco_data:
        uid = entry.get("user_id")
        h = entry.get("honesty_humility", {})
        if uid and isinstance(h, dict) and "total" in h:
            hex_by_user[uid] = float(h["total"])
    return _correlate_revealed_with_external(
        revealed_means, hex_by_user, domain, seed_offset=1, threshold_low=0.15
    )


def compute_h6_stated_revealed_correlation(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    stated_aspirational: dict[tuple[str, str], float],
    domain: str = "truth-telling",
) -> dict[str, Any] | None:
    """
    Per pre-registration.md H6: stated-revealed correlation should fall
    in [0.20, 0.60]. Too high collapses the gap signal; too low suggests
    measurement noise. Range check, not a single-threshold test.

    Uses Pearson r between revealed score and aspirational stated score
    across users in the specified domain.
    """
    xs: list[float] = []
    ys: list[float] = []
    for (user, d), s in revealed_means.items():
        if d != domain:
            continue
        if (user, d) in stated_aspirational:
            xs.append(s["mean"])
            ys.append(stated_aspirational[(user, d)])

    if len(xs) < 3:
        return None

    r = _pearson_r(xs, ys)
    if r is None:
        return None

    rng = random.Random(BOOTSTRAP_SEED + 3)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)

    in_range = None
    if r is not None:
        in_range = 0.20 <= r <= 0.60

    return {
        "r": r,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n": len(xs),
        "in_pre_registered_range": in_range,
        "range_low": 0.20,
        "range_high": 0.60,
    }


def compute_h7_discriminant_validity(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    big5_data: list[dict],
    domain: str = "truth-telling",
) -> dict[str, Any] | None:
    """
    Per pre-registration.md H7: Pearson r between revealed truth-telling
    and Big-5 neuroticism should be ≤ 0.40 (discriminant). If too high,
    the revealed measure is partly measuring neuroticism rather than
    honesty-as-construct.
    """
    n_by_user: dict[str, float] = {}
    for entry in big5_data:
        uid = entry.get("user_id")
        if uid and "neuroticism" in entry:
            n_by_user[uid] = float(entry["neuroticism"])
    return _correlate_revealed_with_external(
        revealed_means, n_by_user, domain, seed_offset=4, threshold_high=0.40
    )


def _domain_test_retest_r(
    window_a: dict[tuple[str, str], float],
    window_b: dict[tuple[str, str], float],
    seed_offset: int,
    threshold: float,
) -> dict[str, dict[str, Any]]:
    """
    Per-domain Pearson r between two windows of the same user score.
    Returns dict {domain: {r, ci_low, ci_high, n, threshold_met}}.
    Domains with < 3 users present in both windows are skipped.

    Used by H3 (revealed scores) and H5 (probe break-points).
    """
    # Group per domain
    domains: set[str] = set()
    for (_, d) in window_a:
        domains.add(d)
    for (_, d) in window_b:
        domains.add(d)

    out: dict[str, dict[str, Any]] = {}
    for i, domain in enumerate(sorted(domains)):
        xs: list[float] = []
        ys: list[float] = []
        for (user, d), va in window_a.items():
            if d != domain:
                continue
            vb = window_b.get((user, d))
            if vb is None:
                continue
            xs.append(va)
            ys.append(vb)

        if len(xs) < 3:
            continue
        r = _pearson_r(xs, ys)
        if r is None:
            continue

        rng = random.Random(BOOTSTRAP_SEED + seed_offset + i)
        ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
        threshold_met = ci_low >= threshold if ci_low == ci_low else None
        out[domain] = {
            "r": r,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "n": len(xs),
            "pre_registered_threshold_met": threshold_met,
            "threshold": threshold,
        }
    return out


def compute_h3_test_retest_revealed(
    revealed_a: dict[tuple[str, str], dict[str, Any]],
    revealed_b: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Per pre-registration.md H3 (primary): per-domain test-retest reliability
    r ≥ 0.60 between weeks 1-2 and weeks 3-4 revealed scores.

    Threshold check is CI-based (lower 95% bootstrap CI ≥ 0.60) to match
    H2's conservative form for a primary hypothesis. With n=3 fixture users
    the CI is volatile; n≈200 cohort is where the test is real.
    """
    a = {k: s["mean"] for k, s in revealed_a.items()}
    b = {k: s["mean"] for k, s in revealed_b.items()}
    return _domain_test_retest_r(a, b, seed_offset=5, threshold=0.60)


def compute_h5_test_retest_probes(
    probes_a: dict[tuple[str, str], list[dict[str, Any]]],
    probes_b: dict[tuple[str, str], list[dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    """
    Per pre-registration.md H5 (secondary): per-domain test-retest
    reliability of cost-of-virtue probe break-points, r ≥ 0.50 between
    weeks 1-2 and weeks 3-4. Per (user, domain), aggregate is the mean
    log_score across that user's probes in that domain.
    """
    def mean_log(by_ud: dict[tuple[str, str], list[dict[str, Any]]]) -> dict[tuple[str, str], float]:
        out: dict[tuple[str, str], float] = {}
        for k, probes in by_ud.items():
            ls = [p["log_score"] for p in probes if isinstance(p.get("log_score"), (int, float))]
            if ls:
                out[k] = sum(ls) / len(ls)
        return out
    return _domain_test_retest_r(
        mean_log(probes_a), mean_log(probes_b), seed_offset=6, threshold=0.50
    )


def compute_h4_informant_validity(
    revealed_means: dict[tuple[str, str], dict[str, Any]],
    informant_data: list[dict],
    domain: str = "truth-telling",
) -> dict[str, Any] | None:
    """
    Per pre-registration.md H4: Pearson r between revealed truth-telling
    and averaged informant HEXACO honesty-humility ratings. Secondary
    hypothesis; pre-registered threshold (effect-size point estimate)
    r ≥ 0.20. Reported with effect size + 95% CI rather than NHST.

    Informant ratings are averaged across informants per subject before
    correlation. Subjects with < 2 informants are still included (per
    pilot-protocol.md "at least one informant" partial-data tolerance).
    """
    # Group informant H by subject_user_id; average across multiple informants
    informant_h: dict[str, list[float]] = defaultdict(list)
    for entry in informant_data:
        uid = entry.get("subject_user_id")
        h = entry.get("honesty_humility", {})
        if uid and isinstance(h, dict) and "total" in h:
            informant_h[uid].append(float(h["total"]))
    averaged = {uid: sum(vs) / len(vs) for uid, vs in informant_h.items()}
    return _correlate_revealed_with_external(
        revealed_means, averaged, domain, seed_offset=2, threshold_low=0.20
    )


# ---------------------------------------------------------------------------
# H9 — self-prediction calibration (scoring.md §14; h9-self-calibration.md;
# DECISIONS §19). Measures how well a participant predicts their own revealed
# choices. Introduces NO new scale: predictions resolve on the same primary
# axis (§2.2, via item_score) and the same cost-of-virtue ladder (§4) as the
# choices they forecast. Two channels, NEVER pooled (§14.7): the axis channel
# (axis units) and the cost-of-virtue channel (log10-dollar units).
# ---------------------------------------------------------------------------

# Domains with a consensual desirable pole (§14.3). The in-group axis
# (loyalty +, universalism −) is value-contested and excluded from the signed
# H9a test (entered exploratory only; h9-self-calibration.md §1.1, §6 Q5).
H9_CONSENSUAL_DOMAINS = {"truth-telling", "resource-allocation", "reciprocity-cooperation"}

# Per-participant inclusion minima (§14.6).
H9A_MIN_PROBES = 3   # ≥3 valid consensual-domain probes to enter H9a
H9B_MIN_PROBES = 2   # cal_error computable in each window (≥2 valid probes)

# Pre-registered thresholds (scoring.md §14.3–§14.5). PROPOSED — lock at OSF
# filing (DECISIONS §19); the analyzer reports met/not-met, never gates on H9.
H9A_BIAS_FLOOR = 0.10   # lower 95% CI of mean cal_bias ≥ this (axis units)
H9B_STABILITY_FLOOR = 0.40  # lower 95% CI of test-retest r of cal_error ≥ this
# H9c is directional: lower 95% CI of mean blind > 0 (no magnitude floor).


def load_predictions(path: Path) -> list[dict]:
    """
    Load a predictions fixture. Accepts either a bare JSON array of prediction
    records or an object with a top-level "predictions" array (the fixture form,
    which also carries a documenting _comment/expected). Each record is a
    RESOLVED calibration pair (the prediction beat joined to its realized choice
    — in production the join is on probe_id between the prediction event log,
    types.ts PredictionLogEntry, and the choice log; the fixtures pre-resolve it
    so the §14 math is testable in isolation).
    """
    with path.open() as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("predictions", [])
    return data if isinstance(data, list) else []


def calibration_axis_records(
    predictions: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> list[dict[str, Any]]:
    """
    Axis channel (§14.1). For each channel=='axis' prediction, score the
    predicted option and the realized choice on the domain's primary axis with
    the SAME item_score used everywhere else (so pred and rev share a scale and
    the parity-locked scoring applies identically):

        pred = item_score(predicted_tags)   rev = item_score(realized_tags)
        e    = pred - rev                    # signed; e>0 = predicted more virtuous

    A record is admitted only when BOTH the prediction and the choice contribute
    ≥1 tag on the primary axis (else the item is NA-for-score-purposes, §2.2).
    Returns a flat list of {user_id, domain, stakes_pool, pred, rev, e}.
    """
    out: list[dict[str, Any]] = []
    for p in predictions:
        if p.get("channel") != "axis":
            continue
        domain = p.get("domain", "")
        pred_score, pn = item_score({"domain": domain, "tags": p.get("predicted_tags", [])}, tag_map)
        rev_score, rn = item_score({"domain": domain, "tags": p.get("realized_tags", [])}, tag_map)
        if pn == 0 or rn == 0:
            continue  # NA — a channel with no primary-axis contribution
        out.append({
            "user_id": p.get("user_id"),
            "domain": domain,
            "stakes_pool": p.get("stakes_pool"),
            "pred": pred_score,
            "rev": rev_score,
            "e": pred_score - rev_score,
        })
    return out


def calibration_person_indices(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Per-participant reveal-eligible indices (§14.2), over that participant's
    completed axis-channel probes:

        cal_bias  = mean_p e          # signed self-enhancement bias
        cal_error = mean_p |e|        # magnitude; lower = better self-knowledge

    N=1-interpretable (pred and rev share a pre-defined axis — no cross-scale or
    cross-person standardization, contrast the §6 gap), hence eligible for the
    personal reveal without cohort norms. Reported descriptively, never as a
    score-out-of-N and never cross-person-ranked (§14.7).
    """
    by_user: dict[str, list[float]] = defaultdict(list)
    for r in records:
        by_user[r["user_id"]].append(r["e"])
    out: dict[str, dict[str, Any]] = {}
    for user in sorted(by_user):
        es = by_user[user]
        out[user] = {
            "cal_bias": sum(es) / len(es),
            "cal_error": sum(abs(x) for x in es) / len(es),
            "n_probes": len(es),
        }
    return out


def compute_h9a_self_enhancement(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    H9a (§14.3): across participants, mean signed calibration error is positive
    — people predict more value-aligned behavior than they reveal (Epley &
    Dunning 2000). Restricted to the consensual-pole domains. Test statistic:
    lower 95% bootstrap-CI bound of mean_i cal_bias_i ≥ 0.10 (axis units).
    """
    consensual = [r for r in records if r["domain"] in H9_CONSENSUAL_DOMAINS]
    by_user: dict[str, list[float]] = defaultdict(list)
    for r in consensual:
        by_user[r["user_id"]].append(r["e"])
    biases = [
        sum(es) / len(es)
        for es in by_user.values()
        if len(es) >= H9A_MIN_PROBES
    ]
    if len(biases) < 3:
        return None
    mean_bias = sum(biases) / len(biases)
    rng = random.Random(BOOTSTRAP_SEED + 10)
    ci_low, ci_high = _bootstrap_ci_mean(biases, rng)
    met = None if ci_low != ci_low else (ci_low >= H9A_BIAS_FLOOR)
    return {
        "mean_cal_bias": mean_bias,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n_participants": len(biases),
        "threshold_low": H9A_BIAS_FLOOR,
        "pre_registered_threshold_met": met,
    }


def compute_h9b_stability(
    records_a: list[dict[str, Any]],
    records_b: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """
    H9b, stability half (§14.4): split-window test-retest of cal_error_i
    (first-half vs second-half sessions). Lower 95% CI ≥ 0.40 (deliberately
    below H3's 0.60 — a second-order derived quantity is noisier).

    NOTE — the discriminant half of H9b (regress cal_error on [gap,
    revealed_level], R² upper CI < 0.50) is DEFERRED to the next increment: it
    couples calibration to the H2–H7 cohort pipeline (per-user gap + revealed
    level), whereas this increment keeps H9 isolated on its own fixtures. See
    build-and-validate.md.
    """
    def err_by_user(records: list[dict[str, Any]]) -> dict[str, float]:
        by_user: dict[str, list[float]] = defaultdict(list)
        for r in records:
            by_user[r["user_id"]].append(abs(r["e"]))
        return {
            u: sum(es) / len(es)
            for u, es in by_user.items()
            if len(es) >= H9B_MIN_PROBES
        }

    ea, eb = err_by_user(records_a), err_by_user(records_b)
    shared = sorted(set(ea) & set(eb))
    if len(shared) < 3:
        return None
    xs = [ea[u] for u in shared]
    ys = [eb[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 11)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else (ci_low >= H9B_STABILITY_FLOOR)
    return {
        "r": r,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n": len(shared),
        "threshold_low": H9B_STABILITY_FLOOR,
        "pre_registered_threshold_met": met,
    }


def compute_h9c_stakes_blindness(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    H9c (§14.5), the load-bearing one: self-prediction error is LARGER on
    high-stakes probes than low-stakes probes — the behavioral fingerprint of
    the hot–cold projection gap (Loewenstein) / EV-4 stakes discontinuity.

        blind_i = mean|e| over the H8b high-stakes pool
                - mean|e| over the H8a low-stakes pool

    Axis channel only (unit consistency; the cost-of-virtue break-point
    calibration is a SEPARATE convergent read in price units, never pooled —
    §14.5, §14.7). A participant enters with ≥1 valid error in EACH pool. Test:
    lower 95% bootstrap-CI bound of mean_i blind_i > 0 (one-sided, directional).
    """
    low_by_user: dict[str, list[float]] = defaultdict(list)
    high_by_user: dict[str, list[float]] = defaultdict(list)
    for r in records:
        if r["stakes_pool"] == "low":
            low_by_user[r["user_id"]].append(abs(r["e"]))
        elif r["stakes_pool"] == "high":
            high_by_user[r["user_id"]].append(abs(r["e"]))
    blinds = []
    for user in set(low_by_user) & set(high_by_user):
        lo = low_by_user[user]
        hi = high_by_user[user]
        blinds.append(sum(hi) / len(hi) - sum(lo) / len(lo))
    if len(blinds) < 3:
        return None
    mean_blind = sum(blinds) / len(blinds)
    rng = random.Random(BOOTSTRAP_SEED + 12)
    ci_low, ci_high = _bootstrap_ci_mean(blinds, rng)
    met = None if ci_low != ci_low else (ci_low > 0.0)
    return {
        "mean_blind": mean_blind,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n_participants": len(blinds),
        "threshold": 0.0,
        "pre_registered_threshold_met": met,
    }


def calibration_cov_records(predictions: list[dict]) -> dict[str, Any]:
    """
    Cost-of-virtue channel (§14.1), price units — reported convergently with
    H9c, NEVER pooled into the axis-channel blind_i (mixing axis and log-dollar
    units would manufacture a pseudo-quantity, §13.5/§14.7).

        pred_price = log10(predicted_break_stake)   (negated if inverted, §4.2)
        rev_price  = log10(first_accept_stake)       (same flip)
        e_price    = pred_price - rev_price

    CENSORING LOCK (§14.1, inherited from §13.2/§13.3, load-bearing). If EITHER
    endpoint is 'never' (right-censored, price > ladder top), e_price is
    SUPPRESSED — never made finite. The pair is reported only categorically.
    This is the H9 analog of the |8.0| ceiling lock: 'never' stays 'never',
    it is never priced.
    """
    finite: list[dict[str, Any]] = []
    censored: list[dict[str, Any]] = []
    cat_counts: dict[str, int] = defaultdict(int)

    def price(rung: str, inverted: bool) -> float:
        p = math.log10(float(rung))
        return -p if inverted else p

    for p in predictions:
        if p.get("channel") != "cov":
            continue
        pred_rung = str(p.get("predicted_rung"))
        rev_rung = str(p.get("realized_rung"))
        inverted = bool(p.get("inverted", False))
        pred_never = pred_rung.lower() == "never"
        rev_never = rev_rung.lower() == "never"
        if pred_never or rev_never:
            if pred_never and rev_never:
                category = "both-never"
            elif pred_never:
                category = "predicted-never & acted-finite"
            else:
                category = "predicted-finite & acted-never"
            cat_counts[category] += 1
            censored.append({
                "user_id": p.get("user_id"),
                "domain": p.get("domain"),
                "category": category,
            })
            continue
        pred_price = price(pred_rung, inverted)
        rev_price = price(rev_rung, inverted)
        finite.append({
            "user_id": p.get("user_id"),
            "domain": p.get("domain"),
            "pred_price": pred_price,
            "rev_price": rev_price,
            "e_price": pred_price - rev_price,
        })
    finite_abs = [abs(f["e_price"]) for f in finite]
    return {
        "finite": finite,
        "censored": censored,
        "n_finite": len(finite),
        "n_censored": len(censored),
        "censored_categories": dict(cat_counts),
        "finite_mean_abs_e_price": (sum(finite_abs) / len(finite_abs)) if finite_abs else None,
    }


# ----------------------------------------------------------------------------
# H10 — cross-situational moral consistency (scoring.md §15, h10-cross-
# situational-consistency.md). Within-person variability of the revealed axis
# score ACROSS surface contexts, treated as a stable individual-difference trait
# (Fleeson density-distribution; Mischel; Doris situationism). Value-neutral per
# Dancy: low variability = "steadiness", high = "responsiveness" — never ranked.
# N=1: sd_i(c) is a within-person quantity on the fixed primary axis, so it is
# reveal-eligible for a single user without cohort standardization. V_i is the
# mean of per-construct SDs reported ALONGSIDE the facets (§13.5) — never summed
# into a composite index, and never pooled across the CoV channel.
# ----------------------------------------------------------------------------

H10_CONTEXT_PREFIX = "context:"
H10_ITEMS_PER_CONTEXT_MIN = 2   # ≥2 informative items per context (§1.5 suppression)
H10_CONTEXT_MIN = 3             # ≥3 distinct qualifying contexts for a construct's sd (§1.5)
H10_CONSTRUCT_MIN = 3           # ≥3 qualifying constructs before V_i is formed (§1.5)
H10A_RELIABILITY_FLOOR = 0.40   # split-half reliability lower 95% CI (§1.2; Fleeson & Gallagher 2009)
# H10c is directional: lower 95% CI of the mean observer-effect gap > 0 (§1.4).
H10_OBSERVED_CONTEXTS = {"public", "observed"}      # observed pole (§1.4)
H10_ANONYMOUS_CONTEXTS = {"anonymous"}              # anonymous pole (§1.4)


def _context_of(entry: dict) -> str | None:
    """The surface-context setting from an entry's `context:*` tag (§1.1), e.g.
    'workplace' / 'anonymous'. None if the item carries no context tag — such
    items are invisible to H10 (they still score normally for every other
    hypothesis; context:* is a metadata-axis stratifier, ignored by item_score)."""
    for tag in entry.get("tags", []):
        if tag.startswith(H10_CONTEXT_PREFIX):
            return tag[len(H10_CONTEXT_PREFIX):]
    return None


def _sample_sd(xs: list[float]) -> float:
    """Sample (n−1) standard deviation; nan if <2 points (§1.1 sd_i(c))."""
    n = len(xs)
    if n < 2:
        return float("nan")
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def context_item_records(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> list[dict[str, Any]]:
    """Per-item H10 inputs {user, session, domain, context, score}. The score is
    the SAME primary-axis item_score used by the revealed pipeline (§2). Items
    with no primary-axis contribution (n==0) or no context:* tag are dropped. The
    §10 inattentive-session exclusion is applied at (user, session, domain)
    granularity — matching session_aggregates — and fails open when RTs are
    absent/non-numeric (as with synthetic fixtures)."""
    grouped: dict[tuple[str, str, str], dict[str, list]] = defaultdict(
        lambda: {"items": [], "rts": []}
    )
    for entry in entries:
        ctx = _context_of(entry)
        if ctx is None:
            continue
        score, n = item_score(entry, tag_map)
        if n == 0:
            continue
        key = (entry.get("user_id"), entry.get("session_id"), entry.get("domain"))
        grouped[key]["items"].append((ctx, score))
        grouped[key]["rts"].append(entry.get("response_time_ms"))
    records: list[dict[str, Any]] = []
    for (user, session, domain), g in grouped.items():
        rts = [r for r in g["rts"] if isinstance(r, (int, float)) and not isinstance(r, bool)]
        if len(rts) == len(g["rts"]) and rts and _median(rts) < INATTENTIVE_RT_MS:
            continue  # §10 inattentive drop (fails open when any RT is absent/non-numeric)
        for ctx, score in g["items"]:
            records.append({
                "user": user, "session": session, "domain": domain,
                "context": ctx, "score": score,
            })
    return records


def context_sd_by_user_construct(
    records: list[dict[str, Any]],
    session_ok=None,
) -> dict[tuple[str, str], float]:
    """sd_i(c): per (user, domain) cross-context SD of the context-means r_i(c,k)
    (§1.1). A context enters only with ≥H10_ITEMS_PER_CONTEXT_MIN items; a
    construct yields an sd only with ≥H10_CONTEXT_MIN qualifying contexts (§1.5),
    else it is SUPPRESSED (omitted). `session_ok(user, session)` optionally
    restricts to a session subset (the H10a odd/even split)."""
    cell: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for r in records:
        if session_ok is not None and not session_ok(r["user"], r["session"]):
            continue
        cell[(r["user"], r["domain"], r["context"])].append(r["score"])
    ctx_mean: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (user, domain, _ctx), scores in cell.items():
        if len(scores) >= H10_ITEMS_PER_CONTEXT_MIN:
            ctx_mean[(user, domain)].append(sum(scores) / len(scores))
    out: dict[tuple[str, str], float] = {}
    for (user, domain), means in ctx_mean.items():
        if len(means) >= H10_CONTEXT_MIN:
            out[(user, domain)] = _sample_sd(means)
    return out


def variability_index_by_user(
    sd_by_uc: dict[tuple[str, str], float],
) -> dict[str, float]:
    """V_i = mean_c sd_i(c) over a user's qualifying constructs; the user enters
    only with ≥H10_CONSTRUCT_MIN qualifying constructs (§1.5), else V_i is
    suppressed (the per-construct sd_i(c) is still reveal-eligible on its own)."""
    by_user: dict[str, list[float]] = defaultdict(list)
    for (user, _domain), sd in sd_by_uc.items():
        by_user[user].append(sd)
    return {u: sum(v) / len(v) for u, v in by_user.items() if len(v) >= H10_CONSTRUCT_MIN}


def _odd_even_sessions(
    records: list[dict[str, Any]],
) -> tuple[dict[str, set], dict[str, set]]:
    """Split each user's sessions into odd/even halves by sorted session order
    (1-indexed: 1st, 3rd, … = odd; 2nd, 4th, … = even) — §1.2."""
    user_sessions: dict[str, set] = defaultdict(set)
    for r in records:
        user_sessions[r["user"]].add(r["session"])
    odd: dict[str, set] = {}
    even: dict[str, set] = {}
    for user, sess in user_sessions.items():
        ordered = sorted(sess)
        odd[user] = set(ordered[0::2])
        even[user] = set(ordered[1::2])
    return odd, even


def compute_h10a_reliability(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """H10a: split each user's sessions odd/even, recompute V_i on each half,
    correlate across users. Supported iff the lower 95% bootstrap CI of the
    correlation ≥ H10A_RELIABILITY_FLOOR (§1.2). Reliability of the variability
    TRAIT itself — orthogonal to the person's level (that de-confound is H10b,
    deferred). Seed BOOTSTRAP_SEED+13."""
    odd, even = _odd_even_sessions(records)
    v_odd = variability_index_by_user(
        context_sd_by_user_construct(records, lambda u, s: s in odd.get(u, set()))
    )
    v_even = variability_index_by_user(
        context_sd_by_user_construct(records, lambda u, s: s in even.get(u, set()))
    )
    shared = sorted(set(v_odd) & set(v_even))
    if len(shared) < 3:
        return None
    xs = [v_odd[u] for u in shared]
    ys = [v_even[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 13)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else bool(ci_low >= H10A_RELIABILITY_FLOOR)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n": len(shared),
        "threshold_low": H10A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_h10c_observer_effect(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """H10c (observer-effect anchor, directional): per user,
        obs_gap_i = mean(score over observed/public items) − mean(over anonymous items)
    pooled across constructs (§1.4). Supported iff the lower 95% CI of
    mean_i obs_gap_i > 0 (one-sided). A user enters with ≥1 item in each pole.
    Axis scores only; no cross-channel pooling. Seed BOOTSTRAP_SEED+14."""
    pub: dict[str, list[float]] = defaultdict(list)
    anon: dict[str, list[float]] = defaultdict(list)
    for r in records:
        if r["context"] in H10_OBSERVED_CONTEXTS:
            pub[r["user"]].append(r["score"])
        elif r["context"] in H10_ANONYMOUS_CONTEXTS:
            anon[r["user"]].append(r["score"])
    gaps: list[float] = []
    for user in sorted(set(pub) & set(anon)):
        gaps.append(sum(pub[user]) / len(pub[user]) - sum(anon[user]) / len(anon[user]))
    if len(gaps) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 14)
    ci_low, ci_high = _bootstrap_ci_mean(gaps, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_obs_gap": sum(gaps) / len(gaps),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(gaps),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


# ----------------------------------------------------------------------------
# H11 — moral-circle radius (scoring.md §16, h11-moral-circle-radius.md). The
# REACH of concern across recipient social/moral distance, read from the
# `circle_radius` SECONDARY axis (hospitality +1 / boundaries −1, §2.3) binned by
# each item's `counterparty:*` tag through a versioned distance-ordering map (§3
# A1). Two within-person summaries (§1.1): β_i = OLS slope of concern on distance
# (parochialism steepness), and R_i = the distance bin at which concern first
# crosses the person's own midpoint — the DISTANCE-axis analog of the cost-of-
# virtue break point, RIGHT-CENSORED when concern never declines (a wide/flat,
# impartial circle), and — inheriting §13.2 verbatim — NEVER made finite.
# Value-neutral (§1.5, load-bearing): a wider circle is not scored as better
# (Singer's impartialism vs Williams/MacIntyre partialism); the reveal names the
# shape, never ranks it. N=1: β_i/R_i are within-person on the fixed axis +
# ordering, reveal-eligible; reported as facets, never summed into a composite
# (§13.5), never pooled with the primary or cost-of-virtue channels. This scorer
# reads the circle_radius axis SEPARATELY from the primary item_score — the
# parity secondary-axis-exclusion lock (hospitality out of the revealed score)
# still holds, so this increment is Python-only and parity stays green.
# ----------------------------------------------------------------------------

H11_CIRCLE_AXIS = "circle_radius"
H11_COUNTERPARTY_PREFIX = "counterparty:"
H11_ITEMS_PER_BIN_MIN = 2       # ≥2 informative items per distance bin (§1.5 suppression)
H11_BINS_MIN = 4                # ≥4 populated ordered bins before β_i / R_i form (§1.5)
H11A_RELIABILITY_FLOOR = 0.40   # split-window shape reliability lower 95% CI (§1.2)
H11_AXIS_FLOOR = -1.0           # circle_radius axis minimum (boundaries pole) — the R_i midpoint anchor
# H11c is directional: lower 95% CI of the mean near−far concern gradient > 0 (§1.4).


def load_counterparty_distance_map(path: Path) -> tuple[dict[str, int], dict[int, str]]:
    """The versioned counterparty→distance-bin ordering map (§3 A1): a bare
    counterparty tag (e.g. 'close', 'stranger') → ordered bin index (0 = nearest).
    Rows whose bin_index is not an integer are EXCLUDED from the ladder but remain
    documented in the file — the power/role tags (senior/subordinate/business, §6
    Q4, a distance/power confound) and the within-item distance-contrast markers
    (near-vs-far, …, used by H11c). Returns (tag→bin, bin→label). The ordering is
    researcher-imposed (CV-2 smuggled values, §1.5); this is a v0.1 DRAFT whose
    REL-2 inter-rater validation is human-gated (see build-and-validate.md)."""
    m: dict[str, int] = {}
    labels: dict[int, str] = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = (row.get("counterparty_tag") or "").strip()
            bin_str = (row.get("bin_index") or "").strip()
            if not tag:
                continue
            try:
                b = int(bin_str)
            except ValueError:
                continue  # excluded (power/role or contrast marker) — documented, not laddered
            m[tag] = b
            labels[b] = (row.get("bin_label") or "").strip()
    return m, labels


def _circle_axis_score(
    entry: dict, tag_map: dict[tuple[str, str], tuple[str, float]]
) -> tuple[float, int]:
    """Per-item score on the circle_radius SECONDARY axis (hospitality +1 /
    boundaries −1, §2.3); clamped to [-1, +1]. Structurally identical to
    item_score but filtered to the circle_radius axis instead of the domain's
    primary axis — kept SEPARATE so the primary revealed score (and its parity
    lock) is untouched. Returns (score, n_contributing); (0.0, 0) if no
    circle_radius tag contributes (NA-for-H11-purposes)."""
    domain = entry.get("domain", "")
    total = 0.0
    n = 0
    for tag in entry.get("tags", []):
        hit = tag_map.get((domain, tag))
        if hit and hit[0] == H11_CIRCLE_AXIS:
            total += hit[1]
            n += 1
    return (max(-1.0, min(1.0, total)), n)


def _distance_bin_of(entry: dict, dist_map: dict[str, int]) -> int | None:
    """The distance-bin index from an entry's `counterparty:*` tag via the
    ordering map (§1.1). None if the item carries no mapped counterparty tag —
    power/role and contrast-marker counterparties are excluded from the ladder,
    so such items are invisible to the radius (they still score normally on every
    other axis)."""
    for tag in entry.get("tags", []):
        if tag.startswith(H11_COUNTERPARTY_PREFIX):
            key = tag[len(H11_COUNTERPARTY_PREFIX):]
            if key in dist_map:
                return dist_map[key]
    return None


def circle_item_records(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
    dist_map: dict[str, int],
) -> list[dict[str, Any]]:
    """Per-item H11 inputs {user, session, domain, bin, score}: the circle_radius-
    axis score of each item that carries BOTH a circle_radius tag and a mapped
    counterparty distance tag. Items missing either are dropped. The §10
    inattentive-session exclusion is applied at (user, session, domain)
    granularity — matching context_item_records — and fails open when RTs are
    absent/non-numeric (as with synthetic fixtures)."""
    grouped: dict[tuple[str, str, str], dict[str, list]] = defaultdict(
        lambda: {"items": [], "rts": []}
    )
    for entry in entries:
        b = _distance_bin_of(entry, dist_map)
        if b is None:
            continue
        score, n = _circle_axis_score(entry, tag_map)
        if n == 0:
            continue
        key = (entry.get("user_id"), entry.get("session_id"), entry.get("domain"))
        grouped[key]["items"].append((b, score))
        grouped[key]["rts"].append(entry.get("response_time_ms"))
    records: list[dict[str, Any]] = []
    for (user, session, domain), g in grouped.items():
        rts = [r for r in g["rts"] if isinstance(r, (int, float)) and not isinstance(r, bool)]
        if len(rts) == len(g["rts"]) and rts and _median(rts) < INATTENTIVE_RT_MS:
            continue  # §10 inattentive drop (fails open when any RT is absent/non-numeric)
        for b, score in g["items"]:
            records.append({
                "user": user, "session": session, "domain": domain,
                "bin": b, "score": score,
            })
    return records


def _ols_slope(xs: list[float], ys: list[float]) -> float:
    """Ordinary-least-squares slope of ys on xs; nan if xs has no spread."""
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return float("nan")
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / denom


def circle_shape_by_user(
    records: list[dict[str, Any]],
    session_ok=None,
) -> dict[str, dict[str, Any]]:
    """Per-user circle shape (§1.1): concern_i(d) = mean circle_radius score per
    distance bin (a bin enters only with ≥H11_ITEMS_PER_BIN_MIN items); then
        β_i = OLS slope of concern on bin index (parochialism steepness), and
        R_i = the first bin where concern ≤ midpoint_i, where
              midpoint_i = ½·(concern at the nearest populated bin + axis floor).
    R_i is RIGHT-CENSORED (radius=None, censored=True) when concern never crosses
    — inheriting the §13.2 censoring discipline; a censored radius is NEVER made
    finite. Suppressed (user omitted) below H11_BINS_MIN populated bins (§1.5).
    `session_ok(user, session)` optionally restricts to a session subset (the
    H11a odd/even split)."""
    cell: dict[tuple[str, int], list[float]] = defaultdict(list)
    for r in records:
        if session_ok is not None and not session_ok(r["user"], r["session"]):
            continue
        cell[(r["user"], r["bin"])].append(r["score"])
    by_user: dict[str, dict[int, float]] = defaultdict(dict)
    for (user, b), scores in cell.items():
        if len(scores) >= H11_ITEMS_PER_BIN_MIN:
            by_user[user][b] = sum(scores) / len(scores)
    out: dict[str, dict[str, Any]] = {}
    for user, concern in by_user.items():
        if len(concern) < H11_BINS_MIN:
            continue  # §1.5 suppression — fewer than 4 populated ordered bins
        bins = sorted(concern)
        beta = _ols_slope([float(b) for b in bins], [concern[b] for b in bins])
        near_bin, far_bin = bins[0], bins[-1]
        near_c, far_c = concern[near_bin], concern[far_bin]
        midpoint = (near_c + H11_AXIS_FLOOR) / 2.0
        radius: int | None = None
        censored = True
        for b in bins:
            if concern[b] <= midpoint:
                radius, censored = b, False
                break
        out[user] = {
            "beta": beta, "radius": radius, "censored": censored,
            "n_bins": len(concern), "midpoint": midpoint,
            "near_bin": near_bin, "far_bin": far_bin,
            "near_concern": near_c, "far_concern": far_c,
        }
    return out


def compute_h11a_reliability(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """H11a: split each user's sessions odd/even, recompute β_i on each half,
    correlate across users. Supported iff the lower 95% bootstrap CI of the
    correlation ≥ H11A_RELIABILITY_FLOOR (§1.2). β_i (the slope) is the robust
    circle-SHAPE read — always finite, whereas R_i can be right-censored (§6 Q3),
    so β_i carries the reliability. The de-confound from generosity level is H11b
    (deferred, cohort-coupled). Seed BOOTSTRAP_SEED+15."""
    odd, even = _odd_even_sessions(records)
    shape_odd = circle_shape_by_user(records, lambda u, s: s in odd.get(u, set()))
    shape_even = circle_shape_by_user(records, lambda u, s: s in even.get(u, set()))
    shared = sorted(set(shape_odd) & set(shape_even))
    if len(shared) < 3:
        return None
    xs = [shape_odd[u]["beta"] for u in shared]
    ys = [shape_even[u]["beta"] for u in shared]
    if any(v != v for v in xs + ys):
        return None
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 15)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else bool(ci_low >= H11A_RELIABILITY_FLOOR)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n": len(shared),
        "threshold_low": H11A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_h11c_gradient(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """H11c (parochial-gradient anchor, directional): per user,
        gradient_i = concern at the nearest populated bin − concern at the furthest.
    Supported iff the lower 95% CI of mean_i gradient_i > 0 (one-sided) — concern
    declines with social distance, validating the distance ordering as
    behaviorally real (§1.4; Cikara & Bruneau). A user enters with ≥4 populated
    bins (a formed shape). circle_radius scores only; no cross-channel pooling.
    Seed BOOTSTRAP_SEED+16."""
    shapes = circle_shape_by_user(records)
    gaps = [s["near_concern"] - s["far_concern"] for s in shapes.values()]
    if len(gaps) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 16)
    ci_low, ci_high = _bootstrap_ci_mean(gaps, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_gradient": sum(gaps) / len(gaps),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(gaps),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


# R2 — sacred / protected values (scoring.md §17, r2-sacred-protected-values.md).
# A pure RE-READ of the cost-of-virtue channel's right-censored `never` tail (§4,
# §13.2): the values a person refuses to price at ANY stake in range ARE their
# protected set. P_i = { v : response(i,v) is a censored `never` } — categorical
# set membership, keyed by value_slot, NEVER finitized into a price (the §13.2
# lock, load-bearing here). This adds NO new break-point math; it names the tail
# the censoring discipline was already storing. Two within-person reads (§17.1):
#   R2a — set reliability: test-retest Jaccard of P_i across two waves (§17.2).
#   R2b — protected ≠ EXPENSIVE (§17.3, load-bearing distinctness): among
#         never-responders, the `taboo` marker ("was being asked to price this
#         wrong?") is higher on protected values than on merely high-but-finite
#         ones — a distinct construct, not just "very expensive."
# `taboo` is a NEW light data-contract field (§3 A1), a one-tap after a cov probe,
# scored here on synthetic fixtures; real collection + its exact phrasing are
# runtime/design-gated (Q1) and surfaced to Dave. Value-neutral (§17.5): a large
# protected set can be integrity OR rigid dogmatism — the reveal NAMES the set,
# never ranks it. Cheap-talk caveat (load-bearing): a hypothetical `never` is
# costless, so P_i is labelled PROFESSED protected values; real-stakes validation
# (which `never`s survive a real price) rides H-A2 → Phase-2 (IRB-gated, to Dave).
# No composite (§13.5): P_i is a set, taboo a marker — never summed into a
# "sacredness score" (§4 rejected exactly that). R2c (discriminant vs importance
# rank) is DEFERRED — cohort-coupled, needs the inventory-rank + log-price
# pipeline (like the H9b/H11b deferred halves). Python-only: this re-reads the
# cov break-point PRIMITIVE (already parity-locked; the runtime emits per-slot
# no_break_point at poc-projection.js:212) without changing it, so the on-device
# protected-set reveal is deferred and parity stays green.
# ----------------------------------------------------------------------------

R2A_RELIABILITY_FLOOR = 0.40   # protected-set test-retest Jaccard lower 95% CI (§17.2)
# R2b is directional: lower 95% CI of the mean (taboo|never − taboo|finite) > 0 (§17.3).


def _cov_response_is_protected(r: dict) -> bool:
    """A protected (`never`) cost-of-virtue response per §13.2: refused at every
    rung in range. This is the SAME predicate probe_break_point_score censors on
    (line ~427) — a protected value is exactly the right-censored tail, read here
    categorically as set membership and NEVER finitized into a price (the §17
    censoring lock). Pole-agnostic: a `never` on an inverted probe is still a
    `never`."""
    return r.get("no_break_point") is True or r.get("first_accept_rung") == "never"


def protected_value_sets(
    responses: list[dict],
    wave_of=lambda r: r.get("wave"),
) -> tuple[dict[tuple[str, str], set[str]], dict[str, set[str]]]:
    """P_i per (user, wave) (§17.1): the SET of value_slots the user marked
    `never`. Returns (sets, waves_seen) where sets[(user, wave)] = {value_slot,…}
    and waves_seen[user] = {wave,…} (every wave the user was asked in, so R2a can
    find users present in ≥2 waves even when a wave's protected set is empty).
    Membership is categorical — the set holds value_slot STRINGS, never prices
    (§13.2). `wave_of(response)` → a hashable wave key, or None to drop."""
    sets: dict[tuple[str, str], set[str]] = defaultdict(set)
    waves_seen: dict[str, set[str]] = defaultdict(set)
    for r in responses:
        w = wave_of(r)
        if w is None:
            continue
        user = r.get("user_id")
        if user is None:
            continue
        waves_seen[user].add(w)
        slot = r.get("value_slot")
        if slot and _cov_response_is_protected(r):
            sets[(user, w)].add(slot)
    return sets, waves_seen


def compute_r2a_reliability(
    responses: list[dict],
    wave_of=lambda r: r.get("wave"),
) -> dict[str, Any] | None:
    """R2a (§17.2): protected-set test-retest. For each user present in ≥2 waves,
        jaccard_i = |P_i^w1 ∩ P_i^w2| / |P_i^w1 ∪ P_i^w2|   (first vs last wave)
    the set-agreement of their protected values across occasions. Supported iff
    the lower 95% bootstrap CI of mean_i jaccard_i ≥ R2A_RELIABILITY_FLOOR. Users
    whose union is empty in BOTH waves (protect nothing either time) have an
    undefined Jaccard and are EXCLUDED — reported as n_excluded_empty, not scored
    as perfect agreement. Seed BOOTSTRAP_SEED+17."""
    sets, waves_seen = protected_value_sets(responses, wave_of)
    jaccards: list[float] = []
    n_excluded_empty = 0
    for user in sorted(waves_seen):
        ws = sorted(waves_seen[user])
        if len(ws) < 2:
            continue
        p1 = sets.get((user, ws[0]), set())
        p2 = sets.get((user, ws[-1]), set())
        union = p1 | p2
        if not union:
            n_excluded_empty += 1
            continue
        jaccards.append(len(p1 & p2) / len(union))
    if len(jaccards) < 3:
        return None
    mean_j = sum(jaccards) / len(jaccards)
    rng = random.Random(BOOTSTRAP_SEED + 17)
    ci_low, ci_high = _bootstrap_ci_mean(jaccards, rng)
    met = None if ci_low != ci_low else bool(ci_low >= R2A_RELIABILITY_FLOOR)
    return {
        "mean_jaccard": mean_j, "ci_low": ci_low, "ci_high": ci_high,
        "n_participants": len(jaccards), "n_excluded_empty": n_excluded_empty,
        "threshold_low": R2A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_r2b_distinctness(responses: list[dict]) -> dict[str, Any] | None:
    """R2b (§17.3, protected ≠ expensive — load-bearing distinctness): among
    never-responders, per user
        contrast_i = mean(taboo | protected `never`) − mean(taboo | finite price)
    where taboo ∈ {0,1} marks "was even being ASKED to price this wrong?". A user
    contributes only with BOTH a never-cell AND a finite-cell carrying taboo
    markers. Supported iff the lower 95% CI of mean_i contrast_i > 0 (one-sided,
    directional): pricing a protected value draws outrage that pricing a merely
    high-but-finite value does not — so a `never` is NOT just "very expensive."
    Seed BOOTSTRAP_SEED+18. (The quantity-insensitivity leg needs per-rung
    trajectories the single-break-point contract doesn't carry — bounded/deferred,
    §17.5 / §6 Q3; the taboo contrast is the primary distinctness test, §2.)"""
    by_user: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"never": [], "finite": []}
    )
    for r in responses:
        taboo = r.get("taboo")
        if isinstance(taboo, bool):
            taboo = int(taboo)
        if not isinstance(taboo, (int, float)):
            continue
        user = r.get("user_id")
        if user is None:
            continue
        if _cov_response_is_protected(r):
            by_user[user]["never"].append(float(taboo))
        else:
            stake = r.get("first_accept_stake")
            if isinstance(stake, (int, float)) and not isinstance(stake, bool):
                by_user[user]["finite"].append(float(taboo))
    contrasts: list[float] = []
    for user in sorted(by_user):
        cells = by_user[user]
        if cells["never"] and cells["finite"]:
            m_never = sum(cells["never"]) / len(cells["never"])
            m_finite = sum(cells["finite"]) / len(cells["finite"])
            contrasts.append(m_never - m_finite)
    if len(contrasts) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 18)
    ci_low, ci_high = _bootstrap_ci_mean(contrasts, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_contrast": sum(contrasts) / len(contrasts),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(contrasts),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


# ----------------------------------------------------------------------------
# H12 — moral hypocrisy: the self–other judgment asymmetry (scoring.md §18).
# A paired within-person contrast on a COMMON severity scale — the SAME act is
# judged as one's own and as another's, and H_i = mean(severity_other −
# severity_self) is the person's self–other asymmetry. Grounded in the moral-
# superiority / holier-than-thou findings (Tappin & McKay 2017; Epley & Dunning
# 2000; the actor–observer asymmetry) — NOT the excluded paradigms. Python-only:
# a paired contrast reusing the reliability/bootstrap machinery, with NO on-device
# H_i reveal this increment (like the H9b/H10b/H11b/R2c deferred halves), so
# parity stays green. The H12b discriminant (vs the §6 gap / calibration error) is
# cohort-coupled and deferred. The pairing/missing-data lock (a declined judgment
# drops the pair, never imputed to 0; sign preserved) is the H12 analog of the
# §13.2 censoring lock — asserted against the code by check_h12_pairing_lock().
# ----------------------------------------------------------------------------

H12A_RELIABILITY_FLOOR = 0.40   # self–other asymmetry split-half reliability lower 95% CI (§18.2)
H12_MIN_PAIRS = 3               # per-person scorable-pair floor for a reveal-eligible H_i (§1.5 N=1)
# H12c is directional: lower 95% CI of the mean self–other asymmetry mean_i H_i > 0 (§18.3).


def _hypocrisy_pair_delta(r: dict) -> float | None:
    """The self–other asymmetry for ONE matched item (§18.1): severity_other −
    severity_self, both rating the SAME act on a common severity scale. Returns
    None — the pair is DROPPED, never imputed — when either judgment is absent or
    non-numeric: a declined "can't say" judgment is MISSING DATA, not a 0 delta
    (the H12 pairing lock, the analog of the §13.2 censoring `never` lock). Sign is
    PRESERVED: positive = harsher on others than on self (the self-serving /
    moral-superiority direction), negative = harsher on self (value-neutral)."""
    so = r.get("severity_self")
    oo = r.get("severity_other")
    if not isinstance(so, (int, float)) or isinstance(so, bool):
        return None
    if not isinstance(oo, (int, float)) or isinstance(oo, bool):
        return None
    return float(oo) - float(so)


def hypocrisy_deltas_by_user(
    records: list[dict],
    session_filter=None,
) -> dict[str, list[float]]:
    """Per user, the list of matched-item self–other deltas (§18.1). A record
    contributes only if BOTH severities are present (the pairing lock: a declined
    judgment drops that pair, never imputed to 0). Optional
    session_filter(user, session) -> bool restricts to a session subset (the H12a
    odd/even split). Keys `user` / `session` mirror the H10/H11 logs consumed by
    _odd_even_sessions."""
    by_user: dict[str, list[float]] = defaultdict(list)
    for r in records:
        user = r.get("user")
        if user is None:
            continue
        if session_filter is not None and not session_filter(user, r.get("session")):
            continue
        d = _hypocrisy_pair_delta(r)
        if d is not None:
            by_user[user].append(d)
    return by_user


def hypocrisy_asymmetry_by_user(
    records: list[dict],
    session_filter=None,
    min_pairs: int = H12_MIN_PAIRS,
) -> dict[str, float]:
    """H_i = mean matched-item delta per user (§18.1), for users with ≥min_pairs
    scorable pairs (the §1.5 N=1 floor). Signed and value-neutral — a person
    harsher on themselves keeps a NEGATIVE H_i, never clamped."""
    out: dict[str, float] = {}
    for user, deltas in hypocrisy_deltas_by_user(records, session_filter).items():
        if len(deltas) >= min_pairs:
            out[user] = sum(deltas) / len(deltas)
    return out


def compute_h12a_reliability(records: list[dict]) -> dict[str, Any] | None:
    """H12a (§18.2): split each user's sessions odd/even, recompute the self–other
    asymmetry H_i on each half, correlate across users. Supported iff the lower
    95% bootstrap CI of the correlation ≥ H12A_RELIABILITY_FLOOR. Reliability of
    the asymmetry TRAIT itself — orthogonal to whether the cohort is self-serving
    on average (that anchor is H12c) and to the person's level (the H12b
    discriminant, deferred). Seed BOOTSTRAP_SEED+19."""
    odd, even = _odd_even_sessions(records)
    h_odd = hypocrisy_asymmetry_by_user(records, lambda u, s: s in odd.get(u, set()))
    h_even = hypocrisy_asymmetry_by_user(records, lambda u, s: s in even.get(u, set()))
    shared = sorted(set(h_odd) & set(h_even))
    if len(shared) < 3:
        return None
    xs = [h_odd[u] for u in shared]
    ys = [h_even[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 19)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else bool(ci_low >= H12A_RELIABILITY_FLOOR)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n": len(shared),
        "threshold_low": H12A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_h12c_self_serving(
    records: list[dict], min_pairs: int = H12_MIN_PAIRS
) -> dict[str, Any] | None:
    """H12c (§18.3, self-serving asymmetry anchor, directional): per user,
        H_i = mean matched-item (severity_other − severity_self)
    Supported iff the lower 95% CI of mean_i H_i > 0 (one-sided): on average people
    judge OTHERS' identical transgressions more harshly than their own — the
    moral-superiority / holier-than-thou direction (Tappin & McKay 2017; Epley &
    Dunning 2000). This is a COHORT-level validity anchor (does the self-serving
    asymmetry replicate as theorized), NOT a per-person verdict: the person-level
    H_i reveal stays signed and value-neutral (harsher-on-self is described, never
    ranked, §18.4). Seed BOOTSTRAP_SEED+20."""
    h_by_user = hypocrisy_asymmetry_by_user(records, None, min_pairs)
    asymmetries = [h_by_user[u] for u in sorted(h_by_user)]
    if len(asymmetries) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 20)
    ci_low, ci_high = _bootstrap_ci_mean(asymmetries, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_asymmetry": sum(asymmetries) / len(asymmetries),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(asymmetries),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


# ----------------------------------------------------------------------------
# R1 — moral identity centrality: how self-defining moral traits are (scoring.md §19).
# The Aquino & Reed 2002 "Self-Importance of Moral Identity" construct, read as TWO
# DISJOINT facets kept strictly separate — INTERNALIZATION (private: "being a moral
# person is core to who I am") and SYMBOLIZATION (public: outward display of moral
# identity). Per §13.5 the two facets are NEVER pooled into one "moral-identity
# score" (that no-composite discipline is load-bearing for a centrality read and is
# asserted against the code by check_r1_no_pool()). R1 is the meta-MODERATOR — it
# moderates the §6 gap / H10–H12 — but the moderation legs couple to the cohort gap
# pipeline and are DEFERRED (R1b), exactly like the H9b/H10b/H11b/R2c discriminant
# halves; this increment ships the self-contained centrality read + its reliability
# (R1a) + the internalization>symbolization construct anchor (R1c). Python-only (no
# on-device reveal this increment) so parity stays green. A declined item is DROPPED,
# never imputed to 0 (the §1.5 missing-data discipline), and a facet below the item
# floor is SUPPRESSED, never scored on too-few items.
# ----------------------------------------------------------------------------

R1A_RELIABILITY_FLOOR = 0.40   # internalization-centrality split-half reliability lower 95% CI (§19.2)
R1_MIN_ITEMS = 3               # per-facet item floor for a scorable facet (§1.5 N=1)
R1_FACETS = ("internalization", "symbolization")
# R1c is directional: lower 95% CI of mean_i (internalization_i − symbolization_i) > 0 (§19.3).


def _centrality_response(r: dict) -> float | None:
    """One centrality-item Likert response (§19.1). Returns None — the item is
    DROPPED, never imputed — when absent or non-numeric: a declined "prefer not to
    say" item is MISSING DATA, not a 0 (the §1.5 missing-data discipline). A bool is
    rejected (guards against True==1 coercion)."""
    v = r.get("response")
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return None
    return float(v)


def centrality_items_by_user(
    records: list[dict],
    facet: str,
    session_filter=None,
) -> dict[str, list[float]]:
    """Per user, the list of scorable Likert responses for ONE facet (§19.1). A
    record contributes only to its OWN facet — internalization and symbolization are
    routed to DISJOINT item sets and never mixed (§13.5). A declined item is dropped
    (never imputed). Optional session_filter(user, session) -> bool restricts to a
    session subset (the R1a odd/even split). Keys `user` / `session` mirror the
    H10/H11/H12 logs consumed by _odd_even_sessions."""
    by_user: dict[str, list[float]] = defaultdict(list)
    for r in records:
        user = r.get("user")
        if user is None:
            continue
        if r.get("facet") != facet:
            continue
        if session_filter is not None and not session_filter(user, r.get("session")):
            continue
        v = _centrality_response(r)
        if v is not None:
            by_user[user].append(v)
    return by_user


def centrality_facet_by_user(
    records: list[dict],
    facet: str,
    session_filter=None,
    min_items: int = R1_MIN_ITEMS,
) -> dict[str, float]:
    """C^facet_i = mean item response per user for ONE facet (§19.1), for users with
    ≥min_items scorable items in that facet (the §1.5 floor — a facet below it is
    SUPPRESSED, absent from the result, never scored on too-few items). The two
    facets are kept SEPARATE; this never averages internalization with symbolization
    into a single centrality scalar (§13.5)."""
    out: dict[str, float] = {}
    for user, vals in centrality_items_by_user(records, facet, session_filter).items():
        if len(vals) >= min_items:
            out[user] = sum(vals) / len(vals)
    return out


def compute_r1a_reliability(records: list[dict]) -> dict[str, Any] | None:
    """R1a (§19.2): split each user's sessions odd/even, recompute the
    INTERNALIZATION centrality facet on each half, correlate across users. Supported
    iff the lower 95% bootstrap CI of the correlation ≥ R1A_RELIABILITY_FLOOR.
    Internalization is the primary (private, more-predictive) dimension (Aquino &
    Reed 2002); its stability is the trait-reliability leg — orthogonal to the
    cohort ordering (that anchor is R1c) and to whether centrality moderates the gap
    (the R1b moderation leg, deferred). Seed BOOTSTRAP_SEED+21."""
    odd, even = _odd_even_sessions(records)
    c_odd = centrality_facet_by_user(records, "internalization", lambda u, s: s in odd.get(u, set()))
    c_even = centrality_facet_by_user(records, "internalization", lambda u, s: s in even.get(u, set()))
    shared = sorted(set(c_odd) & set(c_even))
    if len(shared) < 3:
        return None
    xs = [c_odd[u] for u in shared]
    ys = [c_even[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 21)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else bool(ci_low >= R1A_RELIABILITY_FLOOR)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n": len(shared),
        "threshold_low": R1A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_r1c_internalization_anchor(
    records: list[dict], min_items: int = R1_MIN_ITEMS
) -> dict[str, Any] | None:
    """R1c (§19.3, internalization > symbolization anchor, directional): per user
    with BOTH facets scored,
        d_i = internalization_i − symbolization_i        (same Likert scale — a
                                                           within-construct contrast,
                                                           not cross-scale pooling)
    Supported iff the lower 95% CI of mean_i d_i > 0 (one-sided): on average the
    private/internalized dimension is endorsed more strongly than the public/
    symbolization one (Aquino & Reed 2002). A COHORT-level construct-validity anchor
    (does the established ordering replicate), NOT a per-person verdict and NOT a
    per-person composite: the person-level reveal keeps the two facets SEPARATE and
    value-neutral (§19.4). Seed BOOTSTRAP_SEED+22."""
    intern = centrality_facet_by_user(records, "internalization", None, min_items)
    symbol = centrality_facet_by_user(records, "symbolization", None, min_items)
    shared = sorted(set(intern) & set(symbol))
    deltas = [intern[u] - symbol[u] for u in shared]
    if len(deltas) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 22)
    ci_low, ci_high = _bootstrap_ci_mean(deltas, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_delta": sum(deltas) / len(deltas),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(deltas),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


# --- R6: moral conviction / metaethical objectivism (scoring.md §20, Goodwin & Darley
# 2008 + Skitka 2010). The STATED objectivism probe: how OBJECTIVE a person treats a
# moral claim (a fact true for everyone) vs. a matter of opinion (their own). The
# load-bearing discipline (§13.5) is to hold the STATED probe apart from the REVEALED
# tolerance/compromise/language signatures — NEVER pooled into one "conviction score" —
# and the revealed signatures (κ-gated language + tolerance coding) are DEFERRED with
# R6b/R6c. Python-only this increment (no on-device reveal touched). Value-neutrality
# binds with EXTRA FORCE here: the construct predicts intolerance/force, so neither pole
# is ever ranked (§20.4).
R6A_RELIABILITY_FLOOR = 0.50   # objectivism split-half reliability lower 95% CI (§20.2) — the HIGHER bar
R6_MIN_ITEMS = 3               # per-claim-type item floor for a scorable read (§1.5 N=1)
R6_CLAIM_TYPES = ("moral", "taste")
# R6d is directional: lower 95% CI of mean_i (objectivism_moral_i − objectivism_taste_i) > 0 (§20.3).


def _objectivism_response(r: dict) -> float | None:
    """One metaethical-objectivism item response (§20.1): a Likert rating of how
    OBJECTIVE a claim is (1 = purely a matter of opinion/preference … 7 = objectively
    true or false, a fact independent of anyone's view). Returns None — the item is
    DROPPED, never imputed — when absent or non-numeric (a declined item is MISSING
    DATA, not a 0; §1.5). A bool is rejected (guards against True==1 coercion)."""
    v = r.get("objectivism")
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return None
    return float(v)


def objectivism_items_by_user(
    records: list[dict],
    claim_type: str,
    session_filter=None,
) -> dict[str, list[float]]:
    """Per user, the list of scorable objectivism ratings for ONE claim type (§20.1).
    A record contributes only to its OWN claim_type — moral and taste items route to
    DISJOINT sets and are never mixed (objectivism_i reads the MORAL items, not a
    moral/taste blend; §13.5). A declined item is dropped (never imputed). Optional
    session_filter(user, session) -> bool restricts to a session subset (the R6a
    odd/even split). Keys `user` / `session` mirror the H10/H11/H12/R1 logs consumed
    by _odd_even_sessions."""
    by_user: dict[str, list[float]] = defaultdict(list)
    for r in records:
        user = r.get("user")
        if user is None:
            continue
        if r.get("claim_type") != claim_type:
            continue
        if session_filter is not None and not session_filter(user, r.get("session")):
            continue
        v = _objectivism_response(r)
        if v is not None:
            by_user[user].append(v)
    return by_user


def objectivism_by_user(
    records: list[dict],
    claim_type: str,
    session_filter=None,
    min_items: int = R6_MIN_ITEMS,
) -> dict[str, float]:
    """objectivism_type_i = mean objectivism rating per user for ONE claim type
    (§20.1), for users with ≥min_items scorable items of that type (the §1.5 floor —
    a read below it is SUPPRESSED, absent from the result, never scored on too-few
    items). objectivism_i (the reveal quantity) is the MORAL read; the taste read is
    the cohort-anchor baseline (R6d). This never averages moral with taste into a
    single scalar (§13.5), and — the R6 load-bearing discipline — never pools the
    STATED objectivism probe with the (deferred, κ-gated) REVEALED tolerance/language
    signatures."""
    out: dict[str, float] = {}
    for user, vals in objectivism_items_by_user(records, claim_type, session_filter).items():
        if len(vals) >= min_items:
            out[user] = sum(vals) / len(vals)
    return out


def compute_r6a_reliability(records: list[dict]) -> dict[str, Any] | None:
    """R6a (§20.2): split each user's sessions odd/even, recompute the MORAL-claim
    objectivism read on each half, correlate across users. Supported iff the lower
    95% bootstrap CI of the correlation ≥ R6A_RELIABILITY_FLOOR (0.50 — a HIGHER bar
    than the exploratory branches' 0.40, because metaethical objectivism is a stable,
    reliable individual difference; Goodwin & Darley 2008, Skitka 2010). Anchored on
    the moral read (the metaethical stance toward moral claims). Orthogonal to the
    cohort ordering (that anchor is R6d), the discriminant (R6b, deferred), and the
    stated–revealed meta-gap (R6c, deferred — κ-gated). Seed BOOTSTRAP_SEED+23."""
    odd, even = _odd_even_sessions(records)
    o_odd = objectivism_by_user(records, "moral", lambda u, s: s in odd.get(u, set()))
    o_even = objectivism_by_user(records, "moral", lambda u, s: s in even.get(u, set()))
    shared = sorted(set(o_odd) & set(o_even))
    if len(shared) < 3:
        return None
    xs = [o_odd[u] for u in shared]
    ys = [o_even[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 23)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_low != ci_low else bool(ci_low >= R6A_RELIABILITY_FLOOR)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n": len(shared),
        "threshold_low": R6A_RELIABILITY_FLOOR, "pre_registered_threshold_met": met,
    }


def compute_r6d_moral_objectivism_anchor(
    records: list[dict], min_items: int = R6_MIN_ITEMS
) -> dict[str, Any] | None:
    """R6d (§20.3, moral > taste objectivism anchor, directional): per user with BOTH
    a moral and a taste read,
        d_i = objectivism_moral_i − objectivism_taste_i      (same objectivism scale —
                                                              a within-scale contrast,
                                                              not cross-scale pooling)
    Supported iff the lower 95% CI of mean_i d_i > 0 (one-sided): on average people
    treat moral claims as MORE objective (fact-like) than matters of taste (Goodwin &
    Darley 2008, the canonical objectivism gradient). A COHORT-level construct-validity
    anchor (does the established ordering replicate), NOT a per-person verdict: an
    individual with d_i < 0 is described, never ranked (§20.4). Labelled R6d (not the
    spec's R6c) to avoid colliding with R6c the stated–revealed meta-gap — the deferred
    distinctive extension. Seed BOOTSTRAP_SEED+24."""
    moral = objectivism_by_user(records, "moral", None, min_items)
    taste = objectivism_by_user(records, "taste", None, min_items)
    shared = sorted(set(moral) & set(taste))
    deltas = [moral[u] - taste[u] for u in shared]
    if len(deltas) < 3:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 24)
    ci_low, ci_high = _bootstrap_ci_mean(deltas, rng)
    met = None if ci_low != ci_low else bool(ci_low > 0.0)
    return {
        "mean_delta": sum(deltas) / len(deltas),
        "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(deltas),
        "threshold": 0.0, "pre_registered_threshold_met": met,
    }


def render_correlation_result(name: str, threshold_text: str, result: dict[str, Any] | None) -> str:
    if result is None:
        return f"({name}: insufficient data — need ≥3 users with both revealed truth-telling and the external measure)"
    ci_str = (
        "nan" if result["ci_low"] != result["ci_low"]
        else f"[{result['ci_low']:+.3f}, {result['ci_high']:+.3f}]"
    )
    met = result.get("pre_registered_threshold_met")
    threshold_str = "✓" if met is True else ("✗" if met is False else "—")
    return (
        f"{name}:\n"
        f"  Pearson r = {result['r']:+.3f}, 95% CI {ci_str}, n = {result['n']}\n"
        f"  Pre-registered threshold ({threshold_text}): {threshold_str}"
    )


def render_h6_result(result: dict[str, Any] | None) -> str:
    if result is None:
        return "(H6: insufficient data — need ≥3 users with both revealed and stated_aspirational truth-telling)"
    ci_str = (
        "nan" if result["ci_low"] != result["ci_low"]
        else f"[{result['ci_low']:+.3f}, {result['ci_high']:+.3f}]"
    )
    in_range = result.get("in_pre_registered_range")
    range_str = "✓" if in_range else "✗"
    return (
        f"H6 (stated-revealed correlation, range check):\n"
        f"  Pearson r = {result['r']:+.3f}, 95% CI {ci_str}, n = {result['n']}\n"
        f"  Pre-registered range [{result['range_low']:.2f}, {result['range_high']:.2f}]: {range_str}\n"
        f"  Reading: too-high r collapses the gap signal; too-low suggests measurement noise."
    )


def _met_glyph(met: bool | None) -> str:
    return "✓" if met is True else ("✗" if met is False else "—")


def _ci_str(res: dict[str, Any]) -> str:
    return (
        "nan" if res["ci_low"] != res["ci_low"]
        else f"[{res['ci_low']:+.3f}, {res['ci_high']:+.3f}]"
    )


def render_h9_result(
    h9a: dict[str, Any] | None,
    h9b: dict[str, Any] | None,
    h9c: dict[str, Any] | None,
    cov: dict[str, Any] | None,
    person_indices_n: int,
) -> str:
    """H9 self-prediction calibration (scoring.md §14). Axis channel and cost-of-
    virtue channel reported SEPARATELY — never pooled (§14.7)."""
    if all(x is None for x in (h9a, h9b, h9c)) and cov is None:
        return "(H9: insufficient data — supply --predictions to compute self-prediction calibration)"
    lines = ["H9 (self-prediction calibration — self-knowledge vs self-deception):"]
    lines.append(f"  Reveal-eligible person indices (cal_bias / cal_error): {person_indices_n} participant(s)")
    lines.append("  -- Axis channel (axis units; never pooled with the cost-of-virtue channel) --")
    if h9a is not None:
        lines.append(
            f"  H9a self-enhancement  mean cal_bias = {h9a['mean_cal_bias']:+.3f}, "
            f"95% CI {_ci_str(h9a)}, n = {h9a['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {h9a['threshold_low']:.2f}, over consensual-pole domains): "
            f"{_met_glyph(h9a['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  H9a self-enhancement: insufficient data (need ≥3 participants, ≥3 consensual probes each)")
    if h9b is not None:
        lines.append(
            f"  H9b stability (test-retest of cal_error)  r = {h9b['r']:+.3f}, "
            f"95% CI {_ci_str(h9b)}, n = {h9b['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {h9b['threshold_low']:.2f}): "
            f"{_met_glyph(h9b['pre_registered_threshold_met'])}  "
            f"(discriminant half deferred — see build-and-validate.md)"
        )
    else:
        lines.append("  H9b stability: insufficient data (need --predictions-window-b, ≥3 shared participants)")
    if h9c is not None:
        lines.append(
            f"  H9c stakes-blindness (LOAD-BEARING)  mean blind = {h9c['mean_blind']:+.3f}, "
            f"95% CI {_ci_str(h9c)}, n = {h9c['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {h9c['threshold']:.1f}, one-sided): "
            f"{_met_glyph(h9c['pre_registered_threshold_met'])}  "
            f"(high-stakes self-prediction error exceeds low-stakes)"
        )
    else:
        lines.append("  H9c stakes-blindness: insufficient data (need ≥3 participants with both a low- and high-pool error)")
    if cov is not None:
        cats = ", ".join(f"{k}={v}" for k, v in sorted(cov["censored_categories"].items())) or "none"
        mean_e = cov["finite_mean_abs_e_price"]
        mean_e_str = "n/a" if mean_e is None else f"{mean_e:.3f}"
        lines.append("  -- Cost-of-virtue channel (log10-dollar units; convergent, reported separately) --")
        lines.append(
            f"  finite pairs = {cov['n_finite']} (mean |e_price| = {mean_e_str}), "
            f"censored = {cov['n_censored']} [{cats}]"
        )
        lines.append(
            "     censoring lock (§14.1): a 'never' endpoint is NEVER priced — "
            "reported categorically only."
        )
    return "\n".join(lines)


def render_h10_result(
    h10a: dict[str, Any] | None,
    h10c: dict[str, Any] | None,
    person_variability_n: int,
    n_construct_sd_cells: int,
) -> str:
    """H10 cross-situational consistency (scoring.md §15). Value-neutral: the
    per-construct sd_i(c) and V_i name WHERE a person sits on steadiness↔
    responsiveness; they never rank (Dancy caveat, §15.5)."""
    if h10a is None and h10c is None and n_construct_sd_cells == 0:
        return (
            "(H10: insufficient data — supply --context-log with context:*-tagged "
            "items to compute cross-situational consistency)"
        )
    lines = ["H10 (cross-situational moral consistency — steadiness vs responsiveness, value-neutral):"]
    lines.append(
        f"  Reveal-eligible per-construct sd_i(c): {n_construct_sd_cells} (user × construct) cell(s); "
        f"V_i formed for {person_variability_n} participant(s) (≥3 qualifying constructs each)"
    )
    lines.append("  -- Axis channel (axis units; per-construct SDs never summed into a composite, §13.5) --")
    if h10a is not None:
        lines.append(
            f"  H10a trait reliability (split-half, odd/even sessions)  r = {h10a['r']:+.3f}, "
            f"95% CI {_ci_str(h10a)}, n = {h10a['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {h10a['threshold_low']:.2f}): "
            f"{_met_glyph(h10a['pre_registered_threshold_met'])}  "
            f"(discriminant half H10b deferred — see build-and-validate.md)"
        )
    else:
        lines.append("  H10a trait reliability: insufficient data (need ≥3 users with a V_i in both session halves)")
    if h10c is not None:
        lines.append(
            f"  H10c observer-effect anchor (public − anonymous)  mean gap = {h10c['mean_obs_gap']:+.3f}, "
            f"95% CI {_ci_str(h10c)}, n = {h10c['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {h10c['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(h10c['pre_registered_threshold_met'])}  "
            f"(scores shift between observed and anonymous settings)"
        )
    else:
        lines.append("  H10c observer-effect anchor: insufficient data (need ≥3 users with both a public and an anonymous item)")
    return "\n".join(lines)


def render_h11_result(
    h11a: dict[str, Any] | None,
    h11c: dict[str, Any] | None,
    person_shape_n: int,
    radius_finite: int,
    radius_censored: int,
) -> str:
    """H11 moral-circle radius (scoring.md §16). Value-neutral: β_i (parochialism
    steepness) and R_i (the reach of concern) name the SHAPE of a person's circle;
    a wider circle is never scored as better (§1.5, Singer vs Williams/MacIntyre)."""
    if h11a is None and h11c is None and person_shape_n == 0:
        return (
            "(H11: insufficient data — supply --circle-log with counterparty:*-tagged "
            "in-group items to compute the moral-circle radius)"
        )
    lines = ["H11 (moral-circle radius — the reach of concern across social distance, value-neutral):"]
    lines.append(
        f"  Reveal-eligible circle shapes: {person_shape_n} participant(s) with β_i/R_i "
        f"(≥{H11_BINS_MIN} populated distance bins each); R_i finite for {radius_finite}, "
        f"right-censored for {radius_censored} "
        f"(concern never crosses the midpoint — a wide/flat circle; never made finite, §13.2)"
    )
    lines.append("  -- circle_radius axis (secondary, §2.3); β_i/R_i reported as facets, never summed (§13.5) --")
    if h11a is not None:
        lines.append(
            f"  H11a shape reliability (β_i split-window, odd/even sessions)  r = {h11a['r']:+.3f}, "
            f"95% CI {_ci_str(h11a)}, n = {h11a['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {h11a['threshold_low']:.2f}): "
            f"{_met_glyph(h11a['pre_registered_threshold_met'])}  "
            f"(discriminant half H11b deferred — see build-and-validate.md)"
        )
    else:
        lines.append("  H11a shape reliability: insufficient data (need ≥3 users with a β_i in both session halves)")
    if h11c is not None:
        lines.append(
            f"  H11c parochial gradient (near − far concern)  mean = {h11c['mean_gradient']:+.3f}, "
            f"95% CI {_ci_str(h11c)}, n = {h11c['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {h11c['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(h11c['pre_registered_threshold_met'])}  "
            f"(concern declines with social distance — the parochial gradient is behaviorally real)"
        )
    else:
        lines.append("  H11c parochial gradient: insufficient data (need ≥3 users with ≥4 populated bins)")
    lines.append(
        "  Value-neutral: a wider circle is not scored as better (Singer's impartialism vs "
        "Williams/MacIntyre partialism, §1.5) — the reveal names the shape, never ranks it."
    )
    return "\n".join(lines)


def render_r2_result(
    r2a: dict[str, Any] | None,
    r2b: dict[str, Any] | None,
    protected_set_n: int,
    protected_none_n: int,
    protected_set_sizes: list[int],
) -> str:
    """R2 sacred / protected values (scoring.md §17). Value-neutral: P_i names the
    values a person won't price (professed) — integrity OR dogmatism, never ranked
    (§17.5). The `never` tail is read categorically, never finitized (§13.2)."""
    if r2a is None and r2b is None and protected_set_n == 0 and protected_none_n == 0:
        return (
            "(R2: insufficient data — supply --protected-log with cost-of-virtue "
            "responses carrying value_slot + wave (+ taboo) to read the protected set)"
        )
    lines = ["R2 (sacred / protected values — the values a person won't price, value-neutral):"]
    mean_size = (sum(protected_set_sizes) / len(protected_set_sizes)) if protected_set_sizes else 0.0
    lines.append(
        f"  Professed protected sets P_i: {protected_set_n} participant(s) with ≥1 protected "
        f"value (mean set size {mean_size:.2f}); {protected_none_n} protect nothing "
        f"(all values priced). A `never` is read categorically — right-censored, never "
        f"finitized into a price (§13.2)."
    )
    lines.append("  -- cost-of-virtue `never` tail re-read as the protected set (§17.1); a SET + a marker, never summed (§13.5) --")
    if r2a is not None:
        lines.append(
            f"  R2a set reliability (protected-set test-retest, Jaccard over waves)  "
            f"mean = {r2a['mean_jaccard']:.3f}, 95% CI {_ci_str(r2a)}, n = {r2a['n_participants']}"
            + (f" ({r2a['n_excluded_empty']} excluded: empty in both waves)" if r2a['n_excluded_empty'] else "")
        )
        lines.append(
            f"     threshold (lower CI ≥ {r2a['threshold_low']:.2f}): "
            f"{_met_glyph(r2a['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  R2a set reliability: insufficient data (need ≥3 users with a non-empty protected set across ≥2 waves)")
    if r2b is not None:
        lines.append(
            f"  R2b protected ≠ expensive (taboo|never − taboo|finite)  mean = {r2b['mean_contrast']:+.3f}, "
            f"95% CI {_ci_str(r2b)}, n = {r2b['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {r2b['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(r2b['pre_registered_threshold_met'])}  "
            f"(being asked to price a protected value draws outrage a merely-expensive one does not)"
        )
    else:
        lines.append("  R2b protected ≠ expensive: insufficient data (need ≥3 users with both a taboo-marked `never` and finite response)")
    lines.append(
        "  Value-neutral: a large protected set is not scored as better (integrity vs rigid "
        "dogmatism, §17.5). Cheap-talk: these are PROFESSED protected values — real-stakes "
        "validation (H-A2) is Phase-2. R2c discriminant (vs importance rank) deferred; see build-and-validate.md."
    )
    return "\n".join(lines)


def render_h12_result(
    h12a: dict[str, Any] | None,
    h12c: dict[str, Any] | None,
    person_asymmetry_n: int,
    mean_asymmetry_census: float,
) -> str:
    """H12 moral hypocrisy / self–other judgment asymmetry (scoring.md §18).
    Value-neutral: H_i names the direction and size of a person's self–other gap —
    harsher-on-others (self-serving) and harsher-on-self (self-critical) are both
    described, never ranked (§18.4). "Hypocrisy" is the construct's name in the
    literature; the reveal states the asymmetry descriptively, never as a verdict.
    A declined judgment drops the pair, never imputed to 0 (§18.1 pairing lock)."""
    if h12a is None and h12c is None and person_asymmetry_n == 0:
        return (
            "(H12: insufficient data — supply --hypocrisy-log with matched "
            "severity_self + severity_other judgments of the same acts)"
        )
    lines = ["H12 (moral hypocrisy — the self–other judgment asymmetry, signed & value-neutral):"]
    lines.append(
        f"  Person asymmetry H_i = mean(severity_other − severity_self) over matched acts: "
        f"{person_asymmetry_n} participant(s) scored (mean H_i {mean_asymmetry_census:+.3f}). "
        f"A declined judgment drops the pair — never imputed to 0 (§18.1 pairing lock)."
    )
    lines.append("  -- self & other rate the SAME act on a common scale; the signed delta is a facet, never summed (§13.5) --")
    if h12a is not None:
        lines.append(
            f"  H12a asymmetry reliability (split-half odd/even, corr of H_i)  r = {h12a['r']:+.3f}, "
            f"95% CI {_ci_str(h12a)}, n = {h12a['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {h12a['threshold_low']:.2f}): "
            f"{_met_glyph(h12a['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  H12a asymmetry reliability: insufficient data (need ≥3 users scorable in both odd & even session halves)")
    if h12c is not None:
        lines.append(
            f"  H12c self-serving asymmetry (mean_i H_i, cohort anchor)  mean = {h12c['mean_asymmetry']:+.3f}, "
            f"95% CI {_ci_str(h12c)}, n = {h12c['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {h12c['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(h12c['pre_registered_threshold_met'])}  "
            f"(people judge others' identical acts more harshly than their own — Tappin & McKay 2017)"
        )
    else:
        lines.append("  H12c self-serving asymmetry: insufficient data (need ≥3 users with ≥3 matched pairs)")
    lines.append(
        "  Value-neutral: harsher-on-others (self-serving) and harsher-on-self (self-critical/scrupulous) "
        "are both just described — neither is scored as better (§18.4). H12c is a cohort validity anchor, "
        "not a per-person verdict. H12b discriminant (vs gap / calibration) deferred; see build-and-validate.md."
    )
    return "\n".join(lines)


def render_r1_result(
    r1a: dict[str, Any] | None,
    r1c: dict[str, Any] | None,
    profile_n: int,
    mean_internalization: float,
    mean_symbolization: float,
) -> str:
    """R1 moral identity centrality (scoring.md §19). Two DISJOINT facets reported
    SEPARATELY — internalization (private) and symbolization (public) — never pooled
    into one "moral-identity score" (§13.5, load-bearing here). Value-neutral: high
    centrality is NOT scored as better than low (a self-defining moral identity can
    be integrity OR rigid self-righteousness — the dark side of moral identity), and
    internalizing is not ranked above symbolizing; the reveal describes the profile,
    never a verdict (§19.4)."""
    if r1a is None and r1c is None and profile_n == 0:
        return (
            "(R1: insufficient data — supply --identity-log with per-item "
            "internalization + symbolization centrality responses)"
        )
    lines = ["R1 (moral identity centrality — two facets, kept separate & value-neutral):"]
    lines.append(
        f"  Centrality profile (mean item response, 1–7): internalization {mean_internalization:+.3f}, "
        f"symbolization {mean_symbolization:+.3f} over {profile_n} participant(s) with both facets scored."
    )
    lines.append("  -- the two facets are DISJOINT item sets; never averaged into one centrality score (§13.5) --")
    if r1a is not None:
        lines.append(
            f"  R1a centrality reliability (split-half odd/even, corr of internalization)  r = {r1a['r']:+.3f}, "
            f"95% CI {_ci_str(r1a)}, n = {r1a['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {r1a['threshold_low']:.2f}): "
            f"{_met_glyph(r1a['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  R1a centrality reliability: insufficient data (need ≥3 users scorable in both odd & even session halves)")
    if r1c is not None:
        lines.append(
            f"  R1c internalization > symbolization (mean_i of the within-scale delta, cohort anchor)  "
            f"mean = {r1c['mean_delta']:+.3f}, 95% CI {_ci_str(r1c)}, n = {r1c['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {r1c['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(r1c['pre_registered_threshold_met'])}  "
            f"(the private/internalized dimension is endorsed more than the public/symbolic — Aquino & Reed 2002)"
        )
    else:
        lines.append("  R1c internalization > symbolization: insufficient data (need ≥3 users with both facets scored)")
    lines.append(
        "  Value-neutral: a highly self-defining moral identity is NOT scored as better than a peripheral one "
        "(centrality can be integrity OR rigid self-righteousness, §19.4); the facets are described, never ranked. "
        "R1c is a cohort construct-validity anchor, not a per-person verdict. R1b — whether centrality MODERATES "
        "the stated–revealed gap / H10–H12 — is deferred (cohort-coupled); see build-and-validate.md."
    )
    return "\n".join(lines)


def render_r6_result(
    r6a: dict[str, Any] | None,
    r6d: dict[str, Any] | None,
    profile_n: int,
    mean_moral_objectivism: float,
    mean_taste_objectivism: float,
) -> str:
    """R6 moral conviction / metaethical objectivism (scoring.md §20). The STATED
    objectivism probe read (Goodwin & Darley 2008): how objective a person treats
    moral claims (a fact for everyone) vs. matters of taste (their own). Reported as a
    standalone STATED quantity — NEVER pooled with the (deferred, κ-gated) REVEALED
    tolerance/compromise/language signatures (§13.5, the load-bearing discipline here),
    and the moral read is never blended with the taste read. Value-neutral with EXTRA
    FORCE (the branch is charged — conviction predicts intolerance/force): neither pole
    is better — objectivism can be moral clarity OR rigid intolerance of dissent,
    subjectivism tolerant pluralism OR a relativism that won't stand for anything; the
    reveal names where you sit, never ranks (§20.4)."""
    if r6a is None and r6d is None and profile_n == 0:
        return (
            "(R6: insufficient data — supply --objectivism-log with per-item "
            "metaethical-objectivism ratings across moral + taste claim types)"
        )
    lines = ["R6 (metaethical objectivism — stated probe, value-neutral under extra force):"]
    lines.append(
        f"  Objectivism profile (mean rating, 1=opinion … 7=objective fact): moral claims {mean_moral_objectivism:+.3f}, "
        f"taste/preference {mean_taste_objectivism:+.3f} over {profile_n} participant(s) with both reads scored."
    )
    lines.append("  -- the STATED probe is never pooled with the (deferred) revealed tolerance/language signatures (§13.5) --")
    if r6a is not None:
        lines.append(
            f"  R6a objectivism reliability (split-half odd/even, corr of the moral read)  r = {r6a['r']:+.3f}, "
            f"95% CI {_ci_str(r6a)}, n = {r6a['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {r6a['threshold_low']:.2f}, the higher bar): "
            f"{_met_glyph(r6a['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  R6a objectivism reliability: insufficient data (need ≥3 users scorable in both odd & even session halves)")
    if r6d is not None:
        lines.append(
            f"  R6d moral > taste objectivism (mean_i of the within-scale delta, cohort anchor)  "
            f"mean = {r6d['mean_delta']:+.3f}, 95% CI {_ci_str(r6d)}, n = {r6d['n_participants']}"
        )
        lines.append(
            f"     threshold (lower CI > {r6d['threshold']:.1f}, one-sided, directional): "
            f"{_met_glyph(r6d['pre_registered_threshold_met'])}  "
            f"(moral claims treated as more fact-like than matters of taste — Goodwin & Darley 2008)"
        )
    else:
        lines.append("  R6d moral > taste objectivism: insufficient data (need ≥3 users with both a moral and a taste read)")
    lines.append(
        "  Value-neutral (extra force — the branch is charged): holding morals as objective facts is NOT scored as "
        "better or worse than holding them as your own (objectivism = moral clarity OR rigid intolerance; subjectivism "
        "= tolerant pluralism OR standing for nothing — each pole dual-read, §20.4); the stance is described, never ranked. "
        "R6d is a cohort construct-validity anchor, not a per-person verdict. R6b (discriminant vs R2 sacredness / R1 "
        "centrality / value-content) and R6c (the stated–revealed meta-gap — the revealed tolerance/compromise + "
        "objectivist-language signatures) are deferred (cohort-coupled / κ-gated); see build-and-validate.md."
    )
    return "\n".join(lines)


def render_test_retest_result(
    name: str, threshold_text: str, results: dict[str, dict[str, Any]]
) -> str:
    if not results:
        return f"({name}: insufficient data — need ≥3 users present in both windows for any single domain)"
    lines = [f"{name}:", f"  Pre-registered threshold ({threshold_text})"]
    header = f"  {'domain':<26} {'r':>7} {'95% CI':>20} {'n':>4} {'met':>4}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for domain, res in sorted(results.items()):
        ci_str = (
            "nan" if res["ci_low"] != res["ci_low"]
            else f"[{res['ci_low']:+.3f}, {res['ci_high']:+.3f}]"
        )
        met = res.get("pre_registered_threshold_met")
        met_str = "✓" if met is True else ("✗" if met is False else "—")
        lines.append(
            f"  {domain:<26} {res['r']:+7.3f} {ci_str:>20} {res['n']:>4} {met_str:>4}"
        )
    return "\n".join(lines)


def render_gap_table(gaps: dict[tuple[str, str], dict[str, float]]) -> str:
    rows = sorted(gaps.items())
    if not rows:
        return "(no gaps computed — need ≥2 users per domain with both revealed and stated)"
    header = f"{'user_id':<24} {'domain':<26} {'z_revealed':>10} {'z_stated':>9} {'gap':>7}"
    out = [header, "-" * len(header)]
    for (user, domain), g in rows:
        out.append(
            f"{user:<24} {domain:<26} {g['z_revealed']:>+10.3f} "
            f"{g['z_stated_aspirational']:>+9.3f} {g['gap']:>+7.3f}"
        )
    return "\n".join(out)


def render_probe_table(grouped: dict[tuple[str, str], list[dict[str, Any]]]) -> str:
    """Per-probe break-points per user. Higher log_score = stronger virtue
    (sign-flipped at scoring time for inverted probes)."""
    rows: list[tuple[str, str, dict[str, Any]]] = []
    for (user, domain), probes in sorted(grouped.items()):
        for p in probes:
            rows.append((user, domain, p))
    if not rows:
        return "(no probe responses)"

    header = f"{'user_id':<24} {'domain':<26} {'probe_id':<22} {'log_score':>10} {'inv':>4}"
    out = [header, "-" * len(header)]
    for user, domain, p in rows:
        log_score_fmt = f"{p['log_score']:+.3f}"
        inv = " Y" if p["inverted"] else " N"
        out.append(
            f"{user:<24} {domain:<26} {str(p['probe_id']):<22} {log_score_fmt:>10} {inv:>4}"
        )
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log",
        type=Path,
        required=True,
        help="Path to a session-log JSON file (array of SessionLogEntry).",
    )
    parser.add_argument(
        "--tag-map",
        type=Path,
        default=DEFAULT_TAG_MAP,
        help=f"Path to the tag-axis CSV (default: {DEFAULT_TAG_MAP.relative_to(REPO_ROOT)}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of table.",
    )
    parser.add_argument(
        "--probes",
        type=Path,
        default=None,
        help="Optional path to a probe-responses JSON file (array of ProbeResponse).",
    )
    parser.add_argument(
        "--card-sort",
        type=Path,
        default=None,
        help="Optional path to a card-sort responses JSON file (compact or full format).",
    )
    parser.add_argument(
        "--pairwise",
        type=Path,
        default=None,
        help="Optional path to a pairwise-comparisons JSON file (compact format).",
    )
    parser.add_argument(
        "--hexaco",
        type=Path,
        default=None,
        help="Optional path to HEXACO-60 H scores per user (for H2 convergent validity).",
    )
    parser.add_argument(
        "--informant-hexaco",
        type=Path,
        default=None,
        help="Optional path to informant HEXACO-60 H ratings (for H4 informant convergent validity).",
    )
    parser.add_argument(
        "--big5",
        type=Path,
        default=None,
        help="Optional path to Big-5 N scores per user (for H7 discriminant validity).",
    )
    parser.add_argument(
        "--log-window-b",
        type=Path,
        default=None,
        help="Optional second session-log JSON (weeks 3-4) for H3 test-retest.",
    )
    parser.add_argument(
        "--probes-window-b",
        type=Path,
        default=None,
        help="Optional second probe-responses JSON (weeks 3-4) for H5 test-retest.",
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        default=None,
        help="Optional self-prediction calibration JSON (resolved prediction↔choice pairs) for H9.",
    )
    parser.add_argument(
        "--predictions-window-b",
        type=Path,
        default=None,
        help="Optional second predictions JSON (weeks 3-4) for the H9b test-retest split.",
    )
    parser.add_argument(
        "--context-log",
        type=Path,
        default=None,
        help="Optional context-tagged session log (context:* items) for H10 cross-situational consistency.",
    )
    parser.add_argument(
        "--circle-log",
        type=Path,
        default=None,
        help="Optional counterparty-tagged in-group session log (circle_radius + counterparty:* items) for H11 moral-circle radius.",
    )
    parser.add_argument(
        "--distance-map",
        type=Path,
        default=DEFAULT_DISTANCE_MAP,
        help="Counterparty→distance-bin ordering map for H11 (default: analysis/counterparty_distance_map_v0.1.csv).",
    )
    parser.add_argument(
        "--protected-log",
        type=Path,
        default=None,
        help="Optional cost-of-virtue log (value_slot + wave + taboo) for R2 sacred/protected values (§17).",
    )
    parser.add_argument(
        "--hypocrisy-log",
        type=Path,
        default=None,
        help="Optional self–other judgment log (severity_self + severity_other per matched act) for H12 moral hypocrisy (§18).",
    )
    parser.add_argument(
        "--identity-log",
        type=Path,
        default=None,
        help="Optional moral-identity-centrality log (per-item internalization + symbolization responses) for R1 (§19).",
    )
    parser.add_argument(
        "--objectivism-log",
        type=Path,
        default=None,
        help="Optional metaethical-objectivism log (per-item objectivism ratings, moral + taste claim types) for R6 (§20).",
    )
    parser.add_argument(
        "--min-items",
        type=int,
        default=3,
        help="Minimum items per session×domain for the session to score (default: 3).",
    )
    args = parser.parse_args()

    try:
        with args.log.open() as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR loading session log: {e}", file=sys.stderr)
        return 2

    if not isinstance(entries, list):
        print(f"ERROR: session log must be a JSON array, got {type(entries).__name__}", file=sys.stderr)
        return 2

    try:
        tag_map = load_tag_axis_map(args.tag_map)
    except FileNotFoundError:
        print(f"ERROR: tag-axis map not found at {args.tag_map}", file=sys.stderr)
        return 2

    grouped = session_aggregates(entries, tag_map)
    session_scores = session_means(grouped, min_items_per_session=args.min_items)
    user_scores = user_domain_means(session_scores)

    probe_grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    if args.probes:
        try:
            with args.probes.open() as f:
                probe_responses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading probe file: {e}", file=sys.stderr)
            return 2
        inversion_map = load_probe_inversion_map()
        ceiling_map = load_probe_ceiling_map()
        probe_grouped = probe_scores_by_user_domain(probe_responses, inversion_map, ceiling_map)

    cs_scores: dict[tuple[str, str, str], float] = {}
    if args.card_sort:
        try:
            with args.card_sort.open() as f:
                cs_responses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading card-sort file: {e}", file=sys.stderr)
            return 2
        value_domain = load_values_deck_domains()
        cs_scores = card_sort_scores(cs_responses, value_domain)

    hexaco_data: list[dict] = []
    if args.hexaco:
        try:
            with args.hexaco.open() as f:
                hexaco_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading HEXACO file: {e}", file=sys.stderr)
            return 2

    big5_data: list[dict] = []
    if args.big5:
        try:
            with args.big5.open() as f:
                big5_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading Big-5 file: {e}", file=sys.stderr)
            return 2

    informant_data: list[dict] = []
    if args.informant_hexaco:
        try:
            with args.informant_hexaco.open() as f:
                informant_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading informant-HEXACO file: {e}", file=sys.stderr)
            return 2

    pw_scores: dict[tuple[str, str, str], float] = {}
    if args.pairwise:
        try:
            with args.pairwise.open() as f:
                pw_responses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading pairwise file: {e}", file=sys.stderr)
            return 2
        if not args.card_sort:
            value_domain = load_values_deck_domains()
        pw_scores = pairwise_scores(pw_responses, value_domain)

    # If both card-sort and pairwise are supplied, compute the combined per §5.3
    combined_stated: dict[tuple[str, str, str], dict[str, Any]] = {}
    if cs_scores and pw_scores:
        combined_stated = combined_stated_score(cs_scores, pw_scores)

    # H2 convergent validity if hexaco supplied
    h2_result: dict[str, Any] | None = None
    if hexaco_data and user_scores:
        h2_result = compute_h2_convergent_validity(user_scores, hexaco_data)

    # H4 informant convergent validity if informant data supplied
    h4_result: dict[str, Any] | None = None
    if informant_data and user_scores:
        h4_result = compute_h4_informant_validity(user_scores, informant_data)

    # H7 discriminant validity if Big-5 N data supplied
    h7_result: dict[str, Any] | None = None
    if big5_data and user_scores:
        h7_result = compute_h7_discriminant_validity(user_scores, big5_data)

    # H3 test-retest reliability of revealed scores if window-B log supplied
    h3_result: dict[str, dict[str, Any]] = {}
    if args.log_window_b and user_scores:
        try:
            with args.log_window_b.open() as f:
                entries_b = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading window-B session log: {e}", file=sys.stderr)
            return 2
        grouped_b = session_aggregates(entries_b, tag_map)
        session_scores_b = session_means(grouped_b, min_items_per_session=args.min_items)
        user_scores_b = user_domain_means(session_scores_b)
        h3_result = compute_h3_test_retest_revealed(user_scores, user_scores_b)

    # H5 test-retest reliability of probes if window-B probes supplied
    h5_result: dict[str, dict[str, Any]] = {}
    if args.probes_window_b and probe_grouped:
        try:
            with args.probes_window_b.open() as f:
                probe_responses_b = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading window-B probe responses: {e}", file=sys.stderr)
            return 2
        inversion_map_b = load_probe_inversion_map()
        ceiling_map_b = load_probe_ceiling_map()
        probe_grouped_b = probe_scores_by_user_domain(probe_responses_b, inversion_map_b, ceiling_map_b)
        h5_result = compute_h5_test_retest_probes(probe_grouped, probe_grouped_b)

    # Pick the best-available stated layer for gap computation
    gaps: dict[tuple[str, str], dict[str, float]] = {}
    if user_scores:
        # Prefer combined; fall back to card-sort alone
        if combined_stated:
            asp_filtered = {
                (u, d): r["combined"]
                for (u, d, l), r in combined_stated.items()
                if l == "aspirational_self"
            }
            source = "combined"
        elif cs_scores:
            asp_filtered = {
                (u, d): s
                for (u, d, l), s in cs_scores.items()
                if l == "aspirational_self"
            }
            source = "card_sort"
        elif pw_scores:
            asp_filtered = {
                (u, d): s
                for (u, d, l), s in pw_scores.items()
                if l == "aspirational_self"
            }
            source = "pairwise"
        else:
            asp_filtered = {}
            source = "none"

        if asp_filtered:
            gaps = compute_gaps(user_scores, asp_filtered, stated_source=source)

    # H6 reuses the aspirational-stated layer used for the gap; computed
    # here so both JSON and text consumers see it
    h6_result: dict[str, Any] | None = None
    if gaps and asp_filtered:
        revealed_for_h6 = {k: v for k, v in user_scores.items() if k in asp_filtered}
        h6_result = compute_h6_stated_revealed_correlation(
            revealed_for_h6, asp_filtered
        )

    # H9 self-prediction calibration if predictions supplied. Self-contained on
    # its own fixtures (scoring.md §14) — does NOT read the H2-H7 cohort pipeline
    # above, so it never perturbs those results.
    h9a_result: dict[str, Any] | None = None
    h9b_result: dict[str, Any] | None = None
    h9c_result: dict[str, Any] | None = None
    h9_person_indices: dict[str, dict[str, Any]] = {}
    h9_cov: dict[str, Any] | None = None
    if args.predictions:
        try:
            predictions = load_predictions(args.predictions)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading predictions file: {e}", file=sys.stderr)
            return 2
        h9_axis_records = calibration_axis_records(predictions, tag_map)
        h9_person_indices = calibration_person_indices(h9_axis_records)
        h9a_result = compute_h9a_self_enhancement(h9_axis_records)
        h9c_result = compute_h9c_stakes_blindness(h9_axis_records)
        h9_cov = calibration_cov_records(predictions)
        if args.predictions_window_b:
            try:
                predictions_b = load_predictions(args.predictions_window_b)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"ERROR loading window-B predictions file: {e}", file=sys.stderr)
                return 2
            h9_axis_records_b = calibration_axis_records(predictions_b, tag_map)
            h9b_result = compute_h9b_stability(h9_axis_records, h9_axis_records_b)

    # H10 cross-situational consistency (scoring.md §15) if a context-tagged log
    # is supplied. Self-contained on its own fixture; Python-only this increment —
    # the on-device sd_i(c) reveal in poc-projection.js is deferred, so parity
    # stays green (same scope pattern as the H9 increment).
    h10a_result: dict[str, Any] | None = None
    h10c_result: dict[str, Any] | None = None
    h10_person_variability_n = 0
    h10_construct_sd_n = 0
    if args.context_log:
        try:
            with args.context_log.open() as f:
                context_entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading context log: {e}", file=sys.stderr)
            return 2
        if not isinstance(context_entries, list):
            print("ERROR: context log must be a JSON array", file=sys.stderr)
            return 2
        h10_records = context_item_records(context_entries, tag_map)
        h10_sd = context_sd_by_user_construct(h10_records)
        h10_construct_sd_n = len(h10_sd)
        h10_person_variability_n = len(variability_index_by_user(h10_sd))
        h10a_result = compute_h10a_reliability(h10_records)
        h10c_result = compute_h10c_observer_effect(h10_records)

    # H11 moral-circle radius (scoring.md §16) if a counterparty-tagged in-group
    # log is supplied. Self-contained on its own fixture; Python-only this
    # increment — the on-device R_i reveal in poc-projection.js is deferred, so
    # parity stays green (same scope pattern as H9/H10). Reads the circle_radius
    # secondary axis via the versioned counterparty→distance-bin ordering map (a
    # v0.1 DRAFT; its REL-2 inter-rater validation is Dave/human-gated).
    h11a_result: dict[str, Any] | None = None
    h11c_result: dict[str, Any] | None = None
    h11_person_shape_n = 0
    h11_radius_finite = 0
    h11_radius_censored = 0
    if args.circle_log:
        try:
            with args.circle_log.open() as f:
                circle_entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading circle log: {e}", file=sys.stderr)
            return 2
        if not isinstance(circle_entries, list):
            print("ERROR: circle log must be a JSON array", file=sys.stderr)
            return 2
        try:
            dist_map, _dist_labels = load_counterparty_distance_map(args.distance_map)
        except FileNotFoundError:
            print(f"ERROR: distance map not found at {args.distance_map}", file=sys.stderr)
            return 2
        h11_records = circle_item_records(circle_entries, tag_map, dist_map)
        h11_shapes = circle_shape_by_user(h11_records)
        h11_person_shape_n = len(h11_shapes)
        h11_radius_finite = sum(1 for s in h11_shapes.values() if not s["censored"])
        h11_radius_censored = sum(1 for s in h11_shapes.values() if s["censored"])
        h11a_result = compute_h11a_reliability(h11_records)
        h11c_result = compute_h11c_gradient(h11_records)

    # R2 sacred / protected values (scoring.md §17) if a cost-of-virtue log with
    # value_slot + wave (+ taboo) is supplied. Pure re-read of the `never` tail as
    # the protected set P_i (§13.2 censoring, categorical, never finitized).
    # Python-only this increment — the on-device protected-set reveal is deferred
    # (same scope pattern as H9/H10/H11), so parity stays green.
    r2a_result: dict[str, Any] | None = None
    r2b_result: dict[str, Any] | None = None
    r2_protected_set_n = 0
    r2_protected_none_n = 0
    r2_protected_set_sizes: list[int] = []
    if args.protected_log:
        try:
            with args.protected_log.open() as f:
                protected_responses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading protected-values log: {e}", file=sys.stderr)
            return 2
        if not isinstance(protected_responses, list):
            print("ERROR: protected-values log must be a JSON array", file=sys.stderr)
            return 2
        # First-wave protected-set census (per participant) for the reveal count.
        _psets, _pwaves = protected_value_sets(protected_responses)
        for _user in sorted(_pwaves):
            first_wave = sorted(_pwaves[_user])[0]
            size = len(_psets.get((_user, first_wave), set()))
            if size > 0:
                r2_protected_set_n += 1
                r2_protected_set_sizes.append(size)
            else:
                r2_protected_none_n += 1
        r2a_result = compute_r2a_reliability(protected_responses)
        r2b_result = compute_r2b_distinctness(protected_responses)

    # --- H12 moral hypocrisy: the self–other judgment asymmetry (§18). A paired
    # within-person contrast on a COMMON severity scale, so this is Python-only
    # and parity stays green — no on-device H_i reveal this increment (same scope
    # pattern as the H9b/H10b/H11b/R2c deferred halves).
    h12a_result: dict[str, Any] | None = None
    h12c_result: dict[str, Any] | None = None
    h12_person_asymmetry_n = 0
    h12_mean_asymmetry = 0.0
    if args.hypocrisy_log:
        try:
            with args.hypocrisy_log.open() as f:
                hypocrisy_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading hypocrisy log: {e}", file=sys.stderr)
            return 2
        if not isinstance(hypocrisy_records, list):
            print("ERROR: hypocrisy log must be a JSON array", file=sys.stderr)
            return 2
        _h12_census = hypocrisy_asymmetry_by_user(hypocrisy_records)
        h12_person_asymmetry_n = len(_h12_census)
        if _h12_census:
            h12_mean_asymmetry = sum(_h12_census.values()) / len(_h12_census)
        h12a_result = compute_h12a_reliability(hypocrisy_records)
        h12c_result = compute_h12c_self_serving(hypocrisy_records)

    # --- R1 moral identity centrality: the two-facet centrality read (§19). The
    # two facets are kept SEPARATE (never pooled, §13.5); the moderation legs (R1b —
    # centrality × the §6 gap / H10–H12) are cohort-coupled and DEFERRED. Python-only,
    # parity stays green — no on-device reveal this increment.
    r1a_result: dict[str, Any] | None = None
    r1c_result: dict[str, Any] | None = None
    r1_profile_n = 0
    r1_mean_internalization = 0.0
    r1_mean_symbolization = 0.0
    if args.identity_log:
        try:
            with args.identity_log.open() as f:
                identity_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading identity log: {e}", file=sys.stderr)
            return 2
        if not isinstance(identity_records, list):
            print("ERROR: identity log must be a JSON array", file=sys.stderr)
            return 2
        _r1_intern = centrality_facet_by_user(identity_records, "internalization")
        _r1_symbol = centrality_facet_by_user(identity_records, "symbolization")
        _r1_both = sorted(set(_r1_intern) & set(_r1_symbol))
        r1_profile_n = len(_r1_both)
        if _r1_both:
            r1_mean_internalization = sum(_r1_intern[u] for u in _r1_both) / len(_r1_both)
            r1_mean_symbolization = sum(_r1_symbol[u] for u in _r1_both) / len(_r1_both)
        r1a_result = compute_r1a_reliability(identity_records)
        r1c_result = compute_r1c_internalization_anchor(identity_records)

    # --- R6 moral conviction / metaethical objectivism: the STATED objectivism probe
    # read (§20). The stated probe is NEVER pooled with the (deferred, κ-gated) revealed
    # tolerance/compromise/language signatures (§13.5, load-bearing here); R6b (discriminant
    # vs R2/R1/content) and R6c (the stated–revealed meta-gap) are cohort-coupled / κ-gated
    # and DEFERRED. Python-only, parity stays green — no on-device reveal this increment.
    r6a_result: dict[str, Any] | None = None
    r6d_result: dict[str, Any] | None = None
    r6_profile_n = 0
    r6_mean_moral = 0.0
    r6_mean_taste = 0.0
    if args.objectivism_log:
        try:
            with args.objectivism_log.open() as f:
                objectivism_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading objectivism log: {e}", file=sys.stderr)
            return 2
        if not isinstance(objectivism_records, list):
            print("ERROR: objectivism log must be a JSON array", file=sys.stderr)
            return 2
        _r6_moral = objectivism_by_user(objectivism_records, "moral")
        _r6_taste = objectivism_by_user(objectivism_records, "taste")
        _r6_both = sorted(set(_r6_moral) & set(_r6_taste))
        r6_profile_n = len(_r6_both)
        if _r6_both:
            r6_mean_moral = sum(_r6_moral[u] for u in _r6_both) / len(_r6_both)
            r6_mean_taste = sum(_r6_taste[u] for u in _r6_both) / len(_r6_both)
        r6a_result = compute_r6a_reliability(objectivism_records)
        r6d_result = compute_r6d_moral_objectivism_anchor(objectivism_records)

    def _nan_to_none(v: float) -> float | None:
        return None if v != v else v

    def _correlation_json(r: dict[str, Any] | None) -> dict[str, Any] | None:
        if r is None:
            return None
        return {
            "r": r["r"],
            "ci_low": _nan_to_none(r["ci_low"]),
            "ci_high": _nan_to_none(r["ci_high"]),
            "n": r["n"],
            "pre_registered_threshold_met": r.get("pre_registered_threshold_met"),
            "threshold_low": r.get("threshold_low"),
            "threshold_high": r.get("threshold_high"),
        }

    def _per_domain_json(per_domain: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "domain": domain,
                "r": res["r"],
                "ci_low": _nan_to_none(res["ci_low"]),
                "ci_high": _nan_to_none(res["ci_high"]),
                "n": res["n"],
                "pre_registered_threshold_met": res.get("pre_registered_threshold_met"),
                "threshold": res.get("threshold"),
            }
            for domain, res in sorted(per_domain.items())
        ]

    if args.json:
        out: dict[str, Any] = {
            "revealed_scores": [
                {
                    "user_id": user,
                    "domain": domain,
                    "revealed_score_mean": s["mean"],
                    "n_sessions_contributing": s["n_sessions"],
                    "se": None if s["se"] != s["se"] else s["se"],
                    "ci_95_low": None if s["ci_low"] != s["ci_low"] else s["ci_low"],
                    "ci_95_high": None if s["ci_high"] != s["ci_high"] else s["ci_high"],
                }
                for (user, domain), s in sorted(user_scores.items())
            ]
        }
        if probe_grouped:
            out["probe_scores"] = [
                {
                    "user_id": user,
                    "domain": domain,
                    "probe_id": p["probe_id"],
                    "value_slot": p["value_slot"],
                    "log_score": p["log_score"],
                    "inverted": p["inverted"],
                    "first_accept_stake": p["first_accept_stake"],
                    "first_accept_rung": p["first_accept_rung"],
                }
                for (user, domain), probes in sorted(probe_grouped.items())
                for p in probes
            ]
        if cs_scores:
            out["card_sort_scores"] = [
                {
                    "user_id": user,
                    "domain": domain,
                    "layer": layer,
                    "frac_in_top5": score,
                }
                for (user, domain, layer), score in sorted(cs_scores.items())
            ]
        if gaps:
            out["gaps"] = [
                {
                    "user_id": user,
                    "domain": domain,
                    "z_revealed": g["z_revealed"],
                    "z_stated_aspirational": g["z_stated_aspirational"],
                    "gap": g["gap"],
                }
                for (user, domain), g in sorted(gaps.items())
            ]
        hypotheses: dict[str, Any] = {}
        if h2_result is not None:
            hypotheses["H2"] = _correlation_json(h2_result)
        if h3_result:
            hypotheses["H3"] = _per_domain_json(h3_result)
        if h4_result is not None:
            hypotheses["H4"] = _correlation_json(h4_result)
        if h5_result:
            hypotheses["H5"] = _per_domain_json(h5_result)
        if h6_result is not None:
            hypotheses["H6"] = {
                "r": h6_result["r"],
                "ci_low": _nan_to_none(h6_result["ci_low"]),
                "ci_high": _nan_to_none(h6_result["ci_high"]),
                "n": h6_result["n"],
                "in_pre_registered_range": h6_result.get("in_pre_registered_range"),
                "range_low": h6_result.get("range_low"),
                "range_high": h6_result.get("range_high"),
            }
        if h7_result is not None:
            hypotheses["H7"] = _correlation_json(h7_result)

        def _h9_json(r: dict[str, Any] | None) -> dict[str, Any] | None:
            if r is None:
                return None
            out_r = dict(r)
            for k in ("ci_low", "ci_high"):
                if k in out_r:
                    out_r[k] = _nan_to_none(out_r[k])
            return out_r

        h9_block: dict[str, Any] = {}
        if h9a_result is not None:
            h9_block["H9a"] = _h9_json(h9a_result)
        if h9b_result is not None:
            h9_block["H9b_stability"] = _h9_json(h9b_result)
        if h9c_result is not None:
            h9_block["H9c"] = _h9_json(h9c_result)
        if h9_cov is not None:
            h9_block["cov_channel"] = {
                "n_finite": h9_cov["n_finite"],
                "n_censored": h9_cov["n_censored"],
                "censored_categories": h9_cov["censored_categories"],
                "finite_mean_abs_e_price": h9_cov["finite_mean_abs_e_price"],
            }
        if h9_person_indices:
            h9_block["person_indices_n"] = len(h9_person_indices)
        if h9_block:
            hypotheses["H9"] = h9_block

        h10_block: dict[str, Any] = {}
        if h10a_result is not None:
            h10_block["H10a"] = _h9_json(h10a_result)
        if h10c_result is not None:
            h10_block["H10c"] = _h9_json(h10c_result)
        if h10_block or h10_construct_sd_n:
            h10_block["person_variability_n"] = h10_person_variability_n
            h10_block["n_construct_sd_cells"] = h10_construct_sd_n
            hypotheses["H10"] = h10_block

        h11_block: dict[str, Any] = {}
        if h11a_result is not None:
            h11_block["H11a"] = _h9_json(h11a_result)
        if h11c_result is not None:
            h11_block["H11c"] = _h9_json(h11c_result)
        if h11_block or h11_person_shape_n:
            h11_block["person_shape_n"] = h11_person_shape_n
            h11_block["radius_finite"] = h11_radius_finite
            h11_block["radius_censored"] = h11_radius_censored
            hypotheses["H11"] = h11_block

        r2_block: dict[str, Any] = {}
        if r2a_result is not None:
            r2_block["R2a"] = _h9_json(r2a_result)
        if r2b_result is not None:
            r2_block["R2b"] = _h9_json(r2b_result)
        if r2_block or r2_protected_set_n or r2_protected_none_n:
            r2_block["protected_set_n"] = r2_protected_set_n
            r2_block["protected_none_n"] = r2_protected_none_n
            r2_block["protected_set_sizes"] = r2_protected_set_sizes
            hypotheses["R2"] = r2_block

        h12_block: dict[str, Any] = {}
        if h12a_result is not None:
            h12_block["H12a"] = _h9_json(h12a_result)
        if h12c_result is not None:
            h12_block["H12c"] = _h9_json(h12c_result)
        if h12_block or h12_person_asymmetry_n:
            h12_block["person_asymmetry_n"] = h12_person_asymmetry_n
            h12_block["mean_asymmetry"] = _nan_to_none(h12_mean_asymmetry)
            hypotheses["H12"] = h12_block

        r1_block: dict[str, Any] = {}
        if r1a_result is not None:
            r1_block["R1a"] = _h9_json(r1a_result)
        if r1c_result is not None:
            r1_block["R1c"] = _h9_json(r1c_result)
        if r1_block or r1_profile_n:
            r1_block["profile_n"] = r1_profile_n
            # Two facets exposed SEPARATELY — no pooled "centrality" key (§13.5).
            r1_block["mean_internalization"] = _nan_to_none(r1_mean_internalization)
            r1_block["mean_symbolization"] = _nan_to_none(r1_mean_symbolization)
            hypotheses["R1"] = r1_block

        r6_block: dict[str, Any] = {}
        if r6a_result is not None:
            r6_block["R6a"] = _h9_json(r6a_result)
        if r6d_result is not None:
            r6_block["R6d"] = _h9_json(r6d_result)
        if r6_block or r6_profile_n:
            r6_block["profile_n"] = r6_profile_n
            # STATED probe only — moral and taste reads exposed SEPARATELY; no pooled
            # "objectivism_score"/"conviction" key, and never fused with the (deferred)
            # revealed tolerance/compromise/language signatures (§13.5, load-bearing).
            r6_block["mean_moral_objectivism"] = _nan_to_none(r6_mean_moral)
            r6_block["mean_taste_objectivism"] = _nan_to_none(r6_mean_taste)
            hypotheses["R6"] = r6_block

        if hypotheses:
            out["hypotheses"] = hypotheses
        print(json.dumps(out, indent=2))
    else:
        print(render_table(user_scores))
        if probe_grouped:
            print()
            print("Cost-of-virtue probe break-points (higher = stronger virtue, inv-flipped):")
            print(render_probe_table(probe_grouped))
        if cs_scores:
            print()
            print("Card-sort stated scores per domain × layer (fraction of in-domain values in top-5):")
            print(render_card_sort_table(cs_scores))
        if pw_scores:
            print()
            print("Bradley-Terry stated scores per domain × layer (mean β across in-domain values):")
            print(render_pairwise_table(pw_scores))
        if gaps:
            print()
            print("Per-domain gaps (z_stated_aspirational − z_revealed, standardized per-domain):")
            print(render_gap_table(gaps))
        if h2_result is not None:
            print()
            print(render_correlation_result(
                "H2 (revealed truth-telling × HEXACO self-report H)",
                "lower 95% CI ≥ 0.15",
                h2_result,
            ))
            print(
                "  Note: with synthetic small samples the CI is narrow because\n"
                "  the fixture data was designed to track. n≈200 is where this is real."
            )
        if h4_result is not None:
            print()
            print(render_correlation_result(
                "H4 (revealed truth-telling × averaged informant HEXACO H)",
                "point estimate r ≥ 0.20",
                h4_result,
            ))
        if h7_result is not None:
            print()
            print(render_correlation_result(
                "H7 (revealed truth-telling × Big-5 neuroticism, DISCRIMINANT)",
                "upper 95% CI ≤ 0.40",
                h7_result,
            ))
        if h3_result:
            print()
            print(render_test_retest_result(
                "H3 (revealed score test-retest, weeks 1-2 vs 3-4)",
                "lower 95% CI ≥ 0.60",
                h3_result,
            ))
        if h5_result:
            print()
            print(render_test_retest_result(
                "H5 (cost-of-virtue probe test-retest, weeks 1-2 vs 3-4)",
                "lower 95% CI ≥ 0.50",
                h5_result,
            ))
        if h6_result is not None:
            print()
            print(render_h6_result(h6_result))
        if any(x is not None for x in (h9a_result, h9b_result, h9c_result)) or h9_cov is not None:
            print()
            print(render_h9_result(
                h9a_result, h9b_result, h9c_result, h9_cov, len(h9_person_indices)
            ))
        if h10a_result is not None or h10c_result is not None or h10_construct_sd_n:
            print()
            print(render_h10_result(
                h10a_result, h10c_result, h10_person_variability_n, h10_construct_sd_n
            ))
        if h11a_result is not None or h11c_result is not None or h11_person_shape_n:
            print()
            print(render_h11_result(
                h11a_result, h11c_result, h11_person_shape_n,
                h11_radius_finite, h11_radius_censored,
            ))
        if r2a_result is not None or r2b_result is not None or r2_protected_set_n or r2_protected_none_n:
            print()
            print(render_r2_result(
                r2a_result, r2b_result, r2_protected_set_n,
                r2_protected_none_n, r2_protected_set_sizes,
            ))
        if h12a_result is not None or h12c_result is not None or h12_person_asymmetry_n:
            print()
            print(render_h12_result(
                h12a_result, h12c_result, h12_person_asymmetry_n, h12_mean_asymmetry,
            ))
        if r1a_result is not None or r1c_result is not None or r1_profile_n:
            print()
            print(render_r1_result(
                r1a_result, r1c_result, r1_profile_n,
                r1_mean_internalization, r1_mean_symbolization,
            ))
        if r6a_result is not None or r6d_result is not None or r6_profile_n:
            print()
            print(render_r6_result(
                r6a_result, r6d_result, r6_profile_n,
                r6_mean_moral, r6_mean_taste,
            ))

    return 0


if __name__ == "__main__":
    sys.exit(main())
