# R3 — Moral disengagement (how you switch off the alarm)

**Status:** Design proposal, drafted 2026-06-26 (extension loop, iteration 14 — Round 2). Develops **R3** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 2". **MVP-1 exploratory** (detection leans on the choices + the κ-gated language channel). Carded. The lock is Dave's.

**Provenance.** R3. A5 measures the **felt pull** when you act against a norm — the residual guilt that says the norm is internalized even in violation. Moral disengagement (Bandura 1999/2002) is the **opposite machinery**: the cognitive moves that *deactivate* moral self-sanction so you can violate your own standard **without** the guilt. R3 measures that machinery — and sits as the negative pole of the same axis A5 anchors: when you fall short, do you *feel* it (A5) or *neutralize* it (R3)?

---

## 1. The hypothesis statement

**R3 (proposed `pre-registration.md` §6, secondary; exploratory).**

*The disengagement mechanisms a person reaches for when they act against their own standards form a reliable profile; disengagement decouples the stated–revealed gap from felt guilt (it is what lets a gap exist without a moral remainder); and it predicts larger gaps and more under-pressure lapses.*

### 1.1 Measurement primitive (the eight mechanisms; multi-channel detection)
Bandura's eight mechanisms, in four loci: **moral justification**, **euphemistic labeling**, **advantageous comparison** (reconstrue the act); **displacement** and **diffusion of responsibility** (obscure agency); **distortion/minimizing of consequences** (disregard the harm); **dehumanization** and **attribution of blame** (devalue the target). The disengagement profile `D_i` is detected, per mechanism, from:
- **Choices** — a subset of items offer a disengaging vs. a responsibility-owning framing of the same act; which the person endorses.
- **Language** (A3 / `scoring.md §20`) — disengagement markers in free-text (euphemism, blame-attribution, "everyone does it"); the moral-language channel is the natural detector.
- *(Optional)* a short validated self-report (Moore et al. 2012 Propensity-to-Morally-Disengage), heavily desirability-discounted (§1.5).

### 1.2 R3a — the disengagement profile is reliable
Split-window test–retest of `D_i` (which mechanisms a person reaches for): lower 95% CI ≥ **0.40**. Some people chronically reach for blame-attribution, others for diffusion, others for none. Bootstrap per §8.

### 1.3 R3b — disengagement decouples the gap from guilt (load-bearing; the A5 link)
The distinctive claim: disengagement is *what lets a gap exist without a remainder*. For a matched stated–revealed gap (§6), higher `D_i` predicts **lower** A5 felt-pull/guilt:
```
R3b:  among participants with a comparable gap, corr( D_i , A5 felt-pull )  < 0,  upper 95% CI < 0
```
So R3 is the **moderator between the gap and the guilt** — it explains why two people with the same gap differ on whether they feel it. (And R3 → B4: the disengaged violator doesn't grieve [low A5] and doesn't grow [B4 rationalizer/entrenched, not grower]; the felt violator grieves and grows.)

### 1.4 The central validity problem — disengagement vs. legitimate justification (load-bearing)
**Moral justification is indistinguishable *in form* from genuine moral reasoning.** "I broke the vow because the king was about to burn the city" is a real justification, not a disengagement; "I padded the expense report because everyone does it" is disengagement wearing the same grammar. R3 therefore **cannot flag a reason as disengagement merely because it is a reason.** The discriminant signature of self-serving disengagement (vs. principled justification):
- **self-serving** — the reframe reduces the person's *own* cost/guilt specifically;
- **inconsistent** — applied to the self but not to others doing the same act (the H12 self–other double standard is the tell);
- **post-hoc** — invoked *after* a lapse rather than expressed as a stable prior conviction (cross-poses / latency);
- **standard-preserving** — it removes the guilt *without lowering the professed standard* (contrast B4 rationalization, which lowers the bar; disengagement keeps the bar and exempts the instance).
R3 is scored only on this signature, never on the presence of a justification. This is the hardest part of the branch and the place it is most likely to mismeasure; it is flagged, not finessed.

### 1.5 N=1, value-neutrality, the desirability caveat
- **N=1.** `D_i` (which mechanisms you reach for) is within-person, reveal-eligible (descriptive: "when you fall short, you tend toward 'everyone does it' and 'they had it coming'"). R3a/b/c are cohort.
- **Value-neutrality.** Not all reframing is pathological — advantageous comparison can be honest perspective, displacement can be *accurate* when responsibility genuinely is shared. The reveal names the mechanisms; it doesn't moralize them, and it does not call the person bad.
- **Desirability.** Admitting you make excuses is itself socially sanctioned, so self-report under-reports; the behavioral/linguistic detection (the choices + A3) is the harder-to-fake channel and the primary one.

### 1.6 Falsification and exploratory
Combined R3 = **R3a ∧ R3b** (a reliable profile that genuinely decouples gap from guilt). R3c (criterion validity — disengagement predicts larger gaps / more C2 lapses) sharpens it. A null R3b (disengagement doesn't predict lower guilt) collapses the construct toward "just another framing." **Exploratory:** R3 as the **A5 negative pole** (felt-vs-neutralized as one axis); R3 ↔ H12 (the inconsistency tell *is* the self–other double standard); R3 ↔ R1 (symbolic-but-not-internalized identity should disengage more); R3 ↔ B4 (disengagers don't grow).

