# MVP Scope — Patterns of Choice

**Status:** Draft 0.1 — first concrete build spec. Pending review against the second lit-pass on ecological validity.

---

## Goal of MVP-1

Build the smallest thing that empirically tests **Claim 1** from the validation plan (`concept.md`): *the instrument measures something real*. That means: revealed-value scores are reliable within users, vary meaningfully across users, correlate with at least one existing validated instrument, and can be computed against a stated-values inventory to produce a per-domain gap with usable confidence intervals.

**MVP-1 does not test the intervention layer (Claim 2).** That's MVP-2, gated on Claim 1 holding up. Stacking them in one study is a category error — you cannot interpret an intervention result if the underlying measurement isn't validated.

---

## Out of scope for MVP-1

- The intervention layer in any form — no growth-direction selection, no implementation intentions, no scenario rehearsal mode, no daily check-ins
- All 10 domains — start with 4 (see below)
- LLM-driven scenarios — authored only, for reproducibility and pre-registration
- Mobile app — web only
- Real-stakes channels — flagged for MVP-2 once feasibility is clearer
- Cross-cultural / non-English — single-language English baseline
- Anonymous / observed comparison mode — useful longitudinally but not for Phase-1 validation
- Identity-anchored relational variant — flagged in the concept doc as a remaining gap; not in MVP

---

## In scope

