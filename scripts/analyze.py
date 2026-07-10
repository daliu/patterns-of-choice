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
- A3 moral-language channel — the coder + the κ gate (§21 of scoring.md,
  h-a3-moral-language.md; a THIRD channel on values, distinct from the elicited-stated
  inventory and revealed behavior). When --language-log is supplied (free-text
  utterances + gold_foundations reference codes): a DETERMINISTIC MFD-style foundation
  coder (v0.1 DRAFT `word*`-wildcard lexicon — care/fairness/loyalty/authority/sanctity/
  liberty), Cohen's κ inter-rater validation of the coder vs. gold, and the
  foundation_i(f) invocation-rate profile. THE BINDING GATE: the whole channel is
  DESCRIPTIVE/EXPLORATORY-ONLY until κ ≥ 0.70 vs. REAL human gold (~200 codes, 50/domain
  × 2 raters — Dave/human-gated); synthetic κ certifies only the machinery (promotable is
  always False). Value-neutral (§21.4): the coder assigns foundation LABELS, never ranks
  them, never emits a scalar score; more moral language is not better; fluency ≠ virtue;
  declining to moralize is a Dancy particularist move, not a deficient zero. κ is a
  coder-PAIR reliability statistic, never a person score (§13.5). NOT parity-gated BY
  DESIGN — LLM coding is non-deterministic, deliberately outside the poc-projection ↔
  analyze.py parity contract (§1.5). The framing ratio, the third ordering L_i + the
  three S/R/L concordances (extending §13.4), and H-A3a/b/c are cohort/κ-gated, DEFERRED.
- A4 decision conflict — the PROCESS channel (§22 of scoring.md, h-a4-a5-process-emotion.md
  Part 1; the dynamics that SURROUND a choice, not the choice itself). When --process-log is
  supplied (per-item response_time_ms + prompt_chars + presented_position across ≥2 sessions):
  conflict(i, domain) = the within-person z-score of response time, RESIDUALIZED on reading-load
  (prompt_chars) + presented position, with timeouts and the TIMED quick-fire set (CV-1)
  EXCLUDED, z within-person (people read at different speeds). A4a reliability = split-half
  odd/even per-domain test–retest, lower CI ≥ 0.40 (the exploratory bar). THE LOAD-BEARING
  DISCIPLINE (Bago & De Neys 2019): conflict is EFFORT/ambivalence, FULL STOP — never a moral
  framework read (slow ≠ deontological, fast ≠ utilitarian; concept.md disclaims the Greene
  fast/slow mapping). Value-neutral (§3): effort is not graded (effortful virtue arguably the
  STRONGER signal). RT-ONLY (answer-revision capture Dave/runtime-gated, §4 Q1); an analysis
  adjunct with NO public card (§1.4). Parity-gated in principle; the on-device conflict reveal +
  its JS parity lock are DEFERRED this increment (as the H9–R6 on-device reveals are). A4b
  (conflict adds information beyond the choice) is cohort-coupled, DEFERRED.
- H8 narrative immersion — the COHORT secondary channel (§9 of scoring.md, h8-narrative-immersion-
  design.md; does an established-arc "narrative" form of a moral choice pull behaviour toward stated
  values vs a structurally-equivalent quick-fire "abstract" form?). When --h8-log is supplied (per-form
  primary_axis_score + stated_aspirational, paired via scenarios/h8-probe-pairs.json): H8a debiasing
  (low-stakes) correlates per-participant mean D = z(r_narr)−z(r_abs) with the stated−revealed gap
  z(stated)−z(r_abs); confirmatory rho_8a lower CI ≥ 0.15, POSITIVE (§6 convention; reconciles the
  design-doc's one-line "negative" which assumed revealed−stated). THE LOAD-BEARING DISCIPLINE (§9.2):
  D and gap SHARE r_abs, inflating their correlation under the null (regression to the mean), so the
  headline is CONJOINED with a de-coupled Frisch–Waugh–Lovell partial (r_narr·stated | r_abs) that must
  be positive — SUPPORTED only if both AGREE. COHORT property, NEVER a per-person reveal and never a
  gate-criterion (§9.5) → no on-device projection (parity stays green), no public card. H8b (attachment-
  laden shift, §9.4) needs the §9.3 per-character attachment instrument and is DEFERRED.

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
DEFAULT_H8_MANIFEST = REPO_ROOT / "scenarios" / "h8-probe-pairs.json"
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

# H9b DISCRIMINANT half (§14.4) — the deferred sibling of the stability half above.
# Regress the self-prediction error MAGNITUDE cal_error_i on [ gap_i, revealed_level_i ]
# (the aspirational stated−revealed gap and the revealed behavioral level, both from the
# §6/§3 cohort pipeline). Self-knowledge is a DISTINCT construct — NOT reducible to "how
# much you over-claim" + "how virtuous you are" — iff the UPPER 95% bootstrap CI of the
# model R² < H9B_R2_CEILING (the calibration axis carries variance those two predictors
# do not). PROPOSED locks (DECISIONS §19); the analyzer reports met/not-met, never gates.
H9B_R2_CEILING = 0.50          # discriminant: UPPER 95% CI of cal_error~[gap,revealed_level] R² must clear this
H9B_MIN_PARTICIPANTS = 8       # ≥8 users with gap + revealed_level + cal_error before a 2-predictor R² is stable
H9B_SEED_OFFSET = 28           # bootstrap seed band for the R² CI (A4A 25, H8A 26, H11B 27; next free)


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

    NOTE — the DISCRIMINANT half of H9b (regress cal_error on [gap,
    revealed_level], R² upper CI < 0.50) is compute_h9b_discriminant below: it
    couples calibration to the §3/§6 cohort pipeline (per-user gap + revealed
    level), so it reads a combined --h9b-log rather than the isolated
    --predictions fixture this stability half uses.
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


def _h9b_person_predictors(
    session_entries: list[dict],
    card_sort_responses: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, dict[str, float]]:
    """The [gap_i, revealed_level_i] predictor pair for the H9b discriminant (§14.4),
    built from the SAME §3/§6 cohort primitives the main analyzer uses — so the parity-
    locked item_score, the §10 inattentive drop and the ≥3-items-per-session floor apply
    identically:

        revealed_means = user_domain_means(session_means(session_aggregates(...)))   (§3)
        stated_layer   = card_sort_scores(...)[aspirational_self]                      (§5.1)
        gaps           = compute_gaps(revealed_means, stated_layer)                    (§6)
        gap_i            = mean_d gap(i, d)          (how much a person OVER-CLAIMS)
        revealed_level_i = mean_d z_revealed(i, d)   (their revealed behavioral LEVEL)

    Both predictors ride the per-domain z-scores compute_gaps already emits, so gap and
    revealed_level share the cohort-standardized scale. Returns {user: {gap, revealed}}."""
    revealed_means = user_domain_means(session_means(session_aggregates(session_entries, tag_map)))
    value_domain = load_values_deck_domains()
    cs_scores = card_sort_scores(card_sort_responses, value_domain)
    stated_layer = {
        (u, d): s for (u, d, layer), s in cs_scores.items() if layer == "aspirational_self"
    }
    gaps = compute_gaps(revealed_means, stated_layer, stated_source="card_sort")
    by_gap: dict[str, list[float]] = defaultdict(list)
    by_rev: dict[str, list[float]] = defaultdict(list)
    for (user, _domain), r in gaps.items():
        by_gap[user].append(r["gap"])
        by_rev[user].append(r["z_revealed"])
    return {
        user: {
            "gap": sum(by_gap[user]) / len(by_gap[user]),
            "revealed": sum(by_rev[user]) / len(by_rev[user]),
        }
        for user in by_gap
    }


def compute_h9b_discriminant(
    session_entries: list[dict],
    card_sort_responses: list[dict],
    predictions: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, Any] | None:
    """H9b — the self-CALIBRATION DISCRIMINANT (§14.4), the deferred sibling of the H9b
    stability half. Regress the self-prediction error MAGNITUDE cal_error_i (mean_p |pred−rev|
    over a person's axis-channel probes, §14.2) on [ gap_i, revealed_level_i ] (their
    aspirational over-claim and their revealed behavioral level, §6/§3); self-knowledge is
    a DISTINCT construct — NOT reducible to how much a person over-claims plus how virtuous
    they are — iff the UPPER 95% bootstrap CI of the model R² < H9B_R2_CEILING (the calibration
    axis carries variance those two predictors do not; Dunning 2005 — self-insight dissociates
    from both self-idealization and trait level). Completes H9b = stability ∧ discriminant.

    cal_error is the MAGNITUDE from the SEPARATE prediction channel, NOT a signed echo of
    stated−revealed: were the outcome the signed cal_bias_i under predictions that merely
    parrot the card-sort aspiration (pred≈stated, rev≈revealed), cal_bias would be an EXACT
    affine function of [gap, revealed_level] (within-domain z is affine) → R² ≡ 1 → the
    discriminant would falsely FAIL. check_h9b_discriminant_lock demonstrates exactly that
    trap. COHORT-level statistic, NEVER a per-person reveal: cal_error_i, gap_i and
    revealed_level_i stay separate facets, never pooled (§13.5). Seed BOOTSTRAP_SEED+28."""
    predictors_by_user = _h9b_person_predictors(session_entries, card_sort_responses, tag_map)
    cal = calibration_person_indices(calibration_axis_records(predictions, tag_map))
    rows: list[tuple[float, float, float]] = []
    for user in sorted(set(predictors_by_user) & set(cal)):
        gap = predictors_by_user[user]["gap"]
        rev = predictors_by_user[user]["revealed"]
        cal_error = cal[user]["cal_error"]
        if gap != gap or rev != rev or cal_error != cal_error:
            continue
        rows.append((gap, rev, cal_error))   # predictors = [gap, revealed_level]; y = cal_error
    if len(rows) < H9B_MIN_PARTICIPANTS:
        return None
    predictors = [[r[0] for r in rows], [r[1] for r in rows]]
    y = [r[2] for r in rows]
    r2 = _ols_r_squared(predictors, y)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + H9B_SEED_OFFSET))
    supported = None if ci_high != ci_high else bool(ci_high < H9B_R2_CEILING)
    # Descriptive companions (reported, NOT the gate): cal_error's bare correlation with each
    # predictor alone, so a reader sees WHICH predictor (if any) carries the leakage — without
    # pooling anything per person.
    cal_gap_r = _pearson_r([r[0] for r in rows], y)
    cal_revealed_r = _pearson_r([r[1] for r in rows], y)
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": H9B_R2_CEILING,
        "cal_gap_r": cal_gap_r,
        "cal_revealed_r": cal_revealed_r,
        "n_participants": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
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
# H10b DISCRIMINANT (§1.3), the deferred sibling of the H10a reliability + H10c observer
# halves. Cross-situational moral CONSISTENCY is a DISTINCT construct — NOT reducible to how
# HIGH a person scores (level), how much they over-claim (the §6 aspirational gap), or how
# poorly they know themselves (the §14.2 self-prediction error). TWO criteria, BOTH required:
#  (1) MAIN — regress V_i on [level_i, gap_i, cal_error_i]; supported iff the UPPER 95%
#      bootstrap CI of that R² < H10B_R2_CEILING (the context-variance channel carries variance
#      none of the three explain; Fleeson 2001 density-distributions vs Mischel & Shoda 1995
#      if-then signatures vs Doris 2002 situationism).
#  (2) DE-CONFOUND — regress each cell's sd_i(c) on |mbar_i(c)|; supported iff the upper 95%
#      CI of THAT R² < H10B_R2_CEILING too, proving the within-person variability is not merely
#      a mid-scale RANGE artifact (a person parked near 0 has more headroom to vary than one
#      pinned at an axis extreme). Cell-level → a pseudo-replication caveat (documented, not
#      gated); it is a descriptive de-confound on the same 0.50 ceiling, never a per-person score.
# Supported iff BOTH agree. Like the H12b/R6b discriminants there is NO algebraic trap: V_i
# rides the context-variance channel, not an affine echo of level/gap/cal_error, so the lock is
# honestly two-sided. PROPOSED locks (DECISIONS §19); the analyzer reports met/not-met, never gates.
H10B_R2_CEILING = 0.50          # BOTH the discriminant AND the de-confound upper 95% CI must clear this
H10B_MIN_PARTICIPANTS = 8       # ≥8 users with V_i + level + gap + cal_error before a 3-predictor R² is stable
H10B_MIN_DECONF_CELLS = 8       # ≥8 (user×construct) sd cells before the sd~|mbar| range-artifact R² is stable
H10B_SEED_OFFSET = 31           # bootstrap seed band for the main discriminant R² CI (R6B 30; next free)
H10B_DECONF_SEED_OFFSET = 32    # bootstrap seed band for the de-confound sd~|mbar| R² CI


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


def _context_cells(
    records: list[dict[str, Any]],
    session_ok=None,
) -> dict[tuple[str, str], tuple[float, float, int]]:
    """The single §1.5-floor implementation every H10 census rides: per
    (user, domain) cell, (sd_i(c), mbar_i(c), n_qualifying_contexts). A context
    enters with ≥H10_ITEMS_PER_CONTEXT_MIN items, a construct survives with
    ≥H10_CONTEXT_MIN qualifying contexts — else the cell is SUPPRESSED (absent).
    `session_ok(user, session)` optionally restricts to a session subset."""
    cell: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for r in records:
        if session_ok is not None and not session_ok(r["user"], r["session"]):
            continue
        cell[(r["user"], r["domain"], r["context"])].append(r["score"])
    ctx_mean: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (user, domain, _ctx), scores in cell.items():
        if len(scores) >= H10_ITEMS_PER_CONTEXT_MIN:
            ctx_mean[(user, domain)].append(sum(scores) / len(scores))
    out: dict[tuple[str, str], tuple[float, float, int]] = {}
    for (user, domain), means in ctx_mean.items():
        if len(means) >= H10_CONTEXT_MIN:
            out[(user, domain)] = (_sample_sd(means), sum(means) / len(means), len(means))
    return out


def context_sd_mbar_by_user_construct(
    records: list[dict[str, Any]],
    session_ok=None,
) -> dict[tuple[str, str], tuple[float, float]]:
    """Both sd_i(c) AND mbar_i(c) per (user, domain) cell (§1.1): sd = the
    cross-context SD of the context-means r_i(c,k); mbar = the GRAND MEAN over
    those same context-means (the construct's level). Identical suppression floors
    to context_sd_by_user_construct, so the two agree exactly on which cells
    survive: a context enters with ≥H10_ITEMS_PER_CONTEXT_MIN items, a construct
    with ≥H10_CONTEXT_MIN qualifying contexts (§1.5). Powers the H10b discriminant
    (level_i = mean_c mbar) and its range-artifact de-confound (sd vs |mbar|).
    `session_ok(user, session)` optionally restricts to a session subset.
    Derived from _context_cells (drops the count leg), so every census shares
    one floor implementation bit-for-bit."""
    return {
        k: (sd, mbar) for k, (sd, mbar, _n)
        in _context_cells(records, session_ok).items()
    }


def context_sd_by_user_construct(
    records: list[dict[str, Any]],
    session_ok=None,
) -> dict[tuple[str, str], float]:
    """sd_i(c): per (user, domain) cross-context SD of the context-means r_i(c,k)
    (§1.1). A context enters only with ≥H10_ITEMS_PER_CONTEXT_MIN items; a
    construct yields an sd only with ≥H10_CONTEXT_MIN qualifying contexts (§1.5),
    else it is SUPPRESSED (omitted). `session_ok(user, session)` optionally
    restricts to a session subset (the H10a odd/even split). Derived from
    context_sd_mbar_by_user_construct (drops the mbar leg), so the two share
    identical suppression floors bit-for-bit."""
    return {
        k: sd for k, (sd, _mbar)
        in context_sd_mbar_by_user_construct(records, session_ok).items()
    }


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


