# C1 — Multi-method convergence (the MTMM capstone)

**Status:** Design proposal, drafted 2026-06-17 (extension loop, iteration 8). Develops branch **C1** of [`measurement-avenues.md`](measurement-avenues.md) — a *meta* method, not a measurement modality. **Unblocked** now that A3 (`h-a3-moral-language.md`) supplies a third channel. **Cohort-level for the matrix; N=1 for the per-person convergence profile.** Not a public "facet" card (it's the framework behind the facets — see §4). The lock is Dave's.

**Provenance.** Branch C1, and the capstone of the whole branch-out. The avenues map's founding bet was that adding channels *whose errors are uncorrelated with the scenario layer's* turns the instrument from one modality into a triangulating set. C1 is where that bet is **tested and cashed**: it treats the channels as a multitrait–multimethod (MTMM) matrix (Campbell & Fiske 1959), asks whether they actually converge on the moral *constructs* (vs. just sharing *method* artifacts), and — its deepest contribution — **unifies every gap the instrument already measures as one structured object**: the stated–revealed gap (§6), the talk–walk gap (H-A3), the self–other double standard (H12), self-vs-predicted (H9), self-vs-informant (H-A1), hypothetical-vs-real (H-A2) are all *off-diagonal cells of the same matrix*.

---

## 1. The hypothesis statement

**C1 (proposed `pre-registration.md` §6, secondary; staged as channels come online).**

*Across channels, the moral constructs converge (same construct measured different ways correlates — the multi-channel bet pays off); the convergence survives method change better than method-shared variance (discriminant); and no single channel's method variance dominates. Where channels systematically diverge, the divergence is a reliable signal (a real gap), not method noise.*

### 1.1 The MTMM object

**Traits** = the moral constructs (the four MVP-1 domains: truth-telling, allocation, in-group, reciprocity). **Methods** = the channels measuring them:
- *elicited-stated* — the inventory (card-sort / Bradley-Terry, §5)
- *revealed* — scenario behavior (§2–3)
- *external anchor* — HEXACO honesty-humility (the H2/H4 convergent anchor)
- *spontaneous-language* — H-A3 (§20; exploratory, κ-gated)
- *self-prediction* — H9 (a meta-channel)
- *informant* — H-A1 (Phase-2); *real-stakes* — H-A2 (Phase-2)

The trait×method matrix has the three Campbell–Fiske regions: **monotrait-heteromethod** (same construct, different channels — should correlate: *convergent*), **heterotrait-heteromethod** (different construct, different channels — should be lowest), **heterotrait-monomethod** (different constructs, same channel — reveals *method variance*).

### 1.2 C1a — convergent validity across methods

Same construct, different channels, correlate:
```
C1a:  per construct, lower 95% bootstrap-CI bound of the mean monotrait-heteromethod correlation > 0
```
Threshold honestly modest — cross-method moral correlations run low (the Thielmann ρ̂ ≈ 0.20 ceiling that already set H2's bar, `DECISIONS.md` §11; and a method-change penalty on top). Bootstrap per `scoring.md` §8. This is the test of the **branch-out bet**: if channels don't converge on constructs, the multi-channel strategy measured *methods*, not morality (see §1.6 falsification).

### 1.3 C1b — discriminant validity / the method-robustness map (the new signal)

The construct signal must survive method change better than method-shared variance:
```
C1b:  per construct, monotrait-heteromethod > heterotrait-heteromethod (the trait correlates across channels
      more than unrelated traits do) AND > the construct's heterotrait-monomethod (it survives method change
      better than the channel's method variance) — Campbell & Fiske's criteria.
```
The output is the **method-robustness map**: per construct, *method-robust* (channels agree — a real trait) vs. *method-bound* (only shows up in one channel — likely an artifact of elicited choice). This is C1's new deliverable: it tells you which of the instrument's readings are trustworthy traits and which are method ghosts.

### 1.4 C1c — method variance is bounded

No single channel's method-shared variance swamps trait variance:
```
C1c:  for each channel, mean heterotrait-monomethod correlation < the channel's mean monotrait-heteromethod
      (i.e., the channel shares less variance across unrelated traits than it shares with the same trait elsewhere)
```
This flags the artifact-prone channels (e.g., the forced-choice inventory may carry acquiescence/desirability variance; story-language may carry verbal-fluency variance, the H-A3 §1.5 confound). Anchor: Podsakoff et al. 2003 (common-method variance).

### 1.5 The per-person convergence profile (N=1) — and gaps-as-signal

The cohort matrix (C1a–c) validates the architecture. The **reveal-facing** object is per-person: the matrix of pairwise channel concordances among *that person's own* channels — the `scoring.md` §13.4 stated-vs-revealed concordance, generalized to every channel-pair the person has data for (stated↔revealed, language↔revealed, predicted↔revealed, …). It honors §13.4/§13.5 exactly: each pair is a 3-band ordinal read with `|C| ≥ 3`, within-person uncertainty, **never a composite "consistency score"** (the §13.5 prohibition on a forced single-subject cross-channel scalar holds — C1 reports the *set* of pairwise concordances, not one number).

This is the unification: **the instrument's gaps are this matrix's off-diagonals.** The stated–revealed gap (§6), talk–walk (H-A3), self–other (H12), predicted–actual (H9), self–informant (H-A1), hypothetical–real (H-A2) are all specific channel-pairs. C1's job is to certify *which* divergences are reliable (real gaps worth reflecting on) vs. method artifacts (to discount) — turning the whole gap-zoo into one principled structure: convergence where it's a trait, structured divergence where it's a gap.

### 1.6 Falsification and staging

C1 can **falsify the multi-channel strategy**: if C1a fails (channels don't converge on constructs), the branch-out bet didn't pay — the instrument has many methods measuring method, and the honest report is that the channels are not interchangeable measures of shared traits (still publishable, and it would refocus the project on the single best-validated channel). **Staging:** the *full* MTMM needs all channels built — in MVP-1 only elicited-stated, revealed, and the HEXACO anchor are available (a 3-method matrix), so MVP-1 runs the **partial MTMM**; language (κ-gated), informant and real-stakes (Phase-2) join the matrix as they come online. C1 is reported at whatever channel-count exists, growing toward the full matrix.

**Exploratory.** Per-construct method-robustness predicting which gaps are stable over time (the robust traits should have the most reliable longitudinal gaps); and whether method variance concentrates in the channels the §1.5/H-A3 confounds predict.

---

## 2. Theoretical grounding

- **Campbell & Fiske 1959 — the multitrait–multimethod matrix.** The foundational framework and criteria (convergent, discriminant, method variance). The whole "gap = delta between two measurements" premise of `concept.md` is a two-cell special case; C1 is the general object.
- **Eid 2000; Eid et al. 2003 — CFA-MTMM.** The modern model-based version (latent trait + method factors) that replaces eyeballing the matrix; the analysis path if n permits (§6 Q).
- **Podsakoff et al. 2003 — common-method variance.** The basis for C1c (method variance as the threat to take seriously, not assume away).
- **Westfall & Yarkoni 2016 — establishing discriminant validity is statistically harder than it looks.** The rigor caveat: naive discriminant claims (ignoring measurement error in the covariates) overstate; C1b must use error-aware comparisons. Keeps C1 honest about how strong a discriminant claim it can actually make.

---

## 3. Instrument modification required

### Already in place
- The channels themselves (the prior branches) — C1 introduces **no new data collection**; it is an analysis layer over what the other channels produce.
- The `scoring.md` §13.4 concordance machinery (the per-person profile, §1.5) and §8 bootstrap.

### What needs to be added
- **A1. Scoring `§21` (proposed)** — assemble the trait×method matrix from the per-channel per-construct scores; the C1a/b/c statistics (with error-aware discriminant per Westfall & Yarkoni); the per-person concordance-set (extending §13.4 to all channel-pairs); the partial-matrix handling (run at current channel-count). Parity-gated for the deterministic parts; the language channel enters only once κ-validated.
- **A2. A channel registry** — a small declared list of which channels are live (and at what validation status), so the matrix is assembled reproducibly and the partial-vs-full staging is explicit.

No new scenarios; corpus untouched.

---

## 4. Implications for existing locked decisions

**Analysis layer, no new collection.** C1 reuses every channel's existing output. **Cohort-level** for the matrix (cross-person correlations); **N=1** for the per-person concordance profile (§1.5). MVP-1 runs the **partial MTMM** (3 methods available); it grows as channels come online.

**No public "facet" card.** Unlike H9–H12 / the moral-360 / the language channel, C1 is not a self-knowledge *facet* a user would browse — it's the *framework behind* them. So it gets **no `research-program.json` card** (the manifest is for facet cards). Its public expression is the site's existing "many views of the same choices" synthesis and the validity section (where the real-stakes keystone also lives): *we measure your morality several ways and the disagreements are the interesting part — and we've checked which disagreements are real.* (Same call as H-A2, which went to the validity section, not the grid.)

**Proposed `DECISIONS.md` entry (pending Dave's lock):** "Add C1 (MTMM convergence) as a secondary analysis layer; partial matrix at current channel-count, growing to full; scoring §21; cohort matrix + N=1 concordance profile; no public card; no new collection." Considered-and-rejected: a single per-person "coherence score" (rejected — §13.5); waiting for all channels before any MTMM (rejected — the partial matrix is informative now and pre-registers the growth path).

---

## 5. Why this is a research contribution

C1 is what makes the multi-channel instrument *more than the sum of its channels*. It (a) **tests the branch-out bet** (do the channels converge on traits, or just share methods?), (b) produces the **method-robustness map** (which moral readings are real traits vs. elicited-choice artifacts — a thing single-method instruments cannot ask), and (c) **unifies the instrument's entire gap-vocabulary** — stated–revealed, talk–walk, self–other, predicted–actual, self–informant, hypothetical–real — as off-diagonals of one matrix, with a principled rule for which gaps are signal. The project's core insight ("the actionable signal is the delta between two measurements") becomes a general, validated structure rather than a series of ad-hoc pairs.

---

## 6. Open design questions
- **Q1. CFA-MTMM vs. Campbell–Fiske inspection.** The model-based latent-trait/method-factor approach is stronger but needs n and identification; at n=200 with few methods it may not identify. Provisional: Campbell–Fiske correlational matrix as primary, CFA-MTMM as a sensitivity analysis if it converges.
- **Q2. How many channels for a stable matrix?** Three methods is the minimum honest MTMM; the matrix sharpens as channels (language, informant, real-stakes) come online. Pre-register the growth path, not a fixed matrix.
- **Q3. Error-aware discriminant.** Per Westfall & Yarkoni, naive discriminant comparisons overstate; specify disattenuated or model-based comparisons so C1b doesn't over-claim.
- **Q4. Cross-method standardization vs. the unit discipline.** The matrix needs comparable scales, but §13.5 forbids forcing different-unit channels onto one scale for *within-person* reads; the *cohort* matrix uses correlations (scale-free) — keep the two faces' standardization separate.

---

## 7. Downstream changes this design unblocks
1. `scoring.md §21` — the trait×method matrix assembly, C1a/b/c (error-aware discriminant), the per-person concordance-set (extends §13.4), partial-matrix staging
2. `pre-registration.md` §6 — C1 as a secondary analysis layer, with the channel-count growth path
3. a channel registry (which channels are live + validation status)
4. `concept.md` — frame the gap insight as the MTMM special case it is; the method-robustness map as an output
5. `validity-threats.md` — C1 is the formal answer to "is this measuring traits or methods?"; method-variance (C1c) as a named, tested threat
6. `DECISIONS.md` — the C1 lock (Dave's call)

---

## 8. Relationship to every prior branch (C1 is the capstone)
- **Unifies the gaps.** §6 stated–revealed, H-A3 talk–walk, H12 self–other, H9 predicted–actual, H-A1 self–informant, H-A2 hypothetical–real = off-diagonal cells of C1's matrix. C1 certifies which are reliable.
- **Validates the branch-out.** The avenues map's premise (uncorrelated-error channels triangulate) is exactly C1a's convergent test.
- **Depends on the channels.** Inventory, revealed, HEXACO (MVP-1); language (H-A3, κ-gated); informant (H-A1), real-stakes (H-A2) — Phase-2. C1 grows with them.
- **Honors the disciplines.** No composite score (§13.5); error-aware discriminant (Westfall & Yarkoni); cohort matrix vs N=1 profile kept distinct.

## Cross-references
- [`measurement-avenues.md`](measurement-avenues.md) C1 (the capstone of the map); every `h*.md`/`h-a*.md` branch (the channels it integrates)
- [`scoring.md`](scoring.md) §6 (the gap = a two-cell MTMM), §13.4 (the per-person concordance machinery C1 generalizes), §13.5 (no composite), §8 (bootstrap) — where §21 lands
- [`concept.md`](concept.md) (the "delta between two measurements" insight C1 generalizes), [`DECISIONS.md`](DECISIONS.md) §11 (the modest cross-method threshold precedent), §16/§17 (corpus untouched)
- [`validity-threats.md`](validity-threats.md) (traits-vs-methods; method variance), [`pre-registration.md`](pre-registration.md) §6
