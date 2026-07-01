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
    "H11": {"kind": "h11", "sub_met": {"H11a": True, "H11c": True}},
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

    if all_pass:
        print("OK: all expectations met.")
        return 0
    print("FAIL: one or more expectations violated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
