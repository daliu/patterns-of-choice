# Design Decisions

A running log of the load-bearing design choices for patterns-of-choice. Format is lightweight ADR (Architecture Decision Record): each entry has the question, the decision, the rationale, and what was considered and rejected. Locked decisions are marked; open ones are flagged for revisit.

Append-only. Older decisions remain in place even when revisited; revisits get new entries with cross-references.

---

## 1. Naming

**Question.** What should the project be called?

**Decision.** `patterns-of-choice` (Decision date: 2026-05-10).

**Rationale.** The original working name was "character-lab," which collided with Angela Duckworth's nonprofit at characterlab.org. The lit-review agent caught the collision after initial commits. "Patterns of choice" echoes the framing that opened the design conversation ("character and values are a series of decisions") and has no known major-org collision.

**Considered and rejected.** "values-mirror" (good but Mirror is overloaded in tech); "character-lab" (Duckworth); "revealed-values" (accurate but workmanlike); "value-gap" (captures the central insight but reads as adversarial).

**Status.** Locked.

---

## 2. Scope of MVP-1

**Question.** What's the smallest deliverable that meaningfully tests the project's premise?

**Decision.** A measurement-only validation study: instrument psychometrics, no intervention claim. n=200, 8-week protocol, four domains.

**Rationale.** The two claims in `concept.md` (measurement works; intervention works) need separate validation. Stacking them is a category error — you can't interpret an intervention effect if the underlying measurement isn't shown to work. MVP-1 tests Claim 1; MVP-2 builds on it.

**Considered and rejected.** A combined measurement+intervention MVP that would have produced "results" faster but at the cost of being unable to interpret them. Also rejected: an even smaller pilot (n=50) — too underpowered for the convergent-validity hypothesis at the literature's expected effect sizes.

**Status.** Locked.

---

## 3. Domain selection for MVP-1

**Question.** Which of the 10 proposed domains in `concept.md` go in MVP-1?

**Decision.** Truth-telling, resource-allocation, in-group/out-group, reciprocity-cooperation (4 of 10).

**Rationale.** These have the strongest existing literature anchors and the cleanest behavioral operationalizations. Specifically: Abeler 2019 meta on honesty stakes; Engel 2011 dictator-game meta; Cikara/Bruneau parochial-empathy; Axelrod-Berg-Karlan trust-and-cooperation. They also avoid the formats that are *most* contested for ecological validity.

**Deliberately excluded for MVP-1.**
- **Harm tradeoffs (trolley-class)** — Bostyn et al. 2018 showed these have weak lab→life correspondence; including them would anchor the instrument on a contested paradigm.
- **Purity / disgust** — Haidt's most cross-culturally contested foundation (Atari 2023).
- **Speech / reputation** — harder to operationalize as 60-second scenarios.
- **Authority / rule-following** — overlaps with reciprocity at MVP scale.
- **Intergenerational / future others** — hard to operationalize at the 5-minute granularity.
- **Effort / self-sacrifice** — overlaps with resource-allocation in ways that obscure rather than clarify.

**Status.** Locked for MVP-1; revisited at MVP-2.

---

## 4. Forced-choice inventory, not Likert

**Question.** How should the user's stated values be captured?

**Decision.** Forced-choice pairwise comparison (30 pairs) plus a top-5 card sort, both repeated across three layers (current / aspirational / admired-other). Bradley-Terry posterior for analysis.

**Rationale.** Likert scales let users max all values; everyone endorses honesty, fairness, generosity, etc. Forced-choice forces real tradeoffs and produces ranked utilities with confidence intervals. The trick is the same one that makes ELO work — relative comparisons are dramatically more informative than absolute ratings.

**Considered and rejected.** Likert (cheaper, faster, weaker signal); ranking via drag-sort alone (loses the cross-value-pair information); auction-style point allocation (cognitively heavier and the analysis is messier).

**Status.** Locked.

---

## 5. Three layers, not one

**Question.** How many self-framings should the inventory capture?

**Decision.** Three: current self, aspirational self, admired other. Each run separately through card-sort and pairwise.

**Rationale.** Current alone misses aspiration. Aspiration alone inflates. Admired-other dodges self-flattery and surfaces traits users won't claim for themselves. The three together permit:
- Primary gap (aspirational − current) → growth direction
- Consistency check (admired-other − aspirational) → aspiration honesty
- Honesty check (current − admired-other) → halo / self-flattery

**Considered and rejected.** Single-layer (cheapest, but loses gap signal); five-or-more layers (e.g. parents' view, partner's view) — too much onboarding load for marginal information.

**Status.** Locked. The relational-role variant (see `inventory/relational-variant.json`) is an opt-in alternative to the trait framing within each layer.

---

## 6. Descriptive, never prescriptive

**Question.** Should the system tell the user that any choice was right or wrong?

**Decision.** No. Never. The system only describes patterns and surfaces gaps. The user defines whether a gap matters.

**Rationale.** A product that tells users what's ethically correct is no longer measuring their values — it's training them on the authors' values. That conflicts directly with the trust premise. It also smuggles a particular ethical framework into a product that should be framework-agnostic.