def context_profile_by_user(
    records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """The §15.5 N=1 reveal census: per user, the QUALIFYING per-construct
    sd_i(c) facets ({domain, sd, n_contexts}, domain-sorted) plus the
    within-branch V_i — None below the ≥H10_CONSTRUCT_MIN floor, in which case
    the per-construct facets still reveal on their own (§1.5). Floors are
    bit-for-bit those of context_sd_by_user_construct (both ride
    _context_cells). V_i is the §15.1 within-branch mean of this branch's own
    sd facets, reported ALONGSIDE them — never a cross-branch composite
    (§13.5), and steadiness↔responsiveness is never ranked. The shape
    poc-projection.js mirrors under the §15.7 parity lock."""
    cells = _context_cells(records)
    v_by_user = variability_index_by_user(
        {k: sd for k, (sd, _mbar, _n) in cells.items()}
    )
    profiles: dict[str, dict[str, Any]] = {}
    for (user, domain), (sd, _mbar, n_ctx) in sorted(cells.items()):
        p = profiles.setdefault(user, {"constructs": []})
        p["constructs"].append({"domain": domain, "sd": sd, "n_contexts": n_ctx})
    for u, p in profiles.items():
        p["n_constructs"] = len(p["constructs"])
        p["v"] = v_by_user.get(u)   # None ⇔ below the ≥3-construct floor (§1.5)
    return profiles


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


def compute_h10b_discriminant(
    context_entries: list[dict],
    session_entries: list[dict],
    card_sort_responses: list[dict],
    predictions: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, Any] | None:
    """H10b — the cross-situational-consistency DISCRIMINANT (§1.3), the deferred sibling of
    the H10a reliability and H10c observer-effect halves. TWO criteria that must BOTH agree:

    (1) MAIN discriminant — regress the person variability index V_i (§1.1, mean_c sd_i(c)) on
    [ level_i = mean_c mbar_i(c), gap_i (the §6 aspirational stated−revealed over-claim),
    cal_error_i (the §14.2 self-prediction error MAGNITUDE) ]; consistency is a DISTINCT
    construct — NOT reducible to how high a person scores + how much they over-claim + how
    poorly they know themselves — iff the UPPER 95% bootstrap CI of the model R² <
    H10B_R2_CEILING (the cross-context variability channel carries variance none of level,
    over-claim, or self-insight explains; Fleeson 2001 density-distributions vs Mischel & Shoda
    1995 if-then signatures vs Doris 2002 situationism).

    (2) Residual-variability DE-CONFOUND — regress each (user, construct) cell's sd_i(c) on
    |mbar_i(c)|, supported iff the upper 95% CI of THAT R² < H10B_R2_CEILING too: the
    within-person variability is NOT merely a mid-scale RANGE artifact (a person whose construct
    mean sits near 0 has more headroom to vary than one pinned near an axis extreme). Cell-level,
    so it carries a pseudo-replication caveat (multiple cells per person) — documented, NOT
    gated; a descriptive de-confound on the SAME 0.50 ceiling, never a per-person score.

    Supported iff BOTH criteria hold. NO algebraic trap — by design: V_i is measured on the
    context-variance channel (§1.1), NOT an affine echo of level/gap/cal_error, so the lock is
    honestly two-sided (check_h10b_discriminant_lock exercises the main leg AND the de-confound
    on real-pipeline corpora, and confirms BOTH are load-bearing). COHORT-level statistic, NEVER
    a per-person reveal: V_i, level_i, gap_i, cal_error_i and each sd/|mbar| cell stay separate
    facets, never pooled (§13.5). Seeds BOOTSTRAP_SEED+31 (main) / +32 (de-confound)."""
    records = context_item_records(context_entries, tag_map)
    sd_mbar = context_sd_mbar_by_user_construct(records)
    v_by_user = variability_index_by_user({k: sd for k, (sd, _m) in sd_mbar.items()})
    # level_i = mean_c mbar_i(c) over the SAME qualifying constructs that form V_i (same floor).
    mbar_acc: dict[str, list[float]] = defaultdict(list)
    for (user, _domain), (_sd, mbar) in sd_mbar.items():
        mbar_acc[user].append(mbar)
    level_by_user = {
        u: sum(ms) / len(ms) for u, ms in mbar_acc.items() if len(ms) >= H10_CONSTRUCT_MIN
    }
    predictors_by_user = _h9b_person_predictors(session_entries, card_sort_responses, tag_map)
    cal = calibration_person_indices(calibration_axis_records(predictions, tag_map))
    rows: list[tuple[float, float, float, float]] = []
    for user in sorted(set(v_by_user) & set(level_by_user) & set(predictors_by_user) & set(cal)):
        v = v_by_user[user]
        level = level_by_user[user]
        gap = predictors_by_user[user]["gap"]
        cal_error = cal[user]["cal_error"]
        if v != v or level != level or gap != gap or cal_error != cal_error:
            continue
        rows.append((level, gap, cal_error, v))   # predictors = [level, gap, cal_error]; y = V_i
    if len(rows) < H10B_MIN_PARTICIPANTS:
        return None
    predictors = [[r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]]
    y = [r[3] for r in rows]
    r2 = _ols_r_squared(predictors, y)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + H10B_SEED_OFFSET))
    disc_met = None if ci_high != ci_high else bool(ci_high < H10B_R2_CEILING)
    # Descriptive companions (reported, NOT the gate): V_i's bare correlation with each
    # predictor alone, so a reader sees WHICH predictor (if any) carries leakage — no pooling.
    v_level_r = _pearson_r([r[0] for r in rows], y)
    v_gap_r = _pearson_r([r[1] for r in rows], y)
    v_cal_error_r = _pearson_r([r[2] for r in rows], y)

    # (2) DE-CONFOUND: regress each surviving cell's sd on |mbar| (the range-artifact check).
    deconf_rows: list[tuple[float, float]] = [
        (abs(mbar), sd) for (sd, mbar) in sd_mbar.values() if sd == sd
    ]
    deconf_r2 = None
    deconf_ci_low = deconf_ci_high = float("nan")
    deconf_met: bool | None = None
    deconf_sd_absmbar_r = None
    if len(deconf_rows) >= H10B_MIN_DECONF_CELLS:
        deconf_r2 = _ols_r_squared([[r[0] for r in deconf_rows]], [r[1] for r in deconf_rows])
        if deconf_r2 is not None:
            deconf_ci_low, deconf_ci_high = _bootstrap_ci_r2(
                deconf_rows, random.Random(BOOTSTRAP_SEED + H10B_DECONF_SEED_OFFSET)
            )
            deconf_met = (
                None if deconf_ci_high != deconf_ci_high
                else bool(deconf_ci_high < H10B_R2_CEILING)
            )
            deconf_sd_absmbar_r = _pearson_r([r[0] for r in deconf_rows], [r[1] for r in deconf_rows])
    # Overall support requires BOTH the discriminant AND the de-confound to clear the ceiling.
    supported = (
        None if disc_met is None or deconf_met is None else bool(disc_met and deconf_met)
    )
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": H10B_R2_CEILING,
        "v_level_r": v_level_r,
        "v_gap_r": v_gap_r,
        "v_cal_error_r": v_cal_error_r,
        "discriminant_met": disc_met,
        "deconf_r2": deconf_r2,
        "deconf_r2_ci_low": deconf_ci_low,
        "deconf_r2_ci_high": deconf_ci_high,
        "deconf_sd_absmbar_r": deconf_sd_absmbar_r,
        "deconf_n_cells": len(deconf_rows),
        "deconf_met": deconf_met,
        "n_participants": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
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
H11B_R2_CEILING = 0.50          # discriminant (§1.3): UPPER 95% CI of the shape~[near,generosity] R² must clear this
H11B_MIN_PARTICIPANTS = 8       # ≥8 shapes with a generosity read before a 2-predictor R² is stable
H11B_SEED_OFFSET = 27           # bootstrap seed band for the R² CI (A4A used 25, H8A 26; +17..24 taken)
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


def _resource_allocation_generosity(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
    domain: str = "resource-allocation",
) -> dict[str, float]:
    """Per-user EXTERNAL generosity level for the H11b discriminant (§3.2): the §3.1
    revealed-mean pipeline (session_aggregates → session_means → average the per-session
    means) restricted to the resource-allocation domain, scored on its `generosity`
    primary axis by the SAME item_score every channel uses (so the §10 inattentive drop
    and the ≥3-items-per-session floor apply identically). This is a SEPARATE revealed
    measure, NOT the circle mean — see compute_h11b_discriminant for why that distinction
    is load-bearing."""
    means = session_means(session_aggregates(entries, tag_map))
    per_user: dict[str, list[float]] = defaultdict(list)
    for (user, _session, dom), m in means.items():
        if dom == domain:
            per_user[user].append(m)
    return {u: sum(v) / len(v) for u, v in per_user.items()}


def compute_h11b_discriminant(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
    dist_map: dict[str, int],
) -> dict[str, Any] | None:
    """H11b — the moral-circle SHAPE DISCRIMINANT (§1.3). Regress the shape slope β_i
    (parochialism steepness) on [ near-bin concern_i, a SEPARATE resource-allocation
    generosity level_i (§3.2) ]; the circle shape is DISCRIMINABLE from generosity iff
    the UPPER 95% bootstrap CI of the model R² < H11B_R2_CEILING — i.e. at least half the
    shape variance is NOT explained by how generous a person is ("reach is not height": a
    person can be lavish to kin then drop off a cliff — narrow — or modest but flat — wide;
    Crimston et al. 2016, the moral-expansiveness shape is dissociable from generosity).
    Completes H11 = H11a ∧ H11b.

    Generosity is the EXTERNAL revealed measure, NOT the circle mean: were it the circle
    mean, β_i (an OLS slope over the same bins) would be a MECHANICAL function of the
    predictors and R²→1, so the discriminant would falsely FAIL — check_h11b_discriminant_lock
    demonstrates exactly this. COHORT-level statistic, NEVER a per-person reveal: no pooled
    circle score is emitted; β_i and generosity_i stay separate facets (§13.5). Seed
    BOOTSTRAP_SEED+27."""
    shapes = circle_shape_by_user(circle_item_records(entries, tag_map, dist_map))
    generosity = _resource_allocation_generosity(entries, tag_map)
    rows: list[tuple[float, float, float]] = []
    for user in sorted(set(shapes) & set(generosity)):
        beta = shapes[user]["beta"]
        near = shapes[user]["near_concern"]
        gen = generosity[user]
        if beta != beta or near != near or gen != gen:
            continue
        rows.append((near, gen, beta))   # predictors = [near, generosity]; y = beta
    if len(rows) < H11B_MIN_PARTICIPANTS:
        return None
    predictors = [[r[0] for r in rows], [r[1] for r in rows]]
    y = [r[2] for r in rows]
    r2 = _ols_r_squared(predictors, y)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + H11B_SEED_OFFSET))
    supported = None if ci_high != ci_high else bool(ci_high < H11B_R2_CEILING)
    # Descriptive companions (reported, NOT the gate): β's bare correlations with each
    # predictor alone, so a reader sees WHICH predictor (if any) carries the leakage —
    # without pooling anything per person.
    beta_generosity_r = _pearson_r([r[1] for r in rows], y)
    beta_near_r = _pearson_r([r[0] for r in rows], y)
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": H11B_R2_CEILING,
        "beta_generosity_r": beta_generosity_r,
        "beta_near_r": beta_near_r,
        "n_participants": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
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
# pipeline (like the H9b/H11b deferred halves). This re-reads the cov break-point
# PRIMITIVE (already parity-locked; the runtime emits per-slot no_break_point at
# poc-projection.js:212) without changing it; the on-device P_i reveal is
# protectedValues in poc-projection.js, mirroring protected_profile_by_user
# under the §17.7 parity lock.
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


def protected_profile_by_user(
    responses: list[dict],
    wave_of=lambda r: r.get("wave"),
) -> dict[str, dict[str, Any]]:
    """Per-user FIRST-WAVE professed-protected-set profile — the §17.5 N=1 reveal
    census (and the shape protectedValues in poc-projection.js mirrors under the
    §17.7 parity lock). For every user with ≥1 probed wave:
        {"wave": first wave, "professed": sorted value_slot strings marked `never`,
         "n_professed": …, "n_slots_probed": distinct slots probed that wave}
    `professed` holds value-slot STRINGS, never prices (§13.2 — the categorical
    right-censored tail, never finitized); the key name carries the §17.5
    cheap-talk caveat (PROFESSED, not validated against a real offer). An EMPTY
    set is DATA (every probed value has a price at some stake), not suppression —
    set membership is exact per item, nothing is estimated, so no §1.5 floor
    applies. Never summed into a sacredness score (§13.5)."""
    sets, waves_seen = protected_value_sets(responses, wave_of)
    slots_probed: dict[tuple[str, str], set[str]] = defaultdict(set)
    for r in responses:
        w = wave_of(r)
        if w is None:
            continue
        user = r.get("user_id")
        if user is None:
            continue
        slot = r.get("value_slot")
        if slot:
            slots_probed[(user, w)].add(slot)
    out: dict[str, dict[str, Any]] = {}
    for user in sorted(waves_seen):
        first_wave = sorted(waves_seen[user])[0]
        professed = sorted(sets.get((user, first_wave), set()))
        out[user] = {
            "wave": first_wave,
            "professed": professed,
            "n_professed": len(professed),
            "n_slots_probed": len(slots_probed.get((user, first_wave), set())),
        }
    return out


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
# 2000; the actor–observer asymmetry) — NOT the excluded paradigms. The on-device
# H_i reveal is SHIPPED (§18.7): hypocrisyAsymmetry() in poc-projection.js mirrors
# hypocrisy_asymmetry_by_user under the JS↔Python parity lock, and the analyzer
# emits the companion H12.hypocrisy_asymmetry_reveal. The H12b discriminant (vs
# the §6 gap / calibration error) is BUILT — compute_h12b_discriminant, cohort-
# level. The pairing/missing-data lock (a declined judgment
# drops the pair, never imputed to 0; sign preserved) is the H12 analog of the
# §13.2 censoring lock — asserted against the code by check_h12_pairing_lock().
# ----------------------------------------------------------------------------

H12A_RELIABILITY_FLOOR = 0.40   # self–other asymmetry split-half reliability lower 95% CI (§18.2)
H12_MIN_PAIRS = 3               # per-person scorable-pair floor for a reveal-eligible H_i (§1.5 N=1)
# H12c is directional: lower 95% CI of the mean self–other asymmetry mean_i H_i > 0 (§18.3).

# H12b DISCRIMINANT half (§18.5) — the deferred sibling of the reliability (H12a) and
# self-serving-anchor (H12c) halves above. Regress the self–other severity asymmetry H_i
# (§18.1) on [ gap_i, cal_error_i ] (the aspirational stated−revealed over-claim from §6
# and the self-prediction error MAGNITUDE from §14.2). Moral hypocrisy is a DISTINCT
# construct — NOT reducible to "how much you over-claim" + "how poorly you know yourself"
# — iff the UPPER 95% bootstrap CI of the model R² < H12B_R2_CEILING (the paired self/other
# severity channel carries variance those two predictors do not). Unlike the H9b / H11b
# discriminants there is NO algebraic trap: H_i rides an INDEPENDENT measurement channel,
# not an affine echo of the predictors, so the lock is honestly two-sided. PROPOSED locks
# (DECISIONS §19); the analyzer reports met/not-met, never gates.
H12B_R2_CEILING = 0.50          # discriminant: UPPER 95% CI of H_i~[gap,cal_error] R² must clear this
H12B_MIN_PARTICIPANTS = 8       # ≥8 users with gap + cal_error + H_i before a 2-predictor R² is stable
H12B_SEED_OFFSET = 29           # bootstrap seed band for the R² CI (H11B 27, H9B 28; next free)


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


def compute_h12b_discriminant(
    session_entries: list[dict],
    card_sort_responses: list[dict],
    predictions: list[dict],
    hypocrisy_records: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, Any] | None:
    """H12b — the moral-hypocrisy DISCRIMINANT (§18.5), the deferred sibling of the H12a
    reliability and H12c self-serving-anchor halves. Regress the self–other severity
    asymmetry H_i (§18.1, mean_act severity_other − severity_self) on [ gap_i, cal_error_i ]
    (the aspirational stated−revealed over-claim from §6 and the self-prediction error
    MAGNITUDE from §14.2); moral hypocrisy is a DISTINCT construct — NOT reducible to how
    much a person over-claims plus how poorly they know themselves — iff the UPPER 95%
    bootstrap CI of the model R² < H12B_R2_CEILING (the paired self/other severity channel
    carries variance neither the over-claim gap nor the self-insight magnitude explains;
    Batson's moral-hypocrisy line dissociates the self-favoring double standard from both
    self-idealization and self-knowledge). Completes H12 = reliability ∧ anchor ∧ discriminant.

    NO algebraic trap here — and by design. H_i is measured on an INDEPENDENT channel (paired
    self/other severity judgments, §18.1), NOT an affine echo of gap or cal_error the way the
    H9b signed-cal_bias or H11b circle-mean outcomes were, so the discriminant cannot be
    manufactured true or false by construction: the lock is honestly two-sided — SUPPORTED
    when the asymmetry channel carries its own variance, NOT-supported when H_i is linearly
    reducible to over-claiming + self-insight. check_h12b_discriminant_lock exercises both
    directions on real-pipeline corpora (no hand-built identity). COHORT-level statistic,
    NEVER a per-person reveal: H_i, gap_i and cal_error_i stay separate facets, never pooled
    (§13.5). Seed BOOTSTRAP_SEED+29."""
    predictors_by_user = _h9b_person_predictors(session_entries, card_sort_responses, tag_map)
    cal = calibration_person_indices(calibration_axis_records(predictions, tag_map))
    asymmetry = hypocrisy_asymmetry_by_user(hypocrisy_records)
    rows: list[tuple[float, float, float]] = []
    for user in sorted(set(predictors_by_user) & set(cal) & set(asymmetry)):
        gap = predictors_by_user[user]["gap"]
        cal_error = cal[user]["cal_error"]
        h = asymmetry[user]
        if gap != gap or cal_error != cal_error or h != h:
            continue
        rows.append((gap, cal_error, h))   # predictors = [gap, cal_error]; y = H_i
    if len(rows) < H12B_MIN_PARTICIPANTS:
        return None
    predictors = [[r[0] for r in rows], [r[1] for r in rows]]
    y = [r[2] for r in rows]
    r2 = _ols_r_squared(predictors, y)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + H12B_SEED_OFFSET))
    supported = None if ci_high != ci_high else bool(ci_high < H12B_R2_CEILING)
    # Descriptive companions (reported, NOT the gate): H_i's bare correlation with each
    # predictor alone, so a reader sees WHICH predictor (if any) carries leakage — without
    # pooling anything per person.
    h_gap_r = _pearson_r([r[0] for r in rows], y)
    h_cal_error_r = _pearson_r([r[1] for r in rows], y)
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": H12B_R2_CEILING,
        "h_gap_r": h_gap_r,
        "h_cal_error_r": h_cal_error_r,
        "n_participants": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
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
# R1b (§19.4/§19.5) is the moral-identity META-MODERATOR leg (the gap leg): regress the
# §6 over-claim gap_i on internalization_i across the cohort; supported iff the UPPER 95%
# CI of corr(internalization_i, gap_i) < R1B_MODERATION_CEILING (0.0) — i.e. a more
# internalized moral identity predicts a SIGNIFICANTLY smaller (more negative) stated–
# revealed over-claim, the Aquino & Reed 2002 identity→behavior-congruence prediction.
# DIRECTIONAL (a signed slope test, not an R²-ceiling discriminant) and COHORT-level: the
# two channels are INDEPENDENT (internalization from the identity log; gap from session +
# card_sort), so there is no algebraic identity, and the reveal describes a cohort
# relationship, NEVER a per-person verdict (a very negative gap is modesty, not "better").
# The H10–H12 dampening legs (does internalization also blunt the framing/anchor/decoy
# effects) are a DEFERRED R1b extension — they need two more cohort channels. Seed +34.
R1B_MIN_PARTICIPANTS = 8       # cohort floor for the moderation regression (§19.5); shared by the H12-dampening leg
R1B_MODERATION_CEILING = 0.0   # upper 95% CI of corr(internalization, over-claim gap) must clear this (be < 0)
R1B_SEED_OFFSET = 34           # BOOTSTRAP_SEED offset registry: next free slot after A4b (+33)
R1B_H12_SEED_OFFSET = 36       # BOOTSTRAP_SEED offset registry: next free after R1a_symbolization (+35); R1b H12-dampening leg (§19.5)


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


def compute_r1a_symbolization_reliability(records: list[dict]) -> dict[str, Any] | None:
    """R1a-symbolization (§19.2): the reliability leg for the SYMBOLIZATION facet —
    identical machinery to compute_r1a_reliability (split each user's sessions
    odd/even, recompute the facet on each half, correlate across users; supported iff
    the lower 95% bootstrap CI of the correlation ≥ R1A_RELIABILITY_FLOOR), but on the
    public/symbolization dimension. Reported SEPARATELY from the internalization leg
    (§13.5 — the two facets are never pooled into one reliability figure); together the
    two legs give R1 its complete two-facet reliability story. Symbolization is the more
    situational, less trait-stable dimension (Aquino & Reed 2002), so passing this bar
    is a genuine test, not a foregone conclusion. Seed BOOTSTRAP_SEED+35."""
    odd, even = _odd_even_sessions(records)
    c_odd = centrality_facet_by_user(records, "symbolization", lambda u, s: s in odd.get(u, set()))
    c_even = centrality_facet_by_user(records, "symbolization", lambda u, s: s in even.get(u, set()))
    shared = sorted(set(c_odd) & set(c_even))
    if len(shared) < 3:
        return None
    xs = [c_odd[u] for u in shared]
    ys = [c_even[u] for u in shared]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + 35)
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