- Web-based daily-session app (React + TypeScript single-page)
- **4 scenario domains × ~12 scenarios each ≈ 48 authored scenarios**
- **Stated-values inventory:** forced-choice pairwise comparison + card-sort, three layers (current / aspirational / admired)
- **Per-domain gap computation** with confidence intervals
- **4-week minimum, 8-week target** longitudinal protocol
- **External validation hooks:**
  - HEXACO-60 at baseline (convergent validity)
  - Opt-in informant-report wave at week 4 — recruit **≥2 informants per user, aim for 3** (Connelly & Ones 2010 meta shows reliability plateaus near 3; marginal validity gain from #3→#4 is small). Canonical pair: romantic partner + coworker, the configuration with strongest evaluative-trait agreement in the SOKA literature. HEXACO-60 is scored at the **facet level** (fairness, sincerity, modesty, greed avoidance) not just the domain total, since Pletzer 2019 and Lee-Ashton facet-level work show facet prediction frequently exceeds domain-level for specific behaviors
- Local-first data; encrypted opt-in sync for the validation cohort

---

## Domain selection for MVP-1

Pick the 4 domains with the **strongest existing literature anchors** and **cleanest operationalization**, deliberately favoring formats with better ecological-validity evidence:

| Domain | Why include | Operational anchor |
|---|---|---|
| Truth-telling under cost | Abeler et al. 2019 *Econometrica* meta-analysis (N≈44,000 across 90 games) gives the cleanest calibration; Cohn et al. 2019 *Science* lost-wallet field study provides the closest lab→field analog | Fischbacher & Föllmi-Heusi 2013 die-roll and sender-receiver paradigms as the spine; matrix task as behavior elicitor but **not** the Mazar/Ariely 2008 moral-priming framing (failed Verschuere et al. 2018 RRR, 25 labs, N=5,786) |
| Resource allocation | Dictator / ultimatum games are the most-replicated paradigm in behavioral economics | Real-money or imagined-money dictator with varying recipients |
| In-group vs. out-group | Cikara parochial-empathy work; clean behavioral signature | Allocation / harm tradeoffs across kin / friend / national / stranger gradients |
| Reciprocity & cooperation | Iterated trust games and iterated PD are well-established; show real-life correlates | Trust game with iterated rounds; PD variants |

**Deliberately excluded for MVP-1:**

- **Harm tradeoffs (trolley-class)** — precisely the format Bostyn et al. 2018 showed has poor ecological validity. Including it would risk anchoring the whole instrument to a contested paradigm.
- **Purity / disgust** — Haidt's most cross-culturally contested foundation (Atari et al. 2023 nomological-network instability). Defer until MVP-2 when the relational variant is also being designed.
- **Speech / reputation** — harder to operationalize as 60-second scenarios. Worth doing eventually.
- **Authority / rule-following** — meaningful but overlaps with reciprocity for an MVP.
- **Intergenerational / future others** — hard to operationalize at the 5-minute session granularity.
- **Effort / self-sacrifice** — overlaps with resource allocation in a way that obscures rather than clarifies the construct space at MVP scale.

---

## Session protocol

- **~5 min daily sessions**, designed to feel like a daily puzzle rather than a study
- Each session covers **one domain**, with 4–6 scenarios + 1 cost-of-virtue probe
- **All 4 domains rotated each week** — by week 4, every user has ~7 sessions per domain (enough for individual-level reliability estimation)
- **Quick-fire round (~60s)**: 4–6 paired forced choices under visible timer (captures System 1)
- **Core scenario (~3 min)**: one branching narrative with 4–6 decisions
- **Cost-of-virtue probe (~90s)**: stake-laddering auction on one previously-stated value
- **Optional reflection (~30s)**: skippable in-context aspirational overlay
- **One observation, no score** — never a numerical reveal during the protocol

---

## Inventory protocol

**Onboarding (sessions 1–3):**

- Card sort: top 5 values from a deck of 20 (behaviorally-anchored descriptions, not abstractions)
- Forced-choice pairwise calibration: ~30 pairs across the 4 domains for Bradley-Terry ranking
- Three layers captured separately:
  - Current self ("I am a person who...")
  - Aspirational self ("I want to be a person who...")
  - Admired other ("someone I respect is...")
- Open story prompts: 2 free-text items (proud moment / let-self-down moment), LLM-coded back to taxonomy post-hoc

**Ongoing capture:** 1–2 inventory items per session thereafter, rotating across the 4 domains and the 3 layers.

**Drift tracking:** inventory responses timestamped; movement *toward* revealed behavior tagged as rationalization, *away* as aspiration.

---

## Data captured per session

| Field | Notes |
|---|---|
| Session timestamp + duration | UTC + local |
| Scenario IDs presented (in order) | Pre-randomized rotation seed per user |
| Choices made | Including the "no choice" / skip option |
| Response time per decision | Critical for the speed-vs-deliberation signature |
| Cost-of-virtue probe outcome | Break-point stake size on the day's probed value |
| Optional reflection text | If user supplied |
| Inventory items presented + responses | Pairwise comparisons + drift items |

**Stored locally first.** Sync (for the validation cohort only, with explicit consent) is opt-in and end-to-end encrypted.

---

## Outputs to user during MVP-1

- One observation per session (descriptive, never prescriptive — e.g., "you weighted loyalty over fairness in 3 of today's 5 choices")
- **Profile reveal at session 15** (≈ end of week 3): per-domain revealed score (with CI) × stated score (with CI) × gap (with CI)
- No "ethics score." No social comparison. No growth-direction prompt during MVP-1 (that's MVP-2).

---

## Outputs to research / validation

- Per-user per-domain revealed score with bootstrap CI
- Per-user per-domain stated score (Bradley-Terry posterior)
- Per-user per-domain gap = (stated − revealed) standardized within domain
- Within-user test-retest reliability per domain (weeks 1–2 vs. weeks 3–4 sessions)
- Between-user variance per domain
- Cross-domain factor structure (does the 4-domain taxonomy hold up?)
- Convergent validity: gap and revealed scores vs. HEXACO-60 honesty-humility
- Informant-report convergence (at week 4 wave)
- Per-user inventory drift trajectory

---

## Validation targets for MVP-1 (Phase 1 of the concept doc's plan)

**Construct validity**
- Factor structure of revealed scores recovers the 4-domain taxonomy (CFA loadings > 0.5 on intended factor)
- Internal consistency per domain: α ≥ 0.65 (Cronbach), ω ≥ 0.70 (McDonald)

**Convergent validity (pre-registered)**
- Revealed *truth-telling* domain correlates **r ≥ 0.25** with HEXACO honesty-humility (calibrated to Thielmann 2020 meta ρ̂ ≈ 0.20 with prosocial behavior; the originally-drafted r ≥ 0.30 sat above the meta-analytic upper edge and would risk pre-registration failure even at the strongest replicable effect size)
- Informant H rating correlates r ≥ 0.25 with revealed truth-telling (Pletzer 2019 informant-rated H ρ = −0.48 with workplace deviance is the upper bound; r ≥ 0.25 against a scenario-derived measure is the defensible lower target)
- Stated and revealed scores correlate moderately (r between 0.20 and 0.60); too-high collapses the gap signal, too-low suggests measurement noise

**Reliability**
- 3-week test-retest per domain: r ≥ 0.60
- Cost-of-virtue probe across sessions: r ≥ 0.50

**Discriminant validity**
- Revealed scores do not collapse onto a single g-factor (eigenvalue ratio test)
- No correlation > 0.40 with Big-5 neuroticism (controls for response bias)

These targets are conservative; pre-registration matters more than the exact thresholds.

---

## Tech stack proposal

| Layer | Choice | Rationale |
|---|---|---|
| Frontend | React + TypeScript SPA | Standard, fast, reusable |
| Scenario engine | Custom JSON DSL with Twine-style branching | Authoring-first; non-engineer can write scenarios |
| State management | Local-first via IndexedDB; opt-in sync | Privacy default-on |
| Sync (validation cohort) | Y.js + CRDT sync server, or PocketBase | Need encrypted-at-rest, audit-able |
| Auth | Passkey or magic-link, no passwords | Account hygiene matters for trust premise |
| Backend | Minimal — session log + inventory storage | Postgres + a thin API |
| Hosting | Vercel or self-hosted | TBD |

**Estimated MVP-1 build:** 4–6 weeks for one mid-senior engineer (assuming scenarios are authored in parallel). Scenario authoring + IRB run on independent critical paths and converge for pilot.

---

## Recruitment & study design

- **Target n = 200** for Phase-1 measurement validation
- Recruit via Prolific (or comparable paid panel) for demographic diversity beyond a college sample
- **8-week protocol**: 7 sessions/week × 8 weeks = ≥ 50 sessions per user (with reasonable attrition, expect median ~30)
- Compensation: ~$25 per user for ~5 hours total engagement (industry standard)
- Optional informant-report wave at week 4: incentivize informants separately
- IRB approval required before launch; aim for academic co-PI to streamline approval
- Pre-registration on OSF before recruitment opens

---

## Timeline estimate

| Months | Track A: scenario authoring + study design | Track B: app build | Track C: IRB / pre-reg |
|---|---|---|---|
| 0–1 | Scenario specs; editorial review | Architecture; auth; session engine | IRB application draft |
| 1–2 | Author 48 scenarios; pilot review | Inventory module; rotation logic | IRB submission |
| 2–3 | Pilot test n=10 for usability + scenario calibration | Sync; informant-report flow | IRB approval (typically) |
| 3 | Pre-registration | Finalization; pilot fixes | Pre-reg locked |
| 4–5 | — | — | Recruitment + 8-week study run |
| 6 | — | — | Analysis + write-up |
| 7 | — | — | Pre-print on PsyArXiv |

~7 months from start to first usable empirical evidence.

---

## Decision points before starting MVP-1

These are real questions that block work; surfacing them now rather than discovering them mid-build:

1. **Scenario authorship.** In-house vs. commission a writer vs. editorial board? Single-voice authorship gives coherence but bakes in the author's perspective; an editorial board gives breadth but raises the cost of producing 48 scenarios.
2. **Funding.** Compensation (~$5k for 200 × $25) + IRB processing + dev time + hosting. Self-fund vs. seek small research grant vs. crowdfund?
3. **Academic co-PI.** IRB approval is much faster (and the pre-print has more weight) with an academic at a research institution as co-PI. Worth the effort to recruit one.
4. **Real-stakes channel for MVP-1?** Even one real-stakes session per user (e.g., a $5 charity allocation) would strengthen ecological-validity claims considerably. Logistical cost: real money handling, charity partnerships. Worth doing if budget allows.
5. **Open-source the scenarios from day one, or after Phase-1 results?** Pre-registration discipline argues for "after lock"; open-science transparency argues for "from day one." Probably the right answer is to register privately at the start, release after the Phase-1 pre-print.
6. **Single-session demo for non-validation visitors?** A 5-minute "what this is like" experience for curious visitors who aren't enrolling. Useful for awareness but distinct from the validation-cohort app. Defer to MVP-2?

---

## What MVP-1 explicitly does NOT validate

For honesty in any future write-up or marketing copy:

- MVP-1 does not show that scenario behavior predicts real-life ethical behavior. The convergent-validity hook (HEXACO + informant) is necessary but not sufficient. **Ecological validity at the predictive level is MVP-2 work.**
- MVP-1 does not show the intervention layer works. **That's Claim 2 / MVP-2.**
- MVP-1 does not establish cross-cultural validity. **WEIRD-only sample explicitly acknowledged.**
- MVP-1 does not validate the cost-of-virtue probe as a clinical tool — only as a research signal.

Stating these explicitly up front is part of the trust premise.
