# H11 — Moral-circle radius (the reach of concern)

**Status:** Design proposal, drafted 2026-06-12 (extension loop, iteration 5). Develops branch **B2** of [`measurement-avenues.md`](measurement-avenues.md). Source for downstream changes to `concept.md`, `pre-registration.md`, `scoring.md`, `DECISIONS.md`. Mirrors [`h8`](h8-narrative-immersion-design.md)/[`h9`](h9-self-calibration.md)/[`h10`](h10-cross-situational-consistency.md)/[`h12`](h12-moral-hypocrisy.md). **MVP-1 secondary** for the human+animal circle (re-analysis, no new scenarios); the full circle (future beings) is MVP-2. The lock is Dave's call.

**Provenance.** Branch B2. The in-group/out-group domain already scores a `circle_radius` secondary axis (`scoring.md` §2.3), and the corpus already carries a dense recipient-distance gradient — `counterparty:*` tags spanning kin / family-of-origin / child → peer / community / in-group → senior / subordinate → stranger / anonymous → out-group / foreign → **animal-dependent**, plus explicit within-item distance contrasts (`near-vs-far`, `family-vs-stranger`, `local-vs-global`). H11 promotes that latent axis into a named construct: the **radius of the moral circle** — how far out a person's concern reaches — measured from revealed choices and tracked over time. Peter Singer's "expanding circle" made behavioral and longitudinal.

---

## 1. The hypothesis statement

**H11 (proposed `pre-registration.md` §6, secondary).**

*The shape of a person's moral circle — how their revealed concern declines with the recipient's social/moral distance, and how far out it still extends — is a reliable individual difference, distinct from how generous they are overall; and concern reliably declines with distance (the parochial gradient is behaviorally real).*

### 1.1 Measurement primitive (a distance-axis break point)

For person *i* and recipient-distance bin *d* (ordered: kin → friends → community/in-group → acquaintance → strangers → out-group/foreign → non-human; future beings = MVP-2), let `concern_i(d)` be the mean `circle_radius`-axis revealed score (`scoring.md` §2.3; + = inclusion/hospitality, − = boundary) over in-group-domain items whose `counterparty:*` tag falls in bin *d*. The tag→bin ordering is a declared, versioned map (§3), with the **researcher-imposed-ordering caveat** of §1.5.

Two within-person summaries:
```
β_i = slope of concern_i(d) on distance d           # parochialism steepness: concern lost per distance step
R_i = the distance at which concern_i(d) crosses the person's own midpoint
      (½ between their nearest-bin concern and the axis floor); RIGHT-CENSORED if it never crosses
```

`R_i` is the **moral-circle radius**, and it is the **distance-axis analog of the cost-of-virtue break point** (§4): cost-of-virtue asks *"at what stake does virtue break?"*; `R_i` asks *"at what distance does concern break?"* Both are break points; both are **right-censored when they never break** — the fully impartial person whose concern never declines has a circle extending past the furthest bin tested, exactly as a `never`-sell cost-of-virtue is `price > ladder top`. Censoring discipline is inherited verbatim from §13.2: **a censored `R_i` is never made finite.**

### 1.2 H11a — circle shape is a reliable individual difference

