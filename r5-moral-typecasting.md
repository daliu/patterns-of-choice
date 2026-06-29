# R5 — Moral typecasting / dyadic structure (the doer or the done-to?)

**Status:** Design proposal, drafted 2026-06-28 (extension loop, iteration 16 — Round 2's last). Develops **R5** of [`measurement-avenues.md`](measurement-avenues.md) §"Round 2". **MVP-1 exploratory, and the most speculative branch on the map** — its in-instrument operationalization is the weakest (it leans on the κ-gated language channel and would genuinely benefit from dedicated items, §3). The lock is Dave's. Honesty up front: this one is closer to a *future direction with a tentative read* than a near-ready measure.

**Provenance.** R5. Moral cognition is structured, per the Theory of Dyadic Morality (Schein & Gray 2018; Gray & Wegner 2009), around a **dyad**: a moral **agent** (the intentional doer) acting on a moral **patient** (the one acted upon, who suffers/benefits). R5 asks how a person *parses* moral scenes into that structure — do they read a situation through the **doer** (responsibility, intent, blame) or the **done-to** (harm, suffering, need)? It is the structure imposed on the scene *before* any choice, and it maps onto the long-standing **justice (agent-focused) vs. care (patient-focused)** emphasis (Gilligan 1982, already a repo reference — with the modern caveat that the orientations are an emphasis, not gendered and not a hard dichotomy).

---

## 1. The hypothesis statement

**R5 (proposed `pre-registration.md` §6, exploratory).**

*The tendency to parse moral situations through the agent (responsibility/intent) vs. the patient (harm/suffering) is a reliable individual difference (a justice-vs-care emphasis); and, more speculatively, people differ in moral typecasting — the degree to which they treat the agent and patient roles as mutually exclusive.*

### 1.1 Measurement primitive (agent/patient framing; mostly indirect)
For person *i*, the **dyadic focus** is the relative weight they put on the two poles when engaging a moral scenario:
```
agent_focus_i   = attention to the doer — responsibility, intent, blameworthiness
patient_focus_i = attention to the done-to — harm, suffering, need
dyadic_emphasis_i = agent_focus_i − patient_focus_i   (justice-leaning > 0 ; care-leaning < 0)
```
Detected — and this is the weak point R5 is honest about — primarily **indirectly**:
- **Language (A3 / `scoring.md §20`)** — agent-language (blame, responsibility, intent) vs. patient-language (harm, victim, suffering) in free-text. κ-gated.
- **Feature-weighting in choices** — whether the person's choices/justifications track the doer's intent vs. the patient's harm (e.g., intent-sensitivity vs. outcome/harm-sensitivity across matched items).
- *(Dedicated, not yet built)* role-assignment items that present the same entity as agent and as patient (the clean typecasting probe, §1.3) — which the current corpus doesn't contain.

### 1.2 R5a — dyadic focus is a reliable individual difference
Split-window test–retest of `dyadic_emphasis_i`: lower 95% CI ≥ **0.40**. (Some people read moral scenes doer-first, some done-to-first, stably.) Bootstrap per §8. *Conditional on the indirect detection (§1.1) carrying real signal — a pilot question, §6.*

### 1.3 R5b — harm-centrality (the TDM signature) and R5c typecasting (exploratory)
- **R5b — harm-centrality.** TDM holds the agent–patient dyad is the template of *all* moral judgment, rooted in perceived harm. R5b: does the person require a perceived **victim** to moralize (moralizes harm-based violations, not victimless ones), or do they moralize victimless acts via binding foundations (purity/authority)? This is distinct from A3's foundation *content* — it's about whether the **dyadic harm structure** is necessary for moralization at all. (Schein & Gray: even "harmless" violations get a *intuited* victim by the harm-focused.)
- **R5c — typecasting (exploratory).** Gray & Wegner: agent and patient are perceived as *mutually exclusive* — the powerful/blameworthy are seen as less capable of being harmed, victims as less capable of acting. R5c measures whether a person typecasts (agent XOR patient) vs. holds both. **This needs the dedicated role-assignment items the corpus lacks**, so it is exploratory / a future-items dependency, flagged as such.

### 1.4 N=1, value-neutrality, the honesty about operationalization
- **N=1.** `dyadic_emphasis_i` is within-person, reveal-eligible (descriptive: "you tend to read a moral situation through who's responsible more than who's harmed" — a justice over care emphasis). R5a/b/c are cohort.
- **Value-neutrality (load-bearing).** Agent-focus (justice/responsibility) and patient-focus (care/harm) are **emphases, not a hierarchy** — neither is the better moral lens (the Kohlberg-justice vs. Gilligan-care debate resolved toward *both are legitimate*, and the gendered framing did not hold). The reveal names the emphasis; it never ranks justice over care or vice versa.
- **Operationalization honesty (the load-bearing caveat).** R5's in-instrument detection is **indirect and the weakest of any branch** — the language channel is κ-gated and the choice-feature read is inferential; the clean typecasting probe (R5c) needs items the corpus doesn't have. So R5 is reported as *exploratory*, and its reliability (R5a) is itself contingent on the detection carrying signal. This branch is the honest edge of the map: a real, validated construct (TDM is well-supported) whose *measurement here* is the most provisional.

### 1.5 Falsification and exploratory
Combined R5 (exploratory) = **R5a** (a reliable, detectable dyadic emphasis). R5b/c are further-exploratory and partly future-items-dependent. A null R5a (no reliable emphasis detectable from the indirect channels) would mean the construct, though real, is **not measurable in this instrument without dedicated items** — itself the honest finding. **Exploratory cross-links:** R5 ↔ A3 (agent/patient *language* is the detector); R5 ↔ H11 (does patient-focus widen the moral circle?); R5 ↔ R3 (blame-attribution disengagement is an agent-focused move).

---

## 2. Theoretical grounding
- **Gray & Wegner 2009 (moral typecasting, JPSP); Schein & Gray 2018 (Theory of Dyadic Morality, PSPR); Gray, Young & Waytz 2012 (mind perception is the essence of morality).** The agent–patient dyad as the structure of moral cognition; typecasting as the mutual-exclusivity of the roles; harm as the template — R5's well-supported theoretical core.
- **Gilligan 1982 (already a repo reference).** The care (patient/harm-focused) vs. justice (agent/rights-focused) *emphasis* — cited for the individual-difference framing, **with** the modern caveat (an emphasis, not gendered, not a dichotomy). The construct's measurability-as-an-emphasis, not the discredited gender claims.

## 3. Instrument modification required
- **Already in place (indirect).** The A3 free-text channel (`scoring.md §20`) for agent/patient language; the existing choices for intent-vs-harm feature-weighting.
- **A1 (the real need).** **Dedicated role-assignment items** — present the same entity as agent and as patient — to measure typecasting (R5c) cleanly. The corpus lacks these; this is R5's main unbuilt dependency.
- **A2.** Scoring `§30` (proposed): `agent_focus`/`patient_focus`/`dyadic_emphasis`, R5a, the R5b harm-centrality read, and (pending the items) R5c. Inherits A3's κ gate.
- No new domains required for R5a/b; R5c needs the new items.

## 4. Implications for existing locked decisions
**MVP-1 exploratory, weakest operationalization, future-items-dependent for the sharpest part.** **Carded** (the doer-vs-done-to facet, honestly labeled most-exploratory). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add R5 (dyadic moral structure) as an *exploratory* secondary; `dyadic_emphasis` from A3 agent/patient language + choice intent-vs-harm weighting (scoring §30); R5b harm-centrality; R5c typecasting deferred to dedicated role-assignment items; value-neutral (justice/care emphasis, not a hierarchy); one design-stage card." Considered-and-rejected: claiming the gendered care/justice account (rejected — didn't replicate); a confirmatory (non-exploratory) status (rejected — the operationalization is too provisional); ranking justice over care or vice versa (rejected — value-neutrality).

## 5. Why this is a (provisional) contribution
R5 reaches for the one thing none of the other branches touch: the **structure** a person imposes on a moral scene — *who is the doer and who the done-to* — which is, per dyadic morality, the template beneath every judgment. Even read indirectly, a stable agent-vs-patient emphasis (the justice/care lens) is a real individual difference with a long literature. R5 is honest that the instrument can presently only glimpse it, and names exactly the dedicated items that would measure it cleanly — so it closes the map not by overclaiming, but by marking precisely where the next real work is.

## 6. Open design questions
- **Q1.** Does the indirect detection (agent/patient language + intent-vs-harm weighting) carry reliable signal, or does R5 genuinely require the dedicated role-assignment items before it can be measured at all? (The pilot decides whether R5a is even testable now.)
- **Q2.** Separating dyadic *structure* (R5) from foundation *content* (A3) and from mere *detection* (R4) — the discriminant among the three perceptual/structural branches.
- **Q3.** The typecasting items (R5c) — designing role-assignment probes that don't lead the participant.

## 7. Downstream changes this design unblocks
1. `scoring.md §30` — `dyadic_emphasis`, R5a, R5b harm-centrality; R5c pending items
2. `pre-registration.md` §6 — R5 *exploratory*, with the operationalization caveat explicit
3. `scenarios/` — (future) dedicated agent/patient role-assignment items for R5c
4. `research-program.json` — the R5 card (design-stage, most-exploratory)
5. `validity-threats.md` — the indirect-operationalization row (R5's measurability is the most provisional)
6. `DECISIONS.md` — the R5 lock (Dave's call)

## 8. Relationship to the other branches
- **A3.** Agent/patient *language* is R5's primary (indirect) detector — R5 reads the A3 corpus for the dyadic structure, distinct from A3's foundation content.
- **R4.** Detection (do you notice morality?) vs. structure (how do you parse the dyad?) — the three perceptual/structural branches (R4 detection, A3 content, R5 structure) need careful discriminant.
- **H11.** Patient-focus (care/harm) may predict a wider moral circle; agent-focus a narrower, responsibility-gated one.
- **R3.** Blame-attribution disengagement is an agent-focused move — the dark side of agent-focus.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) §"Round 2" R5 (the map's last item); [`h-a3-moral-language.md`](h-a3-moral-language.md) (the agent/patient-language detector + the shared κ gate), [`r4-moral-attentiveness.md`](r4-moral-attentiveness.md) (detection vs. structure), [`h11-moral-circle-radius.md`](h11-moral-circle-radius.md) (care-focus ↔ wider circle), [`r3-moral-disengagement.md`](r3-moral-disengagement.md) (blame-attribution = agent-focused)
- [`concept.md`](concept.md) (Gilligan in references; the care/justice frame), [`scoring.md`](scoring.md) §20 (language channel), §8 — where §30 lands
- [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus; R5c needs new items), [`validity-threats.md`](validity-threats.md) (the indirect-operationalization row), [`pre-registration.md`](pre-registration.md) §6
