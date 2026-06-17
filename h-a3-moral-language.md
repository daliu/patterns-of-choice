# H-A3 — The moral-language channel (what you say vs. what you do)

**Status:** Design proposal, drafted 2026-06-16 (extension loop, iteration 7). Develops branch **A3** of [`measurement-avenues.md`](measurement-avenues.md) — an A-series modality. **MVP-1 exploratory**, *gated on the LLM-coding reliability prerequisite* (κ ≥ 0.70, `scoring.md` §5.4) — until that's met it is descriptive-only, like the story-prompt channel it extends. The lock is Dave's call.

**Provenance.** Branch A3. PoC already collects free-text (the story-prompt channel, `scoring.md` §5.4, currently a per-domain "spontaneous mention" frequency, exploratory) but reads almost nothing from it. H-A3 turns that text into a full **moral-language profile** — *what a person spontaneously moralizes about, in what moral vocabulary, framed how* — and contrasts it with what they actually do. The concept doc's own claim is the seed: "what people surface unprompted is more predictive than what they check on a list." This is a **third channel on values**, distinct from both the elicited-stated inventory (rank these values) and revealed behavior.

---

## 1. The hypothesis statement

**H-A3 (proposed `pre-registration.md` §6, exploratory until the coding gate is met).**

*A person's spontaneous moral language forms a reliable profile that is distinct from both their elicited-stated values and their revealed behavior; and the gap between what they talk about morally and what they do (the "talk–walk" gap) is a meaningful signal in its own right.*

### 1.1 Measurement primitive (a third ordering)

From free-text (story prompts §5.4 + optional journaling), each response is LLM-coded into moral content. Three within-person language features:
```
lang_freq_i(d)   = per-domain spontaneous-mention frequency (the existing §5.4 read)
foundation_i(f)  = invocation rate per moral foundation f (care/fairness/loyalty/authority/sanctity/liberty), MFD-coded
framing_i        = universalizing : particularizing ratio (abstract-principle vs concrete-relational language)
```
The **language ordering** `L_i` ranks the person's domains by `lang_freq_i(d)`. It joins the two orderings `scoring.md` §13.4 already builds — the **stated** order `S_i` (card sort) and the **revealed** order `R_i` (behavior) — giving three orderings and three pairwise concordances. H-A3 *extends §13.4*, reusing its exact discipline (Kendall tau-b, the 3-band ordinal output, `|C| ≥ 3`, within-person uncertainty, **never a bare scalar**, and the §13.5 prohibition on forced cross-channel correlations).

### 1.2 H-A3a — the moral-language profile is reliable

Split-window test–retest of `L_i` (and the `foundation_i` profile): lower 95% bootstrap-CI bound ≥ **0.40**. *Conditional on the κ ≥ 0.70 coding gate (§1.5);* below it, reliability is confounded with coding noise and the test is not interpretable.

### 1.3 H-A3b — language is a distinct third channel