def compute_r1b_moderation(
    session_entries: list[dict],
    card_sort_responses: list[dict],
    identity_records: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, Any] | None:
    """R1b (§19.4/§19.5): moral identity as the META-MODERATOR of the stated–revealed
    gap — its headline role. Regress each person's §6 OVER-CLAIM gap on their
    INTERNALIZATION centrality across the cohort:

        internalization_i  = centrality_facet_by_user(identity, "internalization")   (§19.1)
        gap_i              = _h9b_person_predictors(session, card_sort)[i]["gap"]     (§6, signed over-claim)
        r                  = corr(internalization_i, gap_i)   (= the STANDARDIZED moderation slope)

    Supported iff the UPPER 95% bootstrap CI of r < R1B_MODERATION_CEILING (0.0), one-
    sided: a more internalized moral identity predicts a SIGNIFICANTLY smaller (more
    negative) over-claim — the Aquino & Reed 2002 identity→behavior-congruence
    prediction. This is DIRECTIONAL (a signed-slope test), not an R²-ceiling
    discriminant.

    The two channels are INDEPENDENT — internalization rides the identity log; the gap
    rides session + card_sort through the SAME parity-locked §3/§6 primitives H9b/H12b
    use — so there is no algebraic identity linking them (the two-sidedness the R1b lock
    exploits). COHORT-level construct validity, never a per-person verdict: a very
    negative gap is MODESTY (revealing more virtue than one states), not scored as
    "better", and neither internalization pole is ranked (§19.4). The H10–H12 dampening
    legs are a DEFERRED extension. Seed BOOTSTRAP_SEED+R1B_SEED_OFFSET (+34)."""
    intern = centrality_facet_by_user(identity_records, "internalization")
    preds = _h9b_person_predictors(session_entries, card_sort_responses, tag_map)
    rows: list[tuple[float, float]] = []
    for user in sorted(set(intern) & set(preds)):
        iv = intern[user]
        gv = preds[user]["gap"]
        if iv != iv or gv != gv:   # drop NaN on either channel — never imputed (§1.5)
            continue
        rows.append((iv, gv))
    if len(rows) < R1B_MIN_PARTICIPANTS:
        return None
    xs = [row[0] for row in rows]
    ys = [row[1] for row in rows]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + R1B_SEED_OFFSET)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_high != ci_high else bool(ci_high < R1B_MODERATION_CEILING)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(rows),
        "ceiling": R1B_MODERATION_CEILING, "supported": met,
        "pre_registered_threshold_met": met,
    }


def compute_r1b_h12_dampening(
    hypocrisy_records: list[dict],
    identity_records: list[dict],
) -> dict[str, Any] | None:
    """R1b H12-DAMPENING leg (§19.5) — the FIRST of R1b's three deferred H10–H12
    dampening legs. Moral identity should not only shrink the §6 over-claim gap (the
    R1b gap leg) but also DAMPEN the H12 self–other severity asymmetry. Regress each
    person's holier-than-thou asymmetry H_i on their INTERNALIZATION centrality across
    the cohort:

        internalization_i = centrality_facet_by_user(identity, "internalization")   (§19.1)
        H_i               = hypocrisy_asymmetry_by_user(hypocrisy)[i]                (§18.1, SIGNED)
        r                 = corr(internalization_i, H_i)   (= the STANDARDIZED moderation slope)

    Supported iff the UPPER 95% bootstrap CI of r < R1B_MODERATION_CEILING (0.0), one-
    sided: a more internalized moral identity predicts a SIGNIFICANTLY smaller (more
    negative) self–other asymmetry — internalized moral identity → behavioral congruence
    → less self-serving double standard (Aquino & Reed 2002 applied to the Tappin & McKay
    2017 / Epley & Dunning 2000 holier-than-thou asymmetry). DIRECTIONAL (a signed-slope
    test, not an R²-ceiling discriminant), exactly like the R1b gap leg (compute_r1b_
    moderation) — it reuses R1B_MIN_PARTICIPANTS + R1B_MODERATION_CEILING (the R1b family)
    with its OWN bootstrap seed.

    The two channels are INDEPENDENT — internalization rides the identity log; H_i rides
    the matched-severity hypocrisy log — so there is no algebraic identity linking them
    (the two-sidedness check_r1b_h12_dampening_lock exploits, unlike H9b's signed cal_bias
    echo). COHORT-level construct validity, NEVER a per-person verdict: a very negative H_i
    is harsher-on-SELF (described, never ranked "better", §18.4), and neither internalization
    pole is ranked (§19.4). This is DISTINCT from H12b (the discriminant, H_i ~ [gap,
    cal_error] on an R²-ceiling) — a DIFFERENT predictor (internalization, not the person's
    own gap/calibration) and a DIFFERENT question (moderation, not reducibility). Seed
    BOOTSTRAP_SEED+R1B_H12_SEED_OFFSET (+36)."""
    intern = centrality_facet_by_user(identity_records, "internalization")
    h_by_user = hypocrisy_asymmetry_by_user(hypocrisy_records)
    rows: list[tuple[float, float]] = []
    for user in sorted(set(intern) & set(h_by_user)):
        iv = intern[user]
        hv = h_by_user[user]
        if iv != iv or hv != hv:   # drop NaN on either channel — never imputed (§1.5)
            continue
        rows.append((iv, hv))
    if len(rows) < R1B_MIN_PARTICIPANTS:
        return None
    xs = [row[0] for row in rows]
    ys = [row[1] for row in rows]
    r = _pearson_r(xs, ys)
    if r is None:
        return None
    rng = random.Random(BOOTSTRAP_SEED + R1B_H12_SEED_OFFSET)
    ci_low, ci_high = _bootstrap_ci_r(xs, ys, rng)
    met = None if ci_high != ci_high else bool(ci_high < R1B_MODERATION_CEILING)
    return {
        "r": r, "ci_low": ci_low, "ci_high": ci_high, "n_participants": len(rows),
        "ceiling": R1B_MODERATION_CEILING, "supported": met,
        "pre_registered_threshold_met": met,
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


R6B_R2_CEILING = 0.50          # discriminant: UPPER 95% CI of objectivism_moral~[sacredness,centrality,importance] R² must clear this
R6B_MIN_PARTICIPANTS = 8       # ≥8 users with all three predictors + an objectivism read before a 3-predictor R² is stable
R6B_SEED_OFFSET = 30           # bootstrap seed band for the R² CI (H12B 29; next free)


def compute_r6b_discriminant(
    objectivism_records: list[dict],
    protected_responses: list[dict],
    identity_records: list[dict],
    card_sort_responses: list[dict],
) -> dict[str, Any] | None:
    """R6b — the metaethical-objectivism DISCRIMINANT (§20.5), the deferred sibling of the
    R6a reliability and R6d moral>taste-anchor halves. Regress a person's MORAL objectivism
    read objectivism_moral_i (§20.1, how fact-like they treat moral claims) on THREE
    neighbouring "how much morality matters" constructs, each from its OWN channel:
        sacredness_i       = |P_i|, the SIZE of their protected/`never` set   (§17.1, R2)
        centrality_i       = internalization_i, how self-defining morality is (§19.1, R1)
        value_importance_i = mean aspirational_self card-sort endorsement      (§5.1 — the
                             breadth of values a person holds up as their ideal)
    Metaethical objectivism is a DISTINCT construct — NOT reducible to how ABSOLUTE, how
    CENTRAL, or how BROAD a person's values are — iff the UPPER 95% bootstrap CI of the
    model R² < R6B_R2_CEILING (treating morality as objective FACT carries variance those
    three "mattering" channels do not; Goodwin & Darley 2008 dissociate metaethical
    objectivism from moral conviction / importance). Completes R6 = reliability ∧ anchor ∧
    discriminant.

    NO algebraic trap here — and, as with H12b, by design. objectivism_moral_i is measured
    on an INDEPENDENT Likert channel (the §20.1 objectivism probe), NOT an affine echo of
    the three predictors the way the H9b signed-cal_bias or H11b circle-mean outcomes were,
    so the discriminant cannot be manufactured true or false by construction: the lock is
    honestly two-sided — SUPPORTED when the objectivism channel carries its own variance,
    NOT-supported when objectivism_moral_i is linearly reducible to sacredness + centrality +
    importance. check_r6b_discriminant_lock exercises both directions on real-pipeline
    corpora (no hand-built identity). COHORT-level statistic, NEVER a per-person reveal:
    objectivism_moral_i, |P_i|, internalization_i and the importance breadth stay separate
    facets, never pooled (§13.5) — and the R6 load-bearing discipline holds, the STATED
    objectivism probe is never fused with the deferred κ-gated revealed signatures. The four
    predictors/outcome ride four DIFFERENT logs, so this couples the R2 + R1 + card-sort
    pipelines yet keeps every channel isolated. Seed BOOTSTRAP_SEED+30."""
    obj = objectivism_by_user(objectivism_records, "moral")
    intern = centrality_facet_by_user(identity_records, "internalization")
    sets, waves_seen = protected_value_sets(protected_responses)
    sacredness: dict[str, int] = {}
    for user in waves_seen:
        slots: set[str] = set()
        for w in waves_seen[user]:
            slots |= sets.get((user, w), set())
        sacredness[user] = len(slots)   # |P_i| — a count, never a price (§13.2 censoring)
    value_domain = load_values_deck_domains()
    cs = card_sort_scores(card_sort_responses, value_domain)
    imp_by_user: dict[str, list[float]] = defaultdict(list)
    for (user, _domain, layer), s in cs.items():
        if layer == "aspirational_self":
            imp_by_user[user].append(s)
    importance = {u: sum(v) / len(v) for u, v in imp_by_user.items()}
    rows: list[tuple[float, float, float, float]] = []
    for user in sorted(set(obj) & set(sacredness) & set(intern) & set(importance)):
        sv = float(sacredness[user])
        cv = intern[user]
        iv = importance[user]
        ov = obj[user]
        if sv != sv or cv != cv or iv != iv or ov != ov:
            continue
        rows.append((sv, cv, iv, ov))   # predictors = [sacredness, centrality, importance]; y = objectivism_moral
    if len(rows) < R6B_MIN_PARTICIPANTS:
        return None
    predictors = [[r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]]
    y = [r[3] for r in rows]
    r2 = _ols_r_squared(predictors, y)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + R6B_SEED_OFFSET))
    supported = None if ci_high != ci_high else bool(ci_high < R6B_R2_CEILING)
    # Descriptive companions (reported, NOT the gate): objectivism's bare correlation with
    # each predictor alone, so a reader sees WHICH neighbour (if any) carries leakage —
    # without pooling anything per person.
    o_sacredness_r = _pearson_r([r[0] for r in rows], y)
    o_centrality_r = _pearson_r([r[1] for r in rows], y)
    o_importance_r = _pearson_r([r[2] for r in rows], y)
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": R6B_R2_CEILING,
        "o_sacredness_r": o_sacredness_r,
        "o_centrality_r": o_centrality_r,
        "o_importance_r": o_importance_r,
        "n_participants": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
    }


