# R4 — Moral attentiveness (do you even notice?)

**Status:** Design proposal, drafted 2026-06-28 (extension loop, iteration 15 — Round 2). Develops **R4** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 2". **MVP-1 exploratory** (detection leans on spontaneous/incidental measures; the dedicated probe is reactive — §1.5). Carded. The lock is Dave's.

**Provenance.** R4, and the most *upstream* construct in the whole instrument. Every other branch presupposes the moral stakes have already been registered — you can't weigh a choice (cost-of-virtue), feel a pull (A5), or rationalize a lapse (R3, B4) about a situation you never perceived as moral. **Moral attentiveness** (Reynolds 2008) is that front-end: the chronic tendency to *perceive* and *reflect on* the moral dimension of ordinary experience — the trait-level version of the first component of Rest's (1986) model, **moral sensitivity** (recognizing that a situation has a moral aspect at all). R4 measures component 1; the rest of the instrument measures components 2–4.

---

## 1. The hypothesis statement

**R4 (proposed `pre-registration.md` §6, secondary; exploratory).**

*Moral attentiveness — the perceptual and reflective tendency to register the moral dimension of everyday situations — is a reliable individual difference, distinct from how much a person values morality (the inventory) and from how central it is to their identity (R1); and it is the upstream gate that bounds whether the other signals can fire at all.*

