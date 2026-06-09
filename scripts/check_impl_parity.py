#!/usr/bin/env python3
"""
Cross-implementation parity gate.

The on-device projection (runtime/poc-projection.js, the canonical scorer the
app shows the user) and this repo's analyzer (scripts/analyze.py, the future
validation-cohort scorer) must compute the SAME revealed score from the SAME
event log. Each was previously tested only in isolation against hand-coded
expectations, which let three silent drifts accumulate (cov payload field names,
secondary-axis tag inclusion, and the §10 inattentive-RT gate). This gate
compares the two implementations directly, plus locks the analyzer's handling of
the real app event payload.

Two layers:
  1. PURE-PYTHON locks (always run): the analyzer scores the actual app/runtime
     payload correctly — cov by scenario_id + no_break_point, item_score on the
     primary axis only, the inattentive-RT session drop.
  2. CROSS-LANGUAGE parity (when node + the runtime JS are reachable): run
     poc-projection.js on the same inputs and assert JS == Python. Skipped with
     a loud notice (not a silent pass) if node or the runtime sibling is absent.

Exit 0 if all run checks pass; 1 on any mismatch; 2 if the analyzer can't load.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

try:
    import analyze as A
except Exception as e:  # pragma: no cover
    print(f"FAIL: cannot import analyze.py: {e}", file=sys.stderr)
    sys.exit(2)

# The runtime JS lives in the sibling daliu.github.io repo (same assumption as
# runtime/build-arc-bundle.py). Override with POC_RUNTIME.
DEFAULT_RUNTIME = REPO_ROOT.parent / "daliu.github.io" / "patterns-of-choice" / "runtime"
RUNTIME = Path(os.environ.get("POC_RUNTIME", DEFAULT_RUNTIME))

TAG_MAP = A.load_tag_axis_map(A.DEFAULT_TAG_MAP)

passed = 0
failed = 0


def ok(cond, msg, extra=None):
    global passed, failed
    if cond:
        passed += 1
        print(f"  ✓ {msg}")
    else:
        failed += 1
        print(f"  ✗ {msg}" + (f"  {extra}" if extra is not None else ""))


# --- shared canonical inputs (same on both sides) ---------------------------
# item_score cases, deliberately including secondary-axis tags (in-group's
# circle_radius: hospitality/boundaries; reciprocity's cooperation_orientation).
ITEM_CASES = [
    {"domain": "truth-telling", "tags": ["truth:commission"]},
    {"domain": "truth-telling", "tags": ["lie:white"]},
    {"domain": "truth-telling", "tags": ["truth:commission", "truth:confront-direct"]},
    {"domain": "resource-allocation", "tags": ["generosity"]},
    {"domain": "in-group-out-group", "tags": ["loyalty"]},
    {"domain": "in-group-out-group", "tags": ["hospitality"]},                    # secondary axis
    {"domain": "in-group-out-group", "tags": ["particularism", "value:hospitality"]},  # mixed
    {"domain": "in-group-out-group", "tags": ["boundaries"]},                     # secondary axis
    {"domain": "reciprocity-cooperation", "tags": ["trust"]},
    {"domain": "reciprocity-cooperation", "tags": ["cooperation"]},               # secondary axis
    {"domain": "truth-telling", "tags": ["counterparty:close"]},                  # metadata only
]


def py_item(case):
    score, n = A.item_score(case, TAG_MAP)
    return {"score": round(score, 9), "n": n}


# === Layer 1: pure-Python locks (always run) ================================
print("Cross-impl parity — analyzer locks (pure Python):")

# drift #2: secondary-axis tags excluded; primary counted
ok(A.item_score({"domain": "in-group-out-group", "tags": ["hospitality"]}, TAG_MAP)[1] == 0,
   "in-group 'hospitality' (circle_radius, secondary) excluded from revealed score")
ok(A.item_score({"domain": "in-group-out-group", "tags": ["loyalty"]}, TAG_MAP)[1] == 1,
   "in-group 'loyalty' (primary) counted")
ok(A.item_score({"domain": "reciprocity-cooperation", "tags": ["cooperation"]}, TAG_MAP)[1] == 0,
   "reciprocity 'cooperation' (cooperation_orientation, secondary) excluded")

# drift #1: the app cov payload (scenario_id + no_break_point) scores, and equals
# the legacy probe_id + rung=="never" shape.
inv = A.load_probe_inversion_map()
cm = A.load_probe_ceiling_map()
app_refuse = A.probe_break_point_score(
    {"scenario_id": "cov-truth-001", "no_break_point": True}, inv, cm)
legacy_refuse = A.probe_break_point_score(
    {"probe_id": "cov-truth-001", "first_accept_rung": "never"}, inv, cm)
ok(app_refuse is not None, "app cov refusal (scenario_id + no_break_point) scores (not None)", app_refuse)
ok(app_refuse == legacy_refuse, "app refusal == legacy probe_id/never refusal", (app_refuse, legacy_refuse))
app_stake = A.probe_break_point_score(
    {"scenario_id": "cov-truth-001", "first_accept_stake": 1000, "no_break_point": False}, inv, cm)
ok(app_stake is not None and abs(app_stake[0] - 3.0) < 1e-9,
   "app cov finite stake $1000 -> log10 = 3.0", app_stake)

# drift #3: a session×domain with median RT < 2s is dropped; >=2s kept.
def sess(sid, rt):
    return {"user_id": "u", "session_id": sid, "domain": "truth-telling",
            "tags": ["truth:commission"], "response_time_ms": rt}
fast = A.session_aggregates([sess("sf", 400), sess("sf", 500), sess("sf", 600)], TAG_MAP)
slow = A.session_aggregates([sess("ss", 3000), sess("ss", 3500), sess("ss", 4000)], TAG_MAP)
ok(("u", "sf", "truth-telling") not in fast, "inattentive session (median RT 500ms) dropped")
ok(("u", "ss", "truth-telling") in slow, "attentive session (median RT 3500ms) kept")

# === Layer 2: cross-language parity (JS projection vs Python analyzer) ======
print("\nCross-impl parity — JS projection vs Python analyzer:")
node = shutil.which("node")
proj_js = RUNTIME / "poc-projection.js"
tagmap_json = RUNTIME / "tag-axis-map.v0.1.json"
if not node or not proj_js.exists() or not tagmap_json.exists():
    print(f"  ! SKIPPED (not a silent pass): node={'found' if node else 'missing'}, "
          f"runtime={'found' if proj_js.exists() else 'missing @ ' + str(RUNTIME)}.")
    print("    Set POC_RUNTIME to the daliu.github.io patterns-of-choice/runtime dir to enable.")
else:
    node_script = (
        "const P = require(%s);\n"
        "const tagMap = require(%s);\n"
        "const cases = JSON.parse(process.argv[1]);\n"
        "console.log(JSON.stringify(cases.map(c => {\n"
        "  const r = P.itemScore(c.domain, c.tags, tagMap);\n"
        "  return { score: Math.round(r.score * 1e9) / 1e9, n: r.n };\n"
        "})));\n"
    ) % (json.dumps(str(proj_js)), json.dumps(str(tagmap_json)))
    proc = subprocess.run([node, "-e", node_script, json.dumps(ITEM_CASES)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        ok(False, "node projection run", proc.stderr.strip()[:300])
    else:
        js = json.loads(proc.stdout)
        all_match = True
        for case, j in zip(ITEM_CASES, js):
            p = py_item(case)
            match = (p["n"] == j["n"]) and abs(p["score"] - j["score"]) < 1e-9
            all_match = all_match and match
            if not match:
                ok(False, f"itemScore parity {case['domain']} {case['tags']}", f"py={p} js={j}")
        ok(all_match, f"itemScore: JS == Python on all {len(ITEM_CASES)} cases (incl. secondary-axis)")


print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