# --- A3: the moral-language channel — the coder + the κ gate (scoring.md §21,
# h-a3-moral-language.md; branch A3 of measurement-avenues.md). A THIRD channel on
# values: what a person spontaneously MORALIZES about, in what moral vocabulary —
# distinct from the elicited-stated inventory and from revealed behavior. This
# increment builds the buildable KEYSTONE: a deterministic MFD-style foundation coder,
# Cohen's κ inter-rater validation, the κ ≥ 0.70 gate, and the foundation_i(f) profile.
# THE BINDING DISCIPLINE (§21.2/§1.5): the ENTIRE channel is DESCRIPTIVE/EXPLORATORY-ONLY
# until the coder clears κ ≥ 0.70 against REAL human gold-standard coding (~200 codes,
# 50/domain × 2 raters — labor, Dave/human-gated). Synthetic κ proves the MACHINERY, it
# does NOT lift the real gate. Value-neutral with force (§21.4): the coder assigns
# foundation LABELS, never ranks them, never emits a scalar "moral-language score"; more
# moral language is NOT better (engagement OR grandstanding); fluency ≠ virtue. κ is a
# CODER-PAIR reliability statistic, NEVER a person score (§13.5). NOT parity-gated by
# design: LLM/language coding is non-deterministic, so it is deliberately OUTSIDE the
# poc-projection.js ↔ analyze.py parity contract (§1.5/§3) — the first such branch.
A3_KAPPA_GATE = 0.70   # Cohen's κ vs. gold-standard manual coding (§21.2; validity-threats.md)
MFD_FOUNDATIONS = ("care", "fairness", "loyalty", "authority", "sanctity", "liberty")
# v0.1 DRAFT MFD-style lexicon — the MFD `word*` WILDCARD convention (prefix match on
# tokens). A researcher-imposed DRAFT (surfaced to Dave, like the H11 counterparty
# distance map): the production instrument is the validated MFD 2.0 / eMFD, coded by an
# LLM pinned at temperature=0 and κ-validated against human gold. Its KNOWN over-matching
# (e.g. the `care` stem catching "career") is exactly what the κ ≥ 0.70 gate exists to
# catch — a feature of the honest ceiling, not a bug to hide (§21.1/§21.2).
MFD_LEXICON_V0_1 = {
    "care":      ("harm", "hurt", "suffer", "cruel", "care", "protect", "compassion", "victim", "kill", "abuse"),
    "fairness":  ("fair", "unfair", "equal", "cheat", "justice", "rights", "deserv", "unjust", "bias"),
    "loyalty":   ("loyal", "betray", "team", "traitor", "patriot", "solidarity", "belong", "desert"),
    "authority": ("respect", "obey", "duty", "authorit", "defian", "tradition", "hierarch", "disobey"),
    "sanctity":  ("pure", "sacred", "disgust", "degrad", "holy", "defile", "unclean", "sanctit"),
    "liberty":   ("free", "freedom", "oppress", "coerce", "libert", "tyran", "autonom", "subjugat"),
}


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokens (maximal alphanumeric runs). Pure-stdlib, deterministic —
    no regex, no external NLP — so the DRAFT coder is byte-reproducible for the synthetic
    parity test. (The REAL coder is a non-deterministic LLM, κ-gated not parity-gated;
    §21.1/§1.5.)"""
    toks: list[str] = []
    cur: list[str] = []
    for ch in text.lower():
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            toks.append("".join(cur))
            cur = []
    if cur:
        toks.append("".join(cur))
    return toks


def code_foundations(text: str, lexicon: dict[str, tuple] = MFD_LEXICON_V0_1) -> set[str]:
    """Deterministic MFD-style foundation coder (§21.1): a foundation is INVOKED iff any
    token PREFIX-matches any of its lexicon stems (the MFD `word*` wildcard convention).
    Returns the SET of invoked foundations — multi-label: a text may invoke several, or
    NONE (declining to moralize, or speaking in concrete-relational terms, is a Dancy
    particularist move — a legitimate style, not a deficient "zero"; §21.4). VALUE-NEUTRAL:
    it assigns LABELS, never ranks the foundations, never emits a scalar score (§21.4).
    A DRAFT stand-in (v0.1) whose known over-/under-matching is exactly what the κ ≥ 0.70
    human-gold gate exists to catch (§21.2)."""
    toks = _tokenize(text)
    invoked: set[str] = set()
    for foundation, stems in lexicon.items():
        if any(tok.startswith(stem) for tok in toks for stem in stems):
            invoked.add(foundation)
    return invoked


def cohens_kappa(
    a_labels: list[set], b_labels: list[set], categories: tuple = MFD_FOUNDATIONS
) -> float | None:
    """Cohen's κ between two coders over a corpus (§21.2), computed on the binary
    (utterance × foundation) present/absent judgments — the standard multi-label MFD
    reliability operationalization. a_labels[i] / b_labels[i] are the SETS of foundations
    coder A / coder B assigned to utterance i.  κ = (p_o − p_e) / (1 − p_e). Returns None
    when undefined: mismatched/empty corpus, or p_e == 1 (no variance — every cell agrees
    trivially, so there is nothing for chance-correction to correct). κ is a property of
    the CODER PAIR (inter-rater reliability) — it is NEVER attached to a participant as a
    person score (§21.4, §13.5)."""
    if len(a_labels) != len(b_labels) or not a_labels:
        return None
    n = 0
    a_present = b_present = agree = 0
    for sa, sb in zip(a_labels, b_labels):
        for c in categories:
            ia = c in sa
            ib = c in sb
            n += 1
            if ia:
                a_present += 1
            if ib:
                b_present += 1
            if ia == ib:
                agree += 1
    if n == 0:
        return None
    p_o = agree / n
    pa1 = a_present / n
    pb1 = b_present / n
    p_e = pa1 * pb1 + (1.0 - pa1) * (1.0 - pb1)
    if 1.0 - p_e == 0.0:
        return None
    return (p_o - p_e) / (1.0 - p_e)


def _utterance_text(r: dict) -> str | None:
    """The free-text of one utterance, or None if absent/blank. A blank/missing text is
    MISSING DATA — dropped, never coded as a zero-foundation "declined" (§1.5). (Contrast:
    a NON-blank text with no moral words IS a real zero-foundation particularist utterance
    and counts in the profile denominator; §21.4.)"""
    t = r.get("text")
    if not isinstance(t, str):
        return None
    t = t.strip()
    return t or None


def code_corpus(
    records: list[dict], lexicon: dict[str, tuple] = MFD_LEXICON_V0_1
) -> tuple[list[set], list[set]]:
    """Run the deterministic coder over every scorable utterance, returning parallel
    (coder set, gold set) lists — the shared input to κ (validation) and the profile.
    Gold = the `gold_foundations` field: the SYNTHETIC stand-in for ~200 human gold codes
    (§21.2). Blank/missing-text records are dropped from BOTH lists together (§1.5)."""
    coder: list[set] = []
    gold: list[set] = []
    for r in records:
        text = _utterance_text(r)
        if text is None:
            continue
        coder.append(code_foundations(text, lexicon))
        g = r.get("gold_foundations")
        gold.append(set(g) if isinstance(g, list) else set())
    return coder, gold


def compute_a3_coding_kappa(
    records: list[dict], lexicon: dict[str, tuple] = MFD_LEXICON_V0_1
) -> dict[str, Any] | None:
    """A3 coding-reliability GATE (§21.2): Cohen's κ between the automated coder and the
    gold-standard codes. The BINDING prerequisite — until κ ≥ A3_KAPPA_GATE (0.70) against
    REAL human gold, the ENTIRE moral-language channel is descriptive/exploratory-only and
    promotes to nothing primary (§21.5/§1.5). On SYNTHETIC gold this certifies the
    MACHINERY; it does NOT lift the real gate (real κ needs ~200 human codes, 50/domain ×
    2 raters — labor, not engineering). Returns κ + the 2×2 marginals (transparency — κ is
    never a bare scalar), and the gate flags: `kappa_met_synthetic` (does the machinery
    clear 0.70 on THIS fixture) vs. `promotable`, which is ALWAYS False here — real
    promotion is Dave/human-gated (§21.2)."""
    coder, gold = code_corpus(records, lexicon)
    if not coder:
        return None
    k = cohens_kappa(coder, gold)
    n_cells = len(coder) * len(MFD_FOUNDATIONS)
    coder_present = sum(1 for s in coder for c in MFD_FOUNDATIONS if c in s)
    gold_present = sum(1 for s in gold for c in MFD_FOUNDATIONS if c in s)
    agree_cells = sum(
        1 for sa, sb in zip(coder, gold) for c in MFD_FOUNDATIONS if (c in sa) == (c in sb)
    )
    met_synth = k is not None and k >= A3_KAPPA_GATE
    return {
        "kappa": k,
        "kappa_gate": A3_KAPPA_GATE,
        "n_utterances": len(coder),
        "n_cells": n_cells,
        "coder_present": coder_present,
        "gold_present": gold_present,
        "agree_cells": agree_cells,
        "kappa_met_synthetic": met_synth,
        # The WALL: real promotion needs κ ≥ 0.70 vs. HUMAN gold; synthetic κ never lifts it.
        "promotable": False,
        "descriptive_only": True,
    }


def foundation_profile_by_user(
    records: list[dict], lexicon: dict[str, tuple] = MFD_LEXICON_V0_1
) -> dict[str, dict[str, float]]:
    """foundation_i(f) (§21.3): per user, the RATE at which each moral foundation is
    invoked across their scorable utterances = (# utterances invoking f) / (# utterances).
    A within-person DESCRIPTIVE profile — a rate vector over the six foundations, VALUE-
    NEUTRAL: NEVER summed into a scalar "morality score", NEVER ranking the foundations
    (§21.4). Volume-normalized (a rate, not a count) so verbal fluency / output volume is
    not read as virtue (§21.4, the language≠value confound). A zero-foundation utterance
    (non-blank text, no moral words) counts in the denominator — the particularist is
    DESCRIBED as using less moral language, never scored deficient. Descriptive-only until
    the κ gate is met against human gold (§21.2)."""
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    totals: dict[str, int] = defaultdict(int)
    for r in records:
        user = r.get("user")
        if user is None:
            continue
        text = _utterance_text(r)
        if text is None:
            continue
        totals[user] += 1
        for f in code_foundations(text, lexicon):
            counts[user][f] += 1
    out: dict[str, dict[str, float]] = {}
    for user, total in totals.items():
        out[user] = {f: counts[user][f] / total for f in MFD_FOUNDATIONS}
    return out


# --- A4: decision conflict — the PROCESS channel (scoring.md §22, h-a4-a5-process-emotion.md
# Part 1; branch A4 of measurement-avenues.md). The dynamics that SURROUND a choice rather than
# the choice itself: how EFFORTFUL/ambivalent the decision was, read from already-logged response
# times (§5, near-free re-analysis). conflict(i, item) = the within-person, confound-guarded
# z-score of response time — residualized on item reading-load (prompt_chars) + presented
# position, with timeouts and the TIMED quick-fire set (CV-1) EXCLUDED, then z-scored WITHIN each
# person (people read at different speeds). THE LOAD-BEARING DISCIPLINE (§1.1, Bago & De Neys
# 2019): conflict is EFFORT / ambivalence, FULL STOP — NEVER mapped to a moral framework (slow ≠
# deontological, fast ≠ utilitarian; the Greene dual-process mapping does not hold and concept.md
# already disclaims it). VALUE-NEUTRAL (§3): effort is not graded — finding virtue hard is not
# worse than finding it easy (the effortful-virtue cell arguably makes high conflict the STRONGER
# character signal). EXPLORATORY, RT-ONLY: answer-revision capture is a Dave/runtime-gated open
# question (§4 Q1), so this increment omits `rev` and reads RT alone. NO PUBLIC CARD (§1.4): A4 is
# an analysis adjunct — a flag on which of a person's choices were hard-won vs. automatic, context
# for the reveal, never a browsable headline. ON-DEVICE REVEAL SHIPPED: conflict_by_user_domain is
# mirrored by the runtime's conflictReads (poc-projection.js) under the JS↔Python parity lock in
# check_impl_parity.py — legitimate as an N=1 on-device read because the within-person z-score/mean
# are self-contained (the cohort-filtered value equals the solo value exactly; no cohort needed).
A4A_RELIABILITY_FLOOR = 0.40   # conflict split-half reliability lower 95% CI (§1.2) — the exploratory bar
A4_MIN_ITEMS = 4               # per-user scorable-item floor for a within-person residualized RT fit (intercept + 2 predictors + slack)
A4A_SEED_OFFSET = 25           # bootstrap seed band BOOTSTRAP_SEED+25 (+ per-domain i, via _domain_test_retest_r); A3 consumed none, R6d used +24
A4B_R2_CEILING = 0.50          # conflict(i,d) ~ [choice level, |aspirational gap|] upper 95% CI must clear this to be a distinct channel (§22.4)
A4B_MIN_PARTICIPANTS = 8       # cohort participant floor (matches H9B/H10B/H11B/H12B/R6B)
A4B_MIN_DOMAINS = 2            # per-user (user × domain) cell floor — the within-person centering needs ≥2 cells to carry any signal
A4B_MIN_CELLS = 12             # pooled (user × domain) cell floor for a stable within-person R² fit
A4B_SEED_OFFSET = 33           # bootstrap seed band BOOTSTRAP_SEED+33 for the R² CI (A4A 25, H10B main 31, H10B de-confound 32; next free)


def _a4_user(r: dict) -> str | None:
    """Participant id — tolerant of the extension-log `user` and the primary session-log
    `user_id` (A4 re-analyses already-logged session dynamics; §1.1/§5)."""
    return r.get("user") if r.get("user") is not None else r.get("user_id")


def _a4_session(r: dict) -> str | None:
    return r.get("session") if r.get("session") is not None else r.get("session_id")


def _a4_item(r: dict) -> str | None:
    return r.get("item") if r.get("item") is not None else r.get("item_id")


def _a4_excluded(r: dict) -> bool:
    """§1.1 exclusions: timed-out items (no genuine RT) and the TIMED quick-fire set — the CV-1
    timer construct interacts with any RT measure, so conflict is read only on the untimed session
    types. `timed` explicit, else inferred from a quick-fire scenario_type."""
    if r.get("was_timeout"):
        return True
    if r.get("timed"):
        return True
    st = r.get("scenario_type")
    return isinstance(st, str) and st.startswith("quick-fire")


def _a4_prompt_chars(r: dict) -> float | None:
    """Item reading-load — explicit `prompt_chars`, else the length of the item text/prompt (the
    confound §1.1 residualizes out: longer items take longer to read, independent of conflict)."""
    v = r.get("prompt_chars")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    for key in ("text", "prompt", "prompt_text"):
        t = r.get(key)
        if isinstance(t, str):
            return float(len(t))
    return None


def _solve_linear(mat: list[list[float]], vec: list[float]) -> list[float] | None:
    """Gaussian elimination with partial pivoting for a small dense system mat·x = vec. Returns
    None if (near-)singular. Pure stdlib, deterministic — no numpy — so the confound-guarded
    residual is byte-reproducible (§1.1)."""
    n = len(mat)
    aug = [list(mat[i]) + [vec[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda rr: abs(aug[rr][col]))
        if abs(aug[piv][col]) < 1e-12:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        pivot = aug[col][col]
        for rr in range(n):
            if rr == col:
                continue
            factor = aug[rr][col] / pivot
            if factor == 0.0:
                continue
            for cc in range(col, n + 1):
                aug[rr][cc] -= factor * aug[col][cc]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def _ols_residuals(predictors: list[list[float]], y: list[float]) -> list[float] | None:
    """OLS residuals of y on [intercept] + predictors, via the normal equations XᵀX β = Xᵀy
    (small k, Gaussian elimination). Returns None if underdetermined (n ≤ k) or the design is
    rank-deficient (e.g. a predictor has no within-person variance) — the caller then falls back
    to plain within-person mean-centering."""
    n = len(y)
    cols = [[1.0] * n] + [list(c) for c in predictors]
    k = len(cols)
    if n <= k:
        return None
    XtX = [[sum(cols[a][i] * cols[b][i] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(cols[a][i] * y[i] for i in range(n)) for a in range(k)]
    beta = _solve_linear(XtX, Xty)
    if beta is None:
        return None
    resid = []
    for i in range(n):
        pred = sum(beta[a] * cols[a][i] for a in range(k))
        resid.append(y[i] - pred)
    return resid


def _ols_r_squared(predictors: list[list[float]], y: list[float]) -> float | None:
    """Coefficient of determination R² of the OLS fit y ~ [intercept] + predictors,
    via _ols_residuals (R² = 1 − SS_res/SS_tot). Returns None when the design is
    underdetermined/rank-deficient (residuals None) or y has no variance (SS_tot = 0),
    so the caller never divides by zero. Used by the H11b shape discriminant (§1.3):
    y = β_i (shape slope), predictors = [near-bin concern, resource-allocation
    generosity]; a HIGH R² means the shape is reducible to those, a LOW one means the
    circle's shape carries variance generosity does not ("reach is not height")."""
    resid = _ols_residuals(predictors, y)
    if resid is None:
        return None
    n = len(y)
    mean_y = sum(y) / n
    ss_tot = sum((v - mean_y) ** 2 for v in y)
    if ss_tot == 0.0:
        return None
    ss_res = sum(r * r for r in resid)
    return 1.0 - ss_res / ss_tot


def _bootstrap_ci_r2(
    rows: list[tuple[float, ...]],
    rng: random.Random,
    n_iter: int = BOOTSTRAP_N,
    ci: float = BOOTSTRAP_CI,
) -> tuple[float, float]:
    """Percentile bootstrap CI for the multiple-regression R² (scoring.md §8). Each
    `row` is (x1, …, xk, y); we resample rows with replacement, refit, recompute R²,
    and take percentiles. The discriminant gate reads the UPPER bound (a small R²
    whose upper CI clears the ceiling = the predictors genuinely fail to explain the
    outcome). Deterministic per the pre-committed seed in the caller. Returns
    (nan, nan) if underdetermined."""
    n = len(rows)
    if n < 4:
        return (float("nan"), float("nan"))
    vals: list[float] = []
    for _ in range(n_iter):
        idx = [rng.randrange(n) for _ in range(n)]
        sample = [rows[i] for i in idx]
        preds = [[r[c] for r in sample] for c in range(len(rows[0]) - 1)]
        yy = [r[-1] for r in sample]
        r2 = _ols_r_squared(preds, yy)
        if r2 is not None and r2 == r2:
            vals.append(r2)
    if len(vals) < 10:
        return (float("nan"), float("nan"))
    vals.sort()
    alpha = (1 - ci) / 2
    lower_idx = int(len(vals) * alpha)
    upper_idx = int(len(vals) * (1 - alpha))
    return (vals[lower_idx], vals[min(upper_idx, len(vals) - 1)])


def conflict_scores_by_item(records: list[dict]) -> dict[tuple[str, str], float]:
    """rt_z(i, item) (§1.1): the within-person z-score of RESIDUALIZED response_time_ms —
    residualized on [prompt_chars, presented_position] to strip reading-load + order effects, with
    was_timeout and the TIMED quick-fire set (CV-1) EXCLUDED, then z-scored WITHIN each person
    (people read at different speeds). Returns {(user, item): rt_z}; higher = more effortful /
    ambivalent, NOT more deliberative-ergo-utilitarian (Bago & De Neys 2019). If a user's
    within-person design is rank-deficient (no length/position variance) the residual falls back
    to plain mean-centering (still within-person, just no confound removal)."""
    per_user: dict[str, list[tuple[str, float, float, float]]] = defaultdict(list)
    for r in records:
        if _a4_excluded(r):
            continue
        user = _a4_user(r)
        item = _a4_item(r)
        rt = r.get("response_time_ms")
        chars = _a4_prompt_chars(r)
        pos = r.get("presented_position")
        if (user is None or item is None
                or not isinstance(rt, (int, float)) or isinstance(rt, bool)
                or chars is None
                or not isinstance(pos, (int, float)) or isinstance(pos, bool)):
            continue
        per_user[user].append((item, float(rt), chars, float(pos)))
    out: dict[tuple[str, str], float] = {}
    for user, items in per_user.items():
        if len(items) < A4_MIN_ITEMS:
            continue
        y = [it[1] for it in items]
        resid = _ols_residuals([[it[2] for it in items], [it[3] for it in items]], y)
        if resid is None:
            mean_y = sum(y) / len(y)
            resid = [v - mean_y for v in y]
        mu = sum(resid) / len(resid)
        sd = (sum((v - mu) ** 2 for v in resid) / len(resid)) ** 0.5
        for (item, *_rest), rz in zip(items, resid):
            out[(user, item)] = 0.0 if sd == 0.0 else (rz - mu) / sd
    return out


def conflict_by_user_domain(records: list[dict]) -> dict[tuple[str, str], float]:
    """conflict(i, d) (§1.1): the mean rt_z over person i's items in domain d — person i's
    RELATIVE effort on domain d (which of their choices were hard-won vs. automatic). NEVER a
    pooled cross-person scalar (no "conflict score" leaderboard), NEVER a virtue ranking (§3,
    value-neutral). The unit the reveal reads and A4a's reliability is computed over."""
    rz = conflict_scores_by_item(records)
    domain_of: dict[tuple[str, str], str] = {}
    for r in records:
        user = _a4_user(r)
        item = _a4_item(r)
        dom = r.get("domain")
        if user is not None and item is not None and dom is not None:
            domain_of[(user, item)] = dom
    cells: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (user, item), z in rz.items():
        dom = domain_of.get((user, item))
        if dom is None:
            continue
        cells[(user, dom)].append(z)
    return {k: sum(v) / len(v) for k, v in cells.items()}


def _odd_even_sessions_a4(records: list[dict]) -> tuple[dict[str, set], dict[str, set]]:
    """Odd/even session split (as _odd_even_sessions) but via the tolerant A4 accessors, so A4a
    runs on either the extension `user`/`session` log or the primary `user_id`/`session_id`
    session log (§5, already-logged dynamics)."""
    user_sessions: dict[str, set] = defaultdict(set)
    for r in records:
        u, s = _a4_user(r), _a4_session(r)
        if u is not None and s is not None:
            user_sessions[u].add(s)
    odd: dict[str, set] = {}
    even: dict[str, set] = {}
    for user, sess in user_sessions.items():
        ordered = sorted(sess)
        odd[user] = set(ordered[0::2])
        even[user] = set(ordered[1::2])
    return odd, even


def compute_a4a_conflict_reliability(records: list[dict]) -> dict[str, Any] | None:
    """A4a (§1.2): split each user's sessions odd/even, recompute conflict(i, domain) on each
    half, per-domain test–retest correlation across users. Reliable iff the lower 95% bootstrap CI
    ≥ A4A_RELIABILITY_FLOOR (0.40 — the exploratory bar). Reuses the shared _domain_test_retest_r
    machinery (as H3/H5), users the independent bootstrap unit; seed band BOOTSTRAP_SEED+25 (+
    per-domain i). CONDITIONAL, honestly (§1.2/§7 Q2): reliability presumes the confound guards
    actually removed the length/device variance — the residualization here DEMONSTRATES the
    machinery on synthetic dynamics with known injected confounds; real-data confound-adequacy is
    a pilot check (Dave/data-gated). EXPLORATORY, no public card (§1.4)."""
    odd, even = _odd_even_sessions_a4(records)
    window_a = conflict_by_user_domain(
        [r for r in records if _a4_session(r) in odd.get(_a4_user(r), set())]
    )
    window_b = conflict_by_user_domain(
        [r for r in records if _a4_session(r) in even.get(_a4_user(r), set())]
    )
    per_domain = _domain_test_retest_r(window_a, window_b, A4A_SEED_OFFSET, A4A_RELIABILITY_FLOOR)
    if not per_domain:
        return None
    n_met = sum(1 for d in per_domain.values() if d.get("pre_registered_threshold_met"))
    return {
        "per_domain": per_domain,
        "n_domains": len(per_domain),
        "n_domains_met": n_met,
        "threshold_low": A4A_RELIABILITY_FLOOR,
        "any_met": bool(n_met > 0),
    }


def compute_a4b_discriminant(
    process_records: list[dict],
    session_entries: list[dict],
    card_sort_responses: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[str, Any] | None:
    """A4b — does DECISION CONFLICT add information beyond the CHOICE? (§22.4, the process-channel
    DISCRIMINANT of the §22 conflict adjunct.) A person's effort on a domain (A4's conflict(i, d) —
    the RT-derived within-person z, §1.1) could be nothing but a shadow of WHAT they chose: harder
    when they land far from their stated ideal, or at the extremes of their own behaviour. A4b asks
    whether conflict carries variance those two do NOT, by regressing conflict on the SAME §3/§6
    quantities the reveal already reports:
        conflict(i, d) ~ [ z_revealed(i, d) , |gap(i, d)| ]
    where z_revealed is the choice LEVEL (§3.2, per-domain standardized) and |gap| is the departure
    magnitude from the stated-aspirational ideal (§6). Conflict is a distinct channel iff the UPPER
    95% bootstrap CI of the model R² < A4B_R2_CEILING (0.50) — most of its variance is unexplained.

    WITHIN-PERSON (fixed-effects) by construction, and that is LOAD-BEARING (the A4b analog of the
    H11b external-generosity / H9b magnitude-channel choice). conflict is a within-person z (the
    per-person sum constraint leaves it ~zero between-person variance), while the predictors carry
    mostly BETWEEN-person variance (z_revealed is standardized per-domain ACROSS users; |gap| rides
    it). A raw-score pooled regression would therefore cap R² at the predictors' small within-person
    share — a genuinely reducible cohort could NEVER reach the ceiling and the gate would be a
    one-sided rubber stamp. So we PERSON-CENTER conflict AND both predictors within each user before
    pooling: dc, dlev, dgp are each cell-minus-person-mean. The R² then measures purely how much of
    a person's cell-to-cell conflict PROFILE their cell-to-cell choice profile explains — a two-sided
    question the lock can flip.

    NO MANUFACTURED TRAP (the H12b/R6b property, deliberately): conflict rides the INDEPENDENT RT
    channel (response_time_ms residualized on reading-load + order, §1.1), NOT an affine echo of the
    choice columns. So on a FIXED session/card-sort corpus (→ fixed dlev, dgp) the verdict flips
    True→False through the RT channel ALONE: an RT profile drawn ⊥ the choice profile → R² ~ 0 →
    distinct; an RT profile built to track [dlev, dgp] → R² high → not distinct. Had an algebraic
    identity existed (as in H9b's signed cal_bias or H11b's circle-mean), even the ⊥ draw would pin
    R² ≡ 1 — here it is ~0, so the gate tracks the DATA, not a fabricated identity.

    Descriptive companions (bare within-person Pearson r) localize any leakage WITHOUT pooling a
    scalar: conflict·level r and conflict·|gap| r are small when conflict is its own channel, signed
    and large when it is a shadow of the choice. CAVEAT (as the H10b de-confound leg): the bootstrap
    resamples (user × domain) CELLS, so its CI understates dependence from repeated users
    (pseudo-replication) — the gate stays deliberately conservative (a distinctness claim must clear
    a CEILING, so understated width only makes "distinct" HARDER to earn). VALUE-NEUTRAL, COHORT-level
    (§3/§1.4): effort is never graded and no participant is ranked; the reveal reports only whether the
    channel is separable. Returns None below the participant/cell floors (never a bare scalar)."""
    conflict = conflict_by_user_domain(process_records)
    revealed_means = user_domain_means(session_means(session_aggregates(session_entries, tag_map)))
    cs_scores = card_sort_scores(card_sort_responses, load_values_deck_domains())
    stated_layer = {
        (user, domain): score
        for (user, domain, layer), score in cs_scores.items()
        if layer == "aspirational_self"
    }
    gaps = compute_gaps(revealed_means, stated_layer, stated_source="card_sort")

    # Join conflict (process channel) to the choice predictors on the (user, domain) cell.
    by_user: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    for (user, domain), g in gaps.items():
        c = conflict.get((user, domain))
        if c is None:
            continue
        lev = g["z_revealed"]
        gp = abs(g["gap"])
        if c != c or lev != lev or gp != gp:  # drop any NaN cell
            continue
        by_user[user].append((c, lev, gp))

    # Person-center each channel within the user, then pool cells (fixed-effects design).
    rows: list[tuple[float, float, float]] = []
    n_users = 0
    for cells in by_user.values():
        if len(cells) < A4B_MIN_DOMAINS:
            continue
        n = len(cells)
        cbar = sum(c for c, _, _ in cells) / n
        lbar = sum(l for _, l, _ in cells) / n
        gbar = sum(g for _, _, g in cells) / n
        n_users += 1
        for c, l, g in cells:
            rows.append((l - lbar, g - gbar, c - cbar))   # (dlev, dgp, dc) — outcome dc last

    if n_users < A4B_MIN_PARTICIPANTS or len(rows) < A4B_MIN_CELLS:
        return None

    dlev = [r[0] for r in rows]
    dgp = [r[1] for r in rows]
    dc = [r[2] for r in rows]
    r2 = _ols_r_squared([dlev, dgp], dc)
    if r2 is None:
        return None
    ci_low, ci_high = _bootstrap_ci_r2(rows, random.Random(BOOTSTRAP_SEED + A4B_SEED_OFFSET))
    supported = None if ci_high != ci_high else bool(ci_high < A4B_R2_CEILING)
    conflict_level_r = _pearson_r(dlev, dc)
    conflict_gap_r = _pearson_r(dgp, dc)
    return {
        "r2": r2,
        "r2_ci_low": ci_low,
        "r2_ci_high": ci_high,
        "ceiling": A4B_R2_CEILING,
        "conflict_level_r": conflict_level_r,
        "conflict_gap_r": conflict_gap_r,
        "n_participants": n_users,
        "n_cells": len(rows),
        "supported": supported,
        "pre_registered_threshold_met": supported,
    }


# ---------------------------------------------------------------------------
# H8 — narrative-immersion (scoring.md §9). A SECONDARY, COHORT-level hypothesis:
# does an established-arc "narrative" form of a moral choice pull behaviour toward
# a person's stated values relative to a structurally-equivalent "abstract" quick-
# fire form? Cohort research test only — never a per-person reveal, never a gate-
# criterion (§9.5) — so there is NO on-device projection (parity stays green) and
# NO public card. It reuses the §2–§3 item scoring: the log carries the already-
# scored primary-axis values; the pairing / domain / stakes live in the manifest
# (scenarios/h8-probe-pairs.json), exactly as pairwise comparisons live in
# inventory/pairwise-pairs.json.
#
# This increment builds H8a — the DEBIASING leg (low-stakes pairs, §9.2):
#   D_i^p        = z(r_narr) − z(r_abs)                         (§9.1 divergence)
#   gap_abs(i,p) = z(stated_aspirational) − z(r_abs)            (§9.2, §6 convention)
#   rho_8a       = corr_i( mean_p D_i^p , mean_p gap_abs(i,p) )
# The confirmatory criterion is rho_8a's lower 95% bootstrap CI ≥ 0.15, POSITIVE
# under scoring.md §6's canonical stated−revealed gap convention (the design-doc's
# one-line "negative" assumed revealed−stated; reconciled here — §9.2 sign note).
#
# THE LOAD-BEARING DISCIPLINE (§9.2 mathematical-coupling caveat): D_i and gap_i
# SHARE the term r_abs, which inflates their correlation even under the null (a
# regression-to-the-mean artifact). So the confirmatory test is CONJOINED with a
# de-coupled partial-association guard: regress r_narr jointly on stated and r_abs
# and require the partial association of r_narr with stated (controlling r_abs) to
# be positive — the narrative response pulled toward the stated value BEYOND what
# the abstract response already predicts. Computed by Frisch–Waugh–Lovell as
# sign( corr( resid(r_narr ~ r_abs), resid(stated ~ r_abs) ) ), reusing
# _ols_residuals. H8a is SUPPORTED only if the headline CI AND the de-coupled sign
# AGREE — a two-sided conjunction a naive correlation cannot fake. This is the H8
# analog of the §13.2 censoring / |8.0| lock.
#
# H8b (the attachment-laden shift, §9.4) needs the separate per-character
# attachment instrument (§9.3) and is DEFERRED to the next increment.

H8A_RHO_FLOOR = 0.15    # rho_8a lower 95% bootstrap CI ≥ this (§9.2; the deliberately-modest secondary bar)
H8A_MIN_LOW_PAIRS = 3   # a participant enters H8a with ≥ 3 complete low-stakes pairs (§9.5 inclusion)
H8A_SEED_OFFSET = 26    # de-coupling partial-association robustness-CI band; rho_8a uses the §9.5-pinned BOOTSTRAP_SEED


def load_h8_pairs(manifest_path: Path) -> dict[str, dict[str, str]]:
    """Read the paired-probe manifest → {pair_id: {"domain", "stakes_level"}}. The manifest is the
    SOURCE OF TRUTH for which narrative form pairs with which abstract form, in which domain, at which
    stakes level (scoring.md §9.1); the response log carries only the scored primary-axis values."""
    with manifest_path.open() as f:
        manifest = json.load(f)
    out: dict[str, dict[str, str]] = {}
    for entry in manifest.get("pairs", []):
        pid = entry.get("pair_id")
        if pid is None:
            continue
        out[pid] = {"domain": entry.get("domain"), "stakes_level": entry.get("stakes_level")}
    return out


def _h8_completed(rec: dict) -> bool:
    """A form contributes only if it was completed — neither timed-out nor missing (§9.5)."""
    if rec.get("timed_out") is True:
        return False
    sc = rec.get("primary_axis_score")
    return isinstance(sc, (int, float)) and not isinstance(sc, bool)


def compute_h8a_debiasing(
    records: list[dict], pairs: dict[str, dict[str, str]]
) -> dict[str, Any] | None:
    """H8a debiasing test (scoring.md §9.2). Returns the confirmatory rho_8a (with bootstrap CI) AND
    the de-coupled partial-association guard, plus the SUPPORTED verdict (both must agree — §9.2).
    COHORT-level; None if <3 participants clear the ≥3-complete-low-pairs inclusion (§9.5). Never a
    per-person read (no on-device projection, no public card)."""
    low_pairs = {pid for pid, meta in pairs.items() if meta.get("stakes_level") == "low"}
    # 1. Index completed responses: {(user, pair, form): score}; capture stated per (user, domain).
    by_key: dict[tuple[str, str, str], float] = {}
    stated_raw: dict[tuple[str, str], float] = {}
    for rec in records:
        pid = rec.get("pair_id")
        if pid not in low_pairs or not _h8_completed(rec):
            continue
        user = rec.get("user_id")
        form = rec.get("form")
        if user is None or form not in ("narrative", "abstract"):
            continue
        by_key[(user, pid, form)] = float(rec["primary_axis_score"])
        st = rec.get("stated_aspirational")
        if isinstance(st, (int, float)) and not isinstance(st, bool):
            stated_raw[(user, pairs[pid]["domain"])] = float(st)

    # 2. Sample-standardize (§2): each (pair, form) column across users; stated per domain across users.
    zmap: dict[tuple[str, str, str], float] = {}
    for pid in low_pairs:
        for form in ("narrative", "abstract"):
            users = sorted(u for (u, p, f) in by_key if p == pid and f == form)
            zs = _z([by_key[(u, pid, form)] for u in users])
            if zs is None:
                continue
            for u, zv in zip(users, zs):
                zmap[(u, pid, form)] = zv
    zstated: dict[tuple[str, str], float] = {}
    for d in sorted({dd for (_u, dd) in stated_raw}):
        users = sorted(u for (u, dd) in stated_raw if dd == d)
        zs = _z([stated_raw[(u, d)] for u in users])
        if zs is None:
            continue
        for u, zv in zip(users, zs):
            zstated[(u, d)] = zv

    # 3. Per user: collect completed low-stakes probe ROWS — one (participant, pair) each, carrying the
    #    z-scored narrative, abstract, and stated values (both forms present + stated present).
    per_user_rows: dict[str, list[tuple[float, float, float]]] = defaultdict(list)  # (zn, za, zst)
    for pid in sorted(low_pairs):
        d = pairs[pid]["domain"]
        for u in sorted(u for (u, p, f) in zmap if p == pid and f == "abstract"):
            zn = zmap.get((u, pid, "narrative"))
            za = zmap.get((u, pid, "abstract"))
            zst = zstated.get((u, d))
            if zn is None or za is None or zst is None:
                continue
            per_user_rows[u].append((zn, za, zst))

    # 4. Inclusion (§9.5): a participant enters with ≥3 complete low-stakes pairs — and gates BOTH arms,
    #    so the headline correlation and the de-coupling guard describe the SAME cohort. Need ≥3 to correlate.
    users_in = sorted(u for u in per_user_rows if len(per_user_rows[u]) >= H8A_MIN_LOW_PAIRS)
    if len(users_in) < 3:
        return None

    # Confirmatory: correlate per-participant means D_low = mean_p(zn − za) with gap_abs = mean_p(zst − za).
    d_low = [sum(zn - za for (zn, za, _z) in per_user_rows[u]) / len(per_user_rows[u]) for u in users_in]
    gap_abs = [sum(zs - za for (_n, za, zs) in per_user_rows[u]) / len(per_user_rows[u]) for u in users_in]
    rho = _pearson_r(d_low, gap_abs)
    ci_low, ci_high = _bootstrap_ci_r(d_low, gap_abs, random.Random(BOOTSTRAP_SEED))
    headline_met = bool(rho is not None and ci_low == ci_low and ci_low >= H8A_RHO_FLOOR)

    # De-coupling probe rows are drawn from the SAME included participants (row-level pooled partial).
    probe_narr: list[float] = []
    probe_stated: list[float] = []
    probe_abs: list[float] = []
    for u in users_in:
        for (zn, za, zst) in per_user_rows[u]:
            probe_narr.append(zn)
            probe_stated.append(zst)
            probe_abs.append(za)

    # 5. De-coupled partial-association guard via Frisch–Waugh–Lovell (§9.2 caveat). The gate is the
    #    partial's LOWER bootstrap CI clearing ZERO — reliably positive after removing the shared r_abs
    #    — NOT the bare point sign. This matters: under the §9.2 null (r_narr independent of stated
    #    given r_abs) the headline corr(D, gap) is still POSITIVE by regression to the mean (D and gap
    #    share −z(r_abs)), and the partial's POINT sign is a coin-flip — but its CI straddles zero. So
    #    the CI, not the sign, is what deterministically bites. (A lock-time tightening of the design-
    #    doc's one-line "sign > 0"; strictly stronger — CI_low > 0 implies point > 0. Surfaced to Dave.)
    e1 = _ols_residuals([probe_abs], probe_narr)    # resid(r_narr ~ r_abs)
    e2 = _ols_residuals([probe_abs], probe_stated)  # resid(stated ~ r_abs)
    partial_r = _pearson_r(e1, e2) if (e1 is not None and e2 is not None) else None
    p_ci_low = p_ci_high = float("nan")
    if e1 is not None and e2 is not None and len(probe_abs) >= 3:
        rng = random.Random(BOOTSTRAP_SEED + H8A_SEED_OFFSET)
        m = len(probe_abs)
        vals: list[float] = []
        for _ in range(BOOTSTRAP_N):
            idx = [rng.randrange(m) for _ in range(m)]
            b1 = _ols_residuals([[probe_abs[i] for i in idx]], [probe_narr[i] for i in idx])
            b2 = _ols_residuals([[probe_abs[i] for i in idx]], [probe_stated[i] for i in idx])
            if b1 is None or b2 is None:
                continue
            pr = _pearson_r(b1, b2)
            if pr is not None:
                vals.append(pr)
        if len(vals) >= 10:
            vals.sort()
            alpha = (1 - BOOTSTRAP_CI) / 2
            p_ci_low = vals[int(len(vals) * alpha)]
            p_ci_high = vals[min(int(len(vals) * (1 - alpha)), len(vals) - 1)]

    # Reliably positive iff the de-coupled partial's LOWER 95% CI clears zero.
    decoupled_reliably_positive = bool(
        partial_r is not None and p_ci_low == p_ci_low and p_ci_low > 0.0
    )
    return {
        "rho_8a": rho,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "threshold_low": H8A_RHO_FLOOR,
        "headline_met": headline_met,
        "partial_r": partial_r,
        "partial_ci_low": p_ci_low,
        "partial_ci_high": p_ci_high,
        "decoupled_partial_positive": decoupled_reliably_positive,
        "supported": bool(headline_met and decoupled_reliably_positive),
        "n_participants": len(users_in),
        "n_probe_rows": len(probe_abs),
    }


def render_h8_result(h8a: dict[str, Any] | None) -> str:
    """H8 narrative-immersion (scoring.md §9). COHORT secondary hypothesis — reported with effect
    sizes + CIs, NEVER a per-person reveal and never a gate-criterion (§9.5). H8a supported only if
    the headline correlation lower-CI AND the de-coupled partial's lower-CI both clear their floors
    (the §9.2 regression-to-the-mean guard — the partial's CI must clear zero, not just its sign)."""
    if h8a is None:
        return (
            "H8 (narrative immersion — cohort secondary): insufficient data — supply --h8-log with "
            "≥3 participants who each completed both forms of ≥3 low-stakes pairs (§9.2/§9.5)."
        )

    def _f(v: Any) -> str:
        return "nan" if (v is None or v != v) else f"{v:+.3f}"

    lines = [
        "H8a — narrative debiasing (low-stakes paired probes, §9.2; COHORT secondary, never a "
        "per-person reveal):",
        f"  rho_8a = corr(D_low, gap_abs) = {_f(h8a['rho_8a'])}  "
        f"95% CI [{_f(h8a['ci_low'])}, {_f(h8a['ci_high'])}]  "
        f"lower ≥ {h8a['threshold_low']:.2f}? {_met_glyph(h8a['headline_met'])}",
        f"  de-coupled partial (r_narr·stated | r_abs, Frisch–Waugh–Lovell) = {_f(h8a['partial_r'])}  "
        f"95% CI [{_f(h8a['partial_ci_low'])}, {_f(h8a['partial_ci_high'])}]  "
        f"lower CI > 0? {_met_glyph(h8a['decoupled_partial_positive'])}",
        f"  SUPPORTED (headline lower-CI ≥ floor AND de-coupled partial lower-CI > 0 — the "
        f"regression-to-the-mean guard, §9.2) {_met_glyph(h8a['supported'])}  "
        f"[{h8a['n_participants']} participants, {h8a['n_probe_rows']} probe rows]",
        "  Read: a narrative form pulling behaviour toward stated values is DEBIASING, not virtue — "
        "the effect is a cohort property, never scored per person. H8b (attachment-laden shift, "
        "§9.4) deferred — needs the per-character attachment instrument (§9.3).",
    ]
    return "\n".join(lines)


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


def _f3(v: Any) -> str:
    """Format a float to 3dp, or 'nan' for None/NaN (shared by the discriminant renders)."""
    return "nan" if (v is None or v != v) else f"{v:+.3f}"


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
    h9b_disc: dict[str, Any] | None = None,
) -> str:
    """H9 self-prediction calibration (scoring.md §14). Axis channel and cost-of-
    virtue channel reported SEPARATELY — never pooled (§14.7)."""
    if all(x is None for x in (h9a, h9b, h9c, h9b_disc)) and cov is None:
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
            f"{_met_glyph(h9b['pre_registered_threshold_met'])}"
        )
    else:
        lines.append("  H9b stability: insufficient data (need --predictions-window-b, ≥3 shared participants)")
    if h9b_disc is not None:
        lines.append(
            f"  H9b DISCRIMINANT (cal_error ~ [aspirational gap, revealed level])  "
            f"R² = {h9b_disc['r2']:.3f}, upper 95% CI {_f3(h9b_disc['r2_ci_high'])}, n = {h9b_disc['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {h9b_disc['ceiling']:.2f} — self-knowledge NOT reducible to "
            f"over-claiming + virtue level, §14.4): {_met_glyph(h9b_disc['pre_registered_threshold_met'])}  "
            f"(cal·gap r = {_f3(h9b_disc['cal_gap_r'])}, cal·revealed r = {_f3(h9b_disc['cal_revealed_r'])}, cohort/no-pool)"
        )
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
    h10b_disc: dict[str, Any] | None = None,
) -> str:
    """H10 cross-situational consistency (scoring.md §15). Value-neutral: the
    per-construct sd_i(c) and V_i name WHERE a person sits on steadiness↔
    responsiveness; they never rank (Dancy caveat, §15.5)."""
    if h10a is None and h10c is None and n_construct_sd_cells == 0 and h10b_disc is None:
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
            f"(the level de-confound is the H10b discriminant, below)"
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
    if h10b_disc is not None:
        lines.append(
            f"  H10b DISCRIMINANT (V_i ~ [level, aspirational gap, self-prediction error])  "
            f"R² = {h10b_disc['r2']:.3f}, upper 95% CI {_f3(h10b_disc['r2_ci_high'])}, n = {h10b_disc['n_participants']}"
        )
        lines.append(
            f"     main leg (upper CI < {h10b_disc['ceiling']:.2f} — consistency NOT reducible to level + "
            f"over-claim + self-insight, §15.3): {_met_glyph(h10b_disc['discriminant_met'])}  "
            f"(V·level r = {_f3(h10b_disc['v_level_r'])}, V·gap r = {_f3(h10b_disc['v_gap_r'])}, "
            f"V·cal_error r = {_f3(h10b_disc['v_cal_error_r'])}, cohort/no-pool)"
        )
        lines.append(
            f"     de-confound leg — sd_i(c) ~ |mbar_i(c)|  R² = {_f3(h10b_disc['deconf_r2'])}, "
            f"upper 95% CI {_f3(h10b_disc['deconf_r2_ci_high'])}, {h10b_disc['deconf_n_cells']} cells "
            f"(upper CI < {h10b_disc['ceiling']:.2f} — variability is not a mid-scale range artifact): "
            f"{_met_glyph(h10b_disc['deconf_met'])}  (sd·|mbar| r = {_f3(h10b_disc['deconf_sd_absmbar_r'])}; "
            f"cell-level, a pseudo-replication caveat)"
        )
        lines.append(
            f"     H10b supported (BOTH legs clear the ceiling): "
            f"{_met_glyph(h10b_disc['pre_registered_threshold_met'])}"
        )
    return "\n".join(lines)


