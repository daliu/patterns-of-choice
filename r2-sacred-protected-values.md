# R2 — Sacred / protected values (what you won't sell at any price)

**Status:** Design proposal, drafted 2026-06-24 (extension loop, iteration 12 — the first **Round 2** branch, beyond the original avenues map). Develops **R2** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 2". **Mostly MVP-1 re-analysis** (the protected-value set is already-collected data); one part (the cheap-talk validation) is Phase-2. Carded. The lock is Dave's.

**Provenance.** R2, and a quiet payoff of a discipline the repo has honored from the start. The cost-of-virtue probe (§4) asks "at what price do you trade this value?"; a `"never"` answer is right-censored and, per `scoring.md` §13.2, **"not a measured price… must never be turned into a finite number."** That carefully-preserved categorical state *is* a **protected/sacred value** — a value you refuse to trade at any tested price. R2 reads the censored tail of the cost-of-virtue data as exactly what the protected-values literature describes. The censoring rule wasn't just hygiene; it was holding this construct in reserve.

---

## 1. The hypothesis statement

**R2 (proposed `pre-registration.md` §6, secondary).**

*Which of a person's values are treated as protected — refused at any price — is a reliable individual difference; protected values are categorically distinct from merely expensive ones (the incommensurability signature: quantity-insensitivity + taboo at being asked to price); and protectedness is orthogonal to how highly the value is ranked.*

### 1.1 Measurement primitive (the censored tail + a taboo marker)
For person *i*, value *v*: *v* is **protected** if the person's cost-of-virtue response for *v* is `"never"` (right-censored, `price > ladder top`, §4.1/§13.2) — refused across the whole tested ladder. The **protected-value set** `P_i = { v : response(i,v) = never }` comes free from existing data. Two reads:
```
P_i              = the set of never-traded values (from the §13.2 censored responses)
taboo_i(v)       = (light new probe, after a "never") "Was even being asked to put a price on this wrong?"
                   — the moral-outrage/illegitimacy marker that separates a sacred value from a very-expensive one
```

### 1.2 R2a — the protected-value set is reliable
Test–retest of `P_i` (set agreement, e.g., Jaccard over waves): lower 95% CI ≥ **0.40**. Which lines a person won't cross is stable, not mood. Bootstrap per §8.

### 1.3 R2b — protected ≠ expensive (the load-bearing distinctness)
A protected value is a *kind*, not a high point on the price scale (Baron & Spranca; Tetlock). The signature:
- **Quantity-insensitivity** — a protected value's refusal does not soften as the offered amount climbs across the ladder (flat, not graded), whereas a tradeable value shows a graded price response. (Bounded by the finite ladder — §1.5/§6.)
- **Taboo / incommensurability** — `taboo_i(v)` (outrage that pricing was even asked) is elevated for protected values and not for merely-expensive ones.
```
R2b:  among "never"-responders, taboo_i(v) is higher for genuinely protected values than for high-but-finite-price
      values matched on stated importance; and the price response is flatter. Lower 95% CI of that contrast > 0.
```
Without R2b, a "never" is just "very expensive" — R2b is what makes protected values a distinct construct.

### 1.4 R2c — protectedness is orthogonal to importance-ranking
You can rank a value #1 yet trade it (high-but-priced), or protect a value you don't rank highest. So `P_i` is not recoverable from the inventory ranking (§5) or from the cost-of-virtue price *magnitude* (§4): discriminant — `P_i` membership predicted by [inventory rank, log-price] leaves residual variance (model R² upper CI < 0.50). Protectedness is a *second axis* on each value (negotiable vs. not), beside importance.

### 1.5 N=1, value-neutrality, the cheap-talk caveat, the ceiling
- **N=1.** `P_i` is the person's own set of never-traded values — within-person, reveal-eligible (descriptive: "honesty and loyalty are non-negotiable for you; generosity has a price"). R2a/b/c are cohort statistics.
- **Value-neutrality.** Many protected values can be integrity *or* inflexible dogmatism; few can be pragmatic flexibility *or* lack of conviction. The reveal describes the set; it never scores "more sacred = better."
- **Cheap talk (load-bearing).** A `"never"` in a *hypothetical* probe is costless to claim — over-reporting is expected. So a hypothetical protected value is weaker evidence than a refusal under real stakes. **Cross-link to H-A2:** a genuinely protected value should resist even real consequences; the real-stakes channel validates *which* "never"s are real (the Phase-2 part of R2). Until then, `P_i` is "professed protected values," labeled as such.
- **Finite-ladder ceiling.** True quantity-insensitivity can't be fully tested with a bounded ladder (you can't offer infinite amounts); the taboo marker (§1.1) is the supplementary, non-monetary signature, and R2b's quantity-insensitivity claim is bounded to the tested range.

