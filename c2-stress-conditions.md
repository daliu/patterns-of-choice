# C2 — Adversarial / stress conditions (the cheap hot-state proxy)

**Status:** Design proposal, drafted 2026-06-23 (extension loop, iteration 11). Develops branch **C2** of [`measurement-avenues.md`](measurement-avenues.md) — the map's last and **most theoretically fragile** item, so this spec is deliberately short and the rigor is mostly in what it *refuses* to claim. **Phase-2, exploratory, valid only on convergence (§1.3).** No public card. The lock is Dave's.

**Provenance.** Branch C2. EV-4 says the under-pressure ("hot-state") self can differ categorically from the calm app self, and H-A2 (real-stakes) probes it the gold-standard but expensive way. C2 asks whether a **cheap, induced** stressor — mild **time pressure** — can approximate that shift without real consequences. The honest answer is *only if it converges with the real thing*; C2 exists to test that, not to assume it.

---

## 1. The hypothesis statement

**C2 (proposed `pre-registration.md` §6, exploratory; Phase-2).**

*A within-construct time-pressure manipulation produces a reliable behavioral shift; and that shift converges with the real-stakes bend (H-A2b) and the self-report stakes-blindness (H9c) — making induced stress a cheap, validated proxy for the under-pressure self. If it does not converge, C2 measures only stress-reactivity, not the hot-state self, and is demoted accordingly.*

### 1.1 Measurement primitive (lean on time pressure, not load)
For person *i*, construct *d*: the **stress-shift** is the change in revealed score between a **tight-timer** and an **untimed** presentation of structurally-matched items:
```
shift_i(d) = revealed_i(d | tight timer) − revealed_i(d | untimed)
```
**Time pressure, not cognitive load.** The quick-fire timer (8 s, `validity-threats.md` CV-1) is *already* a mild, native time-pressure; C2 generalizes it to a within-construct timed/untimed contrast. It deliberately **avoids cognitive-load manipulations** (hold-a-number-while-deciding): those are aversive and lab-artificial in a daily contemplative practice, and load-as-mechanism rests on discredited ground (§1.4). No mechanism is asserted — `shift` is a descriptive behavioral difference, full stop.