def render_h11_result(
    h11a: dict[str, Any] | None,
    h11c: dict[str, Any] | None,
    person_shape_n: int,
    radius_finite: int,
    radius_censored: int,
    h11b: dict[str, Any] | None = None,
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
            f"(discriminant half H11b runs from --h11b-log, §16.3)"
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
    if h11b is not None:
        lines.append(
            f"  H11b shape DISCRIMINANT (β_i ~ [near concern, resource-allocation generosity])  "
            f"R² = {h11b['r2']:.3f}, upper 95% CI {_f3(h11b['r2_ci_high'])}, n = {h11b['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {h11b['ceiling']:.2f} — shape NOT reducible to generosity, "
            f"§1.3): {_met_glyph(h11b['pre_registered_threshold_met'])}  "
            f"(\"reach is not height\"; β·generosity r = {_f3(h11b['beta_generosity_r'])}, cohort/no-pool)"
        )
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
    h12b_disc: dict[str, Any] | None = None,
) -> str:
    """H12 moral hypocrisy / self–other judgment asymmetry (scoring.md §18).
    Value-neutral: H_i names the direction and size of a person's self–other gap —
    harsher-on-others (self-serving) and harsher-on-self (self-critical) are both
    described, never ranked (§18.4). "Hypocrisy" is the construct's name in the
    literature; the reveal states the asymmetry descriptively, never as a verdict.
    A declined judgment drops the pair, never imputed to 0 (§18.1 pairing lock)."""
    if h12a is None and h12c is None and person_asymmetry_n == 0 and h12b_disc is None:
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
    if h12b_disc is not None:
        lines.append(
            f"  H12b DISCRIMINANT (H_i asymmetry ~ [aspirational gap, self-prediction error])  "
            f"R² = {h12b_disc['r2']:.3f}, upper 95% CI {_f3(h12b_disc['r2_ci_high'])}, n = {h12b_disc['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {h12b_disc['ceiling']:.2f} — the self–other double standard NOT reducible "
            f"to over-claiming + self-insight, §18.5): {_met_glyph(h12b_disc['pre_registered_threshold_met'])}  "
            f"(H·gap r = {_f3(h12b_disc['h_gap_r'])}, H·cal_error r = {_f3(h12b_disc['h_cal_error_r'])}, cohort/no-pool)"
        )
    lines.append(
        "  Value-neutral: harsher-on-others (self-serving) and harsher-on-self (self-critical/scrupulous) "
        "are both just described — neither is scored as better (§18.4). H12c is a cohort validity anchor, "
        "not a per-person verdict. H12b is the discriminant — the asymmetry channel vs the aspirational gap "
        "+ self-prediction error (§18.5)."
    )
    return "\n".join(lines)


