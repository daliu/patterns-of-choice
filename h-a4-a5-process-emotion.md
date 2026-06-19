# H-A4 / H-A5 — Process and moral-emotion signals (the adjuncts to the choice)

**Status:** Design proposal, drafted 2026-06-19 (extension loop, iteration 9). Develops branches **A4** and **A5** of [`measurement-avenues.md`](measurement-avenues.md), bundled because they are the two channels that read what surrounds a choice — *how* it was made (A4) and what was *felt* around it (A5) — rather than the choice itself. These are the **noisiest, most exploratory** channels on the roadmap; the discipline here is mostly in the confounds named and the claims kept modest. **MVP-1 exploratory.** Locks are Dave's.

**Provenance.** A4 and A5. The instrument scores the *choice*; two signals sit adjacent to it and are nearly free to collect. **A4 (process):** the dynamics of deciding — already half-captured (`response_time_ms`, `presented_position`, `was_timeout` in the session log). **A5 (moral emotion):** the affective pull of the road not taken — which is the **internalized-norms leg of the conversation's triad** (the thing that governs the unwatched solo actor) made measurable. Neither is the choice; both are *about* the choice.

---

## Part 1 — H-A4: decision conflict (the process channel)

### 1.1 Measurement primitive
For person *i*, item *p*, define a **conflict** score from already-logged dynamics, all **within-person and confound-guarded**:
```
rt_z(i,p)  = z-score of response_time_ms within i's own distribution, residualized on item text-length
            (and presented_position), excluding was_timeout=true items
rev(i,p)   = answer revisions before commit (IF the runtime captures them — see §4; else omitted)
conflict(i,p) = combine(rt_z, rev)   # higher = more effortful/conflicted, NOT "more deliberative-ergo-utilitarian"
```
**Hard caveats baked in:** exclude timeouts; control item length + reading load; z within-person (people read at different speeds); device/latency noise is real; and the quick-fire **timer construct (CV-1)** interacts with any RT measure, so conflict is read only on the untimed session types or as relative-within-the-timed-set. **No framework mapping:** slower ≠ deontological/utilitarian — the Greene fast/slow mapping does not hold (Bago & De Neys 2019, already disclaimed in `concept.md`). Conflict is *effort/ambivalence*, full stop.

### 1.2 H-A4a — conflict is a reliable signal
Split-window test–retest of per-construct `conflict(i,·)`: lower 95% CI ≥ **0.40** (some people, and some domains, are reliably more conflicted). Bootstrap per §8. Conditional on the confound guards above actually removing the length/device variance (a pilot check, §7).

### 1.3 H-A4b — conflict adds information beyond the choice
A choice made under high conflict differs in its downstream properties from the same choice made fluently — e.g., it is **less stable over time** (predicts lower test–retest of that item) and/or sits on a **larger stated–revealed gap**. Operationally: conflict predicts within-person item-instability and/or gap magnitude, controlling for the choice itself; lower 95% CI of that partial association > 0. If conflict adds nothing beyond the choice, A4 is just RT noise — that is the falsification.

### 1.4 Modesty / status
RT-as-conflict is contested and confound-laden; A4 is **exploratory**, and it gets **no public card** — it is an analysis adjunct (like C1), not a browsable self-knowledge facet. Its honest value: flagging *which* of a person's choices were hard-won vs. automatic, as context for the reveal, not a headline.

---

## Part 2 — H-A5: the counterfactual moral pull (the emotion channel)

### 2.1 Measurement primitive
A short **post-choice affect probe** on a subset of items: *how much do you feel the pull of the option you did not take?* (and, on non-virtuous choices, residual guilt/tension). Crossed with the choice, this yields a 2×2 **internalization signature**:

| | low pull | high pull |
|---|---|---|
| **chose virtuous** | aligned — virtue *is* what you wanted | **effortful virtue** — you overrode a real temptation |
| **chose non-virtuous** | no internalized norm (or a genuine value difference) | **internalized-but-violated** — guilt; the seed of change |

The new dimension is *felt-ness* — orthogonal to the behavioral axis. A5 measures whether a norm is **felt**, not just followed.