The three pairwise concordances — `S↔R` (the existing §13.4 stated–revealed gap), `L↔R` (talk–walk), `L↔S` (talk vs. rank) — are **dissociable**: not all ≈ 1, and `L` adds variance beyond `S` and `R`. Operationally, the `L↔R` and `L↔S` concordances each have a non-degenerate distribution across participants, and `L_i` is not recoverable from `S_i` + `R_i` (a person can rank fairness #1 on the card sort, *talk* mostly about loyalty, and *act* on neither). If `L` collapses onto `S` or `R`, the channel adds nothing — that is the falsification.

### 1.4 H-A3c — the talk–walk gap (and the grandstanding signature)

The `L↔R` concordance is the **talk–walk gap** — moralized-about vs. acted-on, per the §13.4 machinery (3-band ordinal + raw orderings + flagged fragile flips). Its diagnostic edge: a person with **high moral-language volume** *and* **low `L↔R` concordance** fits the **moral-grandstanding** signature (Tosi & Warmke) — moral talk doing self-presentational rather than action-guiding work. Exploratory links: does the talk–walk gap track H12 (the self–other double standard) or H9 (self-prediction error)? Reported exploratory.

### 1.5 N=1, the coding gate, value-neutrality, language ≠ value

- **N=1.** The profile and the three concordances are within-person and ordinal (§13.4-style) — reveal-eligible (descriptive: "you talk most about fairness, but your choices lean loyalty, and you rank honesty first"). The H-A3a/b reliability/distinctness statistics are cohort.
- **The coding gate (binding).** The *entire* channel rests on LLM-coding free-text into moral categories, which the repo already gates at **κ ≥ 0.70 vs. gold-standard manual coding** (`scoring.md` §5.4; the open prerequisite at §12 — ~200 gold codes, 50/domain × 2 raters). Until that's met, H-A3 is **descriptive/exploratory only** and folds into nothing primary. **Unlike the deterministic on-device projection, LLM coding is non-deterministic and cannot be byte-exact parity-gated** — it is an analyzer-side, reliability-gated pipeline, not part of `poc-projection.js` ↔ `analyze.py` parity (§3).
- **Value-neutrality.** More moral language is **not** better — it can be genuine engagement *or* grandstanding; the reveal describes volume and concordance, never ranks them. A large talk–walk gap is descriptive (aspiration-voiced-in-language vs. lip-service), not a verdict.
- **Language ≠ value (the core confound).** Verbally fluent / more-educated participants moralize more readily; fluency must never be read as virtue. The analysis covaries verbal output volume and flags the confound (a `validity-threats.md` row). And a participant who *declines* to moralize, or speaks in concrete-relational terms, is making a Dancy-style particularist move (already named in `concept.md`), not scoring "low" deficiently.

### 1.6 Falsification and exploratory H-A3d

Combined H-A3 = **H-A3a ∧ H-A3b** (a reliable language profile that is a distinct third channel) — *all conditional on the coding gate.* H-A3c is the diagnostic edge. Partial results published.

**Exploratory H-A3d — the three-channel MTMM (the seed for C1).** Inventory (elicited-stated), language (spontaneous-stated), and behavior (revealed) are three *methods* over the same domains; their convergent/discriminant pattern is exactly the multitrait–multimethod matrix branch **C1** will formalize. H-A3 is the channel that makes C1 possible (C1 is "gated on ≥3 channels existing" — language is the third).

---

## 2. Theoretical grounding

- **Moral Foundations Dictionary (Graham, Haidt et al.; Frimer's MFD 2.0; the eMFD).** The validated lexicon for coding moral-foundation invocation from text — the basis for `foundation_i`. (LLM coding is the modern instrument; the MFD is the construct anchor and a κ benchmark.)
- **LIWC (Pennebaker).** The broader text-as-psychological-signal tradition; the methodological precedent that word use carries stable individual differences — and its limits (fluency/volume confounds, §1.5).
- **Narrative identity (McAdams).** What people *spontaneously* narrate about themselves is diagnostic beyond what they endorse on scales — the warrant for treating spontaneous language as a distinct channel.
- **Moral grandstanding (Tosi & Warmke 2016; Grubbs et al. 2019).** The construct behind H-A3c: moral talk used for status/self-presentation, dissociable from moral action — exactly a high-volume / low-`L↔R`-concordance profile.
- **Particularism (Dancy, already in-repo).** Why concrete-relational or non-moralizing language is a legitimate style, not a deficit — the value-neutrality guard.

---

## 3. Instrument modification required

### Already in place
- The **story-prompt channel** (`scoring.md` §5.4; `inventory/story-prompts.json`; schema `(user_id, prompt_id, text, llm_coded_tags)`), currently a per-domain frequency read.
- The **§13.4 concordance machinery** (tau-b, 3-band ordinal, fragility flags) — H-A3 adds the third ordering into it.

### What needs to be added
- **A1. The MFD/foundation coding layer + framing classifier** over the free-text (LLM-coded), producing `foundation_i` and `framing_i` beyond the existing per-domain frequency.
- **A2. The κ ≥ 0.70 validation** — the gating prerequisite: ~200 gold-standard manual codes (50/domain × 2 raters) to certify the coding pipeline before any H-A3 result is more than descriptive. This is the real cost of the branch (labor, not engineering).
- **A3. More free-text prompts (light authoring)** — stable per-person language profiles need more text than the current story-prompt set yields; a modest prompt expansion (free-text, not scenarios).
- **A4. Scoring `§20` (proposed)** — `lang_freq`/`foundation`/`framing`, the third ordering `L_i`, the three pairwise concordances (extending §13.4), the §1.5 caveats. **Not parity-gated** (LLM coding is non-deterministic; it is a separately-validated pipeline, §1.5).

No new scenarios; the §16/§17 corpus is untouched (this is free-text, not scenario items).

---

## 4. Implications for existing locked decisions

**MVP-1 exploratory, gated on the coding reliability.** H-A3 inherits the story-prompt channel's status (`scoring.md` §5.4: exploratory until κ ≥ 0.70) — it cannot be a primary or even a confirmatory secondary until the coding pipeline is certified. Honest dependency, not a deferral.

**Extends, not duplicates, §5.4.** The existing channel is a per-domain frequency; H-A3 adds the foundation profile, the framing ratio, the third ordering, and the talk–walk concordance.

**Corpus untouched** (free-text + light prompt authoring, no scenarios). **Proposed `DECISIONS.md` entry (pending Dave's lock):** "Promote the story-prompt channel (§5.4) to the H-A3 moral-language profile; add the MFD/framing coding layer + the third-ordering concordance (scoring §20); keep exploratory until κ ≥ 0.70; not parity-gated (non-deterministic coding)." Considered-and-rejected: fold language into the primary stated score before the κ gate (rejected — §5.4's whole point); a bare talk–walk tau scalar (rejected — §13.4/§13.5 forbid it).

---

## 5. Why this is a research contribution

Three channels on the same values — **elicited-stated** (inventory), **spontaneous-stated** (language), **revealed** (behavior) — and the gaps among them. Self-report instruments use one; PoC already has two; H-A3 adds the third and the **talk–walk gap** (the measurable form of moral grandstanding). It extends the §13.4 within-person concordance from a two-ordering to a three-ordering object, and it is the channel that **unlocks C1** (multi-method convergence). It also models its own ceiling honestly: language is gated by coding reliability and confounded by fluency, and it says so up front.

---

## 6. Open design questions
- **Q1. Coding instrument.** MFD 2.0 / eMFD dictionary vs. direct LLM coding vs. both (LLM coding validated *against* the dictionary + human gold)? Resolve at the κ-validation step.
- **Q2. Text volume.** How much free-text yields a stable `L_i`? Pilot the prompt count against test–retest of the profile.
- **Q3. Framing operationalization.** "Universalizing vs particularizing" needs a concrete classifier (abstract-principle vs concrete-relational markers); reserve for §20.
- **Q4. Non-determinism vs reproducibility.** LLM coding can't be byte-exact reproduced; pin model + prompt + temperature=0 and report coding-version, and treat κ-vs-gold (not parity) as the reproducibility contract.

---

## 7. Downstream changes this design unblocks
1. The MFD/framing LLM-coding pipeline + the κ ≥ 0.70 gold-standard validation
2. `scoring.md §20` — `lang_freq`/`foundation`/`framing`, the third ordering, the three concordances (extending §13.4); explicitly non-parity-gated
3. `pre-registration.md` §6 — H-A3 as an exploratory channel (promotable to secondary once κ is met); the three-channel MTMM plan (feeds C1)
4. `concept.md` — promote the story-prompt channel to the moral-language profile; the language≠value + grandstanding notes
5. `inventory/` — a modest free-text prompt expansion
6. `validity-threats.md` — a CV row for the fluency/volume confound, and an LLM-coding-reliability row
7. `DECISIONS.md` — the H-A3 lock (Dave's call)

---

## 8. Relationship to §13.4, C1, H12, H9, and the inventory
- **Extends §13.4** from two orderings (stated, revealed) to three (adds language) — same machinery, one more vertex.
- **Unlocks C1.** Language is the third channel C1 (MTMM convergence) is gated on; H-A3d previews it.
- **vs H12.** Grandstanding (high talk, low walk) and hypocrisy (high demand of others, low of self) are cousins; exploratory whether they co-occur.
- **vs H9.** Does a large talk–walk gap track self-prediction error (talking a good game *and* not seeing your own slips)?
- **vs the inventory.** Elicited-stated (forced-choice ranking) and spontaneous-stated (what you bring up unprompted) are different stated channels; L↔S asks whether you talk the way you rank.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) A3, C1 (which this unlocks); [`scoring.md`](scoring.md) §5.4 (the story-prompt channel this promotes), §13.4 (the concordance machinery it extends), §12 (the κ ≥ 0.70 open prerequisite) — where §20 lands
- [`concept.md`](concept.md) ("spontaneous unprompted is more predictive"; the Dancy particularism note), [`h12-moral-hypocrisy.md`](h12-moral-hypocrisy.md) (grandstanding ↔ hypocrisy), [`h9-self-calibration.md`](h9-self-calibration.md) (talk–walk gap ↔ self-knowledge)
- [`validity-threats.md`](validity-threats.md) (fluency-confound + LLM-coding-reliability rows), [`DECISIONS.md`](DECISIONS.md) §16/§17 (corpus untouched), [`pre-registration.md`](pre-registration.md) §6
