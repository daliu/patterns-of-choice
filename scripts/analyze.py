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
  below. It is reserved NOT for a library reason but because it has
  unresolved INPUT preconditions that are design decisions, not code:
  (a) scenarios/h8-probe-pairs.json currently declares zero pairs —
      there is nothing to compute on until the paired probes are
      authored (an editorial task, see pilot-pre-launch-checklist.md);
  (b) how a narrative resolves to one scalar r_narr — terminal-based
      vs path-based — is the open question in scoring.md §11 and must
      be resolved before the divergence score is well-defined;
  (c) the H8a sign convention is flagged in scoring.md §9.2 as
      reconcile-before-OSF-lock.
  Implementing H8 before (a)-(c) are settled would bake in choices that
  are the project owner's / pilot's to make. When they are, this is a
  natural next analyzer addition with a check_analyzer_thresholds gate
  alongside H2-H7.

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


def item_score(entry: dict, tag_map: dict[tuple[str, str], tuple[str, float]]) -> tuple[float, int]:
    """
    Sum scoring contributions for the entry's tags on the primary axis of
    the entry's domain. Clamped to [-1, +1] per scoring.md §2.2.

    Returns (score, contributing_tag_count). If no tags contribute, returns
    (0.0, 0); the caller should treat this as NA-for-score-purposes.
    """
    domain = entry.get("domain", "")
    total = 0.0
    n = 0
    for tag in entry.get("tags", []):
        if (domain, tag) in tag_map:
            _, contrib = tag_map[(domain, tag)]
            total += contrib
            n += 1
    return (max(-1.0, min(1.0, total)), n)


def session_aggregates(
    entries: list[dict],
    tag_map: dict[tuple[str, str], tuple[str, float]],
) -> dict[tuple[str, str, str], list[float]]:
    """
    Group per-item scores by (user_id, session_id, domain). Returns
    raw lists of scores; caller can compute mean / variance / count.

    Items where no tag matched the domain's primary axis are excluded.
    """
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for entry in entries:
        score, n = item_score(entry, tag_map)
        if n == 0:
            continue
        key = (entry["user_id"], entry["session_id"], entry["domain"])
        grouped[key].append(score)
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


def probe_break_point_score(response: dict, inversion_map: dict[str, bool]) -> tuple[float, bool] | None:
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
    probe_id = response.get("probe_id")
    if not probe_id:
        return None
    inverted = inversion_map.get(probe_id, response.get("is_inverted", False))
    stake = response.get("first_accept_stake")
    rung = response.get("first_accept_rung")

    # Conservative default ladder ceiling = $10,000 for normalization (cov-ingroup-002
    # uses $100K but most probes use $10K; analyzer can re-normalize at validation time).
    LADDER_CEIL_LOG10 = 4.0  # log10(10_000)

    if rung == "never":
        # User refused at all rungs
        if inverted:
            return (-LADDER_CEIL_LOG10 - 1.0, True)  # would never do the ethical thing
        return (LADDER_CEIL_LOG10 + 1.0, False)  # would never do the unethical thing

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
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """
    Per-user per-domain bucketing. Each item in the list is one probe response
    with its computed score and metadata for downstream aggregation or display.
    """
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in responses:
        score = probe_break_point_score(r, inversion_map)
        if score is None:
            continue
        log_score, inverted = score
        grouped[(r["user_id"], r["domain"])].append({
            "probe_id": r.get("probe_id"),
            "value_slot": r.get("value_slot"),
            "log_score": log_score,
            "inverted": inverted,
            "first_accept_stake": r.get("first_accept_stake"),
            "first_accept_rung": r.get("first_accept_rung"),
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
        probe_grouped = probe_scores_by_user_domain(probe_responses, inversion_map)

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
        probe_grouped_b = probe_scores_by_user_domain(probe_responses_b, inversion_map_b)
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
