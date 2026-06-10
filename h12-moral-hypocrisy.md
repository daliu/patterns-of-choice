# H12 — Moral hypocrisy (the self–other double standard)

**Status:** Design proposal, drafted 2026-06-10 (extension loop, iteration 4). Develops branch **B3** of [`measurement-avenues.md`](measurement-avenues.md). Source for downstream changes to `concept.md`, `pre-registration.md`, `scoring.md`, `DECISIONS.md`. Mirrors [`h8`](h8-narrative-immersion-design.md)/[`h9`](h9-self-calibration.md)/[`h10`](h10-cross-situational-consistency.md). **MVP-1 secondary** (same cohort; a modest corpus addition). The lock — including the §16-unlock for the new standard-setting items — is Dave's call.

**Provenance.** Branch B3, and the third vertex of a triangle the loop has been assembling. PoC measures what you *do* (revealed behavior), what you *predict you'll do* (H9), and what *others predict you'll do* (H-A1). H12 adds what you *demand of others* — the standard you apply when judging someone else's transgression — and contrasts it with the standard you apply to yourself. The gap is moral hypocrisy: harsh on others, lax on self.

---

## 1. The hypothesis statement

**H12 (proposed `pre-registration.md` §6, secondary).**

*Participants demand more moral behavior of others than they enact themselves; this self–other double standard is distinct from ordinary weakness of will (failing a standard you set for yourself); and it concentrates where being virtuous costs the self.*

### 1.1 Measurement primitive (three standards on one axis)

The instrument already collects what the participant *does*. H12 adds two **standard-setting** elicitations on the *same scenario option set and the same primary axis* (§2.2) — "what is the minimum acceptable choice here?" — asked once about *another* agent and once about *oneself*:

```
self_rev_i(c)  = revealed behavioral choice on construct c (§3.2)       # what I do
self_std_i(c)  = minimum acceptable choice I demand of MYSELF here       # my normative self-standard
other_std_i(c) = minimum acceptable choice I demand of ANOTHER here      # my normative other-standard
```

All three are on the same [−1,+1] axis (+ = more virtuous), so every difference is **unit-legal** and **within-person (N=1)**:

```
hyp_i(c)      = other_std_i(c) − self_rev_i(c)     # practical hypocrisy: demand of others vs my behavior
akrasia_i(c)  = self_std_i(c)  − self_rev_i(c)     # weakness of will: my own standard vs my behavior
pure_hyp_i(c) = other_std_i(c) − self_std_i(c)     # the clean self–other double standard
```

with the identity **`hyp = pure_hyp + akrasia`** — practical hypocrisy decomposes into the pure double standard plus ordinary akrasia. Isolating `pure_hyp` is what separates *hypocrisy* (a higher bar for others) from merely *falling short of your own bar*.

### 1.2 H12a — the double standard exists

People demand more virtue of others than they enact:
```
H12a:  lower 95% bootstrap-CI bound of  mean_i mean_c hyp_i(c)  > 0
```
Aggregated over the consensual-pole domains (the H9a convention; in-group excluded). Bootstrap per `scoring.md` §8, seed `20260510`. Anchor: Batson moral hypocrisy; Valdesolo & DeSteno 2007.

### 1.3 H12b — it is distinct from weakness of will (load-bearing)

The interesting claim is not "people fail their own standards" (akrasia) but "people hold others to a higher standard than themselves":
```
H12b:  lower 95% bootstrap-CI bound of  mean_i mean_c pure_hyp_i(c)  > 0
       AND discriminant: regressing pure_hyp_i on [akrasia_i, gap_i (§6)], model R² upper 95% CI < 0.50
```
This isolates the double standard from ordinary self-failure and from the §6 self-stated–self-revealed gap. Without H12b, H12 is akrasia relabeled.

### 1.4 H12c — self-serving concentration

The double standard is larger where being virtuous costs the self (the self-serving direction):
```
H12c:  within-person, pure_hyp on high-self-cost items > pure_hyp on low-self-cost items;
       lower 95% CI of the paired difference > 0
```
Uses the existing `self-cost:*` tags (`scoring.md` §1.1). A double standard that does *not* track self-interest would point to principled-if-inconsistent other-regard rather than motivated leniency. Anchor: Bocian & Wojciszke 2014; self-serving bias (Miller & Ross 1975).

### 1.5 N=1, value-neutrality, the scrupulosity caveat

