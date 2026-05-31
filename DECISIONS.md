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

**Further engineering: analyzer prototype shipped.** `scripts/analyze.py` (added later) implements scoring.md §2-3 (per-item → per-session → per-user-per-domain revealed-score aggregation). Standard library only; no dependency added beyond what `validate.py` already brought in. Demonstrates that the scoring spec is implementable and surfaces any latent ambiguities. Reserved for the validation-cohort analyzer: Bradley-Terry inventory scoring (§5.2), gap computation (§6), bootstrap CIs (§8), CFA (§7), cost-of-virtue longitudinal trajectories (§4.3). The runtime product stack remains open; this is research-side tooling on the path scoring.md already named.

---

## 16. Corpus structure at MVP-1: full symmetry over depth

**Question.** When the scenario corpus reached the 40/48 point with `5 QF + 3 Narr + 2 CoV per domain × 4 domains` symmetric structure, the final 8 scenarios could have been allocated several ways: (a) 2 more QF per domain → `7+3+2`; (b) 1 more of each type per domain → `6+4+3`; (c) deepen one type (e.g., 2 more narratives per domain → `5+5+2`); (d) deepen one domain (skew toward truth-telling); (e) 1 more QF + 1 more CoV per domain → `6+3+3`. Which?

**Decision.** Option (e): `6 QF + 3 Narr + 3 CoV per domain × 4 = 48 total`. Locked 2026-05-16 with `cov-reciprocity-003`. Full structural symmetry across domains × scenario types preserved at every cell of the matrix.

**Rationale.** Three motivations:

1. *Structural symmetry is load-bearing for the CFA*. The pre-registered H1 (`pre-registration.md` §6) assumes a 4-factor structure with comparable indicator counts per factor. Skewed authoring (option d) would create factor-imbalance that the validation cohort's n=200 may not have enough power to compensate for. Symmetric authoring keeps the construct burden constant across the four scoring domains.

2. *CoV probes are the highest-leverage type per unit*. They directly power H5 (test-retest of cost-of-virtue break-points) and pair-analytically across probes (within-user vector across cov-001 / cov-002 / cov-003 separates types of inconsistency that the QF/Narr items can't isolate). 2-CoV-per-domain was a compromise driven by author-effort cost; the third CoV per domain pulls each domain's probe set up to where pair-analysis becomes a 4-way matrix of types (one-shot exploitation × forgiveness × iterated defection per domain in reciprocity; loyalty-monetization × loyalty-protection × loyalty-against-third-party-harm in in-group; etc.).

3. *Adding QFs is the lowest-marginal-value direction once each domain has 5+*. QFs measure repeated-low-stake decisions; the construct space is well-covered by 5 per domain. The 6th QF in each domain authored during this iteration round (qf-allocation-011 temporal; qf-truth-011 omission-as-lie; qf-ingroup-011 circle-widening; qf-reciprocity-011 breach-response) each opened a distinct construct angle — but additional 7th/8th QFs would have begun to repeat construct ground.

**Construct-distinction discipline for CoV authoring.** Each new CoV-3 was required to target a construct genuinely distinct from CoV-001 and CoV-002 within its domain — captured in the design_intent block of each scenario file and in the commit message rationale. Specifically:

- **truth-telling**: cov-001 third-party endorsement (commission); cov-002 paid omission (active withholding); cov-003 self-misrepresentation (self-presentation lie type per Levine 2010). These are three distinct lie-type constructs, not three variations of one construct.
- **resource-allocation**: cov-001 returning unfound money (fairness, inverted); cov-002 generosity from own resources (giving, inverted); cov-003 silent self-favoring as trusted allocator (taking, forward). Giving-direction × taking-direction × restitution-direction = three orthogonal sides of allocation morality.
- **in-group/out-group**: cov-001 monetized loyalty (user as payee); cov-002 inflated reference (in-group member as beneficiary); cov-003 covering for wrongdoing (loyalty against third-party harm). User-payee × beneficiary-payee × third-party-harm = three structural positions for the loyalty/honesty tradeoff.
- **reciprocity-cooperation**: cov-001 silent extra share (one-shot self-gain); cov-002 restitution to re-extend trust (forgiveness, inverted); cov-003 defection from sustained cooperation (iterated-coop defection). One-shot × past-betrayal × ongoing-relationship = three temporal positions for cooperation morality.

**Trigger for future scenario additions.** Adding to the corpus beyond 48 should be motivated by a specific construct gap surfaced during the pilot, by co-PI review, or by validation-cohort data revealing low loadings for a particular item. Authoring for breadth alone — adding scenarios because more is more — should be resisted at this point; the marginal-value curve has flattened. This is the same discipline as the "lock the schemas at OSF filing" decision in pilot-pre-launch-checklist.md Phase 4.

**Considered and rejected.** Option (a) — extra QFs — would have left the CoV probes at 2 each, which keeps the highest-leverage probe type undersaturated. Option (c) — deepen narratives — narratives are author-expensive and the existing 3 per domain already provide enough setting diversity (workplace × family × peer-group). Option (d) — domain depth — would have broken the H1 factor structure assumption.

**Status.** Locked at 48 scenarios. Future additions require explicit construct-gap motivation per the trigger criteria above.

---

## 17. Add H8 (narrative-immersion-as-debiasing) to MVP-1; unlock corpus from DECISIONS §16

**Question.** Dave's project-direction statement on 2026-05-29 named a novel methodological hypothesis: narrative-immersion-with-recurring-character-attachment as a measure-debiasing mechanism against social-desirability response. Should this be (a) deferred to MVP-2 / MVP-1.5 (the conservative path that protects MVP-1's primary validation scope), or (b) added to MVP-1 as a secondary hypothesis (the ambitious path that bundles the methodological contribution with the primary validation), and either way (c) what does this mean for the §16 corpus lock?