### 2.2 H-A5a — felt pull is a reliable individual difference
Split-window test–retest of per-construct counterfactual pull: lower 95% CI ≥ **0.40**. (Some people feel the road not taken; some don't.)

### 2.3 H-A5b — pull is distinct from the choice *and* from A4 conflict
Affect ≠ RT ≠ choice. A choice can be slow (high A4 conflict) with no affective pull, or fast with strong residual guilt. Discriminant: the pull score is not recoverable from `conflict(i,p)` + the choice (regression residual survives; R² upper CI < 0.50). This keeps A5 from collapsing into A4 or into the behavioral axis.

### 2.4 H-A5c — the internalization signature predicts change (exploratory / longitudinal)
The character-relevant cell is **chose-non-virtuous + high pull** (internalized-but-violated): people who *feel* the pull of the virtue they didn't enact should be the ones who later **close the gap** on that construct — the felt norm is the seed of behavior change. Exploratory, longitudinal; an explicit hook for the (MVP-2) intervention layer (`concept.md`: insight → identity). The mirror image — **chose-virtuous + high pull** (effortful virtue) — is the strongest single-choice character signal (virtue against a real pull).

### 2.5 Caveats (A5 is the hardest channel to validate)
Affect self-report is noisy and **demand-prone** (asking "do you feel the pull?" invites the flattering answer); **alexithymia** and **cultural display rules** vary how affect is reported; and the probe is **reactive** (asking about the feeling changes it, and may itself moralize). Mitigations: indirect/forced-choice affect phrasing over "rate your guilt 1–7"; a no-probe control subset to estimate reactivity (as H9 §14.6 does for the prediction beat); honest exploratory status. **A5 resists gaming *less* than the choice in one sense** (a felt pull is harder to fake than a clean choice) but the *report* of it is fully gameable — so it's not a gaming-proof channel.

### 2.6 The public card (A5 only)
Unlike A4, A5 **is** a compelling, accessible self-knowledge facet — *the pull of the road not taken; felt vs. performed virtue* — so it gets a `research-program.json` card, **honestly labeled design-stage / exploratory** (the most speculative card, with the spec's caveats one click away). This also exercises the now-automated manifest→site pipeline end-to-end.

---

## 3. Shared: N=1 reveal, value-neutrality, the triad, gaming

- **N=1 reveal profiles.** Both are within-person and reveal-eligible: A4 — "honesty is fast and easy for you; generosity is slow and effortful"; A5 — "you feel the pull of the kinder choice even when you don't take it." The H-A4a/b and H-A5a/b/c statistics are cohort. (Affect/RT are on absolute-ish scales, so the per-person reads need no cohort norm.)
- **Value-neutrality.** Effort is not graded (finding virtue easy isn't better than finding it hard — arguably the reverse, per the effortful-virtue cell); felt pull is descriptive of internalization, not a virtue ranking. Both poles descriptive.
- **The triad tie.** A5 operationalizes the **internalized-norms** leg of the moral-systems conversation's triad (character × incentives × norms) — the thing that governs the solo unwatched actor. It is the closest the instrument comes to measuring whether a norm is *internal*.
- **Gaming.** Both widen the Incentive-validity surface modestly; neither is gameproof (affect report and RT are both manipulable). Auditable per IN-1/IN-2.

## 4. Instrument modification required
- **A4:** RT/timeout/position already logged (§1.1). The one open capture question: do answer **revisions** get recorded? In the event-sourced runtime (append-only log) a revision is multiple events for one item; if not currently emitted, that's a small runtime addition (else A4 runs on RT alone). Scoring `§22` (proposed): the confound-guarded conflict score + H-A4a/b. Parity-gated.
- **A5:** a short **post-choice affect probe** (new elicitation, light — a subset of items, indirect phrasing) + a no-probe control subset for reactivity. Scoring `§23` (proposed): the counterfactual-pull score, the internalization 2×2, H-A5a/b/c. The affect probe is self-report (analyzer-side), reactivity-netted like H9.
- No new scenarios; the §16/§17 corpus is untouched (A4 = re-analysis of logged dynamics; A5 = a probe attached to existing items).

## 5. Implications for existing locked decisions
**Both MVP-1 exploratory, high-noise.** A4 is near-free (re-analysis) but interpretively treacherous; A5 is light to add but the hardest to validate. Neither is a primary or confirmatory secondary until its confounds (A4) / reactivity + reliability (A5) are shown. **A4 → no public card; A5 → one design-stage card.** Corpus untouched. **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add H-A4 (decision conflict, RT-derived, no card) and H-A5 (counterfactual moral pull, one design-stage card) as MVP-1 exploratory channels; scoring §22/§23; A5 affect probe + reactivity control; A4 pending the runtime revision-capture question." Considered-and-rejected: an RT→framework mapping (rejected — Bago & De Neys); a direct "rate your guilt 1–7" probe (rejected — demand characteristics; use indirect phrasing); promoting either to primary before validation (rejected — these are the speculative tail).

## 6. Why these are contributions
A4 and A5 add the two dimensions a choice-only instrument is blind to: **how hard the choice was** (conflict/effort) and **what it felt like** (the counterfactual pull). A5 in particular reaches the thing the whole moral-systems thread kept pointing at — whether a norm is *internalized* (felt) vs. merely *performed* — and gives the (MVP-2) intervention layer its most principled hook (felt-but-violated norms are where change starts). Both are honest about being the noisy frontier.

## 7. Open design questions
- **Q1 (A4). Revisions capture.** Does the runtime emit answer-change events? If yes, `rev` strengthens conflict; if no, RT-only (and decide whether the small runtime addition is worth it).
- **Q2 (A4). Confound removal.** Can length/device/reading-speed be modeled out well enough that residual RT is interpretable? Pilot check; if not, A4 stays a flag, not a measure.
- **Q3 (A5). Probe phrasing.** Indirect/forced-choice affect elicitation to minimize demand; pilot the wording against a social-desirability check.
- **Q4 (A5). Probe frequency + reactivity.** How often to probe without making the practice feel like an emotion quiz (and without the probe moralizing the choice). Reactivity estimated via the no-probe control.
- **Q5 (A5). Alexithymia / culture.** A light screen and explicit non-comparability of absolute affect across people from different display-rule cultures.

## 8. Downstream changes this design unblocks
1. `scoring.md §22` (A4 conflict) + `§23` (A5 pull + internalization 2×2); A4 parity-gated, A5 reactivity-netted
2. `pre-registration.md` §6 — H-A4 and H-A5 as exploratory channels (promotable once confounds/reactivity are shown)
3. runtime — (A4) optional answer-revision events; (A5) the post-choice affect probe + no-probe control
4. `research-program.json` — **the A5 card** (design-stage, exploratory); A4 gets none
5. `concept.md` — the process + moral-emotion channels; A5 as the internalized-norms measure + the intervention hook
6. `validity-threats.md` — rows for the RT/device confound (A4) and affect demand-characteristics/reactivity (A5)
7. `DECISIONS.md` — the H-A4/H-A5 locks (Dave's call)

## 9. Relationship to the other branches
- **A4 vs A5.** Distinct (H-A5b enforces it): conflict is *effort*, pull is *affect*; a choice can have either, both, or neither.
- **Both feed C1.** Two more methods/channels for the MTMM matrix (process and affect, whose errors differ from choice's).
- **A5 ↔ H9.** Does felt pull predict self-prediction error — do people who feel the pull foresee their slips better?
- **A4 ↔ cost-of-virtue.** Conflict should peak near a person's cost-of-virtue break point (the stake where they're torn) — a convergence check.
- **A5 ↔ the intervention layer.** The felt-but-violated cell is the seed of change — the MVP-2 hook.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) A4, A5 (and C1, which both feed); [`scoring.md`](scoring.md) §1.1 (the logged RT/timeout/position A4 reuses), §8 (bootstrap), §14.6 (the reactivity-control pattern A5 borrows) — where §22/§23 land
- [`concept.md`](concept.md) (the Greene fast/slow disclaimer A4 honors; scrupulosity guardrails relevant to A5's guilt probe), [`c1-multimethod-convergence.md`](c1-multimethod-convergence.md) (both as channels), [`h9-self-calibration.md`](h9-self-calibration.md) (reactivity control; the A5↔H9 cross-test)
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`validity-threats.md`](validity-threats.md) (CV-1 timer interaction with A4; the new confound rows), [`pre-registration.md`](pre-registration.md) §6