def render_r1_result(
    r1a: dict[str, Any] | None,
    r1c: dict[str, Any] | None,
    profile_n: int,
    mean_internalization: float,
    mean_symbolization: float,
    r1b: dict[str, Any] | None = None,
    r1a_symbol: dict[str, Any] | None = None,
    r1b_h12: dict[str, Any] | None = None,
) -> str:
    """R1 moral identity centrality (scoring.md §19). Two DISJOINT facets reported
    SEPARATELY — internalization (private) and symbolization (public) — never pooled
    into one "moral-identity score" (§13.5, load-bearing here). Value-neutral: high
    centrality is NOT scored as better than low (a self-defining moral identity can
    be integrity OR rigid self-righteousness — the dark side of moral identity), and
    internalizing is not ranked above symbolizing; the reveal describes the profile,
    never a verdict (§19.4)."""
    if r1a is None and r1a_symbol is None and r1c is None and profile_n == 0 and r1b is None and r1b_h12 is None:
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
    if r1a_symbol is not None:
        lines.append(
            f"  R1a centrality reliability (split-half odd/even, corr of symbolization)  r = {r1a_symbol['r']:+.3f}, "
            f"95% CI {_ci_str(r1a_symbol)}, n = {r1a_symbol['n']}"
        )
        lines.append(
            f"     threshold (lower CI ≥ {r1a_symbol['threshold_low']:.2f}): "
            f"{_met_glyph(r1a_symbol['pre_registered_threshold_met'])}"
        )
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
    if r1b is not None:
        lines.append(
            f"  R1b MODERATION (over-claim gap ~ internalization, standardized slope = corr)  "
            f"r = {r1b['r']:+.3f}, 95% CI {_ci_str(r1b)}, n = {r1b['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {r1b['ceiling']:.1f}, one-sided): "
            f"{_met_glyph(r1b['pre_registered_threshold_met'])}  "
            f"(a more internalized moral identity predicts LESS over-claiming — Aquino & Reed 2002; §19.5)"
        )
    else:
        lines.append(
            "  R1b moderation (does internalization predict a smaller over-claim gap?): "
            "insufficient data (need the {session, card_sort, identity} bundle via --r1b-log, "
            f"≥{R1B_MIN_PARTICIPANTS} joined participants)"
        )
    if r1b_h12 is not None:
        lines.append(
            f"  R1b H12-DAMPENING (self–other severity asymmetry H_i ~ internalization, standardized slope = corr)  "
            f"r = {r1b_h12['r']:+.3f}, 95% CI {_ci_str(r1b_h12)}, n = {r1b_h12['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {r1b_h12['ceiling']:.1f}, one-sided): "
            f"{_met_glyph(r1b_h12['pre_registered_threshold_met'])}  "
            f"(a more internalized moral identity predicts a SMALLER holier-than-thou asymmetry — "
            f"Aquino & Reed 2002 × Tappin & McKay 2017; §19.5)"
        )
    else:
        lines.append(
            "  R1b H12-dampening (does internalization predict a smaller self–other severity asymmetry?): "
            "insufficient data (need the {identity, hypocrisy} shared-cohort bundle via --r1b-h12-log, "
            f"≥{R1B_MIN_PARTICIPANTS} joined participants)"
        )
    lines.append(
        "  Value-neutral: a highly self-defining moral identity is NOT scored as better than a peripheral one "
        "(centrality can be integrity OR rigid self-righteousness, §19.4); the facets are described, never ranked. "
        "R1c is a cohort construct-validity anchor, not a per-person verdict. R1b is a COHORT-level moderation "
        "read — never a per-person verdict, and a very negative gap is modesty, not scored better; the H12 "
        "dampening leg is built (§19.5 — a very negative asymmetry is harsher-on-self, not scored better), the "
        "H10/H11 legs remain deferred (cohort-coupled), see build-and-validate.md."
    )
    return "\n".join(lines)