- **N=1.** All three quantities are within-person on a fixed axis — no cohort standardization (unlike §6). `hyp_i`, `pure_hyp_i` are reveal-eligible (descriptive: "you ask more honesty of others than of yourself"). The H12a/b/c statistics are cohort aggregates, separate from the reveal.
- **Value-neutrality and the negative pole.** "Hypocrisy" names the *construct*; the reveal uses neutral language ("self–other standard gap"). Crucially the **negative** pole — demanding *more* of yourself than of others (`pure_hyp < 0`) — is **not** valorized: chronic self-harsh standards are a scrupulosity signature (`concept.md` §"Risks to vulnerable users"), not a virtue. Both poles are descriptive; an extreme negative gap routes to the break / normalize-imperfection content, never to praise.
- **Judging ≠ predicting (distinct from H-A1).** `other_std` is a *normative* judgment (what's acceptable for another), not a *descriptive* prediction of what another would do (that is H-A1's informant channel, and the inverse direction). They must be elicited in clearly different framings.

### 1.6 Falsification and exploratory H12d

Combined H12 = **H12a ∧ H12b** (a double standard that is more than akrasia). H12c sharpens the mechanism. Partial results published, as with H8/H9/H10.

**Exploratory H12d — the judge/act/predict triangle.** With H9 (self-prediction) and H-A1 (informant prediction), H12 closes a triangle: *judge others* (H12) / *act* (revealed) / *predict self* (H9). Cross-tests: do larger hypocrites (`pure_hyp`) show larger self-prediction error (`cal_error`, H9) — is the double standard part of a broader self-opacity? And do informants (H-A1) predict the participant's *behavior* better than the participant's *professed standard* implies? Reported exploratory.

---

## 2. Theoretical grounding

- **Batson moral hypocrisy (1997 "In a very different voice"; 1999).** The motive to *appear* moral while ducking the cost of *being* moral — the coin-flip paradigm (assign yourself the good task; report a self-serving flip beyond chance). The foundational construct. *Caveat:* the "appearing moral" interpretation is debated and some downstream effects are mixed; H12 leans on the robust behavioral asymmetry, not the full motivational account.
- **Valdesolo & DeSteno 2007 (Psychological Science).** People rate their *own* transgression as fairer than an identical transgression by another — the direct self–other judgment asymmetry H12b targets. (The "cognitive load eliminates it" moderation is treated cautiously — a dual-process claim of the kind the repo disclaims elsewhere.)
- **Self-interest bias in moral judgment (Bocian & Wojciszke 2014; self-serving bias, Miller & Ross 1975).** Acts that benefit us are judged more moral — the basis for H12c.
- **Actor–observer asymmetry — with the Malle 2006 caveat.** The classic asymmetry (Jones & Nisbett) is, per Malle's meta-analysis, small and conditional; H12 does *not* rest on it — it measures the moral double standard directly rather than inferring it from attribution theory.
- **Explicitly excluded: the power→hypocrisy work built on Lammers & Stapel (2010).** Diederik Stapel's data were fabricated (mass retraction); that finding is not cited despite its thematic fit with the project's measurement-under-power thread. The power–hypocrisy link may be real, but must be re-sourced from non-fraudulent work before use. (Same post-Gino discipline the repo applies elsewhere.)

---

## 3. Instrument modification required

### Already in place
- The behavioral choice (`self_rev`) and per-item axis scoring (§2); the `self-cost:*` tags (§1.1) for H12c; H9 and H-A1 for the H12d triangle.