Split-window test–retest of `R_i` and `β_i`: lower 95% bootstrap-CI bound ≥ **0.40** (the revealed-behavior analog of the Moral Expansiveness Scale's reliability). Bootstrap per `scoring.md` §8, seed `20260510`.

### 1.3 H11b — circle shape is distinct from generosity level (load-bearing)

Reach is not height. A person can be lavish to kin and drop off a cliff (narrow), or modest but flat (wide). Regress the shape (`β_i`, and `R_i`) on `[ concern at the nearest bin , resource-allocation generosity level (§3.2) ]`; criterion: **upper** 95% CI of model R² **< 0.50** — at least half the circle-shape variance is unexplained by how generous the person is at baseline. Without H11b, "wide circle" is just "nice person" relabeled. Anchor: Crimston et al. 2016 (MES dissociable from agreeableness/generosity).

### 1.4 H11c — the parochial gradient is behaviorally real (directional anchor)

Concern declines with distance:
```
H11c:  across participants, mean concern_i(near) − mean concern_i(far) > 0,  lower 95% CI > 0  (one-sided)
```
Cleanest via the **within-item distance-contrast items** (`near-vs-far`, `family-vs-stranger`, `local-vs-global`), which hold the scenario fixed and vary only distance. This validates the distance ordering as behaviorally real (not researcher fiat) and confirms `R_i`/`β_i` measure where a *real* gradient terminates. Anchor: Cikara & Bruneau parochial empathy (already anchors the in-group domain).

### 1.5 N=1, value-neutrality, the ordering caveat, censoring

- **N=1.** `concern_i(d)`, `R_i`, `β_i` are within-person on the fixed `circle_radius` axis + the distance ordering — reveal-eligible (descriptive: "your concern stays strong out to strangers, then drops sharply at out-group," or "your circle is flat and wide"). The H11a/b/c statistics are cohort, separate from the reveal.
- **Value-neutrality (load-bearing).** A *wider* circle is **not** scored as better. Impartialist ethics (Singer) prizes width; partialist / communitarian / role-ethics traditions (Williams; the MacIntyre & Confucian challenge already named in `concept.md`'s smuggled-values section) hold that special obligations to the near are morally *appropriate* — favoring your own child is not a defect. Waytz et al. 2019 (Nature Communications) show circle *shape* (more-concentric vs flatter-wide) is **ideologically patterned**, a real individual difference rather than a vice. The reveal describes the shape; it never ranks width.
- **The distance ordering is researcher-imposed (CV-2-class smuggled values).** Which entities are "closer" is culturally variable (collectivist/honor cultures order differently; is "community" nearer than "friend"? are senior/subordinate a *distance* or a *power* axis — see §6 Q4?). The ordering map is versioned and open; `R_i` is interpretable *relative to it*; cross-cultural radius comparison requires measurement-invariance testing (Atari 2023, already cited).
- **Censoring + suppression.** Flat/impartial → `R_i` right-censored ("reaches past the furthest bin"), never finite. A bin contributes only with ≥2 informative items; `R_i`/`β_i` suppressed below ≥4 ordered bins populated.

### 1.6 Falsification and exploratory H11d

Combined H11 = **H11a ∧ H11b** (a reliable circle-shape distinct from generosity). H11c is the directional anchor. Partial results published.

**Exploratory H11d.** (a) *Trajectory* — does `R_i` widen or narrow over the protocol (Singer's expanding circle vs. threat-driven contraction)? The **Marisol circle-widening arc** (`scenarios/arcs/arc-marisol.json`) is the in-instrument substrate. (b) *Cross-links* — does `R_i` track the cost-of-virtue break points (a "strength-of-conviction" common factor: do people who hold virtue under high stakes also extend concern far)? Is the circle context-stable (H10)? Does out-group distance interact with the H12 double standard (in-group hypocrisy: a stricter standard demanded of the far than the near)?

---

## 2. Theoretical grounding

- **Singer, *The Expanding Circle* (1981).** The thesis that moral concern has a boundary that can expand outward (kin → community → humanity → sentient life) — the construct H11 measures as a radius.
- **Crimston, Bain, Hornsey & Bastian 2016 (JPSP), the Moral Expansiveness Scale.** The validated self-report instrument for the extent of the moral world; reliable, and dissociable from generic prosociality — the anchor for H11a (reliability) and H11b (distinct from generosity). H11's contribution is the **revealed + longitudinal** version.
- **Waytz, Iyer, Young, Haidt & Graham 2019 (Nature Communications).** Circle *shape* differs ideologically (relatively concentric vs. relatively flat-and-wide) — establishing circle shape as a substantive individual difference and reinforcing the value-neutrality constraint (§1.5).
- **Cikara & Bruneau (parochial empathy).** The behavioral gradient — concern falls for more distant targets — that H11c confirms and that licenses treating distance as an axis. Already cited in-repo.
- **Partialism (Williams; MacIntyre/Confucian role-ethics).** The standing philosophical case that a bounded circle can be *correct*, not deficient — why H11 must stay descriptive.

---

## 3. Instrument modification required

### Already in place (the reason H11 is mostly re-analysis)
- **A dense recipient-distance gradient** — ~35 `counterparty:*` tags from `close`/`family-of-origin`/`child` out to `stranger`/`anonymous`/`out-group-new`/`stranger-foreign` and even `animal-dependent`.
- **Within-item distance-contrast items** (`near-vs-far`, `family-vs-stranger`, `local-vs-global`, `close-distant`) — the clean H11c tests.
- **The `circle_radius` secondary axis** (`scoring.md` §2.3) already scoring in-group items.
- **The Marisol circle-widening arc** for the H11d trajectory.

### What needs to be added
- **A1. A distance-ordering map (no new scenarios).** A declared, versioned artifact mapping the ~35 `counterparty:*` tags → ordered distance bins (parallel to the tag-axis map), with the §1.5 cultural caveat and an inter-rater check on the ordering (REL-2-style). This is the one real authoring task — a *grouping/ordering* pass over existing tags, not new content.
- **A2. Scoring `§18` (proposed).** `concern_i(d)`, `β_i`, `R_i` (with the §13.2 censoring), the H11a/b/c statistics, suppression. Parity-gated (`make check`).
- **A3. (MVP-2) The far circle.** Future beings / non-present generations live in the **intergenerational domain excluded from MVP-1** (`DECISIONS.md` §3). Extending the radius to that bin is an MVP-2 corpus addition; the human+animal circle is complete in MVP-1.

### Promotes an existing axis
The `circle_radius` axis is currently an *exploratory secondary* (§2.3). H11 promotes it to a named, falsifiable hypothesis — no schema change, just a scoring section + the ordering map.

---

## 4. Implications for existing locked decisions

**MVP-1 re-analysis; corpus untouched.** Like H10, the human+animal circle needs no new scenarios — only the distance-ordering map + scoring §18. `DECISIONS.md` §16/§17 hold. (Contrast H12, which needed a §16-unlock for new items.)

**The far bin is MVP-2.** Per `DECISIONS.md` §3 the intergenerational/future-others domain is out of MVP-1; the radius therefore terminates at the non-human-animal bin in MVP-1 and extends to future beings only when that domain enters (MVP-2). Stated as a bounded claim, not a gap.

**Proposed `DECISIONS.md` entry (pending Dave's lock).** "Add H11 (moral-circle radius) as an MVP-1 secondary; promote the `circle_radius` axis (§2.3) to a named hypothesis; add a versioned counterparty→distance-bin ordering map + scoring §18; no new scenarios (human+animal circle); future-beings bin deferred to MVP-2." Considered-and-rejected: a self-report MES bolt-on (rejected — that's the stated channel; H11's whole point is the *revealed* circle); grading wider = healthier (rejected — §1.5 value-neutrality).

---

## 5. Why this is a research contribution

The Moral Expansiveness Scale is a one-shot self-report; H11 makes the moral circle **revealed** (from behavioral tradeoffs across recipient distance, not self-rating) and **longitudinal** (does the circle widen or contract over weeks — H11d). It introduces the **reach-vs-height** distinction (circle shape ≠ generosity level, H11b) that self-report rarely separates, and it operationalizes the cost-of-virtue/distance parallel — concern has a *break point* over distance just as virtue has one over stakes, censoring and all. The ideological circle-shape finding (Waytz et al.) becomes a behavioral, within-person, trackable quantity.

---

## 6. Open design questions

- **Q1. Bin granularity.** Collapse the ~35 tags to ~6–7 ordered bins (stable estimates, coarse radius) or keep finer (precise gradient, sparse bins)? Provisional ~7; pilot informs.
- **Q2. Cultural validity of the ordering.** The single hardest issue — the distance ordering encodes a (WEIRD) social structure. Offer alternative orderings (e.g., a collectivist preset) and report radius only *within* an ordering, never cross-ordering without invariance testing.
- **Q3. Censoring the impartial.** What fraction of participants are flat (right-censored `R_i`)? If most, the radius has a ceiling problem and `β_i` (slope) becomes the primary read. Pilot check.
- **Q4. Distance vs. power.** `senior`/`subordinate`/`business` counterparties confound social *distance* with *power/role*. Either exclude them from the distance ladder or model power as a separate axis; do not let a power effect masquerade as circle radius.

---

## 7. Downstream changes this design unblocks
1. `analysis/` — a versioned `counterparty→distance-bin` ordering map (+ inter-rater check)
2. `scoring.md §18` — `concern_i(d)`, `β_i`, `R_i` (censoring-aware), H11a/b/c; parity-gated
3. `pre-registration.md` §6 (H11 secondary) + §5 (the distance-gradient analysis plan)
4. `concept.md` — promote `circle_radius` from exploratory-secondary to a named construct; the value-neutrality + cultural-ordering notes
5. `scenarios/` (MVP-2) — the future-beings far-circle items, when the intergenerational domain enters
6. `DECISIONS.md` — the H11 lock (Dave's call)
7. `validity-threats.md` — a CV row for the distance-ordering-encodes-values risk (Q2) and the distance/power confound (Q4)

---

## 8. Relationship to the in-group domain, cost-of-virtue, H10, and H12
- **Deepens in-group/out-group.** Promotes the `circle_radius` secondary axis (§2.3) into a hypothesis; the loyalty axis is *who's inside*, the radius is *how far inside reaches*.
- **The cost-of-virtue parallel.** `R_i` is a break point on the distance axis as the cost-of-virtue break point is on the stakes axis — same censoring, same N=1 price-like reading. A unifying shape across two of the instrument's probes.
- **vs H10.** Exploratory: is the circle radius itself context-stable, or does it contract in some settings (a "situational circle")? (H10 × H11.)
- **vs H12.** Out-group distance × the self–other double standard: do people demand a stricter standard of the far than the near (distance-graded hypocrisy)?
- **Conversation echo.** The moral-systems thread argued *"shrink the unit"* for trust and governance; the moral circle is the orthogonal axis — how far *concern* (not trust) extends. Resonant, not identical: you can keep decisions local (small trust unit) while holding a wide circle of concern.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) B2; [`scoring.md`](scoring.md) §2.3 (`circle_radius`), §4 + §13.2 (the break-point/censoring machinery `R_i` reuses), §3.2 (generosity level for H11b)
- [`concept.md`](concept.md) (in-group gradient; the smuggled-values / MacIntyre–Confucian note the value-neutrality leans on), [`DECISIONS.md`](DECISIONS.md) §3 (excluded intergenerational domain → the MVP-2 far bin), §16/§17 (corpus untouched)
- [`h10-cross-situational-consistency.md`](h10-cross-situational-consistency.md), [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md) (the §8 cross-tests), [`validity-threats.md`](validity-threats.md) (ordering-encodes-values + distance/power rows), [`pre-registration.md`](pre-registration.md) §6
