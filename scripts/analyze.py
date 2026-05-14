#!/usr/bin/env python3
"""
Minimal analyzer implementing the per-item / per-session / per-user-per-domain
revealed-score aggregation from `scoring.md` §2-3.

This is *not* the full validation-cohort analyzer. Implemented here:
- Per-item revealed score from tags via the tag-axis map (§2.1, §2.2)
- Per-session aggregation (§3.1)
- Per-user-per-domain aggregation (§3.2)

Reserved for the future validation-cohort analyzer:
- Inventory scoring via Bradley-Terry on pairwise data (§5.2)
- Gap computation (§6)
- Bootstrap CIs (§8)
- CFA on item-level loadings (§7)
- Cost-of-virtue break-point aggregation across sessions (§4)

Usage:
    python scripts/analyze.py --log analysis/fixtures/sample-session-log.json
    python scripts/analyze.py --log <path> --tag-map analysis/tag_axis_map_v0.1.csv
    python scripts/analyze.py --log <path> --json   # emit JSON instead of table

The session log is a JSON file: array of SessionLogEntry per types.ts.
The tag-axis map is `analysis/tag_axis_map_v*.csv` (defaults to v0.1).
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TAG_MAP = REPO_ROOT / "analysis" / "tag_axis_map_v0.1.csv"


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

    if args.json:
        # Convert tuple keys to dotted strings for JSON
        out = [
            {
                "user_id": user,
                "domain": domain,
                "revealed_score_mean": s["mean"],
                "n_sessions_contributing": s["n_sessions"],
                "se": None if s["se"] != s["se"] else s["se"],
            }
            for (user, domain), s in sorted(user_scores.items())
        ]
        print(json.dumps(out, indent=2))
    else:
        print(render_table(user_scores))

    return 0


if __name__ == "__main__":
    sys.exit(main())
