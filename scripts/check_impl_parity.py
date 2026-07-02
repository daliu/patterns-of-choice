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

    # --- centrality facet reveal parity (R1 §19.1): the N=1 on-device reveal -----
    # The runtime's centralityFacets() (computed per person, on-device) must equal
    # the analyzer's centrality_facet_by_user for EVERY participant — same two facet
    # means, same scorable-item counts, same ≥3-item-floor suppression, same declined-
    # item drop. Reuses the R1 fixture, plus a synthetic below-floor user so the
    # SUPPRESSED (null) path is exercised on both sides too. This is the first shipped
    # on-device reveal for the H9–R6 family; the two facets stay SEPARATE (§13.5).
    if node and proj_js.exists():
        id_recs = [r for r in json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-identity-centrality-log.json").read_text())
            if isinstance(r, dict)]
        # a synthetic user with only 2 internalization items (below the ≥3 floor) and 0
        # symbolization items: analyzer suppresses (absent) ⇔ runtime returns null.
        id_recs = id_recs + [
            {"user": "zz-below-floor", "session": "zz-s1", "item_id": "int-a", "facet": "internalization", "response": 5.0},
            {"user": "zz-below-floor", "session": "zz-s1", "item_id": "int-b", "facet": "internalization", "response": 5.0},
        ]
        id_users = sorted({r.get("user") for r in id_recs if r.get("user") is not None})
        py_int = A.centrality_facet_by_user(id_recs, "internalization")
        py_sym = A.centrality_facet_by_user(id_recs, "symbolization")
        py_int_items = A.centrality_items_by_user(id_recs, "internalization")
        py_sym_items = A.centrality_items_by_user(id_recs, "symbolization")
        py_facets = {u: {"internalization": py_int.get(u), "symbolization": py_sym.get(u),
                         "n_internalization": len(py_int_items.get(u, [])),
                         "n_symbolization": len(py_sym_items.get(u, []))} for u in id_users}
        cen_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  const f = P.centralityFacets(recs.filter(r => r.user === u));\n"
            "  out[u] = { internalization: f.internalization, symbolization: f.symbolization,\n"
            "             n_internalization: f.n_internalization, n_symbolization: f.n_symbolization };\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        cproc = subprocess.run([node, "-e", cen_script, json.dumps(id_recs), json.dumps(id_users)],
                               capture_output=True, text=True)
        if cproc.returncode != 0:
            ok(False, "node centralityFacets run", cproc.stderr.strip()[:300])
        else:
            js_facets = json.loads(cproc.stdout)

            def _close(a, b):
                if a is None or b is None:
                    return a is None and b is None
                return abs(a - b) < 1e-9

            all_c = True
            for u in id_users:
                p, j = py_facets[u], js_facets.get(u, {})
                m = (_close(p["internalization"], j.get("internalization"))
                     and _close(p["symbolization"], j.get("symbolization"))
                     and p["n_internalization"] == j.get("n_internalization")
                     and p["n_symbolization"] == j.get("n_symbolization"))
                all_c = all_c and m
                if not m:
                    ok(False, f"centralityFacets parity user {u}", f"py={p} js={j}")
            ok(all_c, f"centralityFacets: JS == Python on all {len(id_users)} participants "
                      f"(facet means + item counts + ≥3-floor suppression)")

    # --- objectivism claim-type reveal parity (R6 §20.1): the N=1 on-device reveal ------
    # The runtime's objectivismReads() (per person, on-device) must equal the analyzer's
    # objectivism_by_user for EVERY participant — same two claim-type means, same scorable-
    # item counts, same ≥3-item-floor suppression, same declined-item drop. Reuses the R6
    # fixture, plus a synthetic below-floor user so the SUPPRESSED (null) path is exercised
    # on both sides. The two reads stay SEPARATE (§13.5); the charged branch, value-neutral.
    if node and proj_js.exists():
        ob_recs = [r for r in json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-objectivism-log.json").read_text())
            if isinstance(r, dict)]
        # a synthetic user with only 2 moral items (below the ≥3 floor) and 0 taste items:
        # analyzer suppresses (absent) ⇔ runtime returns null.
        ob_recs = ob_recs + [
            {"user": "zz-below-floor", "session": "zz-s1", "item_id": "mor-a", "claim_type": "moral", "objectivism": 5.0},
            {"user": "zz-below-floor", "session": "zz-s1", "item_id": "mor-b", "claim_type": "moral", "objectivism": 5.0},
        ]
        ob_users = sorted({r.get("user") for r in ob_recs if r.get("user") is not None})
        py_moral = A.objectivism_by_user(ob_recs, "moral")
        py_taste = A.objectivism_by_user(ob_recs, "taste")
        py_moral_items = A.objectivism_items_by_user(ob_recs, "moral")
        py_taste_items = A.objectivism_items_by_user(ob_recs, "taste")
        py_reads = {u: {"moral": py_moral.get(u), "taste": py_taste.get(u),
                        "n_moral": len(py_moral_items.get(u, [])),
                        "n_taste": len(py_taste_items.get(u, []))} for u in ob_users}
        ob_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  const f = P.objectivismReads(recs.filter(r => r.user === u));\n"
            "  out[u] = { moral: f.moral, taste: f.taste,\n"
            "             n_moral: f.n_moral, n_taste: f.n_taste };\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        oproc = subprocess.run([node, "-e", ob_script, json.dumps(ob_recs), json.dumps(ob_users)],
                               capture_output=True, text=True)
        if oproc.returncode != 0:
            ok(False, "node objectivismReads run", oproc.stderr.strip()[:300])
        else:
            js_reads = json.loads(oproc.stdout)

            def _close_o(a, b):
                if a is None or b is None:
                    return a is None and b is None
                return abs(a - b) < 1e-9

            all_o = True
            for u in ob_users:
                p, j = py_reads[u], js_reads.get(u, {})
                m = (_close_o(p["moral"], j.get("moral"))
                     and _close_o(p["taste"], j.get("taste"))
                     and p["n_moral"] == j.get("n_moral")
                     and p["n_taste"] == j.get("n_taste"))
                all_o = all_o and m
                if not m:
                    ok(False, f"objectivismReads parity user {u}", f"py={p} js={j}")
            ok(all_o, f"objectivismReads: JS == Python on all {len(ob_users)} participants "
                      f"(claim-type means + item counts + ≥3-floor suppression)")

    # --- hypocrisy H_i reveal parity (H12 §18.1): the N=1 on-device reveal -------------
    # The runtime's hypocrisyAsymmetry() (per person, on-device) must equal the analyzer's
    # hypocrisy_asymmetry_by_user for EVERY participant — same SIGNED paired mean, same
    # scorable-pair count, same ≥3-pair-floor suppression, same declined-pair drop (either
    # side missing/non-numeric/boolean ⇒ the PAIR drops, never imputed 0; the §18.1
    # pairing lock). Reuses the H12 fixture, plus a synthetic below-floor user so the
    # SUPPRESSED (null) path is exercised on both sides. Signed, value-neutral, never
    # pooled (§13.5) — no per-person verdict on either side.
    if node and proj_js.exists():
        hy_recs = [r for r in json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-hypocrisy-log.json").read_text())
            if isinstance(r, dict)]
        # a synthetic user with only 2 scorable pairs (below the ≥3 floor) plus 1 declined
        # pair: analyzer suppresses (absent from asymmetry_by_user) ⇔ runtime returns null.
        hy_recs = hy_recs + [
            {"user": "zz-below-floor", "session": "zz-s1", "probe_id": "judge-x-1", "severity_self": 4.0, "severity_other": 6.0},
            {"user": "zz-below-floor", "session": "zz-s1", "probe_id": "judge-x-2", "severity_self": 5.0, "severity_other": 3.0},
            {"user": "zz-below-floor", "session": "zz-s1", "probe_id": "judge-x-3", "severity_self": 5.0, "severity_other": None},
        ]
        hy_users = sorted({r.get("user") for r in hy_recs if r.get("user") is not None})
        py_h = A.hypocrisy_asymmetry_by_user(hy_recs)
        py_deltas = A.hypocrisy_deltas_by_user(hy_recs)
        py_hyp = {u: {"h": py_h.get(u), "n_pairs": len(py_deltas.get(u, []))} for u in hy_users}
        hy_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  const f = P.hypocrisyAsymmetry(recs.filter(r => r.user === u));\n"
            "  out[u] = { h: f.h, n_pairs: f.n_pairs };\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        hproc = subprocess.run([node, "-e", hy_script, json.dumps(hy_recs), json.dumps(hy_users)],
                               capture_output=True, text=True)
        if hproc.returncode != 0:
            ok(False, "node hypocrisyAsymmetry run", hproc.stderr.strip()[:300])
        else:
            js_hyp = json.loads(hproc.stdout)

            def _close_h(a, b):
                if a is None or b is None:
                    return a is None and b is None
                return abs(a - b) < 1e-9

            all_h = True
            for u in hy_users:
                p, j = py_hyp[u], js_hyp.get(u, {})
                m = (_close_h(p["h"], j.get("h"))
                     and p["n_pairs"] == j.get("n_pairs"))
                all_h = all_h and m
                if not m:
                    ok(False, f"hypocrisyAsymmetry parity user {u}", f"py={p} js={j}")
            ok(all_h, f"hypocrisyAsymmetry: JS == Python on all {len(hy_users)} participants "
                      f"(signed paired means + pair counts + ≥3-pair-floor suppression)")


print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