### 1.2 C2a — the stress-shift is a reliable individual difference
Split-window test–retest of `shift_i(d)` ≥ **0.40** (some people shift under pressure, some don't). Descriptive only — *not* "load makes you deontological/selfish-by-mechanism."

### 1.3 C2b — the convergence test (C2's entire reason to exist)
Does the cheap induced shift track the expensive real thing?
```
C2b:  corr( shift_i [C2], bend_i [H-A2b real-stakes] ) > 0   AND   corr( shift_i, blind_i [H9c] ) > 0
      (lower 95% CI > 0)
```
- **Converges** → induced stress is a *validated cheap proxy* for the under-pressure self: a third, inexpensive leg of the EV-4 triangle (real-stakes H-A2 · self-report H9c · induced-stress C2), usable where real stakes are too costly.
- **Does not converge** → stress ≠ stakes; C2 is **demoted** to "time-pressure reactivity" (still a minor signal, but *not* a window on the hot-state self). Either result is reported; the demotion is the honest default.

### 1.4 What C2 explicitly does NOT claim (the load-bearing honesty)
- **No dual-process framework mapping.** Slower/faster or stressed/calm does *not* map to deontological/utilitarian — the Greene-style mapping doesn't hold (Bago & De Neys 2019, already disclaimed in `concept.md`). Greene et al. 2008 is cited only as the modest "load perturbs moral choice" precedent, not a mechanism.
- **No ego-depletion.** The "stress drains self-control" mechanism is **excluded**: the multilab Registered Replication Report (Hagger et al. 2016) failed to replicate ego-depletion. C2 must not assume it — same post-replication-crisis discipline the repo applies to Stapel, Gino, and the Mazar/Ariely priming task.
- C2 is therefore *purely* a descriptive shift (C2a) plus a convergence test (C2b). That narrow claim is all the fragile literature can bear.

### 1.5 Ethics (load-bearing — measurement must not harm)
Inducing stress to measure is ethically loaded. Mitigations are mandatory: **mild** time pressure only (no aversive load, no failure framing); bounded and infrequent; the scrupulosity/anxiety guardrails (`concept.md` §"Risks to vulnerable users") apply with extra force (distress detection, "take a break," opt-out); and the manipulation is disclosed/debriefed. A stress condition that could harm a vulnerable user is not worth a noisy proxy signal — if it can't be made gentle, it isn't built.

### 1.6 N=1, no card, falsification
The per-person `shift` is within-person but **fragile and not reveal-worthy on its own** (it's a validity probe, not a self-knowledge facet) — so **no `research-program.json` card** (like C1 and A4). Cohort-level for C2b. Falsification: C2b failing *is* the expected-and-fine outcome (stress ≠ stakes) — C2 is the rare branch whose null result is as informative as its positive one, and whose positive result is contingent on an expensive channel (H-A2) existing to validate against.

---

## 2. Theoretical grounding (thin, by nature)
- **Greene et al. 2008; Suter & Hertwig 2011.** Time pressure / load *perturbs* moral choice — the modest descriptive precedent for C2a. Cited for the perturbation, not a dual-process interpretation.
- **Bago & De Neys 2019.** Why no framework mapping (the disclaimer C2 honors).
- **Hagger et al. 2016 (RRR).** Why no ego-depletion mechanism (the exclusion).
- **Loewenstein hot–cold empathy gap (already in H9 §2.2); EV-4; H-A2; H9c.** The under-pressure-self construct C2 cheaply approximates and is validated against. C2 is subordinate to H-A2 as the gold standard.

## 3. Instrument modification required
- **A1.** Within-construct **timed/untimed matched items** (a runtime timer-condition flag on existing items, or a small set of timed/untimed twins — light, like the H8 pairs). The native 8 s quick-fire timer is the starting point.
- **A2.** A **manipulation check** (did the timer actually raise felt pressure? — without it, a null C2b is uninterpretable: failed manipulation vs. stress≠stakes).
- **A3.** Scoring `§25` (proposed): `shift_i`, C2a/b, the manipulation-check gate. Parity-gated.
- **Gated on H-A2** (the convergence target) → Phase-2. No new scenarios beyond the optional timed/untimed twins.

## 4. Implications for existing locked decisions
**Phase-2, exploratory, no card, the most contingent branch.** Reuses the timer construct; needs H-A2 for C2b. **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add C2 (stress conditions) as a Phase-2 exploratory probe; within-construct time-pressure shift (scoring §25) + a manipulation check; validity hinges on C2b convergence with H-A2b/H9c; no mechanism claims (no dual-process, no ego-depletion); no card; gentle-only per §1.5." Considered-and-rejected: cognitive-load manipulations (rejected — aversive + discredited mechanism); any depletion/dual-process interpretation (rejected — Hagger 2016 / Bago & De Neys); a public card (rejected — fragile validity probe, not a facet).

## 5. Why this is a (modest) contribution
C2 is a **cheap third leg of the EV-4 triangle** — and it's honest enough to **demote itself** if the cheap and expensive measures disagree. Its value is conditional and bounded, and the design says so up front: a noisy proxy that earns its place only by convergence, never by assumption.

## 6. Open design questions
- **Q1.** Timer tightness that raises pressure without pushing everyone to timeout (and the CV-1 interaction with the existing 8 s timer).
- **Q2.** Manipulation check that doesn't itself moralize/stress.
- **Q3.** Ethics bounds — how mild is mild enough; the distress-detection threshold.
- **Q4.** If C2b converges, can C2 *substitute* for H-A2 where real stakes are infeasible — and how much does the proxy underestimate the real bend?

## 7. Downstream changes this design unblocks
1. `scoring.md §25` — `shift_i`, C2a/b, manipulation-check gate
2. `pre-registration.md` §6 — C2 as a Phase-2 exploratory probe, validity contingent on C2b
3. runtime — a timer-condition flag (or timed/untimed twins) + the manipulation check
4. `validity-threats.md` — C2 as a *contingent* corroborator of EV-4 (only on convergence); the manipulation-validity row
5. `DECISIONS.md` — the C2 lock (Dave's call)

## 8. Relationship to the other branches
- **The EV-4 triangle.** H-A2 (real stakes, gold standard) · H9c (self-report fingerprint) · C2 (induced stress, cheap proxy) — three measurements of the hot-state self; C2 is the cheapest and most contingent.
- **Subordinate to H-A2.** C2 is validated *against* real stakes, not independent of them.
- **CV-1 / the timer.** C2 generalizes the instrument's own quick-fire timer into a deliberate contrast.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) C2; [`h-a2-real-stakes.md`](h-a2-real-stakes.md) (the gold standard C2 validates against), [`h9-self-calibration.md`](h9-self-calibration.md) §1.4/§2.2 (H9c; the hot–cold gap), [`validity-threats.md`](validity-threats.md) EV-4 (the construct), CV-1 (the timer)
- [`concept.md`](concept.md) (the Bago & De Neys disclaimer; the scrupulosity guardrails §1.5 leans on), [`scoring.md`](scoring.md) §8 — where §25 lands; [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus near-untouched)