**Decision.** Option (b) — add H8 to MVP-1 as a secondary hypothesis. Locked 2026-05-30 by Dave's explicit decision after presented with the trade-off. Corpus lock from §16 is unlocked with H8 as the explicit construct-gap motivation; new corpus target ~56-60 scenarios with ~8-12 paired narrative-vs-abstract probes added. The MVP-1 OSF filing will include H8a + H8b as the 8th hypothesis.

**Rationale.**

1. *One cohort, one publication.* H8 tested in MVP-1 means the methodological claim lands with the primary validation rather than waiting on a separate study that may never get funded. The within-subject design uses the same n=200 cohort; statistical power for the H8 secondary thresholds (lower 95% CI ≥ 0.15 / ≥ 0.20) is adequate.

2. *§16's own trigger criterion is met.* §16 named the conditions for unlocking the corpus: "a specific construct gap from pilot data, co-PI review, or low CFA loadings for a particular item." H8 IS a construct gap — the existing instrument cannot test the narrative-immersion-as-debiasing hypothesis because it doesn't have paired narrative-vs-abstract probes by design. §16's unlock criterion is explicitly satisfied by §17 here. No retroactive rewriting of §16 is needed; §17 is a clean follow-on.

3. *Methodological contribution opportunity.* The H8 framework (see [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md) §5) is potentially a real contribution to moral psychology — narrative transportation has been studied in persuasion and health-education but not in measurement. If H8a confirms (debiasing), the instrument has a documented mitigation for the validity-threats.md §CV-1 social-desirability threat. If H8b confirms (attachment-grounding), the instrument has a measured mechanism that abstract framings can't replicate. Both findings are publishable independently of MVP-1's primary validation outcome.

4. *Secondary status preserves the primary-validation gate.* H8 is added as SECONDARY (not gate-criterion). A failed H8 does not falsify the instrument; it just means the narrative-immersion-as-debiasing claim doesn't pan out. The primary validation (H1, H2, H3) remains the gate.

**Considered and rejected.**

- *Defer H8 to MVP-1.5* — cleaner experimentally; but the elapsed time between MVP-1 and MVP-1.5 is realistically 12+ months, during which the H8 claim either gets scooped or loses momentum. The bundling cost (slight MVP-1 scope expansion) is small relative to the bundling benefit (one cohort, one decision).
- *Test H8 informally without pre-registration* — defeats the purpose. The contribution H8 makes is a pre-registered methodological claim; testing it post-hoc would be hypothesizing-after-results-known and not publishable as a rigorous finding.
- *Add H8 but keep §16 locked at 48 by re-tagging existing scenarios as both "narrative" and "abstract" pairs* — the existing 48 scenarios were not authored for paired-probe construct equivalence; retrofitting would require either (a) accepting weaker construct equivalence than the H8 spec requires, or (b) heavy re-authoring of existing scenarios. Adding paired probes as new scenarios (option (b)) is cleaner.

**Status.** Locked at 2026-05-30. Downstream changes triggered:
- `pre-registration.md` §6 adds H8 (H8a + H8b) to the secondary hypotheses table
- `pre-registration.md` §5 adds the within-subject paired-probe analysis plan
- `concept.md` adds a "Narrative immersion as measure-debiasing" section; recurring-NPC mention promoted from idea to mechanism
- `scoring.md` adds §9 operationalizing the divergence and attachment scores
- `validity-threats.md` §CV-1 updates mitigation list (pending H8 outcome)
- `pilot-protocol.md` gains the H8-calibration role (Mode A vs Mode B for buddy-NPC centrality per `h8-narrative-immersion-design.md` §6 Q2)
- `pilot-pre-launch-checklist.md` Phase 4 gains ~8-12 paired-probe authoring + NPC cast + attachment instrument items
- `scenarios/` corpus expands to ~56-60 with the paired-probe additions
- `literature/narrative-immersion.md` new doc anchoring the Green & Brock + Tukachinsky + transportation-theory grounding

These downstream changes are multi-iteration work, scheduled to be applied across subsequent iterations starting with concept + pre-registration in the same iteration as §17 lands.

**Pilot calibration role.** Per `h8-narrative-immersion-design.md` §6 Q2 (resolved 2026-05-30 to "defer to pilot"), the n=10 pilot administers BOTH Mode A (central-buddy NPC) and Mode B (flat-ensemble NPC cast), split-sample with random assignment. Pilot exit interview asks which mode "felt more like the choice was about a real person you knew." The winning mode is locked for the n=200 main study. This is honest deferral within the H8-in-MVP-1 commitment, not a retreat from it.

---

## How to add to this file

Each new decision: copy the section template (Question / Decision / Rationale / Considered and rejected / Status). Number sequentially. Don't renumber when inserting historically — just add to the end.

When a decision is revised, append a new section that says "revisit of §N: ...". Don't edit the historical entry; the original reasoning is itself a record of where the project's thinking has been.