**Considered and rejected.** Light editorial framing of "here's what most people in your community do" — also rejected, since that's a leaderboard with extra steps. Strong framing of "here's what we recommend" — rejected most decisively; that would be the lifestyle-app version of the same idea.

**Status.** Locked as a load-bearing operating constraint (README §Operating constraints).

---

## 7. No engagement-based monetization

**Question.** How does the product sustain itself financially?

**Decision.** Subscription or donation only. No ads, no sponsorships, no data brokerage, no enterprise/employer-screening product ever.

**Rationale.** A system that maps your value gaps is a system that knows exactly how to manipulate you. Engagement-based monetization (ads, sponsored content, recommendation feeds) creates an incentive that destroys the trust premise. Enterprise screening creates a coercion surface — the moment any user can be required to take the test, the product becomes a weapon. These are non-negotiable.

**Considered and rejected.** B2B sales to corporate HR (rejected; coercion surface). Sponsored "value-aligned content" (rejected; corrupts measurement). Aggregate-data sales (rejected; even de-identified, this category of data is too sensitive).

**Status.** Locked as a load-bearing operating constraint.

---

## 8. No streaks for moral behavior

**Question.** Should the product use gamification (streaks, points, badges) to drive engagement?

**Decision.** Gamify *showing up to the system*, never the moral behavior itself. Streaks for daily sessions are fine; streaks for "honesty days" or "fair-allocation days" are not.

**Rationale.** Bénabou & Tirole 2006 *AER* signaling-model framing: when external reward enters the picture, the user (and observers) can no longer infer intrinsic commitment from the behavior, which undermines the commitment itself. This is precautionary — the empirical magnitude is contested (Deci 1971 itself failed replication in Peters et al. 2022) but the theoretical risk is real and the design cost of avoiding it is small.

**Considered and rejected.** No gamification at all (loses the engagement benefit for daily sessions); badges for moral behavior (more obviously problematic).

**Status.** Locked.

---

## 9. No social comparison

**Question.** Should users see how they compare to others (anonymously or otherwise)?

**Decision.** No. No leaderboards, no percentile rankings, no "more honest than 60% of users."

**Rationale.** Ethics is not a competition. Surfacing comparative data turns the product into a status-game and pulls user behavior toward what is socially-rewarded rather than what they actually value. Also: the comparison would itself be a measurement on a contested instrument; reporting it would lend false precision.

**Considered and rejected.** Anonymous percentile feedback (still status-inducing); cohort comparisons of the user against their own past self (acceptable — that's just longitudinal feedback, not social).

**Status.** Locked.

---

## 10. Local-first data architecture

**Question.** Where do user-generated data (choices, inventory responses, story prompts) live?

**Decision.** Local-first by default; cloud sync is opt-in and end-to-end encrypted; no training on user data ever; user can delete the profile and everything is gone.

**Rationale.** A profile of someone's moral compromises is more sensitive in a leak than financial data. Threat model includes employers, partners, governments, future-self in a fragile state, and ML companies training on it. Local-first removes the central honey-pot. E2E encryption for opt-in sync addresses the cohort-validation use case without re-introducing the honey-pot.

**Considered and rejected.** Cloud-first with optional offline (the consumer-app default; rejected for this category). Pure-local with no sync at all (rejected — the validation cohort needs centralized data, and many users would want sync across their devices).

**Status.** Locked.

---

## 11. Convergent-validity threshold

**Question.** What r against HEXACO honesty-humility constitutes successful convergent validity?

**Decision.** Pre-registered threshold: lower 95% bootstrap CI ≥ 0.15. Point-estimate target: r ≥ 0.25.

**Rationale.** Thielmann 2020 meta-analysis puts the population ceiling for moral-construct-vs-prosocial-behavior correlations at ρ̂ ≈ 0.20. Originally drafted at r ≥ 0.30, which would have sat above the meta-analytic upper edge and risked pre-registration failure even at the literature's strongest replicable effect size. Lower-CI thresholds are also more conservative than NHST and more publishable regardless of outcome direction.

**Considered and rejected.** NHST p < 0.05 (less conservative; perverse incentives). Higher threshold (would have looked impressive in the pre-reg but invited failure). Bayesian posterior probability (interesting but unfamiliar to most reviewers — defer to subsequent studies).

**Status.** Locked (pre-registration draft).

**Cross-reference.** This is the decision that was revised after lit pass 2 (Iteration 4). The earlier draft of `pre-registration.md` had the higher threshold.

---

## 12. Authored scenarios, not LLM-generated (MVP-1)

**Question.** Should scenarios be authored by humans, generated by LLMs at runtime, or hybrid?

**Decision.** Fully authored for MVP-1. LLMs are reserved for two non-content uses: coding free-text story prompts back to taxonomy (post-hoc), and powering reflection prompts (low-stakes user-facing copy variation).

**Rationale.** Pre-registration requires a fixed instrument. LLM-generated scenarios at runtime are non-deterministic and can't be pre-registered. They also introduce a content-quality problem (the validator can't audit a stochastic generator). For MVP-1 the validation goal is "does this work" — that needs a fixed instrument to test.