### 1.6 Falsification and exploratory
Combined R2 = **R2a ∧ R2b** (a reliable protected-value set that is categorically distinct from expensive). R2c sharpens it. A null R2b (protected = just expensive) collapses the construct to the cost-of-virtue tail — reported honestly. **Exploratory:** R2 × H-A2 (which professed "never"s survive real stakes — the cheap-talk filter); R2 × H12 (do people demand *others* honor *their* sacred values to a stricter standard — sacred-value double standards?); R2 × the moral-circle (are protections wider for the near than the far?).

---

## 2. Theoretical grounding
- **Baron & Spranca 1997 ("Protected values," OBHDP).** The construct: values protected from tradeoffs, with quantity-insensitivity and agent-relativity — the basis for R2a/b.
- **Tetlock et al. 2000; Fiske & Tetlock 1997 (taboo trade-offs / the psychology of the unthinkable).** Sacred values as *incommensurable* — pricing them triggers moral outrage; the basis for the `taboo` marker and R2b's "protected ≠ expensive."
- **Bartels & Medin 2007.** Quantity-(in)sensitivity is itself measurement-frame-dependent — the nuance that keeps R2b's quantity claim bounded and honest.
- **Ginges et al. 2007 (sacred values in intergroup conflict).** Evidence that sacred values behave categorically differently (material incentives can backfire) — supports the kind-not-degree framing.

## 3. Instrument modification required
- **Already in place.** The censored `"never"` cost-of-virtue responses (§4.1/§13.2) — `P_i` is **pure re-analysis** of data already collected and already preserved categorically.
- **A1 (light add).** The `taboo_i(v)` marker — a one-tap probe after a `"never"` response ("was being asked to price this wrong?"). Optional/gentle; phrased to avoid leading (§6).
- **A2.** Scoring `§26` (proposed): `P_i` from censored responses, `taboo`, R2a/b/c, the discriminant. Parity-gated.
- The cheap-talk validation (R2b under real stakes) rides H-A2 → Phase-2. No new scenarios; the cost-of-virtue corpus is untouched.

## 4. Implications for existing locked decisions
**MVP-1 re-analysis (the set) + a light probe; cheap-talk validation Phase-2.** The censoring discipline (§13.2) is the enabler — R2 is the construct it was preserving. Carded. **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R2 (sacred/protected values) as a secondary; `P_i` from the censored cost-of-virtue `never` responses (scoring §26) + a gentle taboo marker; R2b (protected≠expensive) the distinctness test; cheap-talk validation via H-A2 (Phase-2); one design-stage card; corpus untouched." Considered-and-rejected: treating `"never"` as a finite max-price (rejected — that's exactly the §13.2 violation, and it *is* the construct here); a "sacredness score" (rejected — no composite; report the set + the taboo pattern).

## 5. Why this is a research contribution
R2 turns the **censored tail** of the cost-of-virtue probe — data the instrument already collects and deliberately refuses to numericize — into a distinct, validated construct: *which of your values are non-negotiable*, with the protected-≠-expensive test (R2b) that the price scale alone can't make. It's the rare case where a measurement-hygiene rule (never finitize a "never") turns out to have been quietly storing a second construct the whole time.

## 6. Open design questions
- **Q1.** Taboo-marker phrasing that captures outrage/illegitimacy without *leading* the participant to it (a demand-characteristics risk).
- **Q2.** Distinguishing genuine protection from cheap talk before H-A2 exists — any in-instrument proxy (e.g., consistency of the "never" across re-poses, response latency on the refusal)?
- **Q3.** Quantity-insensitivity within a finite ladder — how high must the top rung go to make a "never" meaningful, without inducing distress?

## 7. Downstream changes this design unblocks
1. `scoring.md §26` — `P_i` from censored responses, `taboo`, R2a/b/c + discriminant
2. `pre-registration.md` §6 — R2 secondary (set + distinctness; cheap-talk validation Phase-2)
3. runtime — the gentle post-"never" taboo marker
4. `research-program.json` — the R2 card (design-stage)
5. `validity-threats.md` — a cheap-talk / hypothetical-"never" over-reporting row
6. `DECISIONS.md` — the R2 lock (Dave's call)

## 8. Relationship to the other branches
- **The cost-of-virtue tail.** R2 is the censored `"never"` tail of §4/§13.2, reinterpreted — the price probe's refusals are the protected-value data.
- **H-A2.** Validates which professed "never"s survive real stakes (the cheap-talk filter) — R2's Phase-2 leg.
- **H12.** Sacred-value double standards: do people demand others honor *their* protected values?
- **The inventory.** Orthogonal — protectedness is a negotiable-vs-not axis beside importance-ranking (R2c).

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 2" R2; [`scoring.md`](scoring.md) §4.1 (the `never` response), §13.2/§13.3 (the censoring discipline that preserved it — R2's substrate), §8 — where §26 lands
- [`h-a2-real-stakes.md`](h-a2-real-stakes.md) (the cheap-talk validator), [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md) (sacred-value double standards), [`concept.md`](concept.md) (no-composite; cost-of-virtue framing)
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`validity-threats.md`](validity-threats.md) (the cheap-talk row), [`pre-registration.md`](pre-registration.md) §6
