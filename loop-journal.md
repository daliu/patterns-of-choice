# Patterns of Choice — extension-loop journal (sidecar)

**Why this file exists.** The canonical loop journal lives in the Obsidian vault
(`wiki/conversations/2026-06-09 - Patterns of Choice — Extension Loop.md`). That
vault is iCloud-synced and the note is a dataless/evicted placeholder, so the
iCloud File Provider denies raw uncoordinated writes (`PermissionError`, errno 1)
while still allowing reads and new-file creation. Rather than lose the per-iteration
log, the loop mirrors entries here, in-repo and non-iCloud. **Reconcile into the
vault** once it is materialized (move the vault off "Optimize Mac Storage", or
download the note) — these entries are the source for that back-fill.

Newest first. Each entry: what branch, what it adds, what it honors, what shipped.

---

## Iteration 22 — 2026-06-30 — H12 · Moral hypocrisy / self–other judgment asymmetry

`build-and-validate.md` item 5, the next cheapest-clean buildable branch: **H12** (`scoring.md §18`). The 13th
pre-reg branch, and the cheapest left because it is a clean **paired within-person contrast** that reuses the
gap/bootstrap/reliability machinery whole — no κ-gated language channel (that's R3–R6), no new axis, no corpus
rewrite. The construct: does a person judge the **same act** more harshly when **another** commits it than when
**they** do? For each matched act the person rates `severity_self` (how wrong when *I* do it) and
`severity_other` (how wrong when *another* does it) on a common 0–10 scale; `H_i = mean_act(severity_other −
severity_self)` is the self–other asymmetry. Grounded in Tappin & McKay 2017 (*The Illusion of Moral
Superiority*), Epley & Dunning 2000 (*Feeling "holier than thou"*), the actor–observer asymmetry (Jones &
Nisbett 1971; Malle 2006), with Batson's *moral hypocrisy* (1997/1999) as origin. **Deliberately avoided**
Valdesolo & DeSteno (manipulation-based, an experimenter-staged asymmetry not a within-person read) and every
excluded paradigm (no Stapel / Gino / Ariely-priming / ego-depletion).

- **What shipped (`scripts/analyze.py`, `--hypocrisy-log`).** The §18.1 primitive — `_hypocrisy_pair_delta`
  (the signed `severity_other − severity_self` per matched act) → `hypocrisy_asymmetry_by_user` → `H_i` = the
  per-person mean over ≥ 3 scorable pairs; **H12a** asymmetry reliability (split-half odd/even sessions,
  `corr(H_i^odd, H_i^even)` supported iff lower bootstrap-CI ≥ 0.40, seed +19 — mirrors H10a/H11a exactly via
  `_odd_even_sessions` + `_pearson_r` + `_bootstrap_ci_r`); **H12c** the self-serving directional anchor
  (`mean_i H_i` supported iff lower-CI > 0, one-sided, seed +20 — the "holier than thou" signature as a
  **cohort validity check**, *not* a per-person verdict). Gated in `check_analyzer_thresholds.py` (H12
  expectations + a `check_h12_pairing_lock()` unit-regression) on a self-contained fixture
  (`analysis/fixtures/sample-hypocrisy-log.json`, 12 participants × 4 sessions × 3 matched probes + one
  declined judgment, known ground truth: `H12a` r=1.000 CI-low 1.000 met (noiseless-by-construction design so
  the gate checks the analyzer *recovers* r=1.0 and clears the 0.40 floor); `H12c` mean_asymmetry=+1.083
  CI-low +0.667 CI-high +1.458 met, n=12; `person_asymmetry_n`=12 reveal-eligible).
- **Disciplines honored.** *Pairing / missing-data lock* (§18.1 — the load-bearing one here, the H12 analog of
  the §13.2 censoring lock): a **declined judgment** (either side missing/non-numeric) makes the delta
  undefined, so the pair is **DROPPED — never imputed to 0** (which would fabricate "no asymmetry"), and the
  delta is **signed** so harsher-on-self stays **NEGATIVE**, never clamped toward the self-serving direction;
  asserted directly against the code in `check_h12_pairing_lock()` (complete pair → other−self sign+magnitude;
  harsher-on-self → −3.0 not clamped; declined self/other/bool → None; declined pair dropped from deltas, H_i
  is the mean over only scorable pairs — 7 assertions, all green). *No composite / never-pool* (§13.5): `H_i`
  is a **signed facet**, never summed with a gap, calibration index, variability index, circle radius,
  protected set, or CoV price, never pooled across branches. *Value-neutral* (load-bearing): harsher-on-others
  AND harsher-on-self are both **described, never ranked** — a self-critical person (`H_i < 0`) is not "more
  honest," a self-serving one is not "more confident"; the fixture's u12 (`H_i` = −0.5) exercises the
  preserved negative sign. This is why **H12c is walled off as a cohort anchor, not an individual verdict.**
  *N=1* — `H_i` is a within-person mean over that user's ≥ 3 pairs, reveal-eligible with no cohort norms.
  *Cheap-talk* — these are judgments of *hypothetical* acts, not behavior under stakes; `H_i` is a **stated**
  asymmetry, behavioral validation is Phase-2. *Fraud/replication* — no excluded paradigms (Tappin &
  McKay / Epley & Dunning / actor–observer clean; V&D and the priming/depletion families deliberately avoided).
- **Scope (same pattern as H9/H10/H11/R2).** A paired within-person contrast reusing the bootstrap + split-half
  machinery whole; **no new axis, no on-device reveal touched** → Python-only → **parity trivially green**
  (poc-projection.js untouched, 9/9). **Deferred (documented):** (a) **H12b-discriminant** — R² of `H_i` on
  `[gap_i, cal_error_i]` < 0.50; couples to the cohort gap + calibration pipelines like the H9b/H10b/H11b/R2c
  discriminants. (b) The **on-device `H_i` reveal** in `poc-projection.js` + its parity lock. (c) The self–other
  judgment log's **real collection + exact phrasing** (avoid a leading "aren't others worse?") and the
  **behavioral validation** — does a large `H_i` predict real self–other double standards — via Phase-2 (both
  surfaced under "Needs Dave / external").
- **PROPOSED lock (Dave's call — not auto-locked).** *DECISIONS §23 — H12 pre-registration.* `H_i` =
  `mean_act(severity_other − severity_self)` over a person's ≥ 3 matched self–other judgment pairs on a common
  0–10 severity scale, read off a new light `--hypocrisy-log` data-contract (`severity_self` + `severity_other`
  per probe). H12a floor 0.40 on the split-half (odd/even sessions) reliability of `H_i` (seed 20260510+19).
  H12c directional, `mean_i H_i` lower-CI > 0 (seed +20) — a **cohort validity anchor** (recovers the
  established self-serving direction), explicitly **not** a per-person verdict. Pairing lock: a declined
  judgment drops the pair (never imputed 0), signed delta preserved (harsher-on-self stays negative).
  Value-neutrality (neither direction ranked) is load-bearing. `H_i` labelled a **stated** asymmetry
  (hypothetical caveat) pending Phase-2 behavioral validation. H12b threshold (R² < 0.50) proposed but not
  built. If this reads right, say "lock §23" and I'll write it into `DECISIONS.md`.
- **Shipped.** `make check` green (exit 0): validate 66 scenarios + analyzer gate (H2–H7, H9, H10, H11, R2,
  **H12**, probe-ceiling, h9-censoring, h10-suppression, h11-suppression, r2-censoring, **h12-pairing**) +
  JS↔Python parity 9/9. Commit on `poc` main.

**Buildable-without-Dave work remains** (`build-and-validate.md` items 6+): R1 identity centrality (a
cohort-coupled meta-moderator), R6 conviction/objectivism (the charged stated–revealed meta-gap, leans on the
κ-gated language channel — needs Dave). Loop continues, thinning toward the Dave-gated tail.

---

## Iteration 21 — 2026-06-30 — R2 · Sacred / protected values

`build-and-validate.md` item 4, the next cheapest-clean buildable branch: **R2** (`scoring.md §17`, design doc
`r2-sacred-protected-values.md`). The cheapest branch left because it builds **no new elicitation and no new
break-point math** — it is a pure **re-read** of the cost-of-virtue channel's **right-censored `never` tail**
(§4, §13.2). The values a person refuses to price at *any* stake in range **are** their protected set; the
censoring discipline (never finitize a `never`) was quietly storing this construct all along. Grounded in
Baron & Spranca 1997 (protected values), Tetlock 2000 / Fiske & Tetlock 1997 (taboo trade-offs,
incommensurability), Bartels & Medin 2007 (quantity-insensitivity), Ginges et al. 2007 (sacred values in
conflict).

- **What shipped (`scripts/analyze.py`, `--protected-log`).** The §17.1 primitive — `protected_value_sets`
  → `P_i` = the SET of value slots a person marks `never` (keyed by `value_slot`, categorical, holding value
  **strings** and never a price); **R2a** set reliability (per participant present in ≥2 waves,
  `jaccard_i = |P_i^{w1} ∩ P_i^{w2}| / |P_i^{w1} ∪ P_i^{w2}|`, supported iff `mean_i jaccard_i` lower
  bootstrap-CI ≥ 0.40, seed +17 — a user whose protected union is empty in *both* waves has an undefined
  Jaccard and is **excluded**, never scored as perfect agreement); **R2b** the load-bearing distinctness
  *protected ≠ EXPENSIVE* (per never-responder, `contrast_i = mean(taboo|never) − mean(taboo|finite)`,
  supported iff `mean_i contrast_i` lower-CI > 0, one-sided, directional, seed +18 — being *asked* to price a
  protected value draws outrage a merely-expensive one does not). Introduces the light `taboo` (0/1) marker as
  a new data-contract field. Gated in `check_analyzer_thresholds.py` (R2 expectations + a
  `check_r2_censoring()` unit-regression) on a self-contained fixture
  (`analysis/fixtures/sample-protected-values-log.json`, 12 participants × 2 waves × 6 CoV values, known
  ground truth: `mean Jaccard`=0.924 CI-low 0.818 with 1 empty-union exclusion, `mean taboo-contrast`=+0.945
  CI-low 0.891, 11 participants with a non-empty `P_i` / 1 who prices everything).
- **Disciplines honored.** *Censoring* (§13.2 — the load-bearing one here, verbatim): a `never` is read
  **categorically** — right-censored, **NEVER finitized into a price** — the R2 analog of the
  `never`-on-$10M `|8.0|` lock; asserted directly against the code in `check_r2_censoring()` (a `never` is
  protected, a finite response is not; the `never` scores the ceiling+1 sentinel not a finite break-point;
  `P_i` holds the value-slot string; the empty-in-both-waves user is excluded from R2a — 4 assertions, all
  green). *No composite / never-pool* (§13.5): `P_i` is a **set** and `taboo` a **marker**, never summed into
  a "sacredness score" (§4 rejected exactly that scalar), never pooled across branches. *Value-neutral*
  (load-bearing): a **large protected set is NOT scored as better** — many `never`s can be **integrity** OR
  rigid **dogmatism**; the reveal names the set and never ranks it by size. *N=1* — `P_i` is a within-person
  set on the fixed value slots, reveal-eligible for one user with no cohort norms. *Cheap-talk* (load-bearing)
  — a hypothetical `never` is costless, so `P_i` is labelled **PROFESSED** protected values; real-stakes
  validation rides H-A2 → Phase-2. *Fraud/replication* — no excluded paradigms (Baron/Tetlock/Ginges clean).
- **Scope (same pattern as H9/H10/H11).** A pure re-read of the CoV break-point **primitive** (already
  parity-locked; the runtime emits per-slot `no_break_point` at `poc-projection.js:212`) **without changing
  it** → Python-only → **parity trivially green** (poc-projection.js untouched, 9/9). **Deferred
  (documented):** (a) **R2c-discriminant** — R² of `P_i`-membership on `[inventory rank, log-price]` < 0.50;
  couples to the cohort inventory pipeline like the H9b/H10b/H11b discriminants. (b) The **on-device `P_i`
  reveal** in `poc-projection.js` + its parity lock. (c) The `taboo` marker's **real collection + exact
  phrasing** (Q1, design-gated) and the **cheap-talk / real-stakes validation** via **H-A2 → Phase-2** (both
  surfaced under "Needs Dave / external"). (d) The **quantity-insensitivity leg** of R2b — a flat refusal that
  doesn't soften as the offer climbs — needs per-rung acceptance trajectories the single-break-point contract
  doesn't carry (§17.5, design-doc §6 Q3); the taboo contrast is the primary distinctness test.
- **PROPOSED lock (Dave's call — not auto-locked).** *DECISIONS §22 — R2 pre-registration.* `P_i` = the set of
  `value_slot`s marked `never` on the CoV ladder, read categorically off the §13.2 right-censored tail, never
  finitized. R2a floor 0.40 on `mean_i Jaccard(P_i^{w1}, P_i^{w2})` (test–retest across waves, seed
  20260510+17; empty-union users excluded, not scored 1.0). R2b directional, `mean_i(taboo|never −
  taboo|finite)` lower-CI > 0 (seed +18) — protected ≠ merely-expensive. `taboo` is a new 0/1
  data-contract field. `P_i` labelled **professed** (cheap-talk caveat) pending H-A2 real-stakes. Value-
  neutrality (integrity↔dogmatism, no ranking by set size) is load-bearing. R2c threshold (R² < 0.50) proposed
  but not built. The `taboo` phrasing is proposed pending Dave's runtime/UX call. If this reads right, say
  "lock §22" and I'll write it into `DECISIONS.md`.
- **Shipped.** `make check` green (exit 0): validate 66 scenarios + analyzer gate (H2–H7, H9, H10, H11,
  **R2**, probe-ceiling, h9-censoring, h10-suppression, h11-suppression, **r2-censoring**) + JS↔Python parity
  9/9. Commit on `poc` main.

**Buildable-without-Dave work remains** (`build-and-validate.md` items 5+): H12 hypocrisy (self–other delta,
needs light corpus authoring), R1 identity centrality, R6 conviction/objectivism. Loop continues.

---

## Iteration 20 — 2026-06-30 — H11 · Moral-circle radius

`build-and-validate.md` item 3, the next cheapest-clean buildable branch: **H11** (`scoring.md §16`,
design doc `h11-moral-circle-radius.md`). Not *where* you sit or how much you *move* (H9/H10) but how far
your concern **reaches** across recipient social/moral distance — Singer's *expanding circle* made
behavioral and within-person (Crimston et al. 2016 Moral Expansiveness Scale; Waytz et al. 2019 on the
*shape* of the ideological circle; Cikara & Bruneau on parochial empathy). No new elicitation: it re-reads
the **`circle_radius` secondary axis** already scored for the in-group domain (hospitality +1 / boundaries
−1) and bins each item by its `counterparty:*` tag through a versioned distance-ordering map.

- **What shipped (`scripts/analyze.py`, `--circle-log` / `--distance-map`).** The §16.1 primitive —
  `circle_item_records` → `concern_i(d)` (mean circle_radius score per distance bin) → `β_i` (OLS slope of
  concern on bin index = parochialism steepness) and `R_i` (the *reach*: first bin where concern crosses the
  person's midpoint `½·(near-concern + −1)`); **H11a** shape reliability (split each person's sessions
  odd/even, correlate `β_i^odd` vs `β_i^even`, lower bootstrap-CI ≥ 0.40, seed +15 — `β_i` carries it
  because it is always finite, whereas `R_i` right-censors on a flat circle, §6 Q3); **H11c** the
  parochial-gradient anchor (`near − far` concern, lower-CI > 0, one-sided, directional, seed +16 — validates
  the distance ordering is behaviorally real). Plus the versioned map
  `analysis/counterparty_distance_map_v0.1.csv` (28 laddered counterparty tags over 7 bins; the §6 Q4
  power/role tags `senior`/`subordinate`/`business` and the within-item contrast markers excluded *in the
  map* via a non-integer bin). Gated in `check_analyzer_thresholds.py` (H11 expectations + a
  `check_h11_suppression()` unit-regression) on a self-contained fixture
  (`analysis/fixtures/sample-circle-log.json`, 12 participants on a 6-level parochialism ladder, 6 bins × 2
  items × 2 sessions; ground truth hand-checked: β-ladder 0→−0.457, `corr(β_odd,β_even)`=+0.992 CI-low 0.959,
  mean near−far gradient +1.5 CI-low 1.083, 10 finite radii / 2 right-censored).
- **Disciplines honored.** *No composite / never-pool* (§13.5): `β_i`/`R_i` are within-branch facets on the
  secondary axis, never summed with a gap/calibration/variability/CoV index, never pooled with the primary
  channel. *Censoring* (§13.2 — verbatim): a flat/impartial circle's `R_i` is right-censored (`radius=None`,
  `censored=True`) and **NEVER made finite** — the distance-axis analog of the `never`-on-$10M `|8.0|` lock;
  asserted directly against the code in `check_h11_suppression()` (flat → censored; parochial control →
  finite R=1). *Suppression* (§1.5): a bin needs ≥2 items, a shape ≥4 populated bins — else omitted, never
  scored on thin data (2 more assertions, all green). *Value-neutral* (load-bearing, R6-grade charge) — a
  **wider circle is NOT scored as better**: Singer's impartialism ↔ Williams/MacIntyre/Confucian partialism,
  the reveal names the shape and **never ranks** it. *N=1* — `β_i`/`R_i` on the fixed secondary axis +
  ordering, reveal-eligible for one user with no cohort norms. *Fraud/replication* — no excluded paradigms.
- **Scope (same pattern as H9/H10).** The scorer reads `circle_radius` **separately** from the primary
  `item_score`, so the parity secondary-axis-exclusion lock (hospitality **out** of the revealed score) is
  untouched → Python-only → **parity trivially green** (poc-projection.js untouched, 9/9; the parity gate
  explicitly re-confirms `hospitality (circle_radius) excluded`). **Deferred (documented):** (a)
  **H11b-discriminant** — R² of shape on `[near-bin concern, generosity level]` < 0.50; couples to the cohort
  pipeline like the H9b/H10b discriminants. (b) The **on-device `β_i`/`R_i` reveal** in `poc-projection.js` +
  its parity lock. (c) The **real-corpus `counterparty:*` ordering** + **REL-2 inter-rater validity** — the
  ordering is a researcher-imposed value judgment (CV-2), needs human raters (surfaced under "Needs Dave /
  external"). (d) The **MVP-2 far-beings (non-human) bin** — the map reserves bin 6 (`animal-dependent`), the
  fixture exercises 0–5 (design-doc §3 A3).
- **PROPOSED lock (Dave's call — not auto-locked).** *DECISIONS §21 — H11 pre-registration.* Concern read on
  the `circle_radius` secondary axis, binned by `counterparty:*` through the v0.1 distance-ordering map
  (28 tags → 7 bins; power/role + contrast markers excluded per §6 Q4). H11a floor 0.40 on `corr(β_i^odd,
  β_i^even)` (split-half odd/even, seed 20260510+15). H11c directional, lower-CI > 0 (seed +16). `R_i`
  right-censored on a non-declining circle, never made finite (§13.2). Suppression: ≥2 items/bin, ≥4
  bins/shape. Value-neutrality (impartial↔partial, no ranking) is load-bearing, matching R6's charge. H11b
  threshold (R² < 0.50) proposed but not built. The v0.1 ordering itself is proposed pending REL-2. If this
  reads right, say "lock §21" and I'll write it into `DECISIONS.md`.
- **Shipped.** `make check` green (exit 0): validate 66 scenarios + analyzer gate (H2–H7, H9, H10, **H11**,
  probe-ceiling, h9-censoring, h10-suppression, **h11-suppression**) + JS↔Python parity 9/9. Commit on
  `poc` main.

**Buildable-without-Dave work remains** (`build-and-validate.md` items 4+): R2 sacred/protected values
(re-reads the already-tested censored `never`s as the protected set — reuses the censoring machinery), H12
hypocrisy (self–other delta, needs light corpus authoring), R1 identity centrality, R6 conviction. Loop
continues.

---

## Iteration 19 — 2026-06-30 — H10 · Cross-situational moral consistency

`build-and-validate.md` item 2, the next cheapest-clean buildable branch: **H10** (`scoring.md §15`,
design doc `h10-cross-situational-consistency.md`). Not *where* you sit on an axis (already measured)
but how much you **move** across surface contexts — and whether that movement is a stable trait of the
person (Fleeson density-distribution; Mischel if–then signatures; Doris situationism). No new
elicitation: it re-reads the revealed axis scores and bins each item by a `context:*` setting tag.

- **What shipped (`scripts/analyze.py`, `--context-log`).** The §15.1 primitive —
  `context_item_records` → `sd_i(c)` (per-construct cross-context SD of the context-means `r_i(c,k)`) →
  `V_i = mean_c sd_i(c)` (person variability index); **H10a** trait reliability (split each person's
  sessions odd/even, correlate `V_i^odd` vs `V_i^even`, lower bootstrap-CI ≥ 0.40, seed +13); **H10c**
  the observer-effect anchor (`mean(public) − mean(anonymous)`, lower-CI > 0, one-sided, directional,
  seed +14). Gated in `check_analyzer_thresholds.py` (H10 expectations + a `check_h10_suppression()`
  unit-regression) on a self-contained fixture (`analysis/fixtures/sample-context-log.json`,
  12 participants on a 6-level variability ladder, 4 contexts × 2 items × 2 sessions; ground truth
  hand-checked: V-ladder .40→.83, `corr(V_odd,V_even)`=+0.946 CI-low 0.870, mean obs_gap +1.51 CI-low 1.26).
- **Disciplines honored.** *No composite / never-pool* (§13.5): `V_i` is a within-branch mean of
  `sd_i(c)` facets, reported alongside them, never summed with a gap/calibration/CoV index. *Suppression*
  (§1.5 — the H10 analog of the §14.1 censoring lock): a context needs ≥2 items, a construct ≥3 qualifying
  contexts, `V_i` ≥3 qualifying constructs — else omitted, never scored on thin data; locked directly
  against the code in `check_h10_suppression()` (3 assertions, all green). *Value-neutral* — low
  variability = "steadiness", high = "responsiveness", **never ranked** (Dancy particularism caveat:
  context-sensitivity can be a virtue). *N=1* — `sd_i(c)` is on the fixed primary axis, reveal-eligible
  for one user with no cohort norms. *Fraud/replication* — no excluded paradigms touched.
- **Scope (same pattern as H9).** Python-only → **parity trivially green** (poc-projection.js untouched,
  9/9). **Deferred (documented):** (a) **H10b-discriminant** — R² of `V_i` on `[level_i, gap_i,
  cal_error_i]` < 0.50 + the residual-variability de-confound; couples to the H2–H7 cohort pipeline like
  the H9b-discriminant. (b) The **on-device `sd_i(c)` reveal** in `poc-projection.js` + its parity lock.
  (c) The **real-corpus `context:*` tag pass** (design-doc §3 A1) + **REL-2 inter-rater validity** —
  needs human raters (surfaced under "Needs Dave / external").
- **PROPOSED lock (Dave's call — not auto-locked).** *DECISIONS §20 — H10 pre-registration.* Contexts =
  {workplace, family, public, anonymous} read from `context:*`. H10a floor 0.40 (split-half odd/even,
  seed 20260510+13). H10c directional, lower-CI > 0 (seed +14). Suppression: ≥2 items/context,
  ≥3 contexts/construct, ≥3 constructs/`V_i`. Value-neutrality (steadiness↔responsiveness, no ranking)
  is load-bearing, matching R6's charge. H10b thresholds (R² < 0.50 + residual de-confound) proposed but
  not built. If this reads right, say "lock §20" and I'll write it into `DECISIONS.md`.
- **Shipped.** `make check` green (exit 0): validate 66 scenarios + analyzer gate (H2–H7, H9, **H10**,
  probe-ceiling, h9-censoring, **h10-suppression**) + JS↔Python parity 9/9. Commit on `poc` main.

**Buildable-without-Dave work remains** (`build-and-validate.md` items 3+): H11 moral-circle radius
(circle_radius already in projection/parity), R2 sacred values (reuses the censoring machinery), H12
hypocrisy, R1, R6. Loop continues.

---

## Iteration 18 — 2026-06-30 — H9 · Self-prediction calibration (FIRST build-and-validate increment)

The pivot's first *code* increment: the build loop stops designing branches and starts closing
the spec→implementation gap. Target per `build-and-validate.md` item 1: **H9 self-calibration**
(`scoring.md §14`) — not the *size* of your stated↔revealed gap (already measured) but your
*awareness* of it: how well you predict your own revealed choices (self-knowledge vs self-deception;
Epley & Dunning 2000, Loewenstein hot–cold, Tetlock calibration).

- **What shipped (`scripts/analyze.py`, `--predictions` / `--predictions-window-b`).**
  Per-person reveal-eligible indices `cal_bias_i = mean e`, `cal_error_i = mean |e|` (e = pred − rev,
  both scored by the SAME parity-locked `item_score` on the same primary axis — no new scale, so
  N=1-interpretable per §1.5); **H9a** self-enhancement (lower-CI of mean `cal_bias` ≥ 0.10 over the
  three consensual-pole domains; in-group EXCLUDED as value-contested); **H9b-stability** (split-window
  test–retest of `cal_error`, lower-CI ≥ 0.40); **H9c** stakes-blindness (the load-bearing one:
  `blind_i` = high-pool |e| − low-pool |e|, lower-CI > 0 one-sided — the behavioral fingerprint of the
  EV-4 stakes discontinuity); and the **cost-of-virtue channel** in log-dollar units, reported
  convergently and **never pooled** into the axis-unit `blind_i` (§14.7).
- **Disciplines honored.** *Never-pool* (§13.5/§14.7): axis and CoV channels kept on separate scales,
  each reported in its own units. *Censoring* (§14.1 — the H9 analog of the `|8.0|` lock): a `never`
  cost-of-virtue endpoint (predicted OR realized) is **never** priced — `e_price` is suppressed and the
  pair reported categorically only ({both-never}, {predicted-never & acted-finite}, {predicted-finite &
  acted-never}). *No composite* — the facets stand apart, never summed. *Value-neutral* — descriptive,
  both poles dual-read (well-calibrated vs blindsided; neither ranked). *N=1* — pred and rev share a
  pre-defined axis, so the reveal is defensible for one user without cohort norms. *Fraud/replication* —
  no excluded paradigms touched.
- **Gates.** New synthetic fixtures `analysis/fixtures/sample-predictions{,-window-b}.json` (12 synthetic
  participants in 3 miscalibration clusters, single-tag options → exact hand-verifiable ground truth).
  Threshold gate extended: H9 expectations (H9a/H9b-stability/H9c all met=True on the fixtures) **plus a
  `check_h9_censoring()` unit-regression** that asserts directly against the code that no finite `e_price`
  is ever produced across a `never` endpoint (inversion-agnostic; caught even if a fixture later changes).
  Ground truth verified: cohort mean `cal_bias` = 1.111, `cal_error` r(A,B) = 0.968, mean `blind` = 1.067.
- **`types.ts`.** Added `PredictionLogEntry` (append-only, user-keyed, timestamped; axis + cov channels;
  the mandatory §14.6 counterbalanced-reactivity `prediction_withheld` flag) — completes the **DECISIONS
  §19 pending contract** (H9-in-MVP-1 was locked by Dave 2026-06-08; this is a specified downstream, not a
  new lock).
- **Scope kept tight (parity stays trivially green).** Deferred, documented in `build-and-validate.md`:
  (a) **H9b-discriminant** (R² of `cal_error` on `[gap, revealed_level]` < 0.50) — the only part that
  couples to the H2–H7 cohort pipeline; (b) the **on-device JS reveal** in `poc-projection.js` + parity
  lock; (c) the **reactivity-netting** subset design. So this increment is **Python-only** → no
  `poc-projection.js` / `daliu.github.io` change, and `check_impl_parity.py` stays green (9/9) untouched.
- **`make check` = GREEN** (66 scenarios; H2–H7 **unchanged** = zero regression + H9 met; probe-ceiling +
  h9-censoring locks; JS↔Python parity 9/9). Shipped: poc **main** only (no runtime change this increment).

---

## Checkpoint — 2026-06-28 (after iteration 17): design phase CLOSED → pivot to build-and-validate

R6 shipped (iteration 17, below) — the design phase's last branch, per Dave's redirect
("continue into R6, but then build and validate sounds like a good way forward"). The map
now holds ~18 design branches (Round 1's 10 + R1–R6); **R7 (licensing) and R8 (shame-vs-
guilt) are deferred, not dropped** (genuine, bar-clearing candidates for a later design pass).

**Pivot executed.** The loop turns from *designing* branches to *building and validating* what's
specified. Grounding scan of the repo: the engineering already exists and is **green** —
`scripts/analyze.py` (~1600 lines) implements the core validity spine (the stated↔revealed gap,
censoring-aware probes, H2–H7), with JS↔Python parity (`check_impl_parity.py`) against the
on-device runtime projection, a threshold-gate (`check_analyzer_thresholds.py`), 66 valid
scenarios, and CI. `make check` = exit 0. **What's spec-only = every branch the design phase
added (H8–H12, A-series, R1–R6).** Closing that gap is the new backlog → `build-and-validate.md`.

**Loop re-armed:** design cron `8819f3b8` **deleted**; build-and-validate cron **`f67f29c9`**
(7,22,37,52 * * * *, 15-min, session-only, 7-day auto-expire). Mandate: one branch per iteration,
implement scoring in analyze.py (+ the JS projection where it touches the reveal) + fixtures + a
threshold gate, keep `make check` green, honor every discipline, **never push a red state**,
surface IRB / κ / co-PI / real-stakes / runtime-stack decisions to Dave. First build target:
**H9 self-calibration** (scoring §14 — fully specced, N=1, the window-b fixtures already exist).

---

## Iteration 17 — 2026-06-28 — R6 · Moral conviction / metaethical objectivism (design phase's last)

- **Branch.** `r6-moral-conviction.md` — the meta-stance toward your own values: do you hold a
  moral position as an objective **fact** (true for everyone) or as your **own** commitment?
  `objectivism_i` / `conviction_i`. A **stated anchor** (the Goodwin & Darley objectivism probe:
  fact-vs-opinion + the disagreement-resolution follow-up) + **revealed signatures** (tolerance/
  compromise toward divergent others; objectivist-vs-subjectivist moral language, A3, κ-gated) —
  held apart, never pooled (§13.5).
- **Grounding.** Skitka 2010 (moral conviction — already enters via Hofmann 2014); Goodwin &
  Darley 2008 (metaethical objectivism). Both well-replicated; takes **no** position on moral
  realism itself.
- **Distinctness (R6b, load-bearing).** Not value-content (inventory), not tradeability (R2
  sacredness — the key discriminant pair: *epistemic status ≠ tradeoff resistance*, they
  dissociate), not centrality (R1). R6c lifts the stated-vs-revealed logic to the **meta-layer**:
  the professed relativist who acts with absolute conviction; the professed absolutist who lives
  and lets live.
- **Honesty.** Heavy, charged behavioral payload (conviction predicts intolerance / refusal to
  compromise / any-means acceptance) → value-neutrality binds with **extra force**: descriptive-
  only, both poles dual-read (objectivism = clarity *or* rigidity; subjectivism = pluralism *or*
  won't-stand-for-anything). Censoring preserved (compromise-refusal stays censored, not priced).
- **Card.** Yes — "Facts or your own / Are your morals true for everyone, or true for you?"
  (design-stage). Manifest → 14 cards.
- **Shipped.** poc `9b177ad` (r6 doc + map R6✓ + Round-3/pivot notes + research-program.json).
  Site regenerated 13→14, `--check` green, R6 link 200, daliu `3344b20` (master). scoring §31 +
  DECISIONS entry proposed (pending Dave's lock).

---

## Checkpoint — 2026-06-28 (after iteration 16): planned roadmap complete, Round 3 opened (not exhausted)

Both planned rounds of `measurement-avenues.md` are now drafted: Round 1 (10 items,
H10/H12/H11/H-A1 · H-A2 · H-A3 · C1 · A4/A5 · B4 · C2) and Round 2 (R1–R5). ~17
measurement branches exist.

**Honest status (the important part).** The *marginal* value of one more design doc
has genuinely fallen — the binding constraint is now **build-and-validate** (co-PI,
IRB, multi-user runtime, the κ-validation that ungates the language channel), not
design. **But** a disciplined re-scan of the literature still surfaces genuinely
distinct, validated, measurable constructs the map does not cover, so this is **not**
the loop's stop condition ("genuinely run out of novel, rigorous branches"). Opening
**Round 3**, held to a strictly higher bar (distinct from all ~17 AND validated AND
measurable here):

- **R6. Moral conviction / metaethical objectivism** (Skitka 2010; Goodwin & Darley
  2008) — do you hold a moral position as an objective *fact* or a *preference*? The
  meta-stance toward one's own values; distinct from content (inventory), tradeability
  (R2), centrality (R1). Predicts intolerance of dissent / refusal to compromise /
  any-means acceptance. **HIGH — next iteration.**
- **R7. Moral self-regulation dynamics (licensing)** (Blanken/van de Ven/Zeelenberg
  2015 meta, d≈0.31) — within-sequence: does a virtuous choice at *t* raise the odds
  of a lapse at *t+1*? Distinct from B4's slow drift; the choice stream already exists.
  Replication discipline load-bearing: license only the surviving *licensing* half;
  exclude/caveat the "Macbeth-effect" *cleansing* (Earp et al. 2014 failure). **MEDIUM.**
- **R8. Shame- vs guilt-proneness** (Tangney et al. 2007) — the *form* of moral emotion
  (guilt→repair vs. shame→withdraw) vs. A5's *magnitude*. Overlaps A5 — flagged for a
  discriminant check first; fold in if it doesn't cleanly stand apart. **LOW.**

If a future scan yields nothing that clears this bar, *that* is the genuine stop.
Corrected the premature "flag-and-stop, exhausted" note that had conflated
"planned roadmap done" with "no rigorous branches remain." Loop cron `8819f3b8`
(15-min, session-only) continues into R6 on its next fire unless redirected.

---

## Iteration 16 — 2026-06-28 — R5 · Moral typecasting / dyadic structure (Round 2's last)

- **Branch.** `r5-moral-typecasting.md` — how a person *parses* a moral scene into the
  **agent** (the doer: responsibility, intent, blame) vs. the **patient** (the done-to:
  harm, suffering, need): `dyadic_emphasis = agent_focus − patient_focus`, a justice-vs-
  care emphasis. R5a reliable dyadic emphasis; R5b harm-centrality (do you need a victim
  to moralize?); R5c typecasting (agent XOR patient — exploratory, needs dedicated items).
- **Grounding.** Gray & Wegner 2009 (typecasting); Schein & Gray 2018 (Theory of Dyadic
  Morality); Gilligan 1982 (the care/justice *emphasis* — explicitly not the discredited
  gender claims; already a repo reference).
- **Honesty (load-bearing).** The **weakest operationalization on the map** — detection is
  indirect (κ-gated A3 agent/patient language + inferential intent-vs-harm choice-weighting);
  R5c's clean probe needs role-assignment items the corpus lacks. Reported **exploratory**;
  R5a's reliability is itself contingent on the indirect channels carrying signal (a pilot
  question). Value-neutral (justice/care, neither better). Names exactly the dedicated items
  that would measure it cleanly — closes the map by marking where the next real work is, not
  by overclaiming.
- **Card.** Yes — "Doer or done-to / Whose side of a moral scene do you see first?"
  (design-stage, exploratory). Manifest → 13 cards.
- **Shipped.** poc `86a1fd2` (r5 doc + map R5✓ + research-program.json). Site regenerated
  12→13 cards, `--check` green, R5 link 200, daliu `3fa5d70` (master). DECISIONS entry
  proposed (pending Dave's lock), not auto-locked.

## Iteration 15 — 2026-06-28 — R4 · Moral attentiveness (do you even notice?)

- **Branch.** `r4-moral-attentiveness.md` — Reynolds 2008 moral attentiveness as the
  **perceptual front-end**: `perceptual_i` (do you *see* the ethical dimension?) and
  `reflective_i` (do you *think* about ethics?). The trait-level version of Rest's (1986)
  component-1 *moral sensitivity* — the construct upstream of every other branch (you can't
  show a cost-of-virtue, an A5 pull, or an R3 disengagement on stakes you never perceived).
- **Grounding.** Reynolds 2008 (JAP); Rest 1986 (four-component model); Gantman & Van Bavel
  2014 (the "moral pop-out" effect → the non-reactive incidental-salience read).
- **Honesty (load-bearing).** The **reactivity problem** is the central methodological burden:
  asking "is this a moral situation?" *manufactures* the attention it measures, so R4 uses
  **non-reactive** channels primarily (spontaneous moral-framing *rate* in the A3 corpus —
  distinct from A3's *content*; incidental moral salience) and treats any dedicated probe as
  reactive + educational, never primary. Value-neutral with **extra-force scrupulosity
  guardrails** at the high end (high attention = perceptiveness *or* over-moralizing). R4b: the
  upstream gate, discriminant from value-importance and from R1 centrality (the four corners,
  incl. low-attentive/high-central "well-meaning-but-oblivious").
- **Card.** Yes — "Moral attention / Do you see the moral dimension, or walk past it?"
  (design-stage). Manifest → 12 cards.
- **Shipped.** poc + site (12-card grid) committed/pushed earlier this session. DECISIONS entry
  proposed (pending Dave's lock).

---

*Earlier iterations (1–14) are logged in the vault note; this sidecar begins at 15, the
point the vault became iCloud-gated.*