**Considered and rejected.** Pure LLM at runtime (non-deterministic; bad for pre-reg). Hybrid where LLM generates and human curates (slow; doesn't help the pre-reg constraint). Authored + LLM-generated parallel pool (introduces two probes; doubles the analysis complexity).

**Status.** Locked for MVP-1. Revisit at MVP-2 or post-validation.

---

## 13. Pre-registration as structural commitment

**Question.** How should the validation study be filed?

**Decision.** Pre-registered at OSF before recruitment opens; analysis code, scenario corpus, and instrument items all public at lock time; PsyArXiv preprint within 90 days of analysis lock regardless of outcome direction.

**Rationale.** The trust premise of the product depends on the field's credibility, and the field's credibility is exactly what's contested post-Gino (May 2025 tenure revocation; multiple flagship findings failing replication). Pre-registration is the structural response that distinguishes a serious instrument from another lifestyle app. The negative-result publication commitment is the part that matters most — otherwise publication bias would let the project look successful even if it isn't.

**Considered and rejected.** Conventional unpublished or post-hoc-revised filings (perpetuates the credibility problem). Pre-registration without negative-result commitment (selection bias persists).

**Status.** Locked.

---

## 15. Per-scenario-domain scoring (no cross-domain value-tag aggregation for MVP-1)

**Question.** When a `value:X` tag appears in a scenario whose primary domain is *not* X's home domain (e.g. `value:loyalty` appearing in a truth-telling item), should it contribute to scoring on the loyalty axis?

**Decision.** No, for MVP-1. Cross-domain `value:X` tags are descriptive metadata only; the analyzer scores each item exclusively on its parent scenario's primary axis.

**Rationale.** The pre-registered CFA assumes 4-domain factor structure with item-level loadings on intended factor (`pre-registration.md` H1, `scoring.md` §7). Cross-domain scoring would create cross-loadings and change the factor structure to something not pre-registered. The cost is that some signal is left on the table — a user choosing a `value:loyalty`-tagged option in a truth-telling scenario IS revealing something about loyalty, and we're not capturing it. The benefit is a clean factor structure that's actually testable at n=200 with the simple model.

**Considered and rejected.** Cross-domain scoring with corrective CFA (allowing cross-loadings) — would have more degrees of freedom and confuse the validation. Cross-domain scoring as an exploratory analysis only — defensible but adds analyzer complexity without affecting the primary validation; defer to MVP-2.

**Status.** Locked for MVP-1. Documented in `analysis/README.md` §"Open scoring question — cross-domain value tags". Cross-domain `value:X` tags are entered in `analysis/tag_axis_map_v0.1.csv` as `*,metadata,value:X,,note` rows so the analyzer recognizes them as intentional rather than typos.

**Revisit at MVP-2.** Once MVP-1 confirms the 4-factor structure (or doesn't), a Phase-2 design could specifically test whether cross-domain `value:X` scoring improves predictive validity. Held as a candidate revision.

---

## 14. Engineering: line crossed for tooling, runtime still open

**Question.** When does engineering start, and on what stack?

**Decision (partial, revised).** Engineering line crossed for *tooling*: `scripts/validate.py` is the first runnable code in the repo, a single-purpose Python validator with one dependency (`jsonschema`). Python chosen because `scoring.md` already names Python/R as the analyzer language and content-validation scripts are standard in Python ecosystems. The *runtime/product* stack remains open.

**What this commits to.** Python as a tooling language for content validation and (eventually) the analyzer. A `scripts/` directory pattern for utility scripts. The `jsonschema` library as the canonical JSON-Schema validator.

**What this does NOT commit to.** Any product/runtime stack. The mvp.md tech-stack proposal (React + TypeScript SPA, Y.js sync, Postgres backend) remains the working hypothesis but is not locked. A future engineer could pick a different stack without removing the Python validator.

**How the line was crossed.** Multiple iterations passed with the user continuing autonomous /loop firings and no redirect. Spec coverage reached a state where the natural next step was concretely available. Took a measured step — single file, single dependency, no build tooling — rather than waiting for explicit approval that wasn't going to come because the user is letting the iteration steer.

**Validator first surface findings.** The validator caught 64 errors on its first run across 15 of 20 scenarios: hyphenated-namespace tags (`self-cost:reputation`, `social-cost:none`) didn't match the original schema regex, three early probes were missing the `no_break_point_handling` field, one probe had `stake: 0` which violated `exclusiveMinimum`, and several tags weren't in the tag-axis map. All fixed in the same commit that introduced the validator — exactly the kind of drift it's built to catch.

**Status.** Tooling line crossed. Runtime decision still open.

---

## How to add to this file

Each new decision: copy the section template (Question / Decision / Rationale / Considered and rejected / Status). Number sequentially. Don't renumber when inserting historically — just add to the end.

When a decision is revised, append a new section that says "revisit of §N: ...". Don't edit the historical entry; the original reasoning is itself a record of where the project's thinking has been.
