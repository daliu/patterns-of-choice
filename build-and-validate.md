# Build & validate — the implementation roadmap

**Purpose.** The design phase is closed (Dave, 2026-06-28): ~18 measurement branches are specified (Round 1's 10 + R1–R6 in [`measurement-avenues.md`](measurement-avenues.md)). This file is the **build loop's backlog** — the implementation analog of `measurement-avenues.md` — driving the re-aimed cron loop from *designing* branches to *building and validating* them. One branch per iteration, same disciplines, `make check` stays green.

## Current state (green baseline, 2026-06-28)
`make check` passes (exit 0):
- **Corpus:** 66 scenarios + arcs valid (`scripts/validate.py`).
- **Analyzer (`scripts/analyze.py`, ~1600 lines):** the **core validity spine** is implemented and threshold-gated on synthetic fixtures — the stated↔revealed **gap** (`compute_gaps`), session aggregates + bootstrap CIs, Bradley–Terry pairwise, card-sort, the **censoring-aware** break-point probe scores, and validity hypotheses **H2–H7** (convergent / discriminant validity, stated–revealed correlation, test–retest of revealed + probes, informant validity).
- **Parity:** the JS on-device projection (`daliu.github.io/patterns-of-choice/runtime/poc-projection.js`) == the Python analyzer (`scripts/check_impl_parity.py`) — `itemScore` agrees on all cases incl. secondary-axis exclusion; the censoring locks hold (`never`-on-$10M scores |8.0|, not the old buggy |5.0|).
- **CI:** `.github/workflows/{analyze,validate}.yml` gate the analyzer + corpus on push/PR.

**What's implemented = the core validity spine (H2–H7), plus H9 self-calibration (partial — see item 1 for the deferred discriminant + JS reveal). What's spec-only = the remaining measurement branches (H8, H10–H12, the A-series, R1–R6).** That gap is this backlog.

## The build backlog (spec → implementation), priority order
Cheapest-clean and most-machinery-reusing first. Each item: implement scoring in `analyze.py` (+ the JS projection if it touches the on-device reveal) → synthetic fixture(s) with known ground truth → a threshold gate in `check_analyzer_thresholds.py` → keep parity + disciplines → `make check` green → commit/push → journal.

1. **H9 — self-calibration (`scoring.md §14`).** ✅ **BUILT (partial), 2026-06-30.** Person indices (`cal_bias_i`, `cal_error_i`, axis channel, N=1 reveal-eligible), **H9a** self-enhancement, **H9b-stability** (split-window test–retest of `cal_error`), **H9c** stakes-blindness (the load-bearing signature), and the cost-of-virtue channel with the **§14.1 censoring lock** are implemented in `analyze.py` (`--predictions` / `--predictions-window-b`), gated in `check_analyzer_thresholds.py` (H9 threshold expectations + a `check_h9_censoring()` unit-regression asserting no finite `e_price` across a `never` endpoint — the H9 analog of the `|8.0|` lock), on self-contained synthetic fixtures (`analysis/fixtures/sample-predictions*.json`, 12 synthetic participants, known ground truth). Axis and cost-of-virtue channels never pooled (§14.7). `PredictionLogEntry` added to `types.ts` (completes the DECISIONS §19 pending contract). **Deferred (documented, next increment):** (a) **H9b-discriminant** (R² of `cal_error` on `[gap_i, revealed_level_i]` < 0.50) — it couples to the H2–H7 cohort pipeline, whereas this increment stays isolated on its own fixtures; (b) the **on-device JS reveal** in `poc-projection.js` + its parity lock (so this increment is Python-only and parity stays trivially green); (c) the **reactivity-netting** counterbalanced no-prediction subset (§14.6) — needs the counterbalancing-schedule design (`prediction_withheld` flag is in the type, unused so far).
2. **H10 — cross-situational consistency.** N=1; no new elicitation; reuses session aggregates (within-person variance across settings as its own trait). Clean.
3. **H11 — moral-circle radius.** The `circle_radius` secondary axis **already exists** in the projection + parity locks; implement the concern-falloff-by-distance read on top. Partially scaffolded.
4. **R2 — sacred / protected values.** Re-reads the already-implemented, already-tested censored `never`s as the protected set; quantity-insensitivity + a taboo marker. High value, reuses the censoring machinery.
5. **H12 — moral hypocrisy.** Self–other delta; needs judge-other framings in the corpus (light authoring) + the paired scoring.
6. **R1 — moral identity centrality.** The meta-moderator; needs a centrality read; moderates the §6 gap / H10–H12.
7. **R6 — moral conviction / objectivism.** Clean stated probe (Goodwin & Darley) + revealed tolerance/compromise/language; the stated–revealed meta-gap.
8. **A3 + R3/R4/R5 (language-derived).** All gated on the **κ≥0.70 inter-rater validation** of the language coder — see "Needs Dave / external". Build the coder + the κ-computation + a synthetic parity test *now*; the *real* κ needs human raters.
9. **A4/A5 — process + emotion.** Exploratory; high-noise; tight gates.
10. **B4 — value-change dynamics; C1 — MTMM capstone; C2 — stress.** Sequencing-gated (need ≥3 channels / longitudinal data); build the analysis layer once the channels exist.

(The loop confirms "next cheapest-clean buildable" each iteration by reading the spec, exactly as the design loop did with `measurement-avenues.md`. R7/R8 remain deferred *design* items, not build items.)

## Disciplines every build increment owes (non-negotiable)
- **Unit / never-pool (§13.5):** no forced common scale; the analyzer must not pool across scales (the parity gate already locks secondary-axis exclusion — extend, don't violate).
- **Censoring (§13.2):** `never` cost-of-virtue responses stay right-censored; never made finite (the |8.0| lock is the pattern).
- **No composite score:** never sum a branch's sub-indices into one number; report the facets.
- **Value-neutral / descriptive-only:** the reveal names where you sit; it never ranks. (Extra force for the charged branch, R6.)
- **N=1 interpretability:** the within-person reveal must be defensible for a single user, not just cohort-level.
- **Fraud / non-replication exclusions:** no Stapel / Gino / Ariely-priming / ego-depletion; R7's licensing (if/when built) scoped to the surviving half — no Macbeth cleansing.

## Guardrails for the autonomous build loop
- **Never commit or push a red state.** Run `make check` before every commit; if red, fix or revert — never push broken. (The design loop pushed prose; this loop pushes code to a public repo + a live runtime — the bar is higher.)
- **Keep JS↔Python parity.** Anything touching the on-device reveal changes **both** `analyze.py` and `poc-projection.js`, and `check_impl_parity.py` must stay green.
- **Synthetic data only.** Fixtures with known ground truth; no real human data.
- **Propose, don't lock.** Pre-registration decisions are proposed for Dave's lock, never auto-locked (same as the design loop).
- **One branch per iteration; stop when dry.** If a scan finds no buildable-without-Dave branch left, journal it and halt — don't pad.

## Needs Dave / external (not buildable by the loop — surface, don't guess)
- **IRB + co-PI + real participants** — the whole real-cohort validation.
- **Real κ inter-rater validation** of the language coder (A3 / R3 / R4 / R5) — the loop can build the coder + κ-computation + a synthetic test, but the *real* κ≥0.70 that ungates the language channel needs human raters.
- **A2 real-stakes channel** — consequential real stakes (the EV-3/EV-4 keystone) need real money/consequences + IRB; Phase-2, cohort.
- **Runtime hosting / stack / multi-user architecture** decisions (`DECISIONS.md §18` left the runtime line open) — propose options, let Dave choose.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) — the design backlog this implements (R7/R8 deferred there)
- [`scoring.md`](scoring.md) — the math each increment turns into code (§13.2 censoring, §13.5 unit, §14 H9, §20 language, §29–§31 R4/R5/R6)
- `scripts/analyze.py` (validation-cohort scorer) · `daliu.github.io/patterns-of-choice/runtime/poc-projection.js` (on-device scorer) · `scripts/check_impl_parity.py` (parity gate) · `scripts/check_analyzer_thresholds.py` (regression gate)
- [`DECISIONS.md`](DECISIONS.md) §14/§18 (engineering + runtime lines), §16/§17 (corpus) · [`loop-journal.md`](loop-journal.md) (the build loop's iteration log)