def render_r6_result(
    r6a: dict[str, Any] | None,
    r6d: dict[str, Any] | None,
    profile_n: int,
    mean_moral_objectivism: float,
    mean_taste_objectivism: float,
    r6b_disc: dict[str, Any] | None = None,
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
    if r6a is None and r6d is None and profile_n == 0 and r6b_disc is None:
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
    if r6b_disc is not None:
        lines.append(
            f"  R6b DISCRIMINANT (objectivism_moral ~ [R2 sacredness |P_i|, R1 centrality, value-importance])  "
            f"R² = {r6b_disc['r2']:.3f}, upper 95% CI {_f3(r6b_disc['r2_ci_high'])}, n = {r6b_disc['n_participants']}"
        )
        lines.append(
            f"     threshold (upper CI < {r6b_disc['ceiling']:.2f} — treating morals as objective FACT NOT reducible "
            f"to how absolute/central/broad the values are, §20.5): {_met_glyph(r6b_disc['pre_registered_threshold_met'])}  "
            f"(obj·sacredness r = {_f3(r6b_disc['o_sacredness_r'])}, obj·centrality r = {_f3(r6b_disc['o_centrality_r'])}, "
            f"obj·importance r = {_f3(r6b_disc['o_importance_r'])}, cohort/no-pool)"
        )
    lines.append(
        "  Value-neutral (extra force — the branch is charged): holding morals as objective facts is NOT scored as "
        "better or worse than holding them as your own (objectivism = moral clarity OR rigid intolerance; subjectivism "
        "= tolerant pluralism OR standing for nothing — each pole dual-read, §20.4); the stance is described, never ranked. "
        "R6d is a cohort construct-validity anchor, not a per-person verdict. R6b is the discriminant (objectivism vs R2 "
        "sacredness / R1 centrality / value-importance, §20.5); R6c (the stated–revealed meta-gap — the revealed "
        "tolerance/compromise + objectivist-language signatures) remains deferred (κ-gated); see build-and-validate.md."
    )
    return "\n".join(lines)


def render_a3_result(
    kappa: dict[str, Any] | None,
    profile: dict[str, dict[str, float]],
) -> str:
    """A3 moral-language channel — the coder + the κ gate (scoring.md §21). A THIRD
    channel on values (what a person spontaneously moralizes about, in what moral
    vocabulary), distinct from the elicited-stated inventory and revealed behavior. The
    reveal is DESCRIPTIVE and value-NEUTRAL: it names which foundations a person's
    language invokes and at what rate — never ranks the foundations, never scores "more
    moral language" as better (genuine engagement OR grandstanding), never reads fluency
    as virtue (§21.4). The ENTIRE channel is walled DESCRIPTIVE/EXPLORATORY-ONLY until the
    coder clears κ ≥ 0.70 against REAL human gold (§21.2) — the synthetic κ below certifies
    only the machinery."""
    if kappa is None and not profile:
        return (
            "(A3: insufficient data — supply --language-log with free-text utterances "
            "carrying gold_foundations reference codes)"
        )
    lines = ["A3 (moral-language channel — the MFD coder + the κ gate, DESCRIPTIVE-ONLY until human κ):"]
    if kappa is not None:
        k = kappa["kappa"]
        k_str = "undefined" if k is None else f"{k:+.3f}"
        gate_glyph = "✓" if kappa["kappa_met_synthetic"] else "✗"
        lines.append(
            f"  Coding reliability κ (Cohen, coder vs. gold over {kappa['n_utterances']} utterance(s) "
            f"× {len(MFD_FOUNDATIONS)} foundations = {kappa['n_cells']} binary cells): {k_str}"
        )
        lines.append(
            f"     agreement {kappa['agree_cells']}/{kappa['n_cells']} cells; coder-present {kappa['coder_present']}, "
            f"gold-present {kappa['gold_present']} (marginals shown — κ is never a bare scalar)"
        )
        lines.append(
            f"     κ ≥ {kappa['kappa_gate']:.2f} gate on THIS synthetic fixture: {gate_glyph}  "
            f"— certifies the MACHINERY only; promotable = {kappa['promotable']} "
            f"(real κ needs ~200 HUMAN gold codes, 50/domain × 2 raters — Dave/human-gated)"
        )
    else:
        lines.append("  Coding reliability κ: insufficient data (need ≥1 scorable utterance with gold codes)")
    if profile:
        # Cohort mean foundation rates, in CANONICAL MFD order — deliberately NOT sorted by
        # rate (sorting would imply a ranking; foundations are value-neutral, §21.4).
        n = len(profile)
        means = {
            f: sum(p.get(f, 0.0) for p in profile.values()) / n for f in MFD_FOUNDATIONS
        }
        rate_str = ", ".join(f"{f} {means[f]:.2f}" for f in MFD_FOUNDATIONS)
        lines.append(
            f"  foundation_i(f) profile — cohort mean invocation rate over {n} participant(s), "
            f"canonical order (NOT ranked):"
        )
        lines.append(f"     {rate_str}")
        lines.append(
            "     (a volume-normalized RATE, never pooled into a scalar; a low rate = uses less "
            "moral language, a Dancy particularist style, not a deficit — §21.4)"
        )
    lines.append(
        "  Value-neutral / language ≠ value: more moral talk is NOT better (engagement OR "
        "self-presentational grandstanding, Tosi & Warmke); verbal fluency must never read as "
        "virtue; declining to moralize is a legitimate particularist move (§21.4). κ is a coder-"
        "pair reliability statistic, NEVER a person score (§13.5). NOT parity-gated by design — "
        "LLM coding is non-deterministic, deliberately outside the poc-projection parity contract "
        "(§1.5). Deferred (cohort/κ-gated): the framing ratio, the third ordering L_i + the three "
        "S/R/L concordances (extending §13.4), and H-A3a/b/c (reliability / distinctness / the "
        "talk–walk grandstanding gap); see build-and-validate.md."
    )
    return "\n".join(lines)


def render_a4_result(
    a4a: dict[str, Any] | None,
    n_users: int,
    n_cells: int,
    a4b: dict[str, Any] | None = None,
) -> str:
    """A4 decision conflict — the PROCESS channel (scoring.md §22). RT-derived EFFORT /
    ambivalence, confound-guarded (residualized on reading-load + order, timeouts + the timed set
    excluded, z within-person). NEVER a framework read (slow ≠ deontological; Bago & De Neys 2019)
    and value-neutral (high conflict is not worse — effortful virtue is arguably the stronger
    signal). Exploratory, RT-only (revisions Dave-gated, §4 Q1), NO public card (§1.4)."""
    if a4a is None and a4b is None:
        return (
            "A4 (decision conflict — process channel): insufficient data — supply --process-log "
            "with per-item response_time_ms + prompt_chars + presented_position across ≥2 "
            "sessions/user (untimed, non-timeout items; ≥3 users scorable per domain in both halves)."
        )
    lines = ["A4 (decision conflict — RT-derived effort/ambivalence, value-neutral, exploratory):"]
    if a4a is not None:
        lines.append(
            f"  conflict(i, domain) = within-person z of response time, residualized on reading-load "
            f"+ presented position; timeouts + the timed quick-fire set excluded (CV-1). "
            f"{n_cells} (user × domain) cell(s) over {n_users} participant(s)."
        )
        lines.append(
            f"  A4a conflict reliability (split-half odd/even, per-domain test–retest): "
            f"{a4a['n_domains_met']}/{a4a['n_domains']} domain(s) clear the lower-CI ≥ "
            f"{a4a['threshold_low']:.2f} bar  {_met_glyph(a4a['any_met'])}"
        )
        for dom in sorted(a4a["per_domain"]):
            res = a4a["per_domain"][dom]
            lines.append(
                f"     {dom}: r = {res['r']:+.3f}, 95% CI {_ci_str(res)}, n = {res['n']}  "
                f"{_met_glyph(res.get('pre_registered_threshold_met'))}"
            )
    if a4b is not None:
        ci_hi = a4b["r2_ci_high"]
        ci_lo = a4b["r2_ci_low"]
        ci_txt = (
            "nan" if ci_hi is None or ci_hi != ci_hi
            else f"[{ci_lo:+.3f}, {ci_hi:+.3f}]"
        )
        lines.append(
            f"  A4b — is conflict a DISTINCT channel, or a shadow of the choice? "
            f"conflict(i, d) ~ [z_revealed, |gap|], within-person (cohort/no-pool): "
            f"R² = {a4b['r2']:.3f}, upper 95% CI {ci_txt} vs ceiling {a4b['ceiling']:.2f}  "
            f"{_met_glyph(a4b['supported'])}"
        )
        lev_r = a4b["conflict_level_r"]
        gap_r = a4b["conflict_gap_r"]
        lev_txt = "n/a" if lev_r is None else f"{lev_r:+.3f}"
        gap_txt = "n/a" if gap_r is None else f"{gap_r:+.3f}"
        lines.append(
            f"     within-person descriptive companions: conflict·level r = {lev_txt}, "
            f"conflict·|gap| r = {gap_txt} "
            f"({a4b['n_cells']} cell(s) over {a4b['n_participants']} participant(s))."
        )
        lines.append(
            "     Read: DISTINCT means effort carries information the choice level + aspirational "
            "gap do NOT — NOT reducible to how far from the ideal or how extreme the choice was; "
            "cohort-level, no participant ranked. Cell-bootstrap CI understates repeated-user "
            "dependence, so the distinctness bar stays conservative."
        )
    a4b_note = (
        "A4b (does conflict add information beyond the choice) reported above."
        if a4b is not None
        else "A4b (does conflict add information beyond the choice) is cohort-coupled and DEFERRED."
    )
    lines.append(
        "  Read: EFFORT/ambivalence, never a moral-framework label (slow ≠ deontological, fast ≠ "
        "utilitarian; Bago & De Neys 2019). Value-neutral: high conflict is not worse than low — "
        "finding virtue effortful is arguably the STRONGER character signal (effortful virtue). "
        "Exploratory, RT-only (answer-revision capture deferred, §4 Q1); an analysis adjunct with "
        f"NO public card — context for the reveal, never a headline. {a4b_note}"
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
        "--language-log",
        type=Path,
        default=None,
        help="Optional moral-language log (free-text utterances + gold_foundations codes) for the A3 coder + κ gate (§21).",
    )
    parser.add_argument(
        "--process-log",
        type=Path,
        default=None,
        help="Optional decision-process log (per-item response_time_ms + prompt_chars + presented_position) for the A4 conflict channel (§22).",
    )
    parser.add_argument(
        "--h8-log",
        type=Path,
        default=None,
        help="Optional narrative-immersion paired-probe log (per-form primary_axis_score + stated_aspirational) for the H8a debiasing test (§9.2).",
    )
    parser.add_argument(
        "--h8-manifest",
        type=Path,
        default=DEFAULT_H8_MANIFEST,
        help="Paired-probe manifest (pair_id→domain/stakes/refs) for H8 (default: scenarios/h8-probe-pairs.json).",
    )
    parser.add_argument(
        "--h11b-log",
        type=Path,
        default=None,
        help="Optional combined circle + resource-allocation session log for the H11b moral-circle SHAPE "
             "DISCRIMINANT (§16.3): tests whether the circle shape β_i is reducible to near-bin concern + "
             "generosity level. Uses the same --distance-map as --circle-log.",
    )
    parser.add_argument(
        "--h9b-log",
        type=Path,
        default=None,
        help="Optional combined session + card-sort + predictions log (object with session/card_sort/"
             "predictions arrays for a SHARED cohort) for the H9b self-CALIBRATION DISCRIMINANT (§14.4): "
             "tests whether cal_error_i is reducible to the aspirational gap + revealed level.",
    )
    parser.add_argument(
        "--h12b-log",
        type=Path,
        default=None,
        help="Optional combined session + card-sort + predictions + hypocrisy log (object with session/"
             "card_sort/predictions/hypocrisy arrays for a SHARED cohort) for the H12b moral-hypocrisy "
             "DISCRIMINANT (§18.5): tests whether the self–other asymmetry H_i is reducible to the "
             "aspirational gap + self-prediction error.",
    )
    parser.add_argument(
        "--r6b-log",
        type=Path,
        default=None,
        help="Optional combined objectivism + protected-values + identity + card-sort log (object with "
             "objectivism/protected/identity/card_sort arrays for a SHARED cohort) for the R6b metaethical-"
             "objectivism DISCRIMINANT (§20.5): tests whether objectivism_moral_i is reducible to R2 "
             "sacredness (|P_i|) + R1 centrality (internalization) + value-importance.",
    )
    parser.add_argument(
        "--h10b-log",
        type=Path,
        default=None,
        help="Optional combined context + session + card-sort + predictions log (object with context/"
             "session/card_sort/predictions arrays for a SHARED cohort) for the H10b cross-situational-"
             "consistency DISCRIMINANT (§15.3): tests whether the person variability index V_i is reducible "
             "to level + aspirational gap + self-prediction error, and de-confounds sd_i(c) vs |mbar_i(c)|.",
    )
    parser.add_argument(
        "--a4b-log",
        type=Path,
        default=None,
        help="Optional combined process + session + card-sort log (object with process/session/card_sort "
             "arrays for a SHARED cohort — process `user` must equal session `user_id`) for the A4b "
             "decision-conflict DISCRIMINANT (§22.4): tests whether within-person conflict(i, d) is a "
             "distinct channel or reducible to the choice level + aspirational-gap magnitude.",
    )
    parser.add_argument(
        "--r1b-log",
        type=Path,
        default=None,
        help="Optional combined session + card-sort + identity log (object with session/card_sort/identity "
             "arrays for a SHARED cohort — identity `user` must equal session `user_id`) for the R1b moral-"
             "identity META-MODERATION leg (§19.5): regresses the §6 over-claim gap_i on internalization_i; "
             "supported iff the upper 95%% CI of corr(internalization, gap) < 0 (higher internalization → "
             "smaller over-claim).",
    )
    parser.add_argument(
        "--r1b-h12-log",
        type=Path,
        default=None,
        help="Optional combined identity + hypocrisy log (object with identity/hypocrisy arrays for a "
             "SHARED cohort — identity `user` must equal hypocrisy `user`) for the R1b H12-DAMPENING leg "
             "(§19.5, the first of R1b's H10–H12 dampening legs): regresses the self–other asymmetry H_i on "
             "internalization_i; supported iff the upper 95%% CI of corr(internalization, H) < 0 (higher "
             "internalization → smaller holier-than-thou asymmetry).",
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
    # is supplied. Self-contained on its own fixture. The on-device sd_i(c)/V_i
    # reveal is SHIPPED (§15.7): contextVariability in poc-projection.js mirrors
    # context_profile_by_user under the JS↔Python parity lock, and the analyzer
    # emits the companion H10.context_variability_reveal.
    h10a_result: dict[str, Any] | None = None
    h10c_result: dict[str, Any] | None = None
    h10_person_variability_n = 0
    h10_construct_sd_n = 0
    h10_variability_reveal: list[dict[str, Any]] = []   # per-person N=1 reveal (§15.5), facets + V_i, no-pool
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
        h10_profiles = context_profile_by_user(h10_records)
        for _u in sorted(h10_profiles):
            _p = h10_profiles[_u]
            h10_variability_reveal.append({
                "user": _u,
                "v": _p["v"],            # None ⇔ below the ≥3-construct floor (§1.5)
                "n_constructs": _p["n_constructs"],
                "constructs": _p["constructs"],
            })
        h10a_result = compute_h10a_reliability(h10_records)
        h10c_result = compute_h10c_observer_effect(h10_records)

    # H11 moral-circle radius (scoring.md §16) if a counterparty-tagged in-group
    # log is supplied. Self-contained on its own fixture. The on-device β_i/R_i
    # reveal is mirrored by circleShape in poc-projection.js under the parity
    # lock (§16.7). Reads the circle_radius secondary axis via the versioned
    # counterparty→distance-bin ordering map (a v0.1 DRAFT; its REL-2
    # inter-rater validation is Dave/human-gated).
    h11a_result: dict[str, Any] | None = None
    h11c_result: dict[str, Any] | None = None
    h11_person_shape_n = 0
    h11_radius_finite = 0
    h11_radius_censored = 0
    h11_shape_reveal: list[dict[str, Any]] = []
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
        for _u in sorted(h11_shapes):
            _s = h11_shapes[_u]
            h11_shape_reveal.append({
                "user": _u,
                "beta": _s["beta"],           # steepness facet — described, never ranked (§16.5)
                "radius": _s["radius"],       # None ⇔ right-censored, NEVER made finite (§13.2)
                "censored": _s["censored"],
                "n_bins": _s["n_bins"],
                "midpoint": _s["midpoint"],
                "near_bin": _s["near_bin"],
                "far_bin": _s["far_bin"],
                "near_concern": _s["near_concern"],
                "far_concern": _s["far_concern"],
            })
        h11a_result = compute_h11a_reliability(h11_records)
        h11c_result = compute_h11c_gradient(h11_records)

    # --- H11b moral-circle SHAPE DISCRIMINANT (§16.3): is the circle shape (β_i)
    # reducible to near-bin concern + a SEPARATE resource-allocation generosity level?
    # Discriminant-supported iff the UPPER 95% CI of the regression R² < H11B_R2_CEILING
    # — at least half the shape variance is NOT explained by generosity ("reach is not
    # height", Crimston 2016). Completes H11 = H11a ∧ H11b. Reads a combined log carrying
    # BOTH the in-group circle items and the resource-allocation items for the same
    # cohort, via the same --distance-map. Cohort-level statistic, NO per-person reveal →
    # Python-only, parity stays green (same scope pattern as H9b/H10b/R2c deferred halves).
    h11b_result: dict[str, Any] | None = None
    if args.h11b_log:
        try:
            with args.h11b_log.open() as f:
                h11b_entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H11b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(h11b_entries, list):
            print("ERROR: H11b log must be a JSON array", file=sys.stderr)
            return 2
        try:
            h11b_dist_map, _ = load_counterparty_distance_map(args.distance_map)
        except FileNotFoundError:
            print(f"ERROR: distance map not found at {args.distance_map}", file=sys.stderr)
            return 2
        h11b_result = compute_h11b_discriminant(h11b_entries, tag_map, h11b_dist_map)

    # --- H9b self-CALIBRATION DISCRIMINANT (§14.4): is the self-prediction error magnitude
    # cal_error_i reducible to the aspirational gap_i + revealed level_i? Discriminant-supported
    # iff the UPPER 95% CI of the regression R² < H9B_R2_CEILING — the calibration axis carries
    # variance those two predictors do not. Completes H9b = stability ∧ discriminant. Reads a
    # combined log carrying session + card-sort + predictions for ONE shared cohort (the
    # discriminant couples calibration to the §3/§6 pipeline, so it can't ride the isolated
    # --predictions fixture). Cohort-level statistic, NO per-person reveal → Python-only, parity
    # stays green (same scope pattern as H10b/R2c deferred halves).
    h9b_discriminant_result: dict[str, Any] | None = None
    if args.h9b_log:
        try:
            with args.h9b_log.open() as f:
                h9b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H9b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(h9b_bundle, dict):
            print("ERROR: H9b log must be a JSON object with session/card_sort/predictions arrays", file=sys.stderr)
            return 2
        h9b_discriminant_result = compute_h9b_discriminant(
            h9b_bundle.get("session", []),
            h9b_bundle.get("card_sort", []),
            h9b_bundle.get("predictions", []),
            tag_map,
        )

    h12b_discriminant_result: dict[str, Any] | None = None
    if args.h12b_log:
        try:
            with args.h12b_log.open() as f:
                h12b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H12b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(h12b_bundle, dict):
            print("ERROR: H12b log must be a JSON object with session/card_sort/predictions/hypocrisy arrays", file=sys.stderr)
            return 2
        h12b_discriminant_result = compute_h12b_discriminant(
            h12b_bundle.get("session", []),
            h12b_bundle.get("card_sort", []),
            h12b_bundle.get("predictions", []),
            h12b_bundle.get("hypocrisy", []),
            tag_map,
        )

    r6b_discriminant_result: dict[str, Any] | None = None
    if args.r6b_log:
        try:
            with args.r6b_log.open() as f:
                r6b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading R6b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(r6b_bundle, dict):
            print("ERROR: R6b log must be a JSON object with objectivism/protected/identity/card_sort arrays", file=sys.stderr)
            return 2
        r6b_discriminant_result = compute_r6b_discriminant(
            r6b_bundle.get("objectivism", []),
            r6b_bundle.get("protected", []),
            r6b_bundle.get("identity", []),
            r6b_bundle.get("card_sort", []),
        )

    h10b_discriminant_result: dict[str, Any] | None = None
    if args.h10b_log:
        try:
            with args.h10b_log.open() as f:
                h10b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H10b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(h10b_bundle, dict):
            print("ERROR: H10b log must be a JSON object with context/session/card_sort/predictions arrays", file=sys.stderr)
            return 2
        h10b_discriminant_result = compute_h10b_discriminant(
            h10b_bundle.get("context", []),
            h10b_bundle.get("session", []),
            h10b_bundle.get("card_sort", []),
            h10b_bundle.get("predictions", []),
            tag_map,
        )

    a4b_discriminant_result: dict[str, Any] | None = None
    if args.a4b_log:
        try:
            with args.a4b_log.open() as f:
                a4b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading A4b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(a4b_bundle, dict):
            print("ERROR: A4b log must be a JSON object with process/session/card_sort arrays", file=sys.stderr)
            return 2
        a4b_discriminant_result = compute_a4b_discriminant(
            a4b_bundle.get("process", []),
            a4b_bundle.get("session", []),
            a4b_bundle.get("card_sort", []),
            tag_map,
        )

    # R1b moral-identity META-MODERATION leg (scoring.md §19.5) if a combined
    # {session, card_sort, identity} bundle for a SHARED cohort is supplied. Regresses
    # the §6 over-claim gap_i on internalization_i; supported iff the upper 95% CI of
    # corr(internalization, gap) < 0. Cohort-level, Python-only (no on-device reveal) so
    # parity stays green. Independent channels ⇒ no algebraic identity (the R1b lock).
    r1b_moderation_result: dict[str, Any] | None = None
    if args.r1b_log:
        try:
            with args.r1b_log.open() as f:
                r1b_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading R1b log: {e}", file=sys.stderr)
            return 2
        if not isinstance(r1b_bundle, dict):
            print("ERROR: R1b log must be a JSON object with session/card_sort/identity arrays", file=sys.stderr)
            return 2
        r1b_moderation_result = compute_r1b_moderation(
            r1b_bundle.get("session", []),
            r1b_bundle.get("card_sort", []),
            r1b_bundle.get("identity", []),
            tag_map,
        )

    # R1b H12-DAMPENING leg (scoring.md §19.5), the FIRST of R1b's three deferred H10–H12
    # dampening legs, if a combined {identity, hypocrisy} bundle for a SHARED cohort is
    # supplied. Regresses the self–other asymmetry H_i on internalization_i; supported iff
    # the upper 95% CI of corr(internalization, H) < 0 (higher internalization → smaller
    # holier-than-thou asymmetry). Cohort-level, Python-only (no on-device reveal) so parity
    # stays green. Independent channels ⇒ no algebraic identity (the H12-dampening lock).
    r1b_h12_dampening_result: dict[str, Any] | None = None
    if args.r1b_h12_log:
        try:
            with args.r1b_h12_log.open() as f:
                r1b_h12_bundle = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading R1b H12-dampening log: {e}", file=sys.stderr)
            return 2
        if not isinstance(r1b_h12_bundle, dict):
            print("ERROR: R1b H12-dampening log must be a JSON object with identity/hypocrisy arrays", file=sys.stderr)
            return 2
        r1b_h12_dampening_result = compute_r1b_h12_dampening(
            r1b_h12_bundle.get("hypocrisy", []),
            r1b_h12_bundle.get("identity", []),
        )

    # R2 sacred / protected values (scoring.md §17) if a cost-of-virtue log with
    # value_slot + wave (+ taboo) is supplied. Pure re-read of the `never` tail as
    # the protected set P_i (§13.2 censoring, categorical, never finitized). The
    # on-device P_i reveal is mirrored by protectedValues in poc-projection.js
    # under the parity lock (§17.7).
    r2a_result: dict[str, Any] | None = None
    r2b_result: dict[str, Any] | None = None
    r2_protected_set_n = 0
    r2_protected_none_n = 0
    r2_protected_set_sizes: list[int] = []
    r2_protected_reveal: list[dict[str, Any]] = []
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
        # First-wave protected-set census (per participant): the reveal counts AND
        # the §17.5 N=1 reveal rows come from the same protected_profile_by_user
        # pass (first-wave read unchanged from the original inline census).
        _pprofiles = protected_profile_by_user(protected_responses)
        for _user in sorted(_pprofiles):
            _row = _pprofiles[_user]
            if _row["n_professed"] > 0:
                r2_protected_set_n += 1
                r2_protected_set_sizes.append(_row["n_professed"])
            else:
                r2_protected_none_n += 1
            r2_protected_reveal.append({"user": _user, **_row})
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
    h12_asymmetry_reveal: list[dict[str, Any]] = []   # per-person N=1 H_i reveal (§18.1), signed, no-pool
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
        _h12_deltas = hypocrisy_deltas_by_user(hypocrisy_records)
        for _u in sorted(_h12_deltas):
            h12_asymmetry_reveal.append({
                "user": _u,
                "h": _h12_census.get(_u),   # None ⇔ below the ≥3-pair floor (§1.5), never scored thin
                "n_pairs": len(_h12_deltas[_u]),
            })

    # --- R1 moral identity centrality: the two-facet centrality read (§19). The
    # two facets are kept SEPARATE (never pooled, §13.5); the moderation legs (R1b —
    # centrality × the §6 gap / H10–H12) are cohort-coupled and DEFERRED. Python-only,
    # parity stays green — no on-device reveal this increment.
    r1a_result: dict[str, Any] | None = None
    r1a_symbol_result: dict[str, Any] | None = None
    r1c_result: dict[str, Any] | None = None
    r1_profile_n = 0
    r1_mean_internalization = 0.0
    r1_mean_symbolization = 0.0
    r1_facet_reveal: list[dict[str, Any]] = []   # per-person N=1 facet reveal (§19.1), no-pool
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
        r1a_symbol_result = compute_r1a_symbolization_reliability(identity_records)
        r1c_result = compute_r1c_internalization_anchor(identity_records)
        # The N=1 on-device reveal (§19.1): each person's two facet means, exposed
        # SEPARATELY (never pooled into one centrality scalar, §13.5) — None ⇔ that
        # facet is below the ≥3-item floor (SUPPRESSED, §1.5). Mirrors the runtime's
        # poc-projection.js centralityFacets, whose equality is locked in
        # check_impl_parity.py (JS↔Python). Reuses the already-computed facet dicts.
        _r1_int_items = centrality_items_by_user(identity_records, "internalization")
        _r1_sym_items = centrality_items_by_user(identity_records, "symbolization")
        for _u in sorted(set(_r1_int_items) | set(_r1_sym_items)):
            r1_facet_reveal.append({
                "user": _u,
                "internalization": _r1_intern.get(_u),   # None ⇔ facet below the ≥3-item floor
                "symbolization": _r1_symbol.get(_u),
                "n_internalization": len(_r1_int_items.get(_u, [])),
                "n_symbolization": len(_r1_sym_items.get(_u, [])),
            })

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
    r6_claim_reveal: list[dict[str, Any]] = []   # per-person N=1 claim-type reveal (§20.1), no-pool
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
        # The N=1 on-device reveal (§20.1): each person's two claim-type reads, exposed
        # SEPARATELY (never pooled into one objectivism/conviction scalar, §13.5) — None ⇔
        # that read is below the ≥3-item floor (SUPPRESSED, §1.5). The two reads are shown
        # side by side WITHOUT a per-person moral>taste verdict (that gradient is the
        # cohort-only R6d). Mirrors the runtime's poc-projection.js objectivismReads, whose
        # equality is locked in check_impl_parity.py (JS↔Python). Reuses the facet dicts.
        _r6_moral_items = objectivism_items_by_user(objectivism_records, "moral")
        _r6_taste_items = objectivism_items_by_user(objectivism_records, "taste")
        for _u in sorted(set(_r6_moral_items) | set(_r6_taste_items)):
            r6_claim_reveal.append({
                "user": _u,
                "moral": _r6_moral.get(_u),   # None ⇔ claim type below the ≥3-item floor
                "taste": _r6_taste.get(_u),
                "n_moral": len(_r6_moral_items.get(_u, [])),
                "n_taste": len(_r6_taste_items.get(_u, [])),
            })

    # --- A3 moral-language channel: the coder + the κ gate (§21). Builds the buildable
    # KEYSTONE — a deterministic MFD-style foundation coder, Cohen's κ inter-rater
    # validation, and the foundation_i(f) profile — all walled DESCRIPTIVE-ONLY until the
    # coder clears κ ≥ 0.70 against REAL human gold (§21.2). NOT parity-gated BY DESIGN:
    # LLM/language coding is non-deterministic, deliberately outside the poc-projection ↔
    # analyze.py parity contract (§1.5/§3) — the first branch out of parity scope on
    # purpose. The framing ratio, the third ordering L_i + the three concordances, and
    # H-A3a/b/c are cohort/κ-gated and DEFERRED (see build-and-validate.md).
    a3_kappa_result: dict[str, Any] | None = None
    a3_profile: dict[str, dict[str, float]] = {}
    if args.language_log:
        try:
            with args.language_log.open() as f:
                language_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading language log: {e}", file=sys.stderr)
            return 2
        if not isinstance(language_records, list):
            print("ERROR: language log must be a JSON array", file=sys.stderr)
            return 2
        a3_kappa_result = compute_a3_coding_kappa(language_records)
        a3_profile = foundation_profile_by_user(language_records)

    # --- A4 decision conflict — the PROCESS channel (§22). Re-analysis of already-logged
    # response-time dynamics into a within-person, confound-guarded EFFORT signal — residualized
    # on reading-load + order, timeouts + the timed set (CV-1) excluded, z within-person. RT-only
    # (answer-revision capture Dave/runtime-gated, §4 Q1). Value-neutral and NEVER a framework read
    # (Bago & De Neys 2019). EXPLORATORY, no public card (§1.4). Parity-gated in principle; the
    # on-device conflict reveal + its JS parity lock are DEFERRED (as the H9–R6 reveals are).
    a4a_result: dict[str, Any] | None = None
    a4_n_users = 0
    a4_n_cells = 0
    if args.process_log:
        try:
            with args.process_log.open() as f:
                process_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading process log: {e}", file=sys.stderr)
            return 2
        if not isinstance(process_records, list):
            print("ERROR: process log must be a JSON array", file=sys.stderr)
            return 2
        _a4_cells = conflict_by_user_domain(process_records)
        a4_n_cells = len(_a4_cells)
        a4_n_users = len({u for (u, _d) in _a4_cells})
        a4a_result = compute_a4a_conflict_reliability(process_records)

    # --- H8 narrative immersion — the COHORT secondary channel (scoring.md §9). Re-uses the §2–§3
    # item scoring: the log carries already-scored primary-axis values per (user, pair, form); the
    # manifest supplies pairing/domain/stakes. H8a (debiasing, low-stakes) tests whether the narrative
    # form pulls behaviour toward stated values — with the §9.2 regression-to-the-mean guard (D and gap
    # SHARE r_abs, so a de-coupled Frisch–Waugh–Lovell partial must AGREE with the headline CI). NEVER a
    # per-person reveal and never a gate-criterion (§9.5) → no on-device projection (parity stays green),
    # no public card (like A4). H8b (attachment shift, §9.4) needs the §9.3 instrument and is DEFERRED.
    h8a_result: dict[str, Any] | None = None
    if args.h8_log:
        try:
            with args.h8_log.open() as f:
                h8_records = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H8 log: {e}", file=sys.stderr)
            return 2
        if not isinstance(h8_records, list):
            print("ERROR: H8 log must be a JSON array", file=sys.stderr)
            return 2
        try:
            h8_pairs = load_h8_pairs(args.h8_manifest)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR loading H8 manifest: {e}", file=sys.stderr)
            return 2
        h8a_result = compute_h8a_debiasing(h8_records, h8_pairs)

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
        if h9b_discriminant_result is not None:
            # H9b DISCRIMINANT half — COHORT-level R² (§14.4). NO pooled per-person scalar:
            # cal_error_i, gap_i and revealed_level_i stay separate facets (§13.5). supported
            # is EXACTLY (r2 upper-CI < ceiling); the gate re-derives it (check_h9).
            h9_block["H9b_discriminant"] = {
                "r2": h9b_discriminant_result["r2"],
                "r2_ci_low": _nan_to_none(h9b_discriminant_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(h9b_discriminant_result["r2_ci_high"]),
                "ceiling": h9b_discriminant_result["ceiling"],
                "cal_gap_r": h9b_discriminant_result["cal_gap_r"],
                "cal_revealed_r": h9b_discriminant_result["cal_revealed_r"],
                "n_participants": h9b_discriminant_result["n_participants"],
                "supported": h9b_discriminant_result["supported"],
                "pre_registered_threshold_met": h9b_discriminant_result["pre_registered_threshold_met"],
            }
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
            # Per-person N=1 self-calibration reveal (§14.2). Descriptive only:
            # signed cal_bias (self-enhancement direction) + cal_error (magnitude),
            # never a score-out-of-N and never cross-person-ranked (§14.7). Mirrored
            # on-device by selfCalibration() in poc-projection.js under the JS<->Python
            # parity lock (scripts/check_impl_parity.py).
            h9_block["calibration_reveal"] = [
                {"user": u, **h9_person_indices[u]} for u in sorted(h9_person_indices)
            ]
        if h9_block:
            hypotheses["H9"] = h9_block

        h10_block: dict[str, Any] = {}
        if h10a_result is not None:
            h10_block["H10a"] = _h9_json(h10a_result)
        if h10c_result is not None:
            h10_block["H10c"] = _h9_json(h10c_result)
        if h10b_discriminant_result is not None:
            # H10b DISCRIMINANT half — COHORT-level R² (§15.3). NO pooled per-person scalar:
            # V_i, level_i, gap_i, cal_error_i and each sd/|mbar| cell stay separate facets
            # (§13.5). supported is EXACTLY (main upper-CI < ceiling) AND (de-confound upper-CI
            # < ceiling); the gate re-derives BOTH legs (check_h10b_discriminant_lock).
            h10_block["H10b_discriminant"] = {
                "r2": h10b_discriminant_result["r2"],
                "r2_ci_low": _nan_to_none(h10b_discriminant_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(h10b_discriminant_result["r2_ci_high"]),
                "ceiling": h10b_discriminant_result["ceiling"],
                "v_level_r": h10b_discriminant_result["v_level_r"],
                "v_gap_r": h10b_discriminant_result["v_gap_r"],
                "v_cal_error_r": h10b_discriminant_result["v_cal_error_r"],
                "discriminant_met": h10b_discriminant_result["discriminant_met"],
                "deconf_r2": _nan_to_none(h10b_discriminant_result["deconf_r2"]),
                "deconf_r2_ci_low": _nan_to_none(h10b_discriminant_result["deconf_r2_ci_low"]),
                "deconf_r2_ci_high": _nan_to_none(h10b_discriminant_result["deconf_r2_ci_high"]),
                "deconf_sd_absmbar_r": h10b_discriminant_result["deconf_sd_absmbar_r"],
                "deconf_n_cells": h10b_discriminant_result["deconf_n_cells"],
                "deconf_met": h10b_discriminant_result["deconf_met"],
                "n_participants": h10b_discriminant_result["n_participants"],
                "supported": h10b_discriminant_result["supported"],
                "pre_registered_threshold_met": h10b_discriminant_result["pre_registered_threshold_met"],
            }
        if h10_block or h10_construct_sd_n:
            h10_block["person_variability_n"] = h10_person_variability_n
            h10_block["n_construct_sd_cells"] = h10_construct_sd_n
            if h10_variability_reveal:
                # the per-person N=1 reveal (§15.5): the qualifying per-construct
                # sd_i(c) facets + the within-branch V_i (None below the
                # ≥3-construct floor — the facets still reveal); steadiness↔
                # responsiveness never ranked, no pooled cross-branch score
                # (§13.5); the shape the JS runtime mirrors under the parity
                # lock (§15.7)
                h10_block["context_variability_reveal"] = h10_variability_reveal
            hypotheses["H10"] = h10_block

        h11_block: dict[str, Any] = {}
        if h11a_result is not None:
            h11_block["H11a"] = _h9_json(h11a_result)
        if h11c_result is not None:
            h11_block["H11c"] = _h9_json(h11c_result)
        if h11b_result is not None:
            # H11b SHAPE DISCRIMINANT — COHORT-level R² (§16.3). NO pooled per-person
            # circle scalar: β_i and generosity_i stay separate facets (§13.5). supported
            # is EXACTLY (r2 upper-CI < ceiling); the gate re-derives it (check_h11).
            h11_block["H11b"] = {
                "r2": h11b_result["r2"],
                "r2_ci_low": _nan_to_none(h11b_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(h11b_result["r2_ci_high"]),
                "ceiling": h11b_result["ceiling"],
                "beta_generosity_r": h11b_result["beta_generosity_r"],
                "beta_near_r": h11b_result["beta_near_r"],
                "n_participants": h11b_result["n_participants"],
                "supported": h11b_result["supported"],
                "pre_registered_threshold_met": h11b_result["pre_registered_threshold_met"],
            }
        if h11_block or h11_person_shape_n:
            h11_block["person_shape_n"] = h11_person_shape_n
            h11_block["radius_finite"] = h11_radius_finite
            h11_block["radius_censored"] = h11_radius_censored
            if h11_shape_reveal:
                # The per-person N=1 reveal (§16.5): β_i steepness + R_i reach,
                # reported as separate facets, never pooled into a circle score
                # (§13.5). A right-censored radius stays None (§13.2 — never
                # made finite). Impartial↔partial both described, never ranked.
                # This is the shape circleShape in poc-projection.js mirrors
                # under the JS↔Python parity lock (§16.7).
                h11_block["circle_shape_reveal"] = h11_shape_reveal
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
            if r2_protected_reveal:
                # The per-person N=1 reveal (§17.5): the PROFESSED protected set —
                # value-slot strings only, never prices (§13.2 categorical tail,
                # never finitized), never summed into a sacredness score (§13.5),
                # never ranked by size (many `never`s = integrity OR dogmatism).
                # The key name carries the cheap-talk caveat: professed, not
                # validated against a real offer (that is H-A2 → Phase-2). This is
                # the shape protectedValues in poc-projection.js mirrors under
                # the JS↔Python parity lock (§17.7).
                r2_block["protected_set_reveal"] = r2_protected_reveal
            hypotheses["R2"] = r2_block

        h12_block: dict[str, Any] = {}
        if h12a_result is not None:
            h12_block["H12a"] = _h9_json(h12a_result)
        if h12c_result is not None:
            h12_block["H12c"] = _h9_json(h12c_result)
        if h12b_discriminant_result is not None:
            # H12b DISCRIMINANT half — COHORT-level R² (§18.5). NO pooled per-person scalar:
            # H_i, gap_i and cal_error_i stay separate facets (§13.5). supported is EXACTLY
            # (r2 upper-CI < ceiling); the gate re-derives it (check_h12b_discriminant_lock).
            h12_block["H12b_discriminant"] = {
                "r2": h12b_discriminant_result["r2"],
                "r2_ci_low": _nan_to_none(h12b_discriminant_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(h12b_discriminant_result["r2_ci_high"]),
                "ceiling": h12b_discriminant_result["ceiling"],
                "h_gap_r": h12b_discriminant_result["h_gap_r"],
                "h_cal_error_r": h12b_discriminant_result["h_cal_error_r"],
                "n_participants": h12b_discriminant_result["n_participants"],
                "supported": h12b_discriminant_result["supported"],
                "pre_registered_threshold_met": h12b_discriminant_result["pre_registered_threshold_met"],
            }
        if h12_block or h12_person_asymmetry_n:
            h12_block["person_asymmetry_n"] = h12_person_asymmetry_n
            h12_block["mean_asymmetry"] = _nan_to_none(h12_mean_asymmetry)
            if h12_asymmetry_reveal:
                # the per-person N=1 reveal (§18.1): SIGNED H_i + pair count, None below
                # the ≥3-pair floor — no pooled hypocrisy scalar, no per-person verdict
                # (§18.4); the shape the JS runtime mirrors under the parity lock (§18.7)
                h12_block["hypocrisy_asymmetry_reveal"] = h12_asymmetry_reveal
            hypotheses["H12"] = h12_block

        r1_block: dict[str, Any] = {}
        if r1a_result is not None:
            r1_block["R1a"] = _h9_json(r1a_result)
        if r1a_symbol_result is not None:
            # R1a for the SYMBOLIZATION facet — same split-half machinery, reported as a
            # SEPARATE reliability leg (§13.5, never pooled with internalization).
            r1_block["R1a_symbolization"] = _h9_json(r1a_symbol_result)
        if r1c_result is not None:
            r1_block["R1c"] = _h9_json(r1c_result)
        if r1b_moderation_result is not None:
            # R1b MODERATION leg — COHORT-level directional slope (§19.5). supported is
            # EXACTLY (corr upper-CI < ceiling 0.0); the gate re-derives it
            # (check_r1b_moderation_lock). Independent channels ⇒ no pooled scalar.
            r1_block["R1b_moderation"] = {
                "r": r1b_moderation_result["r"],
                "ci_low": _nan_to_none(r1b_moderation_result["ci_low"]),
                "ci_high": _nan_to_none(r1b_moderation_result["ci_high"]),
                "ceiling": r1b_moderation_result["ceiling"],
                "n_participants": r1b_moderation_result["n_participants"],
                "supported": r1b_moderation_result["supported"],
                "pre_registered_threshold_met": r1b_moderation_result["pre_registered_threshold_met"],
            }
        if r1b_h12_dampening_result is not None:
            # R1b H12-DAMPENING leg — COHORT-level directional slope (§19.5), the first of
            # R1b's three deferred H10–H12 dampening legs. supported is EXACTLY (corr
            # upper-CI < ceiling 0.0) over INDEPENDENT channels (internalization ← identity
            # log, H_i ← hypocrisy log) ⇒ no algebraic identity; the gate re-derives it
            # (check_r1b_h12_dampening_lock). Never a per-person verdict.
            r1_block["R1b_h12_dampening"] = {
                "r": r1b_h12_dampening_result["r"],
                "ci_low": _nan_to_none(r1b_h12_dampening_result["ci_low"]),
                "ci_high": _nan_to_none(r1b_h12_dampening_result["ci_high"]),
                "ceiling": r1b_h12_dampening_result["ceiling"],
                "n_participants": r1b_h12_dampening_result["n_participants"],
                "supported": r1b_h12_dampening_result["supported"],
                "pre_registered_threshold_met": r1b_h12_dampening_result["pre_registered_threshold_met"],
            }
        if r1_block or r1_profile_n:
            r1_block["profile_n"] = r1_profile_n
            # Two facets exposed SEPARATELY — no pooled "centrality" key (§13.5).
            r1_block["mean_internalization"] = _nan_to_none(r1_mean_internalization)
            r1_block["mean_symbolization"] = _nan_to_none(r1_mean_symbolization)
            if r1_facet_reveal:
                # N=1 on-device reveal (§19.1) — per-person facet means, two facets
                # SEPARATE, None ⇔ below the ≥3-item floor. Parity-locked against
                # poc-projection.js centralityFacets (check_impl_parity.py). No pool.
                r1_block["moral_identity_facet_reveal"] = r1_facet_reveal
            hypotheses["R1"] = r1_block

        r6_block: dict[str, Any] = {}
        if r6a_result is not None:
            r6_block["R6a"] = _h9_json(r6a_result)
        if r6d_result is not None:
            r6_block["R6d"] = _h9_json(r6d_result)
        if r6b_discriminant_result is not None:
            # R6b DISCRIMINANT half — COHORT-level R² (§20.5). NO pooled per-person scalar:
            # objectivism_moral_i, |P_i|, internalization_i and the importance breadth stay
            # separate facets (§13.5). supported is EXACTLY (r2 upper-CI < ceiling); the gate
            # re-derives it (check_r6b_discriminant_lock).
            r6_block["R6b_discriminant"] = {
                "r2": r6b_discriminant_result["r2"],
                "r2_ci_low": _nan_to_none(r6b_discriminant_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(r6b_discriminant_result["r2_ci_high"]),
                "ceiling": r6b_discriminant_result["ceiling"],
                "o_sacredness_r": r6b_discriminant_result["o_sacredness_r"],
                "o_centrality_r": r6b_discriminant_result["o_centrality_r"],
                "o_importance_r": r6b_discriminant_result["o_importance_r"],
                "n_participants": r6b_discriminant_result["n_participants"],
                "supported": r6b_discriminant_result["supported"],
                "pre_registered_threshold_met": r6b_discriminant_result["pre_registered_threshold_met"],
            }
        if r6_block or r6_profile_n:
            r6_block["profile_n"] = r6_profile_n
            # STATED probe only — moral and taste reads exposed SEPARATELY; no pooled
            # "objectivism_score"/"conviction" key, and never fused with the (deferred)
            # revealed tolerance/compromise/language signatures (§13.5, load-bearing).
            r6_block["mean_moral_objectivism"] = _nan_to_none(r6_mean_moral)
            r6_block["mean_taste_objectivism"] = _nan_to_none(r6_mean_taste)
            if r6_claim_reveal:
                # N=1 on-device reveal (§20.1) — per-person claim-type reads, moral and
                # taste SEPARATE, None ⇔ below the ≥3-item floor. Parity-locked against
                # poc-projection.js objectivismReads (check_impl_parity.py). No pool, and
                # no per-person moral>taste verdict (that gradient is the cohort-only R6d).
                r6_block["objectivism_claim_reveal"] = r6_claim_reveal
            hypotheses["R6"] = r6_block

        a3_block: dict[str, Any] = {}
        if a3_kappa_result is not None:
            # The κ gate + 2×2 marginals + the descriptive-only wall (promotable=False).
            a3_block["kappa"] = a3_kappa_result
        if a3_profile:
            n_a3 = len(a3_profile)
            a3_block["foundation_profile"] = {
                "profile_n": n_a3,
                # Per-foundation cohort mean invocation RATE, exposed SEPARATELY in canonical
                # MFD order — NO pooled "moral_language_score"/"foundation_score" scalar, and
                # the foundations are never ranked (§21.4, value-neutral).
                "cohort_mean_rates": {
                    f: sum(p.get(f, 0.0) for p in a3_profile.values()) / n_a3
                    for f in MFD_FOUNDATIONS
                },
            }
        if a3_block:
            hypotheses["A3"] = a3_block

        a4_block: dict[str, Any] = {}
        if a4a_result is not None:
            # Per-domain reliability only — NO pooled "conflict_score" scalar and NO framework
            # label (deliberative/utilitarian/deontological): conflict is EFFORT, value-neutral
            # (§1.1/§1.4, Bago & De Neys 2019). No public card (§1.4).
            a4_block["A4a"] = {
                "per_domain": _per_domain_json(a4a_result["per_domain"]),
                "n_domains": a4a_result["n_domains"],
                "n_domains_met": a4a_result["n_domains_met"],
                "threshold_low": a4a_result["threshold_low"],
                "any_met": a4a_result["any_met"],
            }
            a4_block["n_conflict_cells"] = a4_n_cells
            a4_block["n_participants"] = a4_n_users
        if a4b_discriminant_result is not None:
            # A4b discriminant (§22.4): is conflict a DISTINCT channel or a shadow of the choice?
            # Cohort-level R² gate + within-person descriptive companions. supported ⇔ upper 95% CI
            # of R² < ceiling. Value-neutral, no per-person reveal (§3/§1.4).
            a4_block["A4b"] = {
                "r2": a4b_discriminant_result["r2"],
                "r2_ci_low": _nan_to_none(a4b_discriminant_result["r2_ci_low"]),
                "r2_ci_high": _nan_to_none(a4b_discriminant_result["r2_ci_high"]),
                "ceiling": a4b_discriminant_result["ceiling"],
                "conflict_level_r": a4b_discriminant_result["conflict_level_r"],
                "conflict_gap_r": a4b_discriminant_result["conflict_gap_r"],
                "n_participants": a4b_discriminant_result["n_participants"],
                "n_cells": a4b_discriminant_result["n_cells"],
                "supported": a4b_discriminant_result["supported"],
                "pre_registered_threshold_met": a4b_discriminant_result["pre_registered_threshold_met"],
            }
        if a4_block:
            hypotheses["A4"] = a4_block

        if h8a_result is not None:
            # H8a debiasing — COHORT secondary (§9.2). NO pooled narrative/immersion/transportation
            # scalar: the reveal is never per-person (§9.5). `supported` requires the headline CI AND
            # the de-coupled Frisch–Waugh–Lovell partial sign to agree (the regression-to-the-mean guard).
            hypotheses["H8"] = {
                "H8a": {
                    "rho_8a": h8a_result["rho_8a"],
                    "ci_low": _nan_to_none(h8a_result["ci_low"]),
                    "ci_high": _nan_to_none(h8a_result["ci_high"]),
                    "threshold_low": h8a_result["threshold_low"],
                    "headline_met": h8a_result["headline_met"],
                    "partial_r": h8a_result["partial_r"],
                    "partial_ci_low": _nan_to_none(h8a_result["partial_ci_low"]),
                    "partial_ci_high": _nan_to_none(h8a_result["partial_ci_high"]),
                    "decoupled_partial_positive": h8a_result["decoupled_partial_positive"],
                    "supported": h8a_result["supported"],
                    "n_participants": h8a_result["n_participants"],
                    "n_probe_rows": h8a_result["n_probe_rows"],
                },
            }

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
        if (any(x is not None for x in (h9a_result, h9b_result, h9c_result, h9b_discriminant_result))
                or h9_cov is not None):
            print()
            print(render_h9_result(
                h9a_result, h9b_result, h9c_result, h9_cov, len(h9_person_indices),
                h9b_discriminant_result,
            ))
        if (h10a_result is not None or h10c_result is not None or h10_construct_sd_n
                or h10b_discriminant_result is not None):
            print()
            print(render_h10_result(
                h10a_result, h10c_result, h10_person_variability_n, h10_construct_sd_n,
                h10b_discriminant_result,
            ))
        if h11a_result is not None or h11c_result is not None or h11_person_shape_n:
            print()
            print(render_h11_result(
                h11a_result, h11c_result, h11_person_shape_n,
                h11_radius_finite, h11_radius_censored, h11b_result,
            ))
        if r2a_result is not None or r2b_result is not None or r2_protected_set_n or r2_protected_none_n:
            print()
            print(render_r2_result(
                r2a_result, r2b_result, r2_protected_set_n,
                r2_protected_none_n, r2_protected_set_sizes,
            ))
        if (h12a_result is not None or h12c_result is not None or h12_person_asymmetry_n
                or h12b_discriminant_result is not None):
            print()
            print(render_h12_result(
                h12a_result, h12c_result, h12_person_asymmetry_n, h12_mean_asymmetry,
                h12b_discriminant_result,
            ))
        if (r1a_result is not None or r1a_symbol_result is not None or r1c_result is not None
                or r1_profile_n or r1b_moderation_result is not None
                or r1b_h12_dampening_result is not None):
            print()
            print(render_r1_result(
                r1a_result, r1c_result, r1_profile_n,
                r1_mean_internalization, r1_mean_symbolization,
                r1b_moderation_result, r1a_symbol_result,
                r1b_h12_dampening_result,
            ))
        if (r6a_result is not None or r6d_result is not None or r6_profile_n
                or r6b_discriminant_result is not None):
            print()
            print(render_r6_result(
                r6a_result, r6d_result, r6_profile_n,
                r6_mean_moral, r6_mean_taste,
                r6b_discriminant_result,
            ))
        if a3_kappa_result is not None or a3_profile:
            print()
            print(render_a3_result(a3_kappa_result, a3_profile))
        if a4a_result is not None or a4_n_cells or a4b_discriminant_result is not None:
            print()
            print(render_a4_result(a4a_result, a4_n_users, a4_n_cells, a4b_discriminant_result))
        if h8a_result is not None:
            print()
            print(render_h8_result(h8a_result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
