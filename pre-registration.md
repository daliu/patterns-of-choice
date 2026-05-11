# MVP-1 Pre-Registration — Draft Template

**Status:** Draft. Filing-ready template for OSF submission *before* recruitment opens. Not yet locked. Phase-1 measurement-validation only — no intervention claims.

This document follows the OSF Standard Pre-Registration template. Sections in *italics* are placeholder until co-PI is recruited and final ladder/scenario corpus is locked.

---

## 1. Study information

**Title:** Patterns of Choice — Measurement validation of a longitudinal revealed-vs-stated values instrument (Phase 1).

**Authors:** *TBD — academic co-PI required for IRB; corresponding author TBD.*

**Description.** A pre-registered evaluation of the psychometric properties (construct, convergent, discriminant, retest reliability) of a novel longitudinal instrument that captures revealed ethical preferences across four domains (truth-telling, resource allocation, in-group/out-group, reciprocity-cooperation) via repeated low-stakes scenarios and a separately-captured stated-values inventory. No intervention is administered. No causal claim is made.

---

## 2. Design plan

**Study type.** Observational, single-arm, longitudinal (8 weeks of daily-cadence sessions).

**Blinding.** None at the participant level (open-label measurement). Analyses pre-registered.

**Study design.** Each participant completes:
- Onboarding sessions 1–3: card-sort × 3 layers, 30 forced-choice pairwise comparisons across the 3 layers, 2 free-text story prompts.
- Sessions 4–56: daily-cadence ~5-minute sessions covering one of the 4 domains each, with a quick-fire round + core narrative + cost-of-virtue probe + optional reflection.
- HEXACO-60 administered at baseline (session 1) and at week 8.
- Optional informant-report wave at week 4: ≥2 informants per consenting participant rate the participant on HEXACO-60 (facet-level), with romantic partner + coworker as the canonical pair.

**Randomization.** Scenario rotation order randomized per participant from a fixed seed (logged for reproducibility). Pairwise pair order randomized per participant per layer.

---

## 3. Sampling plan

**Recruitment.** Prolific (or equivalent paid panel) for English-speaking adults 18+. Demographic stratification target: age (3 strata), gender (2+ self-identified), education (3 strata). Exclusion of participants who fail two or more of three pre-screened attention checks.

**Sample size.** n = 200.

**Sample-size rationale.** Powered for the primary convergent-validity hypothesis (r ≥ 0.25 against HEXACO honesty-humility) at α = 0.05 two-tailed with 80% power, the required N is 121; n = 200 gives ≥ 95% power at the pre-registered effect size and tolerates ~30% attrition with retained 80%+ power on the per-protocol sample. For the informant-report convergence hypothesis (r ≥ 0.25), with anticipated ~50% opt-in rate (n = 100 with informants), power is ~85% — adequate but not generous; results for the informant hypothesis will be reported with effect size and 95% CI rather than null-hypothesis-test framing.

**Stopping rule.** Recruitment closes at n = 220 enrolled (anticipating ~10% baseline drop-off before session 4), or when 200 participants reach session 28, whichever comes second. No interim analyses; no early-stopping rule.

---

## 4. Variables

**Manipulated.** None.

**Measured (primary).**

| Variable | Operationalization | Source |
|---|---|---|
| Revealed score per domain | Aggregated tag-weighted choice score from quick-fire + narrative sessions in that domain | `scenarios/` JSON + analyzer (pre-registered tag schema) |
| Stated score per domain × per layer | Bradley-Terry posterior on `inventory/pairwise-pairs.json` data | Analysis script (pre-registered) |
| Per-domain gap | (stated_aspirational − revealed) standardized within domain | Derived |
| Cost-of-virtue break-point per domain | First-accept rung from `cov-*-001.json` probe; `Inf` if no break | Probe response |
| HEXACO-60 honesty-humility, facet-level | Standard Lee & Ashton scoring | Lee & Ashton 2018 |
| Informant HEXACO-60 honesty-humility, facet-level | Same instrument, informant-rated | Standard administration |

**Measured (secondary / exploratory).** Response time per choice; inventory drift trajectory; story-prompt LLM tag distribution; observed-vs-anonymous comparison (no observer mode in MVP-1; this is exploratory placeholder for MVP-2).

---

## 5. Analysis plan

**Statistical software.** R 4.x with `psych`, `lavaan`, `BradleyTerry2`, `irr`. Analysis code committed to the repo at `analysis/` before unblinding.

**Models.**
- Construct validity: confirmatory factor analysis (CFA) on revealed scores across the 4 domains, comparing the pre-registered 4-factor solution against (a) a 1-factor (g) solution and (b) a 2-factor (cooperative-vs-self-interested) solution. RMSEA, CFI, TLI reported; pre-registered acceptance: RMSEA ≤ 0.08, CFI ≥ 0.90 for the 4-factor model with comparative ΔCFI ≥ 0.02 over alternatives.
- Convergent validity: Pearson correlations with 95% bootstrap CIs (10,000 resamples). Pre-registered direction is positive for HEXACO H × revealed truth-telling; null hypothesis test reports against r = 0 with the pre-registered support threshold at lower-95%-CI ≥ 0.15 (a more conservative inferential anchor than NHST p < 0.05).
- Reliability: Two-week split-half on weeks 1–2 vs. weeks 3–4 within-user revealed scores (Pearson r per domain), and Cronbach's α / McDonald's ω on quick-fire items within domain.
- Discriminant validity: Pearson correlations with Big-5 neuroticism (administered as 8-item subscale from BFI-2 at baseline); pre-registered ceiling r ≤ 0.40.

