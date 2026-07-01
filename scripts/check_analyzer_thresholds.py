#!/usr/bin/env python3
"""
Analyzer regression gate.

Runs scripts/analyze.py against the synthetic fixtures in --json mode,
parses the resulting hypotheses block, and asserts that the synthetic
data produces the expected pre-registered threshold outcomes.

This is NOT a test of whether the instrument is valid — that requires
real n≈200 cohort data. This is a regression gate that locks in the
analyzer's behavior on the fixtures, so that future changes to the
scoring code or fixtures don't silently shift the outputs.

Expected outcomes on the current synthetic fixtures:
- H2 (HEXACO convergent): threshold met = True
- H3 (revealed test-retest): threshold met = True (per-domain; only
  truth-telling has 3-user coverage)
- H4 (informant convergent): threshold met = True
- H5 (probe test-retest): threshold met = True (per-domain; only
  truth-telling has coverage)
- H6 (stated-revealed range): in_pre_registered_range = False — by
  design, fixtures show near-perfect r≈0.997 which is ABOVE the [0.20,
  0.60] gap-real range. This is informative on synthetic data and
  documents the limitation.
- H7 (Big-5 N discriminant): threshold met = True
- H9 (self-prediction calibration): H9a self-enhancement, H9b-stability,
  and H9c stakes-blindness all met = True on the fixtures (all e > 0;
  cal_error a stable trait across windows; high-pool |e| > low-pool |e|
  within-person). Plus the §14.1 CENSORING LOCK regression: no finite
  e_price is ever produced across a 'never' cost-of-virtue endpoint.
- H10 (cross-situational consistency): H10a trait reliability (split-half
  odd/even, r's lower CI ≥ 0.40) and H10c the observer-effect anchor
  (public − anonymous mean gap's lower CI > 0) both met = True on the
  fixtures, with per-construct sd_i(c) and V_i populated. Plus the §1.5
  SUPPRESSION-FLOOR regression: an under-sampled construct/participant is
  omitted, never scored on thin data.
- H11 (moral-circle radius): H11a shape reliability (β_i split-window
  odd/even, r's lower CI ≥ 0.40) and H11c the parochial-gradient anchor
  (near − far concern mean's lower CI > 0, directional) both met = True on
  the fixtures, with both finite and right-censored radii present (a flat/
  impartial circle yields a censored R_i, never a finite one). Plus the
  §13.2 CENSORING + §1.5 SUPPRESSION regression (check_h11_suppression): a
  flat circle's R_i stays censored — NEVER made finite — and a user below
  the ≥4-populated-bin floor (or a bin below the ≥2-item floor) is omitted.
- R2 (sacred / protected values): R2a protected-set test-retest reliability
  (Jaccard over waves, lower CI ≥ 0.40) and R2b protected ≠ EXPENSIVE (the
  taboo|never − taboo|finite contrast's lower CI > 0, directional) both met =
  True on the fixtures, with ≥1 participant holding a non-empty protected set
  P_i, ≥1 who protects nothing (the empty-set case), and R2a's undefined-
  Jaccard exclusion exercised. Plus the §13.2 CATEGORICAL-`never` regression
  (check_r2_censoring): a protected `never` enters P_i as a value_slot string
  and is NEVER finitized into a price (scores the right-censored sentinel),
  and an empty-in-both-waves user is excluded from R2a, never scored 1.0.
- H12 (moral hypocrisy — self–other judgment asymmetry): H12a asymmetry
  reliability (split-half odd/even correlation of H_i, lower CI ≥ 0.40) and
  H12c the self-serving anchor (mean_i H_i > 0, directional) both met = True on
  the fixtures, with ≥1 reveal-eligible H_i. Plus the PAIRING/MISSING-DATA
  regression (check_h12_pairing_lock): a declined judgment drops the pair —
  never imputed to 0 — and the signed delta (other − self) is preserved so a
  harsher-on-self record stays NEGATIVE, never clamped (the value-neutral lock).
- R1 (moral identity centrality): R1a internalization-facet reliability (split-
  half odd/even, lower CI ≥ 0.40) and R1c the internalization > symbolization
  anchor (mean_i of the within-scale delta > 0, directional) both met = True on
  the fixtures, with ≥1 complete two-facet profile. Plus the §13.5 NO-POOL
  regression (check_r1_no_pool): the two facets are DISJOINT item sets scored
  separately — never averaged into one moral-identity score — a declined item
  drops (never imputed to 0), and a facet below the item floor is suppressed.
- R6 (metaethical objectivism — moral conviction): R6a objectivism reliability
  (split-half odd/even correlation of the MORAL read, lower CI ≥ 0.50 — the higher
  bar, objectivism being a stable individual difference) and R6d the moral > taste
  objectivism anchor (mean_i of the within-scale moral−taste delta > 0, directional
  — moral claims treated as more fact-like than tastes, Goodwin & Darley 2008) both
  met = True on the fixtures, with the moral and taste reads exposed SEPARATELY and
  ≥1 both-scored profile. Plus the §13.5 NO-POOL regression (check_r6_no_pool): the
  STATED probe is never pooled with the (deferred) revealed tolerance/language
  signatures, moral and taste route to DISJOINT means (never a moral/taste blend), a
  declined item drops (never imputed to 0), and a claim-type below the item floor is
  suppressed.
- A3 (moral-language channel — the coder + the κ gate): the deterministic MFD-style
  foundation coder clears the Cohen's-κ ≥ 0.70 reliability gate against gold on the
  synthetic fixture (kappa_met_synthetic = True, κ ≈ 0.90), certifying the MACHINERY —
  while the descriptive-only WALL holds (promotable = False; real promotion needs κ vs.
  ~200 HUMAN gold codes), and the foundation_i(f) profile exposes all six foundations
  SEPARATELY as a value-neutral rate vector (no pooled 'moral-language score'). Plus the
  coder/κ discipline regression (check_a3_kappa_lock): Cohen's κ is correct on hand 2×2
  cases (perfect → 1.0, TP9/TN9/FP1/FN1 → 0.8, no-variance → None), the coder is
  deterministic and value-neutral (the documented 'career'→care MFD-wildcard over-match
  reproduces — the living reason the gate exists), the gate is TWO-SIDED (a low-agreement
  corpus does NOT clear 0.70), and §1.5 holds (a blank text drops from κ and the profile
  denominator; a non-blank zero-foundation utterance counts — the particularist is
  described, never scored deficient). κ is a coder-pair statistic, never a person score.
  NOT parity-gated by design (LLM coding is non-deterministic; §1.5).
- A4 (decision-conflict channel — the RT-derived EFFORT/ambivalence signal, §22): the
  conflict(i, domain) cell is a within-person z of response time RESIDUALIZED on reading-
  load + presented position (timeouts + the timed quick-fire set excluded), and its A4a
  split-half per-domain test–retest clears the exploratory lower-CI ≥ 0.40 bar on the
  synthetic fixture (any_met = True) — certifying the MACHINERY, never a person score.
  The payload carries NO pooled 'conflict score' and NO framework label (slow ≠
  deontological; §22 is value-neutral — effortful virtue is not worse than easy virtue).
  Plus the conflict discipline regression (check_a4_conflict_lock): the OLS residualizer
  is exact on a hand case, residualizing reading-load REMOVES a pure length confound
  (a 10×-longer item does not read as high conflict), timeouts + timed items are
  excluded, the within-person z has mean ≈ 0 (so a person-pooled conflict is degenerate —
  the unit is per-domain), and the reliability gate is TWO-SIDED (a reliable corpus clears
  0.40, an effort-scrambled one does NOT). RT-only; answer-revision capture is deferred
  (§4 Q1). NO public card (§1.4). Parity-gated in principle, but the on-device JS reveal
  is DEFERRED (H9–R6 precedent), so parity is unchanged.

Exits 0 if all expectations match; 1 if any expectation is violated;
2 if the analyzer cannot be run or its output cannot be parsed.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ANALYZE = REPO_ROOT / "scripts" / "analyze.py"
FIXTURES = REPO_ROOT / "analysis" / "fixtures"
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"

# Fall back to system python3 if no venv is set up (CI installs deps
# directly into the runner's Python; venv is a local-dev convenience).
PYTHON = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

EXPECTATIONS = {
    "H2": {"kind": "single", "threshold_met": True},
    "H3": {"kind": "per_domain", "expected_domains": ["truth-telling"], "threshold_met": True},
    "H4": {"kind": "single", "threshold_met": True},
    "H5": {"kind": "per_domain", "expected_domains": ["truth-telling"], "threshold_met": True},
    "H6": {"kind": "range", "in_range": False},
    "H7": {"kind": "single", "threshold_met": True},
    "H9": {"kind": "h9", "sub_met": {"H9a": True, "H9b_stability": True, "H9c": True}},
    "H10": {"kind": "h10", "sub_met": {"H10a": True, "H10c": True}},
    "H11": {"kind": "h11", "sub_met": {"H11a": True, "H11b": True, "H11c": True}},
    "R2": {"kind": "r2", "sub_met": {"R2a": True, "R2b": True}},
    "H12": {"kind": "h12", "sub_met": {"H12a": True, "H12c": True}},
    "R1": {"kind": "r1", "sub_met": {"R1a": True, "R1c": True}},
    "R6": {"kind": "r6", "sub_met": {"R6a": True, "R6d": True}},
    "A3": {"kind": "a3", "kappa_met": True},
    "A4": {"kind": "a4", "any_met": True},
    "H8": {"kind": "a8a", "supported": True},
}


def run_analyzer() -> dict:
    cmd = [
        PYTHON, str(ANALYZE),
        "--log", str(FIXTURES / "sample-session-log.json"),
        "--probes", str(FIXTURES / "sample-probe-responses.json"),
        "--card-sort", str(FIXTURES / "sample-card-sort.json"),
        "--pairwise", str(FIXTURES / "sample-pairwise.json"),
        "--hexaco", str(FIXTURES / "sample-hexaco.json"),
        "--informant-hexaco", str(FIXTURES / "sample-informant-hexaco.json"),
        "--big5", str(FIXTURES / "sample-big5.json"),
        "--log-window-b", str(FIXTURES / "sample-session-log-window-b.json"),
        "--probes-window-b", str(FIXTURES / "sample-probe-responses-window-b.json"),
        "--predictions", str(FIXTURES / "sample-predictions.json"),
        "--predictions-window-b", str(FIXTURES / "sample-predictions-window-b.json"),
        "--context-log", str(FIXTURES / "sample-context-log.json"),
        "--circle-log", str(FIXTURES / "sample-circle-log.json"),
        "--protected-log", str(FIXTURES / "sample-protected-values-log.json"),
        "--hypocrisy-log", str(FIXTURES / "sample-hypocrisy-log.json"),
        "--identity-log", str(FIXTURES / "sample-identity-centrality-log.json"),
        "--objectivism-log", str(FIXTURES / "sample-objectivism-log.json"),
        "--language-log", str(FIXTURES / "sample-language-log.json"),
        "--process-log", str(FIXTURES / "sample-process-log.json"),
        "--h8-log", str(FIXTURES / "sample-h8-log.json"),
        "--h11b-log", str(FIXTURES / "sample-h11b-log.json"),
        "--json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL: analyzer exited {result.returncode}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"FAIL: analyzer output is not valid JSON: {e}", file=sys.stderr)
        print(result.stdout[:500], file=sys.stderr)
        sys.exit(2)


def check_single(hid: str, payload: dict, expected_met: bool) -> tuple[bool, str]:
    if payload is None:
        return False, f"{hid}: missing"
    met = payload.get("pre_registered_threshold_met")
    if met != expected_met:
        return False, f"{hid}: threshold_met = {met!r}, expected {expected_met!r}"
    if payload.get("n", 0) < 3:
        return False, f"{hid}: n = {payload.get('n')}, expected ≥ 3"
    return True, f"{hid}: ✓ threshold_met = {met} (n = {payload['n']}, r = {payload['r']:+.3f})"


def check_per_domain(
    hid: str,
    payload: list,
    expected_domains: list[str],
    expected_met: bool,
) -> tuple[bool, str]:
    if not isinstance(payload, list):
        return False, f"{hid}: missing or not a list"
    domains = [row["domain"] for row in payload]
    for d in expected_domains:
        if d not in domains:
            return False, f"{hid}: expected domain '{d}' not present (got {domains})"
    for row in payload:
        if row["pre_registered_threshold_met"] != expected_met:
            return False, (
                f"{hid}: domain {row['domain']} threshold_met = "
                f"{row['pre_registered_threshold_met']!r}, expected {expected_met!r}"
            )
    rows_str = ", ".join(f"{r['domain']} r={r['r']:+.3f} met={r['pre_registered_threshold_met']}" for r in payload)
    return True, f"{hid}: ✓ {rows_str}"


def check_range(hid: str, payload: dict, expected_in_range: bool) -> tuple[bool, str]:
    if payload is None:
        return False, f"{hid}: missing"
    in_range = payload.get("in_pre_registered_range")
    if in_range != expected_in_range:
        return False, f"{hid}: in_pre_registered_range = {in_range!r}, expected {expected_in_range!r}"
    return True, f"{hid}: ✓ in_range = {in_range} (r = {payload['r']:+.3f}, range [{payload['range_low']}, {payload['range_high']}])"


def check_h9(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """H9 self-prediction calibration. Assert each present sub-hypothesis
    (H9a/H9b_stability/H9c) hit its pre-registered threshold outcome, and that
    the cost-of-virtue channel is present with the censoring split (finite +
    censored). The magnitude of the censoring lock (no finite e_price across a
    'never' endpoint) is asserted directly against the code in
    check_h9_censoring() below — here we just confirm the channel is reported."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    cov = payload.get("cov_channel")
    if not isinstance(cov, dict):
        return False, f"{hid}: cov_channel missing"
    if cov.get("n_censored", 0) < 1 or cov.get("n_finite", 0) < 1:
        return False, f"{hid}: cov_channel must have both finite and censored pairs (got {cov})"
    parts.append(f"cov[finite={cov['n_finite']},censored={cov['n_censored']}]")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_h10(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """H10 cross-situational consistency. Assert each present sub-hypothesis
    (H10a split-half trait reliability, H10c observer-effect anchor) hit its
    pre-registered outcome, and that the N=1 reveal quantities are populated (at
    least one participant with a V_i, and per-construct sd cells present). The
    §1.5 suppression floors are asserted directly against the code in
    check_h10_suppression() below."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if payload.get("person_variability_n", 0) < 1:
        return False, f"{hid}: no reveal-eligible V_i (person_variability_n={payload.get('person_variability_n')})"
    if payload.get("n_construct_sd_cells", 0) < 1:
        return False, f"{hid}: no per-construct sd cells (n_construct_sd_cells={payload.get('n_construct_sd_cells')})"
    parts.append(f"V_i×{payload['person_variability_n']}, sd_cells={payload['n_construct_sd_cells']}")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_h11(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """H11 moral-circle radius. Assert each present sub-hypothesis (H11a β_i
    split-window shape reliability, H11c the parochial-gradient anchor) hit its
    pre-registered outcome, and that the N=1 reveal quantities are populated —
    at least one participant with a formed β_i/R_i, AND both a finite radius and
    a right-censored radius present (proving the flat/impartial circle censors,
    §13.2). The §13.2 censoring + §1.5 suppression floors are asserted directly
    against the code in check_h11_suppression() below."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if payload.get("person_shape_n", 0) < 1:
        return False, f"{hid}: no reveal-eligible β_i/R_i (person_shape_n={payload.get('person_shape_n')})"
    if payload.get("radius_finite", 0) < 1:
        return False, f"{hid}: no finite R_i (radius_finite={payload.get('radius_finite')})"
    if payload.get("radius_censored", 0) < 1:
        return False, (
            f"{hid}: no right-censored R_i — the flat/impartial-circle censoring case "
            f"must be exercised (radius_censored={payload.get('radius_censored')})"
        )
    parts.append(f"shapes×{payload['person_shape_n']}, R[finite={payload['radius_finite']},censored={payload['radius_censored']}]")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_r2(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """R2 sacred / protected values. Assert each present sub-hypothesis (R2a
    protected-set test-retest reliability, R2b protected ≠ expensive) hit its
    pre-registered outcome, and that the reveal quantities are populated — at
    least one participant with a non-empty protected set P_i AND at least one who
    protects nothing (the empty-set / all-priced case exercised), plus R2a's
    undefined-Jaccard exclusion (empty union in both waves) counted, never scored
    as perfect agreement. The §13.2 categorical-`never` lock is asserted directly
    against the code in check_r2_censoring() below."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if payload.get("protected_set_n", 0) < 1:
        return False, f"{hid}: no reveal-eligible P_i (protected_set_n={payload.get('protected_set_n')})"
    if payload.get("protected_none_n", 0) < 1:
        return False, (
            f"{hid}: no all-priced participant — the empty protected-set case must be "
            f"exercised (protected_none_n={payload.get('protected_none_n')})"
        )
    r2a = payload.get("R2a", {})
    if r2a.get("n_excluded_empty", 0) < 1:
        return False, (
            f"{hid}: R2a undefined-Jaccard exclusion not exercised "
            f"(n_excluded_empty={r2a.get('n_excluded_empty')})"
        )
    parts.append(f"P_i×{payload['protected_set_n']}, none={payload['protected_none_n']}, r2a_excl={r2a['n_excluded_empty']}")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_h12(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """H12 moral hypocrisy. Assert each present sub-hypothesis (H12a asymmetry
    split-half reliability, H12c the self-serving directional anchor) hit its
    pre-registered outcome, and that ≥1 participant is reveal-eligible (a scored
    H_i). The pairing/missing-data lock (a declined judgment drops the pair,
    never imputed to 0; the signed delta is preserved so harsher-on-self stays
    negative) is asserted directly against the code in check_h12_pairing_lock()
    below."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if payload.get("person_asymmetry_n", 0) < 1:
        return False, (
            f"{hid}: no reveal-eligible H_i "
            f"(person_asymmetry_n={payload.get('person_asymmetry_n')})"
        )
    parts.append(f"H_i×{payload['person_asymmetry_n']}")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_r1(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """R1 moral identity centrality. Assert each present sub-hypothesis (R1a the
    internalization-facet split-half reliability, R1c the internalization >
    symbolization directional anchor) hit its pre-registered outcome, and that ≥1
    participant has a complete two-facet profile. Crucially, assert the §13.5
    NO-POOL discipline is honored in the shape of the payload itself: the block
    must expose the two facets SEPARATELY (mean_internalization / mean_symbolization)
    and must NOT carry any pooled 'centrality'/'moral-identity' scalar. The facet-
    separation / missing-data lock is asserted directly against the code in
    check_r1_no_pool() below."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    pooled_keys = {"centrality", "centrality_score", "moral_identity",
                   "moral_identity_score", "mean_centrality"}
    present_pooled = pooled_keys & set(payload)
    if present_pooled:
        return False, (
            f"{hid}: pooled moral-identity key(s) present {sorted(present_pooled)} "
            f"— the two facets must never be averaged into one score (§13.5)"
        )
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if "mean_internalization" not in payload or "mean_symbolization" not in payload:
        return False, (
            f"{hid}: the two facets must be exposed separately "
            f"(mean_internalization / mean_symbolization), got keys {sorted(payload)}"
        )
    if payload.get("profile_n", 0) < 1:
        return False, (
            f"{hid}: no complete two-facet profile "
            f"(profile_n={payload.get('profile_n')})"
        )
    parts.append(f"profile×{payload['profile_n']}")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_r6(hid: str, payload: dict, sub_met: dict) -> tuple[bool, str]:
    """R6 metaethical objectivism / moral conviction. Assert each present sub-
    hypothesis (R6a the MORAL-read split-half reliability, R6d the moral > taste
    objectivism directional anchor) hit its pre-registered outcome, and that ≥1
    participant has both reads scored. Crucially, assert the §13.5 NO-POOL
    discipline in the shape of the payload itself: the block must expose the moral
    and taste reads SEPARATELY (mean_moral_objectivism / mean_taste_objectivism) and
    must NOT carry any pooled 'objectivism'/'conviction' scalar — the STATED probe is
    never pooled with the (deferred) revealed tolerance/language signatures, and the
    moral read is never blended with the taste read. The claim-type-separation /
    missing-data lock is asserted directly against the code in check_r6_no_pool()."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    pooled_keys = {"conviction", "conviction_score", "objectivism_score",
                   "r6_score", "moral_conviction"}
    present_pooled = pooled_keys & set(payload)
    if present_pooled:
        return False, (
            f"{hid}: pooled objectivism/conviction key(s) present {sorted(present_pooled)} "
            f"— the stated probe is never pooled with the revealed signatures, and the "
            f"moral read is never blended with the taste read (§13.5)"
        )
    parts = []
    for sub, expected in sub_met.items():
        block = payload.get(sub)
        if block is None:
            return False, f"{hid}: sub-hypothesis {sub} missing"
        met = block.get("pre_registered_threshold_met")
        if met != expected:
            return False, f"{hid}.{sub}: threshold_met = {met!r}, expected {expected!r}"
        if block.get("n", block.get("n_participants", 0)) < 3:
            return False, f"{hid}.{sub}: n too small ({block})"
        parts.append(f"{sub}={met}")
    if "mean_moral_objectivism" not in payload or "mean_taste_objectivism" not in payload:
        return False, (
            f"{hid}: the moral and taste reads must be exposed separately "
            f"(mean_moral_objectivism / mean_taste_objectivism), got keys {sorted(payload)}"
        )
    if payload.get("profile_n", 0) < 1:
        return False, (
            f"{hid}: no both-scored objectivism profile "
            f"(profile_n={payload.get('profile_n')})"
        )
    parts.append(f"profile×{payload['profile_n']}")
    return True, f"{hid}: ✓ {', '.join(parts)}"


def check_a3(hid: str, payload: dict, kappa_met: bool) -> tuple[bool, str]:
    """A3 moral-language channel — the coder + the κ gate (§21). Assert the coding-
    reliability κ hit its expected gate outcome AND that the descriptive-only WALL holds
    in the shape of the payload: even when synthetic κ clears 0.70 (certifying the
    MACHINERY), `promotable` must be False and `descriptive_only` True — real promotion
    needs κ vs. ~200 HUMAN gold codes (§21.2). Assert the §21.4 value-neutrality
    discipline structurally: NO pooled 'moral-language score' scalar anywhere, and the
    foundation_i(f) profile exposes all six foundations SEPARATELY as a rate vector
    (never one number, never ranked). κ carries its integer marginals (never a bare
    scalar) and is a coder-PAIR statistic, never a person score (§13.5). The Cohen's-κ
    math, coder determinism, the two-sided gate, and the §1.5 blank-drop are asserted
    directly against the code in check_a3_kappa_lock()."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    pooled_keys = {"moral_language_score", "foundation_score", "mft_score",
                   "language_score", "moralization_score", "a3_score"}
    present_pooled = pooled_keys & set(payload)
    if present_pooled:
        return False, (
            f"{hid}: pooled moral-language scalar(s) present {sorted(present_pooled)} "
            f"— the coder assigns foundation LABELS, never a score; more moral language "
            f"is not better (§21.4)"
        )
    kap = payload.get("kappa")
    if not isinstance(kap, dict):
        return False, f"{hid}: missing the coding-reliability κ block"
    if kap.get("kappa_met_synthetic") != kappa_met:
        return False, (
            f"{hid}: kappa_met_synthetic = {kap.get('kappa_met_synthetic')!r}, "
            f"expected {kappa_met!r}"
        )
    k = kap.get("kappa")
    gate = kap.get("kappa_gate", 0.70)
    if kappa_met and not (isinstance(k, (int, float)) and k >= gate):
        return False, f"{hid}: κ = {k!r} does not clear the gate {gate!r}"
    # THE WALL: synthetic κ certifies the machinery only — it never lifts the real gate.
    if kap.get("promotable") is not False or kap.get("descriptive_only") is not True:
        return False, (
            f"{hid}: the descriptive-only wall must hold even when synthetic κ clears "
            f"(promotable={kap.get('promotable')!r}, "
            f"descriptive_only={kap.get('descriptive_only')!r}) — real promotion is "
            f"human-κ-gated (§21.2)"
        )
    # κ must carry its integer marginals — never a bare scalar dressed up as reliability.
    for m in ("n_utterances", "coder_present", "gold_present", "agree_cells"):
        if m not in kap:
            return False, f"{hid}: κ block missing marginal '{m}' (κ must not be a bare scalar)"
    prof = payload.get("foundation_profile")
    if not isinstance(prof, dict) or prof.get("profile_n", 0) < 1:
        pn = prof.get("profile_n") if isinstance(prof, dict) else None
        return False, f"{hid}: no foundation_i(f) profile (profile_n={pn})"
    rates = prof.get("cohort_mean_rates")
    expected_foundations = {"care", "fairness", "loyalty", "authority", "sanctity", "liberty"}
    if not isinstance(rates, dict) or set(rates) != expected_foundations:
        got = sorted(rates) if isinstance(rates, dict) else rates
        return False, (
            f"{hid}: the foundation profile must expose all six foundations SEPARATELY "
            f"(got {got}) — never pooled, never ranked (§21.4)"
        )
    glyph = "✓" if kappa_met else "✗"
    return True, (
        f"{hid}: {glyph} κ={k:.3f} (gate {glyph}, promotable={kap.get('promotable')}, "
        f"descriptive_only), foundation profile×{prof['profile_n']} (6 foundations separate)"
    )


def check_a4(hid: str, payload: dict, any_met: bool) -> tuple[bool, str]:
    """A4 decision-conflict channel — the RT-derived EFFORT signal + the A4a reliability
    gate (§22). Assert the split-half per-domain test–retest hit its expected outcome AND
    that the value-neutral / no-pool discipline holds in the SHAPE of the payload: conflict
    is an EFFORT read, so there must be NO pooled 'conflict score' scalar and NO moral-
    framework label (deliberation/utilitarian/deontological) anywhere — slow ≠ deontological
    (§22). conflict(i, domain) is a per-DOMAIN cell (the within-person z has mean 0, so a
    person-pooled conflict would be degenerate), exposed as a per_domain reliability VECTOR
    with its bootstrap CI + n (never a bare scalar). The exploratory bar is the lower CI
    ≥ 0.40, and each domain's `pre_registered_threshold_met` must AGREE with its own
    ci_low ≥ threshold (the gate can't disagree with its own arithmetic). The residualizer
    exactness, the length-confound removal, the timeout/timed exclusions, the within-person
    mean-0 property, and the two-sided reliability gate are asserted directly against the
    code in check_a4_conflict_lock()."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    # No pooled scalar, no framework label — conflict is EFFORT, never a graded score (§22).
    banned_keys = {"conflict_score", "a4_score", "process_score", "effort_score",
                   "deliberation_score", "deliberation", "utilitarian", "deontological",
                   "framework", "framework_label", "rt_score", "moral_conflict_score"}
    def _scan(d, where):
        present = banned_keys & set(d)
        if present:
            return (f"{hid}: pooled/framework key(s) {sorted(present)} present in {where} "
                    f"— conflict is EFFORT/ambivalence, never a score and never a framework "
                    f"label (slow ≠ deontological; §22)")
        return None
    top_bad = _scan(payload, "the A4 block")
    if top_bad:
        return False, top_bad
    a4a = payload.get("A4a")
    if not isinstance(a4a, dict):
        return False, f"{hid}: missing the A4a conflict-reliability block"
    a4a_bad = _scan(a4a, "A4a")
    if a4a_bad:
        return False, a4a_bad
    if a4a.get("any_met") != any_met:
        return False, (
            f"{hid}: A4a any_met = {a4a.get('any_met')!r}, expected {any_met!r}"
        )
    if abs(a4a.get("threshold_low", -1) - 0.40) > 1e-9:
        return False, (
            f"{hid}: A4a threshold_low = {a4a.get('threshold_low')!r}, expected 0.40 "
            f"(the exploratory lower-CI bar, §22)"
        )
    per_domain = a4a.get("per_domain")
    if not isinstance(per_domain, list) or not per_domain:
        return False, f"{hid}: A4a per_domain must be a non-empty reliability vector"
    n_met = 0
    for cell in per_domain:
        if not isinstance(cell, dict):
            return False, f"{hid}: A4a per_domain cell is not a dict"
        for key in ("domain", "r", "ci_low", "ci_high", "n", "pre_registered_threshold_met", "threshold"):
            if key not in cell:
                return False, f"{hid}: A4a per_domain cell missing '{key}' (must carry its CI + n)"
        # The gate must agree with its own arithmetic: met iff lower CI clears the threshold.
        met = cell["pre_registered_threshold_met"]
        ci_low, thr = cell["ci_low"], cell["threshold"]
        if isinstance(ci_low, (int, float)) and isinstance(thr, (int, float)):
            if met != (ci_low >= thr):
                return False, (
                    f"{hid}: domain {cell['domain']!r} met={met!r} disagrees with "
                    f"ci_low {ci_low:.3f} vs threshold {thr:.2f}"
                )
        if met:
            n_met += 1
    if a4a.get("any_met") != (n_met > 0):
        return False, (
            f"{hid}: any_met = {a4a.get('any_met')!r} but {n_met} domain(s) actually met"
        )
    if a4a.get("n_domains_met") != n_met:
        return False, (
            f"{hid}: n_domains_met = {a4a.get('n_domains_met')!r} but counted {n_met}"
        )
    cells = payload.get("n_conflict_cells")
    if not isinstance(cells, int) or cells < 1:
        return False, f"{hid}: no conflict cells (n_conflict_cells={cells!r})"
    glyph = "✓" if any_met else "✗"
    return True, (
        f"{hid}: {glyph} A4a reliability {n_met}/{len(per_domain)} domain(s) clear "
        f"lower-CI ≥ 0.40 (effort, no pool, no framework label), "
        f"{cells} conflict cell(s)×{payload.get('n_participants')} participant(s)"
    )


def check_h8a(hid: str, payload: dict, supported: bool) -> tuple[bool, str]:
    """H8 narrative-immersion — the COHORT-level debiasing test (§9.2). H8a is a SECONDARY research
    hypothesis, NEVER a per-person reveal and never a gate-criterion (§9.5): assert the payload shape
    honours no-pool (no per-person narrative/immersion/transportation scalar anywhere) and that the
    SUPPORTED verdict is the CONJUNCTION the spec requires — the headline correlation's lower CI ≥ 0.15
    AND the de-coupled Frisch–Waugh–Lovell partial's lower CI > 0 (the §9.2 regression-to-the-mean
    guard, whose CI — not its bare point sign — is what bites). The two-sided null lock (headline clears
    the floor by artifact yet the guard withholds support) lives in check_h8a_decoupling_lock()."""
    if not isinstance(payload, dict):
        return False, f"{hid}: missing or not a dict"
    banned = {"narrative_score", "immersion_score", "transportation_score", "h8_score",
              "h8a_score", "narrative_immersion_score", "debiasing_score"}

    def _scan(d, where):
        present = banned & set(d)
        if present:
            return (f"{hid}: pooled per-person key(s) {sorted(present)} present in {where} — H8 is a "
                    f"COHORT effect, never scored per person (§9.5)")
        return None

    bad = _scan(payload, "the H8 block")
    if bad:
        return False, bad
    a = payload.get("H8a")
    if not isinstance(a, dict):
        return False, f"{hid}: missing the H8a debiasing block"
    bad = _scan(a, "H8a")
    if bad:
        return False, bad
    if abs(a.get("threshold_low", -1) - 0.15) > 1e-9:
        return False, f"{hid}: H8a threshold_low = {a.get('threshold_low')!r}, expected 0.15 (§9.2)"
    # The gate must agree with its own arithmetic on BOTH arms of the conjunction.
    ci_low = a.get("ci_low")
    headline_met = a.get("headline_met")
    exp_headline = isinstance(ci_low, (int, float)) and ci_low >= 0.15
    if headline_met != exp_headline:
        return False, (f"{hid}: headline_met={headline_met!r} disagrees with ci_low {ci_low!r} "
                       f"vs floor 0.15")
    p_lo = a.get("partial_ci_low")
    dec = a.get("decoupled_partial_positive")
    exp_dec = isinstance(p_lo, (int, float)) and p_lo > 0.0
    if dec != exp_dec:
        return False, (f"{hid}: decoupled_partial_positive={dec!r} disagrees with partial_ci_low "
                       f"{p_lo!r} vs 0 (the guard is the CI, not the point sign)")
    # SUPPORTED is EXACTLY the conjunction — the de-coupling guard cannot be bypassed.
    exp_supported = bool(headline_met and dec)
    if a.get("supported") != exp_supported:
        return False, (f"{hid}: supported={a.get('supported')!r} != (headline_met AND "
                       f"decoupled_partial_positive)={exp_supported!r}")
    if a.get("supported") != supported:
        return False, f"{hid}: supported={a.get('supported')!r}, expected {supported!r}"
    if a.get("n_participants", 0) < 3:
        return False, f"{hid}: n_participants={a.get('n_participants')!r}, expected ≥ 3 (§9.5)"
    if a.get("n_probe_rows", 0) < 3:
        return False, f"{hid}: n_probe_rows={a.get('n_probe_rows')!r}, expected ≥ 3"
    glyph = "✓" if supported else "✗"
    return True, (
        f"{hid}: {glyph} H8a debiasing SUPPORTED={a['supported']} "
        f"(rho lower-CI ≥ 0.15 ∧ de-coupled partial lower-CI > 0; "
        f"{a['n_participants']} participants, {a['n_probe_rows']} probe rows, cohort/no-pool)"
    )


def check_h9_censoring() -> tuple[bool, list[str]]:
    """Unit regression for the §14.1 CENSORING LOCK (the H9 analog of the |8.0|
    ceiling lock): calibration_cov_records must NEVER emit a finite e_price when
    either the predicted or the realized cost-of-virtue endpoint is 'never'. A
    'never' is right-censored (price above the ladder top) and stays categorical.
    Asserted directly against the code, not via the fixtures, so a regression that
    starts pricing 'never' is caught even if a fixture is later changed."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    # Every combination touching a 'never' endpoint must land in `censored`, never `finite`.
    probes = [
        {"channel": "cov", "user_id": "u1", "domain": "truth-telling",
         "predicted_rung": "never", "realized_rung": "1000", "inverted": False},
        {"channel": "cov", "user_id": "u2", "domain": "truth-telling",
         "predicted_rung": "1000", "realized_rung": "never", "inverted": False},
        {"channel": "cov", "user_id": "u3", "domain": "truth-telling",
         "predicted_rung": "never", "realized_rung": "never", "inverted": False},
        {"channel": "cov", "user_id": "u4", "domain": "truth-telling",
         "predicted_rung": "never", "realized_rung": "10000", "inverted": True},  # inverted too
        {"channel": "cov", "user_id": "u5", "domain": "truth-telling",
         "predicted_rung": "100000", "realized_rung": "1000", "inverted": False},  # the one finite control
    ]
    res = A.calibration_cov_records(probes)
    finite_users = {f["user_id"] for f in res["finite"]}
    checks = [
        ("all four 'never'-touching pairs are censored, none finite", res["n_censored"] == 4),
        ("no finite e_price produced for any 'never' endpoint", finite_users == {"u5"}),
        ("the finite control (100000→1000) IS priced, e_price == +2.0",
         len(res["finite"]) == 1 and abs(res["finite"][0]["e_price"] - 2.0) < 1e-9),
        ("censored categories cover all three cases",
         set(res["censored_categories"]) == {"predicted-never & acted-finite",
                                              "predicted-finite & acted-never", "both-never"}),
        ("inverted 'never'→finite is still censored (predicted-never & acted-finite == 2)",
         res["censored_categories"].get("predicted-never & acted-finite") == 2),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h9-censoring: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_h10_suppression() -> tuple[bool, list[str]]:
    """Unit regression for the §1.5 SUPPRESSION FLOORS (the H10 discipline lock):
    an under-sampled construct or participant must be OMITTED, never scored on
    thin data. Asserted directly against the code so a regression that relaxes a
    floor is caught even if the fixture is later changed.
      (i)  a construct with <3 qualifying contexts yields no sd_i(c);
      (ii) a context with <2 items does not count toward the ≥3-context floor;
      (iii) V_i requires ≥3 qualifying constructs (a 1-construct user is suppressed)."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    tag_map = A.load_tag_axis_map(A.DEFAULT_TAG_MAP)

    def rec(u, s, d, ctx, tag):
        return {"user_id": u, "session_id": s, "domain": d,
                "tags": [tag, f"context:{ctx}"], "response_time_ms": 5000}

    # (i) only two contexts present (workplace, public) -> below the ≥3-context floor.
    two_ctx = [rec("z1", "s1", "truth-telling", c, "truth:commission")
               for c in ("workplace", "workplace", "public", "public")]
    sd_two = A.context_sd_by_user_construct(A.context_item_records(two_ctx, tag_map))
    # (ii) a third context exists but with a single item -> must not satisfy the floor.
    one_item = two_ctx + [rec("z2", "s1", "truth-telling", "anonymous", "lie:white")]
    # re-key the single-item variant onto its own user so it is scored in isolation
    one_item = [dict(r, user_id="z2") for r in two_ctx] + \
               [rec("z2", "s1", "truth-telling", "anonymous", "lie:white")]
    sd_one = A.context_sd_by_user_construct(A.context_item_records(one_item, tag_map))
    # (iii) a user clearing sd on only one construct gets no V_i.
    v_one = A.variability_index_by_user({("z9", "truth-telling"): 0.4})

    checks = [
        ("a construct with <3 qualifying contexts is suppressed (no sd_i(c))",
         ("z1", "truth-telling") not in sd_two),
        ("a context with <2 items does not satisfy the ≥3-context floor",
         ("z2", "truth-telling") not in sd_one),
        ("V_i requires ≥3 qualifying constructs (1 construct → suppressed)",
         v_one == {}),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h10-suppression: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_h11_suppression() -> tuple[bool, list[str]]:
    """Unit regression for the H11 discipline locks, asserted directly against the
    code (via circle_shape_by_user on pre-binned records) so a regression is caught
    even if a fixture is later changed:
      (i)   the §13.2 CENSORING LOCK — a flat/impartial circle (concern never
            declines below the person's midpoint) yields a RIGHT-CENSORED R_i
            (radius None, censored True), NEVER a finite one; a parochial control
            (concern crosses the midpoint) yields a finite R_i;
      (ii)  the §1.5 ≥4-populated-bin floor — a user with <4 bins is suppressed;
      (iii) the §1.5 ≥2-item-per-bin floor — a bin with a single item does not
            count toward the ≥4-bin floor (so the user is suppressed)."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A

    def recs(user, bins_scores):
        out = []
        for b, scores in bins_scores.items():
            for sc in scores:
                out.append({"user": user, "session": "s1", "bin": b, "score": float(sc)})
        return out

    records = []
    # (i) flat/impartial circle: 4 bins all +1 -> concern never crosses midpoint -> CENSORED
    records += recs("flat", {0: [1, 1], 1: [1, 1], 2: [1, 1], 3: [1, 1]})
    #     parochial control: concern [1, 0, -1, -1] -> crosses at bin 1 -> FINITE R_i=1
    records += recs("paro", {0: [1, 1], 1: [1, -1], 2: [-1, -1], 3: [-1, -1]})
    # (ii) thin: only 3 populated bins -> below the >=4-bin floor -> suppressed
    records += recs("thin", {0: [1, 1], 1: [0, 0], 2: [-1, -1]})
    # (iii) sparse: 3 full bins + a single-item bin -> the 1-item bin does not count -> suppressed
    records += recs("sparse", {0: [1, 1], 1: [0, 0], 2: [-1, -1], 3: [-1]})

    shapes = A.circle_shape_by_user(records)
    flat = shapes.get("flat")
    paro = shapes.get("paro")
    checks = [
        ("a flat/impartial circle yields a CENSORED R_i (radius None, censored True), never finite (§13.2)",
         flat is not None and flat["censored"] is True and flat["radius"] is None),
        ("a parochial circle yields a FINITE R_i (control: concern crosses the midpoint at bin 1)",
         paro is not None and paro["censored"] is False and paro["radius"] == 1),
        ("a user with <4 populated bins is suppressed (§1.5, no β_i/R_i)",
         "thin" not in shapes),
        ("a bin with <2 items does not count toward the ≥4-bin floor (user suppressed, §1.5)",
         "sparse" not in shapes),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h11-suppression: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_r2_censoring() -> tuple[bool, list[str]]:
    """Unit regression for the R2 §13.2 CATEGORICAL-`never` LOCK (the R2 analog of
    the |8.0| ceiling / H9 censoring locks): a protected `never` response enters
    P_i as a value_slot STRING (categorical set membership) and is NEVER finitized
    into a price. Asserted directly against the code so a regression that starts
    pricing a protected value — or drops it from P_i — is caught even if a fixture
    is later changed:
      (i)   a `never` response is protected; a finite-price response is not;
      (ii)  a protected `never` scores the RIGHT-CENSORED sentinel (the probe's
            ladder ceiling + 1), never a finite break-point (§4 / §13.2);
      (iii) protected_value_sets holds the value_slot STRING, no price attached;
      (iv)  R2a EXCLUDES a user whose protected union is empty in both waves
            (undefined Jaccard), never scoring it as perfect agreement."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    inv = A.load_probe_inversion_map()
    cm = A.load_probe_ceiling_map()
    never_resp = {"user_id": "n1", "probe_id": "cov-truth-001", "value_slot": "honesty",
                  "first_accept_rung": "never", "first_accept_stake": None,
                  "no_break_point": True, "wave": "w1"}
    fin_resp = {"user_id": "n1", "probe_id": "cov-truth-001", "value_slot": "honesty",
                "first_accept_rung": "r3", "first_accept_stake": 5000,
                "no_break_point": False, "wave": "w1"}
    never_score = A.probe_break_point_score(never_resp, inv, cm)
    ceil_top = cm.get("cov-truth-001", 4.0)
    sets, _ = A.protected_value_sets([never_resp])
    pset = sets.get(("n1", "w1"), set())
    # (iv) one empty-in-both-waves user (excluded) + three stable protected users (scored).
    two_wave = [
        {"user_id": "e1", "value_slot": "honesty", "first_accept_rung": "r3",
         "first_accept_stake": 5000, "no_break_point": False, "wave": w}
        for w in ("w1", "w2")
    ] + [
        {"user_id": f"g{i}", "value_slot": v, "first_accept_rung": "never",
         "first_accept_stake": None, "no_break_point": True, "wave": w}
        for i, v in enumerate(["honesty", "loyalty", "fairness"])
        for w in ("w1", "w2")
    ]
    r2a_empty = A.compute_r2a_reliability(two_wave)
    checks = [
        ("a `never` response is protected; a finite-price response is not",
         A._cov_response_is_protected(never_resp) is True and A._cov_response_is_protected(fin_resp) is False),
        ("a protected `never` scores the RIGHT-CENSORED sentinel (ceiling+1), never a finite price",
         never_score is not None and abs(never_score[0] - (ceil_top + 1.0)) < 1e-9),
        ("P_i holds the value_slot STRING, no price attached (categorical membership)",
         pset == {"honesty"} and all(isinstance(v, str) for v in pset)),
        ("R2a EXCLUDES an empty-in-both-waves user (undefined Jaccard), never scores it 1.0",
         r2a_empty is not None and r2a_empty["n_excluded_empty"] == 1 and r2a_empty["n_participants"] == 3),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  r2-censoring: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_h12_pairing_lock() -> tuple[bool, list[str]]:
    """The H12 analog of the §13.2 censoring lock: the pairing / missing-data
    discipline (§18.1). A self–other judgment pair is scored as the SIGNED delta
    severity_other − severity_self; a declined judgment (either side missing or
    non-numeric) DROPS the pair — it is never imputed to 0, which would fabricate
    'no asymmetry' — and the sign is preserved so harsher-on-self stays NEGATIVE,
    never clamped toward the self-serving direction. Asserted directly against the
    code so a regression that starts imputing declines, or clamps the sign, is
    caught even if the fixture is later changed:
      (i)   a complete pair scores other − self, sign and magnitude preserved;
      (ii)  harsher-on-self yields a NEGATIVE delta (value-neutral: not clamped);
      (iii) a declined judgment (either side None / non-numeric / bool) → None,
            so the pair is DROPPED from the person's deltas, never counted as 0;
      (iv)  a person's H_i is the mean over ONLY the scorable pairs — dropping a
            decline leaves the remaining count and mean unchanged."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    d_pos = A._hypocrisy_pair_delta({"severity_self": 4.0, "severity_other": 7.0})
    d_neg = A._hypocrisy_pair_delta({"severity_self": 5.0, "severity_other": 2.0})
    d_self_none = A._hypocrisy_pair_delta({"severity_self": None, "severity_other": 3.0})
    d_other_none = A._hypocrisy_pair_delta({"severity_self": 3.0, "severity_other": None})
    d_bool = A._hypocrisy_pair_delta({"severity_self": True, "severity_other": 3.0})
    # (iv) two complete pairs (deltas +2.0, +2.0) plus one declined → mean stays 2.0, n stays 2.
    recs = [
        {"user": "p1", "session": "p1-s1", "severity_self": 4.0, "severity_other": 6.0},
        {"user": "p1", "session": "p1-s2", "severity_self": 5.0, "severity_other": 7.0},
        {"user": "p1", "session": "p1-s2", "severity_self": 5.0, "severity_other": None},
    ]
    deltas = A.hypocrisy_deltas_by_user(recs)["p1"]
    h_by_user = A.hypocrisy_asymmetry_by_user(recs, None, min_pairs=1)
    checks = [
        ("a complete pair scores other − self, sign and magnitude preserved",
         d_pos == 3.0),
        ("harsher-on-self yields a NEGATIVE delta (value-neutral, not clamped)",
         d_neg == -3.0),
        ("a declined judgment (self None) → None, pair is droppable not 0",
         d_self_none is None),
        ("a declined judgment (other None) → None, pair is droppable not 0",
         d_other_none is None),
        ("a bool is not a valid severity → None (guards against True==1 coercion)",
         d_bool is None),
        ("declined pair DROPPED from deltas (2 scorable, not 3 with a 0)",
         len(deltas) == 2 and all(d == 2.0 for d in deltas)),
        ("H_i is the mean over ONLY scorable pairs (declined drop leaves it 2.0)",
         abs(h_by_user["p1"] - 2.0) < 1e-9),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h12-pairing: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_r1_no_pool() -> tuple[bool, list[str]]:
    """The R1 analog of the §13.2 censoring / §18.1 pairing lock: the §13.5
    FACET-SEPARATION discipline (§19.1). The two moral-identity facets —
    internalization (private) and symbolization (public) — are DISJOINT item sets
    scored SEPARATELY; they are never averaged into one (I+S)/2 'moral-identity
    score'. A declined item (response None / non-numeric / bool) DROPS from its
    facet — never imputed to 0 — and a facet below the item floor is SUPPRESSED,
    never scored on thin data. Asserted directly against the code so a regression
    that starts pooling, imputing declines, or scoring a one-item facet is caught
    even if the fixture is later changed:
      (i)   a valid Likert response scores; None / str / bool → None (droppable);
      (ii)  the two facets route to DISJOINT means — internalization 6.0 and
            symbolization 2.0 stay separate, neither becomes the pooled 4.0;
      (iii) a declined item drops from its facet (3 scorable, not 4 with a 0);
      (iv)  a facet below the ≥3-item floor is SUPPRESSED (absent), not scored."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    # (ii) disjoint routing: user with 3 internalization @6.0 and 3 symbolization @2.0.
    recs = [
        {"user": "q1", "session": "q1-s1", "item_id": "int-1", "facet": "internalization", "response": 6.0},
        {"user": "q1", "session": "q1-s1", "item_id": "int-2", "facet": "internalization", "response": 6.0},
        {"user": "q1", "session": "q1-s2", "item_id": "int-3", "facet": "internalization", "response": 6.0},
        {"user": "q1", "session": "q1-s1", "item_id": "sym-1", "facet": "symbolization", "response": 2.0},
        {"user": "q1", "session": "q1-s1", "item_id": "sym-2", "facet": "symbolization", "response": 2.0},
        {"user": "q1", "session": "q1-s2", "item_id": "sym-3", "facet": "symbolization", "response": 2.0},
    ]
    intern = A.centrality_facet_by_user(recs, "internalization")
    symbol = A.centrality_facet_by_user(recs, "symbolization")
    # (iii) declined item drops: q2 has 3 valid internalization items + 1 declined.
    recs_declined = [
        {"user": "q2", "session": "q2-s1", "item_id": "int-1", "facet": "internalization", "response": 5.0},
        {"user": "q2", "session": "q2-s1", "item_id": "int-2", "facet": "internalization", "response": 5.0},
        {"user": "q2", "session": "q2-s2", "item_id": "int-3", "facet": "internalization", "response": 5.0},
        {"user": "q2", "session": "q2-s2", "item_id": "int-4", "facet": "internalization", "response": None},
    ]
    items_q2 = A.centrality_items_by_user(recs_declined, "internalization")["q2"]
    facet_q2 = A.centrality_facet_by_user(recs_declined, "internalization")
    # (iv) below-floor suppression: q3 has only 2 internalization items (floor is 3).
    recs_thin = [
        {"user": "q3", "session": "q3-s1", "item_id": "int-1", "facet": "internalization", "response": 6.0},
        {"user": "q3", "session": "q3-s1", "item_id": "int-2", "facet": "internalization", "response": 6.0},
    ]
    thin = A.centrality_facet_by_user(recs_thin, "internalization")
    checks = [
        ("a valid Likert response scores (float)",
         A._centrality_response({"response": 4}) == 4.0),
        ("a declined item (None) → None, droppable not 0",
         A._centrality_response({"response": None}) is None),
        ("a non-numeric response (str) → None",
         A._centrality_response({"response": "5"}) is None),
        ("a bool response → None (guards against True==1 coercion)",
         A._centrality_response({"response": True}) is None),
        ("internalization facet scores its own items (6.0), not pooled",
         abs(intern["q1"] - 6.0) < 1e-9),
        ("symbolization facet scores its own items (2.0), not pooled",
         abs(symbol["q1"] - 2.0) < 1e-9),
        ("the two facets are DISJOINT — neither equals the pooled (I+S)/2 = 4.0",
         abs(intern["q1"] - 4.0) > 1e-9 and abs(symbol["q1"] - 4.0) > 1e-9),
        ("a declined item DROPS from its facet (3 scorable, not 4 with a 0)",
         len(items_q2) == 3 and all(v == 5.0 for v in items_q2)),
        ("the facet mean ignores the declined item (stays 5.0)",
         abs(facet_q2["q2"] - 5.0) < 1e-9),
        ("a facet below the ≥3-item floor is SUPPRESSED (absent, not scored)",
         "q3" not in thin),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  r1-nopool: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_r6_no_pool() -> tuple[bool, list[str]]:
    """The R6 analog of check_r1_no_pool: the §13.5 NO-POOL discipline (§20.1) for
    metaethical objectivism. The STATED objectivism probe is never pooled with the
    (deferred, κ-gated) REVEALED tolerance/compromise + language signatures into one
    'conviction score'; AND the two claim types — moral (the reveal read) and taste
    (the cohort baseline) — are DISJOINT item sets scored SEPARATELY, never blended
    into one (M+T)/2 objectivism scalar. A declined item (objectivism None / non-
    numeric / bool) DROPS from its claim-type — never imputed to 0 — and a claim-type
    below the item floor is SUPPRESSED, never scored on thin data. Asserted directly
    against the code so a regression that starts pooling, imputing declines, or
    scoring a two-item read is caught even if the fixture is later changed:
      (i)   a valid Likert response scores; None / str / bool → None (droppable);
      (ii)  the moral and taste reads route to DISJOINT means — moral 6.0 and taste
            2.0 stay separate, neither becomes the pooled 4.0;
      (iii) a declined item drops from its claim-type (3 scorable, not 4 with a 0);
      (iv)  a claim-type below the ≥3-item floor is SUPPRESSED (absent), not scored."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    # (ii) disjoint routing: user with 3 moral @6.0 and 3 taste @2.0.
    recs = [
        {"user": "q1", "session": "q1-s1", "item_id": "mor-1", "claim_type": "moral", "objectivism": 6.0},
        {"user": "q1", "session": "q1-s1", "item_id": "mor-2", "claim_type": "moral", "objectivism": 6.0},
        {"user": "q1", "session": "q1-s2", "item_id": "mor-3", "claim_type": "moral", "objectivism": 6.0},
        {"user": "q1", "session": "q1-s1", "item_id": "tas-1", "claim_type": "taste", "objectivism": 2.0},
        {"user": "q1", "session": "q1-s1", "item_id": "tas-2", "claim_type": "taste", "objectivism": 2.0},
        {"user": "q1", "session": "q1-s2", "item_id": "tas-3", "claim_type": "taste", "objectivism": 2.0},
    ]
    moral = A.objectivism_by_user(recs, "moral")
    taste = A.objectivism_by_user(recs, "taste")
    # (iii) declined item drops: q2 has 3 valid moral items + 1 declined.
    recs_declined = [
        {"user": "q2", "session": "q2-s1", "item_id": "mor-1", "claim_type": "moral", "objectivism": 5.0},
        {"user": "q2", "session": "q2-s1", "item_id": "mor-2", "claim_type": "moral", "objectivism": 5.0},
        {"user": "q2", "session": "q2-s2", "item_id": "mor-3", "claim_type": "moral", "objectivism": 5.0},
        {"user": "q2", "session": "q2-s2", "item_id": "mor-4", "claim_type": "moral", "objectivism": None},
    ]
    items_q2 = A.objectivism_items_by_user(recs_declined, "moral")["q2"]
    moral_q2 = A.objectivism_by_user(recs_declined, "moral")
    # (iv) below-floor suppression: q3 has only 2 moral items (floor is 3).
    recs_thin = [
        {"user": "q3", "session": "q3-s1", "item_id": "mor-1", "claim_type": "moral", "objectivism": 6.0},
        {"user": "q3", "session": "q3-s1", "item_id": "mor-2", "claim_type": "moral", "objectivism": 6.0},
    ]
    thin = A.objectivism_by_user(recs_thin, "moral")
    checks = [
        ("a valid Likert response scores (float)",
         A._objectivism_response({"objectivism": 4}) == 4.0),
        ("a declined item (None) → None, droppable not 0",
         A._objectivism_response({"objectivism": None}) is None),
        ("a non-numeric response (str) → None",
         A._objectivism_response({"objectivism": "5"}) is None),
        ("a bool response → None (guards against True==1 coercion)",
         A._objectivism_response({"objectivism": True}) is None),
        ("the moral read scores its own items (6.0), not pooled",
         abs(moral["q1"] - 6.0) < 1e-9),
        ("the taste read scores its own items (2.0), not pooled",
         abs(taste["q1"] - 2.0) < 1e-9),
        ("the two reads are DISJOINT — neither equals the pooled (M+T)/2 = 4.0",
         abs(moral["q1"] - 4.0) > 1e-9 and abs(taste["q1"] - 4.0) > 1e-9),
        ("a declined item DROPS from its claim-type (3 scorable, not 4 with a 0)",
         len(items_q2) == 3 and all(v == 5.0 for v in items_q2)),
        ("the moral mean ignores the declined item (stays 5.0)",
         abs(moral_q2["q2"] - 5.0) < 1e-9),
        ("a claim-type below the ≥3-item floor is SUPPRESSED (absent, not scored)",
         "q3" not in thin),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  r6-nopool: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_a3_kappa_lock() -> tuple[bool, list[str]]:
    """The A3 coder + κ discipline (§21), asserted directly against the code so a
    regression is caught even if the fixture is later changed:
      (i)   Cohen's κ is correct on known 2×2 cases — perfect agreement → 1.0; a hand
            TP9/TN9/FP1/FN1 → 0.8; TP8/TN8/FP2/FN2 → 0.6; a no-variance corpus → None
            (κ is UNDEFINED when one rater never varies, not a fake 1.0);
      (ii)  the coder is DETERMINISTIC and value-NEUTRAL — same text → same set (twice),
            it returns a LABEL SET not a scalar, and the documented MFD-wildcard over-
            match ('career' → care) reproduces (the living reason the human-κ gate exists);
      (iii) the gate is TWO-SIDED — a high-agreement corpus clears 0.70, a low-agreement
            one does NOT, and neither is ever `promotable` (real gold is human-gated);
      (iv)  §1.5 missing-data — a blank/None text DROPS from the profile denominator,
            while a NON-blank zero-foundation utterance COUNTS (the particularist who
            writes but doesn't moralize is DESCRIBED, never scored deficient, §21.4);
      (v)   foundation_i(f) is a RATE vector over all six foundations, never pooled."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    # (i) Cohen's κ on hand cases. k08/k06 use a single "care" category so the 2×2 is exact.
    perfect = A.cohens_kappa([{"care"}, set(), {"care"}], [{"care"}, set(), {"care"}])
    k08_a = [{"care"}] * 9 + [set()] * 9 + [{"care"}] * 1 + [set()] * 1
    k08_b = [{"care"}] * 9 + [set()] * 9 + [set()] * 1 + [{"care"}] * 1
    k08 = A.cohens_kappa(k08_a, k08_b, categories=("care",))
    k06_a = [{"care"}] * 8 + [set()] * 8 + [{"care"}] * 2 + [set()] * 2
    k06_b = [{"care"}] * 8 + [set()] * 8 + [set()] * 2 + [{"care"}] * 2
    k06 = A.cohens_kappa(k06_a, k06_b, categories=("care",))
    novar = A.cohens_kappa([set(), set()], [set(), set()], categories=("care",))
    # (iii) two-sided gate on tiny corpora — hi: gold matches the coder; lo: gold is wrong.
    hi = [{"user": "u", "text": "Someone got hurt.", "gold_foundations": ["care"]},
          {"user": "u", "text": "That was unfair.", "gold_foundations": ["fairness"]},
          {"user": "u", "text": "He betrayed his team.", "gold_foundations": ["loyalty"]}]
    lo = [{"user": "u", "text": "Someone got hurt.", "gold_foundations": ["liberty"]},
          {"user": "u", "text": "That was unfair.", "gold_foundations": ["sanctity"]},
          {"user": "u", "text": "He betrayed his team.", "gold_foundations": ["authority"]}]
    hi_k = A.compute_a3_coding_kappa(hi)
    lo_k = A.compute_a3_coding_kappa(lo)
    # (iv) §1.5 — isolate each behavior in its own corpus.
    #   blank DROPS: 1 care-utterance + 1 blank → denominator 1, care rate 1.0 (0.5 if blank counted).
    prof_blank = A.foundation_profile_by_user([
        {"user": "zb", "text": "Someone got hurt.", "gold_foundations": ["care"]},
        {"user": "zb", "text": "   ", "gold_foundations": []},
    ])
    #   non-blank zero COUNTS: 1 care-utterance + 1 zero-foundation → denominator 2, care rate 0.5 (1.0 if dropped).
    prof_zero = A.foundation_profile_by_user([
        {"user": "zz", "text": "Someone got hurt.", "gold_foundations": ["care"]},
        {"user": "zz", "text": "We had lunch by the river.", "gold_foundations": []},
    ])
    checks = [
        ("Cohen's κ: perfect agreement → 1.0", perfect == 1.0),
        ("Cohen's κ: hand TP9/TN9/FP1/FN1 → 0.8", isinstance(k08, float) and abs(k08 - 0.8) < 1e-9),
        ("Cohen's κ: hand TP8/TN8/FP2/FN2 → 0.6", isinstance(k06, float) and abs(k06 - 0.6) < 1e-9),
        ("Cohen's κ: no-variance corpus → None (undefined, not a fake 1.0)", novar is None),
        ("the coder is DETERMINISTIC (same text → same set twice)",
         A.code_foundations("That was unfair and cruel.") == A.code_foundations("That was unfair and cruel.")),
        ("the coder returns a LABEL SET, never a scalar (value-neutral)",
         isinstance(A.code_foundations("That was unfair."), set)),
        ("the documented MFD-wildcard over-match reproduces ('career' → care)",
         A.code_foundations("She loved her career.") == {"care"}),
        ("the gate CLEARS on a high-agreement corpus (κ ≥ 0.70)", hi_k["kappa_met_synthetic"] is True),
        ("the gate HOLDS on a low-agreement corpus (κ < 0.70)", lo_k["kappa_met_synthetic"] is False),
        ("neither corpus is ever promotable (real promotion is human-κ-gated)",
         hi_k["promotable"] is False and lo_k["promotable"] is False),
        ("§1.5: a blank text DROPS from the denominator (care rate 1.0, not 0.5)",
         abs(prof_blank["zb"]["care"] - 1.0) < 1e-9),
        ("a non-blank zero-foundation utterance COUNTS (care rate 0.5, not 1.0 — particularist described)",
         abs(prof_zero["zz"]["care"] - 0.5) < 1e-9),
        ("foundation_i(f) is a RATE vector over all six foundations, never pooled",
         set(prof_zero["zz"]) == set(A.MFD_FOUNDATIONS)),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  a3-kappa: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_a4_conflict_lock() -> tuple[bool, list[str]]:
    """The A4 decision-conflict discipline (§22), asserted directly against the code so a
    regression is caught even if the fixture is later changed:
      (i)   the OLS residualizer is EXACT — residuals of a perfectly linear y on its
            predictors are ~0; a rank-deficient (collinear) design and an underdetermined
            (n ≤ k) design each return None (the caller then falls back to mean-centering);
      (ii)  residualizing reading-load REMOVES a pure length confound — a 10×-longer item
            with MEDIAN effort is a large naive-RT outlier (z ≈ +2) but lands mid-pack after
            residualization (|z| < 0.3): a slow-because-long item is NOT high conflict;
      (iii) the CV-1 exclusions hold — was_timeout, timed, and the quick-fire set are each
            excluded, and an excluded row never becomes a conflict cell;
      (iv)  the conflict score is WITHIN-PERSON z (mean ≈ 0 per person) — so a person-pooled
            conflict is degenerate and the unit is per-DOMAIN (cell keys are (user, domain));
      (v)   the A4a reliability gate is TWO-SIDED — a corpus with a stable per-domain effort
            tilt clears the lower-CI ≥ 0.40 bar (any_met True), while the SAME corpus with the
            tilt flipped at retest does NOT (any_met False): reliability is earned, not structural;
      (vi)  the reveal is value-NEUTRAL — the render frames conflict as EFFORT, never a moral-
            framework label (slow ≠ deontological; Bago & De Neys 2019)."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A

    # (i) residualizer exactness + degeneracy.
    x1, x2 = [1, 2, 3, 4, 5], [0, 1, 0, 1, 0]
    y_lin = [10 + 2 * a + 5 * b for a, b in zip(x1, x2)]
    resid_lin = A._ols_residuals([x1, x2], y_lin)
    collinear = A._ols_residuals([[1, 2, 3, 4], [2, 4, 6, 8]], [1, 2, 3, 5])  # x2 == 2·x1
    underdet = A._ols_residuals([[1, 2, 3], [0, 1, 0]], [1, 2, 3])            # n=3 ≤ k=3

    # (ii) length-confound removal: item i3 is 10× longer but has MEDIAN effort.
    eff = [-1000, -500, 0, 500, 1000]
    chars_c = [100, 100, 1000, 100, 100]
    pos_c = [1, 3, 5, 2, 4]
    rt_c = [2000 + 15 * c + 80 * p + e for c, p, e in zip(chars_c, pos_c, eff)]
    conf_recs = [{"user": "h", "item": f"i{k+1}", "domain": "d",
                  "response_time_ms": float(rt_c[k]), "prompt_chars": chars_c[k],
                  "presented_position": pos_c[k]} for k in range(5)]
    cs = A.conflict_scores_by_item(conf_recs)
    z_long = cs[("h", "i3")]
    mu_c = sum(rt_c) / 5
    sd_c = (sum((v - mu_c) ** 2 for v in rt_c) / 5) ** 0.5
    naive_z_long = (rt_c[2] - mu_c) / sd_c

    # (iii) exclusions — predicate + corpus-level.
    excl_to = A._a4_excluded({"was_timeout": True})
    excl_timed = A._a4_excluded({"timed": True})
    excl_qf = A._a4_excluded({"scenario_type": "quick-fire-round"})
    excl_none = A._a4_excluded({"response_time_ms": 3000})
    cs_to = A.conflict_scores_by_item(conf_recs + [
        {"user": "h", "item": "iTO", "domain": "d", "response_time_ms": 99999.0,
         "prompt_chars": 100, "presented_position": 6, "was_timeout": True}])

    # (iv) within-person z has mean ≈ 0 (per-domain is the unit, not per-person).
    wp = A.conflict_scores_by_item([
        {"user": "z", "item": f"i{k}", "domain": "d", "response_time_ms": float(2000 + 700 * k),
         "prompt_chars": 120 + 5 * k, "presented_position": (k % 3) + 1} for k in range(6)])
    wp_z = [v for (u, _i), v in wp.items() if u == "z"]
    wp_mean = sum(wp_z) / len(wp_z)
    cells_keyed = A.conflict_by_user_domain(conf_recs)

    # (v) two-sided reliability — a stable per-domain effort tilt clears; flip it at retest and it does not.
    def _rel_corpus(scramble):
        recs, tilts = [], {"u1": 1200, "u2": 600, "u3": 0, "u4": -600, "u5": -1200}
        for u, tilt0 in tilts.items():
            for dom in ("harm", "truth"):
                for sess in ("s1", "s2"):
                    tilt = -tilt0 if (scramble and sess == "s2") else tilt0
                    dom_eff = (tilt if dom == "harm" else -tilt) / 2.0
                    for it in range(4):
                        chars = 120 + 40 * ((it * 3) % 4)
                        pos = ((it * 2) % 4) + 1
                        rt = 2000 + 15 * chars + 60 * pos + dom_eff + 30 * it
                        recs.append({"user": u, "session": sess, "domain": dom,
                                     "item": f"{u}-{sess}-{dom}-{it}",
                                     "response_time_ms": float(rt), "prompt_chars": chars,
                                     "presented_position": pos})
        return recs
    rel = A.compute_a4a_conflict_reliability(_rel_corpus(False))
    scr = A.compute_a4a_conflict_reliability(_rel_corpus(True))

    # (vi) value-neutral render.
    rel_cells = A.conflict_by_user_domain(_rel_corpus(False))
    render = A.render_a4_result(rel, len({u for u, _d in rel_cells}), len(rel_cells))

    checks = [
        ("OLS residuals of a perfectly-linear y are ~0 (exact residualizer)",
         resid_lin is not None and max(abs(v) for v in resid_lin) < 1e-9),
        ("a collinear (rank-deficient) design returns None → caller mean-centers", collinear is None),
        ("an underdetermined design (n ≤ k) returns None", underdet is None),
        ("residualizing reading-load REMOVES the length confound: a 10×-longer median-effort "
         "item is a naive-RT outlier (z > 1.5) but mid-pack residualized (|z| < 0.3)",
         naive_z_long > 1.5 and abs(z_long) < 0.3),
        ("was_timeout is excluded (CV-1)", excl_to is True),
        ("the timed quick-fire set is excluded (timed flag)", excl_timed is True),
        ("the quick-fire scenario_type is excluded", excl_qf is True),
        ("a normal row is NOT excluded", excl_none is False),
        ("an excluded (timeout) row never becomes a conflict cell", ("h", "iTO") not in cs_to),
        ("conflict is WITHIN-PERSON z (mean ≈ 0) — a person-pooled score is degenerate",
         abs(wp_mean) < 1e-9),
        ("the conflict unit is per-DOMAIN: cell keys are (user, domain)",
         bool(cells_keyed) and all(isinstance(k, tuple) and len(k) == 2 for k in cells_keyed)),
        ("A4a gate CLEARS on a stable-tilt corpus (any_met True, ≥1 domain over lower-CI 0.40)",
         rel is not None and rel["any_met"] is True and rel["n_domains_met"] >= 1),
        ("A4a gate HOLDS on the SAME corpus with the tilt flipped at retest (any_met False)",
         scr is not None and scr["any_met"] is False and scr["n_domains_met"] == 0),
        ("the reveal is value-neutral EFFORT, never a moral-framework label (Bago & De Neys)",
         "EFFORT" in render and "never a moral-framework label" in render),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  a4-conflict: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_h8a_decoupling_lock() -> tuple[bool, list[str]]:
    """The H8a de-coupling discipline (§9.2), asserted directly against the code so a regression is
    caught even if the fixture changes. H8a's headline — corr(D_low, gap_abs), with D = z(r_narr) −
    z(r_abs) and gap = z(stated) − z(r_abs) — SHARES the term z(r_abs), so under the null it is POSITIVE
    by regression to the mean even when the narrative form carries NO extra pull toward the stated value.
    The confirmatory verdict is therefore CONJOINED with a de-coupled Frisch–Waugh–Lovell partial
    (r_narr · stated | r_abs) whose LOWER 95% CI must clear zero. This lock proves, on synthetic corpora
    with KNOWN ground truth:
      (i)   NULL (r_narr independent of stated given r_abs): the headline CLEARS its own 0.15 floor by
            artifact (headline_met True) yet the de-coupled partial CI straddles zero, so SUPPORTED is
            False — the guard adds discriminating power the headline alone does NOT have;
      (ii)  the guard is the CI, not the bare sign — the design-doc's one-line 'sign > 0' is a coin-flip
            under the null, so the lock-time tightening to 'lower CI > 0' is load-bearing;
      (iii) DIRECTION matters — a corpus whose narrative pulls AWAY from stated yields a NEGATIVE
            headline (headline_met False) and is not supported;
      (iv)  a REAL debiasing pull toward stated is SUPPORTED (positive control);
      (v)   SUPPORTED is EXACTLY (headline lower-CI ≥ 0.15) AND (partial lower-CI > 0) — a strict
            conjunction that cannot be bypassed;
      (vi)  the inclusion floor holds — < 3 qualifying participants returns None (never a bare scalar);
      (vii) the reveal is COHORT-level and value-neutral — framed as DEBIASING, never scored per person.
    This is the H8 analog of the §14.1 censoring lock / the A4 two-sided reliability lock."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import random

    import analyze as A
    pairs = A.load_h8_pairs(REPO_ROOT / "scenarios" / "h8-probe-pairs.json")
    low = sorted(p for p, m in pairs.items() if m["stakes_level"] == "low")
    doms = sorted({pairs[p]["domain"] for p in low})

    def clip(x):
        return max(-1.0, min(1.0, x))

    def corpus(mode, n_users, seed):
        # mode: 'null' = r_narr independent of stated given r_abs (regression-to-the-mean null);
        #       'flip' = narrative pulled AWAY from stated; 'real' = narrative pulled TOWARD stated.
        rng = random.Random(seed)
        recs = []
        for i in range(n_users):
            u = f"u{i:02d}"
            stated = {d: rng.uniform(-0.8, 0.8) for d in doms}
            for pid in low:
                d = pairs[pid]["domain"]
                abst = rng.uniform(-0.8, 0.8)
                if mode == "null":
                    narr = rng.uniform(-0.8, 0.8)
                elif mode == "flip":
                    narr = clip(abst - 0.6 * (stated[d] - abst) + rng.gauss(0, 0.06))
                else:
                    narr = clip(abst + 0.6 * (stated[d] - abst) + rng.gauss(0, 0.06))
                recs.append({"user_id": u, "pair_id": pid, "form": "abstract",
                             "primary_axis_score": round(clip(abst), 4),
                             "stated_aspirational": round(stated[d], 4)})
                recs.append({"user_id": u, "pair_id": pid, "form": "narrative",
                             "primary_axis_score": round(narr, 4),
                             "stated_aspirational": round(stated[d], 4)})
        return recs

    nul = A.compute_h8a_debiasing(corpus("null", 100, 424242), pairs)
    flp = A.compute_h8a_debiasing(corpus("flip", 40, 424242), pairs)
    rea = A.compute_h8a_debiasing(corpus("real", 40, 424242), pairs)
    tiny = A.compute_h8a_debiasing(corpus("real", 2, 424242), pairs)  # below the 3-participant floor
    render = A.render_h8_result(rea)

    def conj_ok(r):
        return r is not None and r["supported"] == bool(r["headline_met"] and r["decoupled_partial_positive"])

    checks = [
        ("NULL: headline CLEARS its 0.15 floor by regression-to-the-mean (headline_met True, rho > 0.15)",
         nul is not None and nul["headline_met"] is True and nul["rho_8a"] > 0.15),
        ("NULL: de-coupled partial CI STRADDLES zero (decoupled_partial_positive False)",
         nul is not None and nul["decoupled_partial_positive"] is False and nul["partial_ci_low"] <= 0),
        ("NULL: SUPPORTED is False — the guard withholds support the headline alone would grant",
         nul is not None and nul["supported"] is False),
        ("FLIP (narrative pulled AWAY from stated): headline NEGATIVE, not supported",
         flp is not None and flp["rho_8a"] < 0 and flp["headline_met"] is False and flp["supported"] is False),
        ("REAL (narrative pulled TOWARD stated): SUPPORTED True, de-coupled partial CI clears 0 (control)",
         rea is not None and rea["supported"] is True and rea["decoupled_partial_positive"] is True),
        ("SUPPORTED is EXACTLY (headline lower-CI ≥ 0.15) ∧ (partial lower-CI > 0) across all corpora",
         conj_ok(nul) and conj_ok(flp) and conj_ok(rea)),
        ("inclusion floor: < 3 qualifying participants returns None (never a bare scalar, §9.5)",
         tiny is None),
        ("the reveal is COHORT-level DEBIASING, never scored per person (value-neutral, §9.5)",
         "DEBIASING" in render and "cohort" in render and "never scored per person" in render),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h8a-decoupling: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_h11b_discriminant_lock() -> tuple[bool, list[str]]:
    """The H11b moral-circle SHAPE-DISCRIMINANT discipline (§1.3), asserted directly against the
    code so a regression survives any fixture change. H11b regresses the shape slope β_i
    (parochialism steepness) on [ near-bin concern_i, a SEPARATE resource-allocation generosity_i ]
    and calls the shape DISCRIMINABLE from generosity iff the UPPER 95% bootstrap CI of the model
    R² < H11B_R2_CEILING ("reach is not height" — at least half the shape variance is NOT explained
    by how generous a person is). This lock proves, on synthetic corpora with KNOWN ground truth:
      (i)   INDEPENDENT (β drawn ⊥ [near, generosity]): R² ~ 0, upper CI clears the 0.50 ceiling,
            SUPPORTED True — a genuinely dissociable circle shape is detected;
      (ii)  REDUCIBLE (β made a deterministic function of the EXTERNAL generosity): R² high, upper
            CI ≥ ceiling, SUPPORTED False — a shape that IS its generosity is correctly NOT supported;
      (iii) SUPPORTED is EXACTLY (upper-CI < ceiling) on both corpora — no bypass of the CI gate;
      (iv)  the MECHANICAL TRAP is real and is WHY external generosity is load-bearing: substitute the
            circle-derived mean (a_i + 2.5·β_i over bins 0..5) for generosity and β becomes an EXACT
            linear combo of [near, circle-mean] → R² ≡ 1 → the discriminant would ALWAYS FAIL. The code
            avoids this by using a SEPARATE revealed measure, so the INDEPENDENT corpus still supports;
      (v)   the descriptive companion localizes leakage — β·generosity r ≈ 0 when independent, strongly
            signed when reducible — WITHOUT pooling anything per person;
      (vi)  the inclusion floor holds — < H11B_MIN_PARTICIPANTS qualifying shapes returns None (never a
            bare scalar);
      (vii) the reveal is COHORT-level and value-neutral — a wider circle is never ranked as better.
    This is the H11 analog of the H8a de-coupling lock / the §14.1 censoring lock."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import random

    import analyze as A
    tag_map = A.load_tag_axis_map(A.DEFAULT_TAG_MAP)
    dist_map, _ = A.load_counterparty_distance_map(A.DEFAULT_DISTANCE_MAP)
    BIN_TAG = {0: "close", 1: "peer", 2: "community", 3: "peer-distant", 4: "stranger", 5: "out-group-new"}
    N_BINS, K, RA, RT = 6, 20, 6, 5000     # K=20 → fine per-bin realization, so quantization ≪ signal

    def clip(x):
        return max(-0.98, min(0.98, x))

    def emit_circle(recs, u, d, mean, pos):
        p = (clip(mean) + 1.0) / 2.0
        n_h = max(0, min(K, round(p * K)))
        for j in range(K):
            recs.append({"session_id": f"{u}-cs", "user_id": u, "timestamp_iso": "2026-07-01T00:00:00Z",
                         "scenario_id": f"lock-ingroup-bin{d}", "scenario_type": "quick-fire-round",
                         "domain": "in-group-out-group", "item_id": f"{u}-bin{d}-{j}", "option_id": "a",
                         "tags": ["hospitality" if j < n_h else "boundaries", f"counterparty:{BIN_TAG[d]}"],
                         "response_time_ms": RT, "presented_position": pos + j, "was_timeout": False})

    def emit_ra(recs, u, gen):
        p = (clip(gen) + 1.0) / 2.0
        n_g = max(0, min(RA, round(p * RA)))
        for j in range(RA):
            recs.append({"session_id": f"{u}-ra", "user_id": u, "timestamp_iso": "2026-07-01T00:00:00Z",
                         "scenario_id": "lock-allocation", "scenario_type": "quick-fire-round",
                         "domain": "resource-allocation", "item_id": f"{u}-ra-{j}", "option_id": "a",
                         "tags": ["generosity" if j < n_g else "self_reliance"],
                         "response_time_ms": RT, "presented_position": j + 1, "was_timeout": False})

    def grids(n, seed):
        r = random.Random(seed)
        def g(lo, hi):
            v = [lo + (hi - lo) * k / (n - 1) for k in range(n)]
            r.shuffle(v)
            return v
        return g(0.10, 0.45), g(-0.10, 0.10), g(-0.70, 0.70)   # near a, slope b, generosity g

    def ortho_seed(n, base):
        for s in range(base, base + 5000):
            near, slope, gen = grids(n, s)
            if max(abs(A._pearson_r(near, slope)), abs(A._pearson_r(gen, slope)),
                   abs(A._pearson_r(near, gen))) < 0.04:
                return s
        return base

    def corpus(mode, n, seed):
        near, slope, gen = grids(n, seed)
        recs: list[dict] = []
        for i in range(n):
            u = f"u{i:02d}"
            a, b, g = near[i], slope[i], gen[i]
            if mode == "reducible":
                b = -0.15 * g            # steepness IS the generosity → [near, gen] explain β → R² high
            for d in range(N_BINS):
                emit_circle(recs, u, d, a + b * d, pos=1 + d * K)
            emit_ra(recs, u, g)
        return recs

    s_ind = ortho_seed(40, 700000)
    ind = A.compute_h11b_discriminant(corpus("independent", 40, s_ind), tag_map, dist_map)
    red = A.compute_h11b_discriminant(corpus("reducible", 40, 700333), tag_map, dist_map)
    tiny = A.compute_h11b_discriminant(corpus("independent", 6, s_ind), tag_map, dist_map)  # < 8-participant floor

    # (iv) MECHANICAL TRAP as an EXACT identity: with concern linear in bin, the circle mean equals
    # near + 2.5·β (bins 0..5), so β = (mean − near)/2.5 is an exact linear combo of [near, mean] and
    # _ols_r_squared MUST report 1.0. This is why generosity must be an EXTERNAL measure, not the mean.
    a_syn = [0.10, 0.42, 0.18, 0.55, 0.30, 0.05, 0.48, 0.22, 0.37, 0.15, 0.60, 0.27]
    b_syn = [-0.12, 0.03, -0.05, 0.10, -0.02, 0.07, -0.09, 0.14, -0.15, 0.01, -0.07, 0.05]
    cmean_syn = [a_syn[k] + 2.5 * b_syn[k] for k in range(len(a_syn))]
    trap_r2 = A._ols_r_squared([a_syn, cmean_syn], b_syn)

    render = A.render_h11_result(None, None, 1, 1, 0, ind)
    ceil = A.H11B_R2_CEILING

    def exact(r):
        return r is not None and r["supported"] == (r["r2_ci_high"] == r["r2_ci_high"] and r["r2_ci_high"] < ceil)

    checks = [
        ("INDEPENDENT (β ⊥ [near, generosity]): SUPPORTED True, upper CI clears the ceiling",
         ind is not None and ind["supported"] is True and ind["r2_ci_high"] == ind["r2_ci_high"]
         and ind["r2_ci_high"] < ceil and ind["n_participants"] == 40),
        ("REDUCIBLE (β = f(external generosity)): SUPPORTED False, R² high, upper CI ≥ ceiling",
         red is not None and red["supported"] is False and red["r2"] > ceil and red["r2_ci_high"] >= ceil),
        ("SUPPORTED is EXACTLY (upper-CI < ceiling) on both corpora — the CI gate cannot be bypassed",
         exact(ind) and exact(red)),
        ("MECHANICAL TRAP: generosity==circle mean ⇒ β exactly linear in [near, mean] ⇒ R² ≡ 1 (why external)",
         trap_r2 is not None and abs(trap_r2 - 1.0) < 1e-9),
        ("descriptive companion localizes leakage: |β·gen r| small when independent, strongly signed when reducible",
         ind is not None and red is not None and abs(ind["beta_generosity_r"]) < 0.30
         and red["beta_generosity_r"] < -0.70),
        ("inclusion floor: < H11B_MIN_PARTICIPANTS qualifying shapes returns None (never a bare scalar)",
         tiny is None),
        ("reveal is COHORT-level & value-neutral — 'reach is not height', cohort/no-pool, never ranked",
         "reach is not height" in render and "cohort/no-pool" in render
         and "NOT reducible to generosity" in render and "never ranks it" in render),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  h11b-discriminant: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def check_probe_ceiling() -> tuple[bool, list[str]]:
    """Unit regression for the cost-of-virtue ladder ceiling: a 'never' refusal must
    anchor to the PROBE'S OWN top rung (log10(max stake) + 1), not a hardcoded $10K.
    Inversion-agnostic (sign just flips), so we assert on the magnitude."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import analyze as A
    cm = A.load_probe_ceiling_map()
    inv = A.load_probe_inversion_map()
    def never_mag(pid):
        s = A.probe_break_point_score({"probe_id": pid, "first_accept_rung": "never"}, inv, cm)
        return abs(s[0]) if s else None
    checks = [
        ("corpus has ladders above $10K (map is per-probe, not hardcoded 4.0)", any(v > 4.0 + 1e-9 for v in cm.values())),
        ("cov-reciprocity-003 ceiling == log10($10M) == 7.0", abs(cm.get("cov-reciprocity-003", 0) - 7.0) < 1e-9),
        ("'never' on the $10M probe scores |8.0| (was the buggy |5.0|)", never_mag("cov-reciprocity-003") == 8.0),
        ("'never' on a genuine $10K probe still scores |5.0|", never_mag("cov-truth-001") == 5.0),
    ]
    msgs, okall = [], True
    for label, passed in checks:
        msgs.append(f"  probe-ceiling: {'✓' if passed else '✗'} {label}")
        okall = okall and passed
    return okall, msgs


def main() -> int:
    out = run_analyzer()
    hypotheses = out.get("hypotheses")
    if not isinstance(hypotheses, dict):
        print("FAIL: analyzer output missing 'hypotheses' key", file=sys.stderr)
        return 1

    all_pass = True
    print("Analyzer threshold-gate results (synthetic fixtures):")
    for hid, spec in EXPECTATIONS.items():
        payload = hypotheses.get(hid)
        if spec["kind"] == "single":
            ok, msg = check_single(hid, payload, spec["threshold_met"])
        elif spec["kind"] == "per_domain":
            ok, msg = check_per_domain(hid, payload, spec["expected_domains"], spec["threshold_met"])
        elif spec["kind"] == "range":
            ok, msg = check_range(hid, payload, spec["in_range"])
        elif spec["kind"] == "h9":
            ok, msg = check_h9(hid, payload, spec["sub_met"])
        elif spec["kind"] == "h10":
            ok, msg = check_h10(hid, payload, spec["sub_met"])
        elif spec["kind"] == "h11":
            ok, msg = check_h11(hid, payload, spec["sub_met"])
        elif spec["kind"] == "r2":
            ok, msg = check_r2(hid, payload, spec["sub_met"])
        elif spec["kind"] == "h12":
            ok, msg = check_h12(hid, payload, spec["sub_met"])
        elif spec["kind"] == "r1":
            ok, msg = check_r1(hid, payload, spec["sub_met"])
        elif spec["kind"] == "r6":
            ok, msg = check_r6(hid, payload, spec["sub_met"])
        elif spec["kind"] == "a3":
            ok, msg = check_a3(hid, payload, spec["kappa_met"])
        elif spec["kind"] == "a4":
            ok, msg = check_a4(hid, payload, spec["any_met"])
        elif spec["kind"] == "a8a":
            ok, msg = check_h8a(hid, payload, spec["supported"])
        else:
            ok, msg = False, f"{hid}: unknown expectation kind '{spec['kind']}'"
        print(f"  {msg}")
        if not ok:
            all_pass = False

    ceil_ok, ceil_msgs = check_probe_ceiling()
    for m in ceil_msgs:
        print(m)
    if not ceil_ok:
        all_pass = False

    h9cens_ok, h9cens_msgs = check_h9_censoring()
    for m in h9cens_msgs:
        print(m)
    if not h9cens_ok:
        all_pass = False

    h10sup_ok, h10sup_msgs = check_h10_suppression()
    for m in h10sup_msgs:
        print(m)
    if not h10sup_ok:
        all_pass = False

    h11sup_ok, h11sup_msgs = check_h11_suppression()
    for m in h11sup_msgs:
        print(m)
    if not h11sup_ok:
        all_pass = False

    r2cens_ok, r2cens_msgs = check_r2_censoring()
    for m in r2cens_msgs:
        print(m)
    if not r2cens_ok:
        all_pass = False

    h12lock_ok, h12lock_msgs = check_h12_pairing_lock()
    for m in h12lock_msgs:
        print(m)
    if not h12lock_ok:
        all_pass = False

    r1pool_ok, r1pool_msgs = check_r1_no_pool()
    for m in r1pool_msgs:
        print(m)
    if not r1pool_ok:
        all_pass = False

    r6pool_ok, r6pool_msgs = check_r6_no_pool()
    for m in r6pool_msgs:
        print(m)
    if not r6pool_ok:
        all_pass = False

    a3lock_ok, a3lock_msgs = check_a3_kappa_lock()
    for m in a3lock_msgs:
        print(m)
    if not a3lock_ok:
        all_pass = False

    a4lock_ok, a4lock_msgs = check_a4_conflict_lock()
    for m in a4lock_msgs:
        print(m)
    if not a4lock_ok:
        all_pass = False

    h8lock_ok, h8lock_msgs = check_h8a_decoupling_lock()
    for m in h8lock_msgs:
        print(m)
    if not h8lock_ok:
        all_pass = False

    h11block_ok, h11block_msgs = check_h11b_discriminant_lock()
    for m in h11block_msgs:
        print(m)
    if not h11block_ok:
        all_pass = False

    if all_pass:
        print("OK: all expectations met.")
        return 0
    print("FAIL: one or more expectations violated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