### What needs to be added
- **A1. Standard-setting items (light authoring; a corpus addition).** For a subset of constructs, a standard-setting probe in two framings — judge-self and judge-other — scored on the same option axis. These are *reframings* of existing constructs but they are **new items**, so they touch the corpus lock (§4). Counterbalanced and **well-separated** from the matched behavioral item so the participant does not consciously align them (the contamination control, parallel to H9's reactivity separation).
- **A2. Scoring `§17` (proposed).** `hyp`, `akrasia`, `pure_hyp`, the decomposition identity, the H12a/b/c statistics, and §1.5 suppression (a "won't judge / it depends" response is **missing, not zero** — the Dancy particularist case). Parity-gated (`make check`).

No informants, no real stakes — same cohort as MVP-1.

---

## 4. Implications for existing locked decisions

**MVP-1 secondary — but it adds items.** Unlike H9/H10 (re-analysis / prediction beat, no new items), H12 needs judge-self/judge-other items — a modest **corpus addition** that requires unlocking `DECISIONS.md §16`, exactly as **§17 unlocked it for H8's paired probes**. The §16 unlock criterion ("a specific construct gap") is met: the instrument currently *cannot* measure the self–other standard because it has no standard-setting items.

**Proposed `DECISIONS.md` entry (pending Dave's lock).** "Add H12 (self–other double standard) as an MVP-1 secondary; unlock §16 for a bounded set of judge-self/judge-other standard-setting items on existing constructs; scoring §17." Considered-and-rejected: approximate `self_std` from the aspirational inventory (rejected — cross-scale, breaks the unit-clean N=1 property; the situated standard-setting choice keeps everything on one axis); defer to Phase-2 (rejected — the same cohort suffices and the items are cheap).

**Relationship to the §6 gap.** `akrasia` is a situated, option-axis cousin of the §6 stated–revealed gap; `pure_hyp` is the genuinely new quantity, and H12b proves it is not the gap relabeled.

---

## 5. Why this is a research contribution

Moral hypocrisy is well-demonstrated in one-shot lab paradigms (Batson; Valdesolo & DeSteno); H12 makes it a **longitudinal, within-person, unit-clean trait**, cleanly **decomposed from weakness of will** (the `hyp = pure_hyp + akrasia` identity) — a distinction the one-shot literature rarely draws. And it completes the **judge/act/predict triangle**: a person measured on what they do, what they expect of themselves, what they demand of others (H12), what they predict about themselves (H9), and what others predict about them (H-A1) — five vertices on the same constructs, which no instrument assembles.

---

## 6. Open design questions
- **Q1. Item budget.** How many constructs get the self/other standard pair? Enough for a stable per-person `pure_hyp`, bounded by session load.
- **Q2. Order and contamination.** Judge-self vs judge-other order, and both well-separated from the behavioral item. Counterbalance; pilot whether proximity collapses the gap.
- **Q3. "Another" — who?** A generic other, a named peer, or the recurring NPC cast (H8)? The NPC option ties hypocrisy to attachment (do you judge your buddy more leniently than a stranger — *in-group* hypocrisy). Reserved.
- **Q4. Particularism handling.** A participant who refuses a universal standard ("it depends") is making a Dancy-style particularist move, not failing to answer; coded missing, and the rate itself reported as a descriptive signal.

---

## 7. Downstream changes this design unblocks
1. `scoring.md §17` — the three standards, the decomposition, H12a/b/c, suppression; parity-gated
2. `pre-registration.md` §6 (H12 secondary) + §5 (standard-setting analysis plan + contamination control)
3. `scenarios/` — the bounded judge-self/judge-other standard-setting item set
4. `DECISIONS.md` — the §16-unlock + H12 lock (Dave's call)
5. `concept.md` — a "self–other standard" subsection; the negative-pole/scrupulosity note in the risk section
6. `validity-threats.md` — a CV row for self/other contamination and the judging-vs-predicting separation from H-A1

---

## 8. Relationship to H9, H-A1, the §6 gap, and the cost-of-virtue probes
- **The triangle.** judge-others (H12) / act (revealed) / predict-self (H9) / predicted-by-others (H-A1) — H12 supplies the normative-other vertex.
- **vs the §6 gap.** §6 is self-stated vs self-revealed; H12's `pure_hyp` is other-demanded vs self-demanded — H12b enforces the distinction.
- **vs cost-of-virtue.** H12c reads the double standard *through* the self-cost dimension the cost-of-virtue probes already operationalize — where virtue is expensive is where hypocrisy should bite.
- **vs H10.** Exploratory: do high-variability people (H10) also show more context-dependence in their *standards* (a "situational hypocrisy")?

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) B3; [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md) (the §16-unlock precedent), [`h9-self-calibration.md`](h9-self-calibration.md) (self vertex), [`h-a1-informant-prediction.md`](h-a1-informant-prediction.md) (informant vertex)
- [`scoring.md`](scoring.md) §1.1 (`self-cost` tags), §3.2 (revealed), §6 (the gap H12b is distinct from), §13.4 (within-person concordance precedent) — where §17 lands
- [`concept.md`](concept.md) (scrupulosity guardrails for the negative pole), [`DECISIONS.md`](DECISIONS.md) §16/§17 (the corpus-unlock this needs)
- [`validity-threats.md`](validity-threats.md) (contamination + judging-vs-predicting rows), [`pre-registration.md`](pre-registration.md) §6