**Transformations.** Response times log-transformed before analysis; revealed scores standardized within domain before gap computation; informant ratings averaged across informants per participant (when ≥ 2 are available).

**Inference criteria.** Pre-registered:
- *Primary*: convergent validity HEXACO H × revealed truth-telling — lower 95% bootstrap CI ≥ 0.15.
- *Primary*: per-domain test-retest reliability — point estimate r ≥ 0.60.
- *Primary*: 4-factor CFA acceptable per thresholds above.
- *Secondary*: informant convergence — point estimate r ≥ 0.20 (lower 95% CI not required).
- *Secondary*: cost-of-virtue probe test-retest — point estimate r ≥ 0.50.
- *Secondary*: discriminant — Big-5 neuroticism correlation r ≤ 0.40.

**Data exclusion.** Pre-registered:
- Participants with < 14 completed sessions (out of 53 protocol sessions) excluded from primary analyses (sensitivity-analyzed at < 7 and < 21).
- Sessions with median response time < 2 s for the quick-fire round excluded as inattentive-responding (~bottom 1% of expected distribution).
- Attention-check failures during onboarding result in exclusion before enrollment, not afterwards.

**Missing data.** Item-level missingness handled with full-information maximum likelihood (FIML) for the CFA; pairwise correlations for the convergent-validity step (since FIML is not standard for non-model-based correlations). Imputation is not used.

**Exploratory.** All response-time analyses, all per-rung cost-of-virtue trajectories (vs. just first-accept-rung), all LLM-coded story-prompt analyses, all subgroup analyses, all moderator analyses. These are reported clearly as exploratory; no inferential thresholds applied.

---

## 6. Hypotheses

**Primary** (pre-registered with stop-on-failure status for instrument validation):

| ID | Hypothesis | Source |
|---|---|---|
| H1 | The 4-domain factor structure of revealed scores fits the data (RMSEA ≤ 0.08, CFI ≥ 0.90) | Concept doc taxonomy |
| H2 | Revealed truth-telling correlates with HEXACO honesty-humility (lower 95% CI ≥ 0.15) | Lit pass 2 |
| H3 | Per-domain test-retest reliability r ≥ 0.60 between weeks 1–2 and weeks 3–4 | Concept doc validation plan |

**Secondary** (reported with effect sizes; not used to gate validation):

| ID | Hypothesis | Source |
|---|---|---|
| H4 | Informant H rating correlates with revealed truth-telling (r ≥ 0.20) | Connelly & Ones 2010 anchor |
| H5 | Cost-of-virtue test-retest r ≥ 0.50 | Concept doc |
| H6 | Stated–revealed correlation falls within 0.20 ≤ r ≤ 0.60 (the "gap is real but not random noise" range) | Design hypothesis |
| H7 | Big-5 neuroticism × revealed scores r ≤ 0.40 | Discriminant validity |

**Falsification thresholds.** Primary H1–H3 failing constitutes a failure of measurement validation. If H2 fails (lower CI < 0.15) but H1 and H3 pass, the result is reported as a "measures something real and reliable but does not converge with HEXACO H at the predicted level" finding — itself useful, with the secondary analyses interpreted as exploratory hypothesis-generation for MVP-2.

---

## 7. Out of scope for this pre-registration

- Any intervention claim. MVP-1 is measurement-only. Intervention efficacy is MVP-2, separately pre-registered.
- Cross-cultural generalization. The sample is English-speaking adults via Prolific; no claim is made about non-WEIRD generalizability. Pre-registered as a Phase-3+ question.
- Long-term stability beyond 8 weeks. Test-retest is week 1–2 vs. week 3–4. Anything longer is exploratory.
- The intervention layer described in `concept.md` — gap-to-plan translator, scenario rehearsal mode, identity language, etc. — is not deployed or measured.

---

## 8. Open-science commitments

- This document is filed at OSF under Project DOI *TBD* before recruitment opens.
- Analysis code, scenario corpus, inventory items, and codebook are public at github.com/daliu/patterns-of-choice/ before recruitment.
- Aggregate (participant-de-identified) results published to OSF within 60 days of analysis lock.
- Pre-print on PsyArXiv within 90 days of analysis lock, regardless of outcome direction. Negative-result findings have the same publication commitment as positive ones.

---

## 9. Limitations explicitly acknowledged

- The instrument format (narratively-embedded daily-puzzle) has no direct lab→field validation precedent. MVP-1 is the first such validation; results should be interpreted accordingly.
- Self-selected participants from a paid panel are systematically non-representative; effects observed here will need replication in different recruitment frames before any generalization.
- The HEXACO H convergent-validity target (r ≥ 0.25) is below classical "good convergent validity" thresholds (typically 0.40+) because the literature meta-analytic ceiling for moral-construct-vs-real-behavior correlations is around 0.20–0.30 (Thielmann 2020).
- The cost-of-virtue probe loyalty domain (cov-ingroup-001) is flagged in `literature/ecological-validity-positive.md` as having no direct lab→field validation; its inclusion in MVP-1 is partly to generate baseline data on the probe itself, not to test it against external criterion.

---

## 10. Authorship credit

Co-authors will be named at lock. Any post-lock changes to this document are tracked as PRs against this file with rationale; substantive changes constitute *deviations from pre-registration* and are reported as such in the final write-up.