---

## 2. Theoretical grounding
- **Bandura 1999 (PSPR), 2002 (J. Moral Education).** Moral disengagement and its eight mechanisms — the construct R3 measures. (The repo already cites Bandura's self-efficacy work; this is his moral-agency work.)
- **Moore, Detert, Treviño, Baker & Mayer 2012 (Personnel Psych).** The validated Propensity to Morally Disengage scale + evidence it predicts unethical behavior — R3a/R3c's anchor.
- **Detert, Treviño & Sweitzer 2008.** Disengagement in ethical decision-making — the choice-level operationalization.
- *(Conceptual)* the justification-vs-disengagement problem (§1.4) is exactly the place Bandura's "moral justification" mechanism shades into legitimate moral reasoning; the discriminant is R3's central methodological burden.

## 3. Instrument modification required
- **A1.** A subset of items with paired disengaging / responsibility-owning framings (light authoring) + the A3 language detectors (`scoring.md §20`, κ-gated).
- **A2.** Scoring `§28` (proposed): `D_i` per mechanism from choices + language; R3a/b/c; the §1.4 discriminant (self-serving + inconsistent + post-hoc + standard-preserving) — built explicitly so a justification is *not* auto-scored as disengagement. Parity-gated for the choice-derived part; language part inherits A3's κ gate.
- No new domains; corpus lightly extended (the paired framings).

## 4. Implications for existing locked decisions
**MVP-1 exploratory; detection multi-channel; the justification discriminant is the gate.** **Carded** (the descriptive "which mechanisms" framing). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R3 (moral disengagement) as a secondary; `D_i` from disengaging-framing choices + A3 language markers (scoring §28); R3b the gap↔guilt decoupling vs. A5; the §1.4 discriminant so legitimate justification is never auto-scored as disengagement; one design-stage card; light corpus extension." Considered-and-rejected: scoring any justification as disengagement (rejected — §1.4, the central error); a self-report-only measure (rejected — desirability); a "disengagement score" headline (rejected — report the mechanism profile).

## 5. Why this is a research contribution
R3 measures the **machinery of self-exculpation** — and pins it to the felt-pull axis (A5) so the instrument can finally say *why* two people with the same moral gap differ on whether they suffer it: one feels the remainder, the other has neutralized it. It also takes on, rather than ducks, the hardest distinction in the area — **a self-serving excuse vs. a principled justification look identical**, and R3's whole design is the attempt to separate them by their *signature* (self-serving + inconsistent + post-hoc + standard-preserving) instead of their grammar. Most instruments either ignore disengagement or conflate it with reasoning; R3 does neither.

## 6. Open design questions
- **Q1.** The justification/disengagement discriminant (§1.4) — can the four-part signature actually be detected at the item level, or only across a person's pattern (the inconsistency tell needs the self-vs-other contrast, i.e. H12 data)?
- **Q2.** Language detection of disengagement markers — κ against gold, like A3 (the shared coding-reliability gate).
- **Q3.** Which mechanisms are even probe-able in a daily practice without inducing the very disengagement you measure?

## 7. Downstream changes this design unblocks
1. `scoring.md §28` — `D_i` per mechanism, R3a/b/c, the §1.4 discriminant
2. `pre-registration.md` §6 — R3 exploratory; R3b (gap↔guilt) the distinctive test
3. `scenarios/` — paired disengaging / responsibility-owning framings (light); A3 disengagement-marker coding
4. `research-program.json` — the R3 card (design-stage)
5. `validity-threats.md` — the justification-misclassified-as-disengagement row (the §1.4 risk) + the desirability row
6. `DECISIONS.md` — the R3 lock (Dave's call)

## 8. Relationship to the other branches
- **A5 (the opposite pole).** Felt-but-violated (A5) vs. disengaged-violation (R3) — one axis: when you breach a norm, do you feel it or neutralize it?
- **H12.** The *inconsistency* tell of disengagement (excuse yourself, not others) **is** the self–other double standard — H12 supplies R3's discriminant.
- **R1.** Symbolic-not-internalized moral identity should disengage more (the performative cluster); internalized should disengage less.
- **B4.** Disengagers don't grieve and don't grow (rationalizer/entrenched, not grower).
- **A3.** The language channel is R3's primary detector (euphemism, blame, "everyone does it").

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 2" R3; [`h-a4-a5-process-emotion.md`](h-a4-a5-process-emotion.md) §Part 2 (A5, the opposite pole — the gap↔guilt link R3b tests), [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md) (the inconsistency discriminant), [`h-a3-moral-language.md`](h-a3-moral-language.md) (the detection channel + its κ gate)
- [`r1-moral-identity-centrality.md`](r1-moral-identity-centrality.md) (symbolic↔disengagement), [`b4-value-change-dynamics.md`](b4-value-change-dynamics.md) (disengager ≠ grower), [`scoring.md`](scoring.md) §6 (the gap), §20 (language), §8 — where §28 lands
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus lightly extended), [`validity-threats.md`](validity-threats.md) (the §1.4 misclassification row), [`pre-registration.md`](pre-registration.md) §6
