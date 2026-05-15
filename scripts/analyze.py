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

Reserved for the future validation-cohort analyzer:
- Bradley-Terry inventory scoring on pairwise data (§5.2)
- Gap computation (§6)
- Bootstrap CIs (§8)
- CFA on item-level loadings (§7)
- Per-domain probe aggregation as a CFA indicator (§7)

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
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

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


def user_domain_means(
    session_score_map: dict[tuple[str, str, str], float],
) -> dict[tuple[str, str], dict[str, Any]]:
    """
    Per scoring.md §3.2: revealed_score(user, d) = mean of session scores.
    Returns dict keyed by (user, domain) → {mean, n_sessions, ci_loose}.
    The 'ci_loose' is a placeholder ±1 SE; production analyzer would do
    bootstrap CI per §8.
    """
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for (user, _session, domain), score in session_score_map.items():
        grouped[(user, domain)].append(score)

    out: dict[tuple[str, str], dict[str, Any]] = {}
    for key, scores in grouped.items():
        n = len(scores)
        mean = sum(scores) / n
        if n > 1:
            var = sum((s - mean) ** 2 for s in scores) / (n - 1)
            se = (var / n) ** 0.5
        else:
            se = float("nan")
        out[key] = {"mean": mean, "n_sessions": n, "se": se}
    return out


def render_table(scores: dict[tuple[str, str], dict[str, Any]]) -> str:
    """Tabular text output for human inspection."""
    rows = sorted(scores.items())
    if not rows:
        return "(no scores computed)"

    header = f"{'user_id':<24} {'domain':<26} {'mean':>7} {'sess':>5} {'se':>7}"
    out = [header, "-" * len(header)]
    for (user, domain), s in rows:
        mean = f"{s['mean']:+.3f}"
        se = "    nan" if s["se"] != s["se"] else f"{s['se']:.3f}"
        out.append(f"{user:<24} {domain:<26} {mean:>7} {s['n_sessions']:>5} {se:>7}")
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

    if args.json:
        out: dict[str, Any] = {
            "revealed_scores": [
                {
                    "user_id": user,
                    "domain": domain,
                    "revealed_score_mean": s["mean"],
                    "n_sessions_contributing": s["n_sessions"],
                    "se": None if s["se"] != s["se"] else s["se"],
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
