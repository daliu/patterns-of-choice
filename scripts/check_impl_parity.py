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

    # --- contextVariability (H10 · scoring.md §15.5/§15.7): the on-device cross-situational
    # consistency reveal. Python context_profile_by_user vs JS contextVariability on the SAME
    # per-user flat records: per-construct sd_i(c) (sample SD of ≥2-item context means, ≥3
    # qualifying contexts) + the within-branch V (≥3 qualifying constructs, else SUPPRESSED
    # null while the surviving facets still reveal alone — §1.5). Fixture entries are parsed
    # once by the analyzer's own context_item_records (item scoring + §10 exclusion), then a
    # synthetic below-floor user is appended POST-PARSE in the flat record shape so all three
    # floors are exercised on both sides. Descriptive only, never pooled (§13.5).
    if node and proj_js.exists():
        cv_entries = json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-context-log.json").read_text())
        cv_recs = A.context_item_records(cv_entries, A.load_tag_axis_map(A.DEFAULT_TAG_MAP))
        # zz-below-floor: d1 = 3 contexts x 2 items (qualifies, n_contexts=3); d2 = 2 contexts
        # x 2 items (killed by the >=3-context floor); d3 = 1 context x 1 item (killed by the
        # >=2-item floor) => constructs=[d1] only, n_constructs=1, V suppressed (1 < 3).
        cv_recs = cv_recs + [
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "anonymous", "score": 2.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "anonymous", "score": 4.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "public", "score": 5.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "public", "score": 7.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "observed", "score": 1.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "context": "observed", "score": 1.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d2", "context": "anonymous", "score": 3.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d2", "context": "anonymous", "score": 5.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d2", "context": "public", "score": 4.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d2", "context": "public", "score": 6.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d3", "context": "anonymous", "score": 2.5},
        ]
        cv_users = sorted({r["user"] for r in cv_recs})
        py_prof = A.context_profile_by_user(cv_recs)
        py_cv = {}
        for u in cv_users:
            p = py_prof.get(u)
            # analyzer-absent user (every construct suppressed) <=> runtime empty profile
            py_cv[u] = ({"v": None, "n_constructs": 0, "constructs": []} if p is None
                        else {"v": p["v"], "n_constructs": p["n_constructs"],
                              "constructs": p["constructs"]})
        cv_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  const f = P.contextVariability(recs.filter(r => r.user === u));\n"
            "  out[u] = { v: f.v, n_constructs: f.n_constructs, constructs: f.constructs };\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        cproc = subprocess.run([node, "-e", cv_script, json.dumps(cv_recs), json.dumps(cv_users)],
                               capture_output=True, text=True)
        if cproc.returncode != 0:
            ok(False, "node contextVariability run", cproc.stderr.strip()[:300])
        else:
            js_cv = json.loads(cproc.stdout)

            def _close_c(a, b):
                if a is None or b is None:
                    return a is None and b is None
                return abs(a - b) < 1e-9

            all_c = True
            for u in cv_users:
                p, j = py_cv[u], js_cv.get(u, {})
                jc = j.get("constructs") or []
                m = (_close_c(p["v"], j.get("v"))
                     and p["n_constructs"] == j.get("n_constructs")
                     and len(p["constructs"]) == len(jc)
                     and all(pc["domain"] == jx.get("domain")
                             and pc["n_contexts"] == jx.get("n_contexts")
                             and _close_c(pc["sd"], jx.get("sd"))
                             for pc, jx in zip(p["constructs"], jc)))
                all_c = all_c and m
                if not m:
                    ok(False, f"contextVariability parity user {u}", f"py={p} js={j}")
            ok(all_c, f"contextVariability: JS == Python on all {len(cv_users)} participants "
                      f"(per-construct sd + context counts + §1.5 floor suppression)")

    # --- circleShape (H11 · scoring.md §16.5/§16.7): the on-device moral-circle shape
    # reveal. Python circle_shape_by_user vs JS circleShape on the SAME per-user flat
    # records: concern per distance bin (mean of ≥2 circle_radius-axis item scores),
    # β_i = OLS slope of concern on bin index, R_i = first bin ascending where concern
    # crosses the near-bin↔axis-floor midpoint — RIGHT-CENSORED (radius None/null,
    # censored true) when it never crosses, never made finite (§13.2). A user forms a
    # shape only with ≥4 populated bins (§1.5): Python-absent ⇔ JS ok=false. Fixture
    # entries are parsed once by the analyzer's own circle_item_records (item scoring +
    # §10 exclusion + counterparty→bin map), then a synthetic below-floor user is
    # appended POST-PARSE in the flat record shape so both suppression floors are
    # exercised; the fixture itself already covers finite AND censored radii. β_i/R_i
    # are facets, never pooled (§13.5); wider is never scored better (§16.5).
    if node and proj_js.exists():
        cs_entries = json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-circle-log.json").read_text())
        cs_recs = A.circle_item_records(
            cs_entries, A.load_tag_axis_map(A.DEFAULT_TAG_MAP),
            A.load_counterparty_distance_map(A.DEFAULT_DISTANCE_MAP)[0])
        # zz-below-floor: bins 0/1/2 = 2 items each (qualify) + bin 3 = 1 item (killed
        # by the >=2-item floor) => 3 populated bins < 4 => no shape on either side.
        cs_recs = cs_recs + [
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 0, "score": 0.9},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 0, "score": 0.7},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 1, "score": 0.5},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 1, "score": 0.3},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 2, "score": 0.2},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 2, "score": 0.0},
            {"user": "zz-below-floor", "session": "zz-s1", "domain": "zz-d1", "bin": 3, "score": -0.5},
        ]
        cs_users = sorted({r["user"] for r in cs_recs})
        py_shapes = A.circle_shape_by_user(cs_recs)
        cs_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  out[u] = P.circleShape(recs.filter(r => r.user === u));\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        sproc = subprocess.run([node, "-e", cs_script, json.dumps(cs_recs), json.dumps(cs_users)],
                               capture_output=True, text=True)
        if sproc.returncode != 0:
            ok(False, "node circleShape run", sproc.stderr.strip()[:300])
        else:
            js_cs = json.loads(sproc.stdout)

            def _close_s(a, b):
                if a is None or b is None:
                    return a is None and b is None
                return abs(a - b) < 1e-9

            all_s = True
            for u in cs_users:
                p, j = py_shapes.get(u), js_cs.get(u, {})
                if p is None:
                    # below the >=4-bin floor: suppressed on both sides (§1.5)
                    m = j.get("ok") is False and j.get("radius") is None and j.get("censored") is None
                else:
                    m = (j.get("ok") is True
                         and _close_s(p["beta"], j.get("beta"))
                         and p["radius"] == j.get("radius")          # int bin or None, exact (§13.2)
                         and p["censored"] == j.get("censored")
                         and p["n_bins"] == j.get("n_bins")
                         and p["near_bin"] == j.get("near_bin")
                         and p["far_bin"] == j.get("far_bin")
                         and _close_s(p["midpoint"], j.get("midpoint"))
                         and _close_s(p["near_concern"], j.get("near_concern"))
                         and _close_s(p["far_concern"], j.get("far_concern")))
                all_s = all_s and m
                if not m:
                    ok(False, f"circleShape parity user {u}", f"py={p} js={j}")
            ok(all_s, f"circleShape: JS == Python on all {len(cs_users)} participants "
                      f"(beta + censored radius + midpoint + §1.5/§13.2 floor-and-censoring)")

    # --- protectedValues (R2 · scoring.md §17.5/§17.7): the on-device professed-
    # protected-set reveal. Python protected_profile_by_user vs JS protectedValues on
    # the SAME flat CoV responses: P_i = the value slots whose response is a right-
    # censored `never` (no_break_point true OR first_accept_rung "never" — both
    # predicate arms exercised below), read on the FIRST wave, held as value-slot
    # STRINGS never prices (§13.2). An EMPTY set is DATA, not suppression (§17.5) —
    # only a user with no probed wave is Python-absent ⇔ JS ok=false. The fixture is
    # consumed AS-IS (the census eats raw responses; no item-scoring parse step), then
    # synthetic edge users are appended POST-LOAD: no-wave, all-priced (empty set),
    # multi-wave (first-wave read must win), and probed-without-slot. Set + counts
    # only, never a sacredness score (§13.5).
    if node and proj_js.exists():
        pv_recs = json.loads(
            (REPO_ROOT / "analysis" / "fixtures" / "sample-protected-values-log.json").read_text())
        pv_recs = pv_recs + [
            # zz-no-wave: records without a wave key are dropped entirely -> no profile
            {"user_id": "zz-no-wave", "value_slot": "honesty", "no_break_point": True},
            {"user_id": "zz-no-wave", "wave": None, "value_slot": "loyalty", "no_break_point": True},
            # zz-all-priced: both slots finite -> professed=[] emitted (empty set is DATA)
            {"user_id": "zz-all-priced", "wave": "w1", "value_slot": "honesty",
             "first_accept_rung": "r2", "first_accept_stake": 100, "no_break_point": False},
            {"user_id": "zz-all-priced", "wave": "w1", "value_slot": "charity",
             "first_accept_rung": "r4", "first_accept_stake": 10000, "no_break_point": False},
            # zz-multiwave: w1 wins (first-wave read); both `never` predicate arms hit
            # (honesty via no_break_point=True, candor via first_accept_rung="never")
            {"user_id": "zz-multiwave", "wave": "w1", "value_slot": "honesty",
             "first_accept_rung": None, "first_accept_stake": None, "no_break_point": True},
            {"user_id": "zz-multiwave", "wave": "w1", "value_slot": "candor",
             "first_accept_rung": "never", "first_accept_stake": None},
            {"user_id": "zz-multiwave", "wave": "w1", "value_slot": "charity",
             "first_accept_rung": "r3", "first_accept_stake": 1000, "no_break_point": False},
            {"user_id": "zz-multiwave", "wave": "w2", "value_slot": "loyalty",
             "first_accept_rung": None, "first_accept_stake": None, "no_break_point": True},
            # zz-probed-noslot: a probed wave with no value_slot -> professed=[], 0 slots
            {"user_id": "zz-probed-noslot", "wave": "w1", "no_break_point": True},
        ]
        pv_users = sorted({r["user_id"] for r in pv_recs})
        py_pv = A.protected_profile_by_user(pv_recs)
        pv_script = (
            "const P = require(%s);\n"
            "const recs = JSON.parse(process.argv[1]);\n"
            "const users = JSON.parse(process.argv[2]);\n"
            "const out = {};\n"
            "for (const u of users) {\n"
            "  out[u] = P.protectedValues(recs.filter(r => r.user_id === u));\n"
            "}\n"
            "console.log(JSON.stringify(out));\n"
        ) % (json.dumps(str(proj_js)),)
        pproc = subprocess.run([node, "-e", pv_script, json.dumps(pv_recs), json.dumps(pv_users)],
                               capture_output=True, text=True)
        if pproc.returncode != 0:
            ok(False, "node protectedValues run", pproc.stderr.strip()[:300])
        else:
            js_pv = json.loads(pproc.stdout)
            all_p = True
            for u in pv_users:
                p, j = py_pv.get(u), js_pv.get(u, {})
                if p is None:
                    # no probed wave: absent on the Python side <=> ok=false in JS
                    m = j.get("ok") is False and j.get("professed") is None
                else:
                    m = (j.get("ok") is True
                         and p["wave"] == j.get("wave")
                         and p["professed"] == j.get("professed")    # exact strings, exact order
                         and p["n_professed"] == j.get("n_professed")
                         and p["n_slots_probed"] == j.get("n_slots_probed"))
                all_p = all_p and m
                if not m:
                    ok(False, f"protectedValues parity user {u}", f"py={p} js={j}")
            ok(all_p, f"protectedValues: JS == Python on all {len(pv_users)} participants "
                      f"(professed set + first-wave read + §13.2 categorical never + empty-set-is-data)")


print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
