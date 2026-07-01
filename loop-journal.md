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