### 1.1 Measurement primitive (two facets; non-reactive detection)
Reynolds' two facets:
```
perceptual_i   = the tendency to perceive/color experiences in moral terms (do you SEE the ethical dimension?)
reflective_i   = the tendency to reflect on / consider moral matters (do you THINK about ethics?)
```
Detected — crucially — **without cueing morality** (asking "is this a moral situation?" *manufactures* the attention it's trying to measure; §1.5). The non-reactive channels:
- **Spontaneous moral framing** — in open-ended/free-text responses where morality is *not* cued, how readily the person frames experience in moral terms. This reads the A3 moral-language data (`scoring.md §20`) for *rate/readiness* (distinct from A3's *content/concordance* — §1.4).
- **Incidental moral salience** — moral details of a scenario are detected/recalled more by the attentive (the "moral pop-out" effect, Gantman & Van Bavel 2014): an incidental-memory or detection read that never asks "did you notice?".
- *(Reactive, used sparingly)* a dedicated issue-detection probe, knowing it perturbs the very thing it measures.

### 1.2 R4a — moral attentiveness is a reliable individual difference
Split-window test–retest of `perceptual_i` and `reflective_i`: lower 95% CI ≥ **0.40** (Reynolds' scale is reliable; this is the behavioral analog). Bootstrap per §8.

### 1.3 R4b — attentiveness is the upstream gate, distinct from values and from identity-centrality
The conceptual core: perceiving the moral stakes is **not** the same as valuing morality or making it central to the self. So `perceptual_i`/`reflective_i` are discriminant from the inventory's value-importance (§5) **and** from R1 centrality — model R² of [value-importance, R1] predicting attentiveness has upper CI < 0.50. The four corners are real people: high-attentive/high-central (the engaged), high-attentive/low-central (the moral *analyst/critic* who notices ethics everywhere without it being core to who they are), **low-attentive/high-central** (the well-meaning-but-oblivious — morality matters to them yet they miss subtle stakes), low-attentive/low-central (the morally relaxed). And the gate claim: low attentiveness *bounds* the downstream signals — you cannot show a cost-of-virtue, an A5 pull, or an R3 disengagement on stakes you never perceived (an exploratory moderation: attentiveness sets a ceiling on the other channels' engagement).

### 1.4 R4c — convergent detection (and distinctness from A3)
The non-reactive measures should agree: `perceptual_i` (spontaneous moral framing rate) correlates with incidental moral salience/recall — convergent validity for "perceives morality." **Distinct from A3:** A3 measures the *content* of a person's moral language (which foundations, the talk–walk concordance); R4 measures the *readiness/volume* to perceive moral stakes at all (a person can be highly attentive but talk about a narrow set of foundations, or attentive-but-not-grandstanding). R4 reads the A3 corpus for a different quantity (rate of unprompted moral framing), and adds the incidental-salience channel A3 doesn't have.

### 1.5 N=1, value-neutrality, the reactivity problem
- **N=1.** The two facets are within-person, reveal-eligible (descriptive: "you readily perceive the ethical dimension of ordinary situations" vs. "you tend to read situations in practical rather than moral terms"). R4a/b/c are cohort.
- **Value-neutrality (load-bearing).** **More attentiveness is not better.** High moral attentiveness can be conscientious moral perceptiveness *or* scrupulous over-moralizing (seeing sin everywhere — the `concept.md` scrupulosity risk, which R4 is the natural early-warning for); low attentiveness can be a relaxed, non-moralizing eye *or* a genuine moral blind spot. The reveal describes where you sit; it never scores "more moral perception = better person." The scrupulosity guardrails apply with extra force at the high end.
- **The reactivity problem (the central methodological burden).** Attentiveness is the construct you most easily *destroy by measuring* — any direct "do you notice the moral issue here?" cues the noticing. R4 therefore primarily uses non-reactive reads (spontaneous framing, incidental salience), and treats any dedicated detection probe as both reactive and educational (it teaches attentiveness), so it cannot be the primary measure.

### 1.6 Falsification and exploratory
Combined R4 = **R4a ∧ R4b** (reliable, and distinct from values/centrality). R4c (convergent non-reactive detection) sharpens it. A null R4b (attentiveness collapses onto value-importance or R1) is the falsification — perception would then be nothing over valuing. **Exploratory:** attentiveness as the **ceiling** on the other channels (you can't engage stakes you don't perceive); R4 ↔ scrupulosity (the high-end risk); R4 ↔ R1 (the analyst vs the oblivious corners); R4 ↔ A3 (rate vs content).

---

## 2. Theoretical grounding
- **Reynolds 2008 ("Moral attentiveness: Who pays attention to the moral aspects of life?", JAP).** The construct and its perceptual/reflective facets; evidence it predicts ethical behavior — R4a/b's anchor.
- **Rest 1986 (Four-Component Model).** Moral sensitivity is *component 1* — recognizing the moral issue, the prerequisite to judgment, motivation, and character. R4 is the trait-level version of component 1; it situates the whole instrument (the other branches are components 2–4).
- **Gantman & Van Bavel 2014 (the "moral pop-out effect").** Moral content captures attention/perception more readily — the basis for the non-reactive incidental-salience read.

## 3. Instrument modification required
- **Already in place.** The A3 free-text / story-prompt channel (`scoring.md §5.4/§20`) — R4 reads it for *rate of spontaneous moral framing* (a new feature over A3's content read).
- **A1 (light add).** An incidental-moral-salience read (e.g., recall of moral vs. neutral scenario details, never cued as a moral test) — a runtime/analysis addition, not new scenarios.
- **A2.** Scoring `§29` (proposed): `perceptual_i`/`reflective_i` from spontaneous-framing rate + incidental salience; R4a/b/c; the discriminant from value-importance and R1. Inherits A3's κ gate for the language-derived part.
- No new domains; corpus untouched (the salience read rides existing scenarios).

## 4. Implications for existing locked decisions
**MVP-1 exploratory; non-reactive detection; the κ gate (shared with A3) and the reactivity caveat bind it.** **Carded** (the perceptual-front-end facet). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R4 (moral attentiveness) as a secondary; perceptual/reflective facets from spontaneous-framing rate (A3 corpus) + incidental moral salience (scoring §29); R4b distinct from value-importance and R1; non-reactive measures primary (the dedicated probe is reactive and educational); one design-stage card; value-neutral with scrupulosity guardrails." Considered-and-rejected: a direct "is this a moral issue?" probe as the primary measure (rejected — manufactures the attention); scoring high attentiveness as healthier (rejected — scrupulosity); folding R4 into A3 (rejected — rate ≠ content, R4c).

## 5. Why this is a research contribution
R4 supplies the **front-end the instrument was missing**: it measures whether a person even *perceives* the moral dimension — the prerequisite (Rest's component 1) that bounds everything downstream — and it does so **without** the dedicated probe that would manufacture the very attention it measures. It separates *perceiving* morality from *valuing* it and from *identifying with* it (R4b's four corners), and it gives the scrupulosity risk an early-warning signal. The instrument can now say not just *what you do with moral stakes* but *whether you see them at all*.

## 6. Open design questions
- **Q1.** Non-reactive incidental-salience read that doesn't tip its hand as a moral test — design and validate the paradigm.
- **Q2.** The rate-vs-content separation from A3 — can the spontaneous-framing *rate* be cleanly factored out of the A3 content profile?
- **Q3.** Scrupulosity at the high end — the threshold above which high attentiveness routes to the break/normalize-imperfection content rather than a neutral reveal.

## 7. Downstream changes this design unblocks
1. `scoring.md §29` — `perceptual_i`/`reflective_i` (spontaneous-framing rate + incidental salience), R4a/b/c, the discriminant
2. `pre-registration.md` §6 — R4 exploratory; R4b the distinctness + the gate
3. runtime/analysis — the incidental-moral-salience read
4. `research-program.json` — the R4 card (design-stage)
5. `validity-threats.md` — the reactivity row (measuring attentiveness perturbs it) + the scrupulosity-at-the-high-end note
6. `DECISIONS.md` — the R4 lock (Dave's call)

## 8. Relationship to the other branches
- **The upstream gate.** Component 1 (perception) bounds components 2–4 (the rest of the instrument): you can't show a cost-of-virtue, A5 pull, or R3 disengagement on stakes you never perceived.
- **R1.** Perceiving morality (R4) ≠ morality being central to the self (R1) — the analyst vs. the oblivious corners (R4b).
- **A3.** Rate/readiness (R4) vs. content/concordance (A3) — R4 reads the same corpus for a different quantity (R4c) + adds incidental salience.
- **Scrupulosity.** R4 is the natural early-warning for over-moralizing (the high-end risk).

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 2" R4; [`h-a3-moral-language.md`](h-a3-moral-language.md) (the corpus R4 reads for *rate*, vs A3's *content*; the shared κ gate), [`r1-moral-identity-centrality.md`](r1-moral-identity-centrality.md) (perception ≠ centrality, the four corners)
- [`concept.md`](concept.md) (the scrupulosity guardrails R4 is the early-warning for), [`scoring.md`](scoring.md) §5.4/§20 (the language channel), §8 — where §29 lands
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`validity-threats.md`](validity-threats.md) (the reactivity + scrupulosity rows), [`pre-registration.md`](pre-registration.md) §6
