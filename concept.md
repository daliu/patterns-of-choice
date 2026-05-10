# Character Lab — Concept Document

**Status:** Draft 0.1 — captured from initial design conversation. Pending literature review and revision.

---

## Premise

Character is not a fixed trait; it is a pattern that emerges from the decisions a person makes, repeatedly, across many small situations. Most personality instruments measure what people *say* they value. Most "self-improvement" products tell users what they *should* value. This project proposes a third thing: a longitudinal instrument that measures what people *reveal* through low-stakes ethical decisions, surfaces the gap between revealed and stated values, and offers optional, opt-in scaffolding for users to close gaps they themselves identify.

The product is not a quiz. It is a contemplative practice, delivered as software, with a research-grade measurement layer underneath.

## Core insight

The actionable signal is not the measurement itself but the **delta** between two separate measurements:

- **Revealed values** — extracted from behavioral choices in repeated low-stakes scenarios
- **Stated values** — captured from a separately-administered forced-choice inventory

Existing instruments measure one or the other. None systematically operationalize the gap. The gap is what makes growth concrete: instead of an abstract goal ("be more honest"), the user sees that under social pressure they softened feedback in 7 of 12 measured contexts, and can decide whether to do something about it.

## Architecture overview

Three layers, each independently useful:

1. **Measurement** — scenario-based extraction of revealed ethical preferences
2. **Inventory** — forced-choice capture of stated and aspirational values
3. **Intervention** — opt-in scaffolding for user-chosen growth directions

The measurement and inventory share a common domain taxonomy, so gap analysis is a direct subtraction per dimension — no translation layer.

---

## 1. Measurement layer

### Scenario taxonomy

A 2D grid: **domains** (situational territory) × **behavioral signatures** (what's measured within each).

**Domains** (10 proposed; subject to revision):

1. **Resource allocation** — dictator, ultimatum, public goods with varying recipients
2. **Truth-telling under cost** — lies that benefit self / others / prevent harm; commission vs. omission
3. **Harm tradeoffs** — trolley-class, but naturalistic and re-framed
4. **In-group vs. out-group** — kin / friend / national / stranger gradients
5. **Authority and rule-following** — defer vs. defy; whistleblowing
6. **Reciprocity and cooperation** — iterated PD, trust games
7. **Intergenerational / future others** — climate, debt, legacy
8. **Purity / disgust** — Haidt-style
9. **Speech and reputation** — gossip, callouts, restorative vs. retributive instincts
10. **Effort and self-sacrifice** — concrete cost-bearing

**Behavioral signatures** measured within each:

- **Consistency under reframing** — same dilemma flipped positive/negative; in-group/out-group swap
- **Cost-of-virtue curve** — at what stake size does a stated principle break (most useful longitudinal signal)
- **Speed vs. deliberation** — System 1 vs. reflected response
- **Observed vs. anonymous** — observer effect
- **Order / anchor effects** — context-dependence of principle
- **Stated–revealed gap** — joint with inventory layer

**Why this taxonomy rather than Haidt / Kohlberg / Schwartz directly:** each is partial. Foundations describe weighting; stages describe reasoning; values describe stated preferences. The grid captures all three implicitly while forcing the behavioral measurement that none does well alone.

### Session design

5–10 minute daily sessions. Closer to a daily puzzle than a personality test. Each session covers a small slice of the grid; breadth comes from repetition over weeks.

**Session shape:**

1. **Quick-fire round (~60s).** 5–8 paired forced choices under visible timer. Captures System 1.
2. **Core narrative (3–5 min).** Interactive-fiction scene with 4–6 branching decisions. Where domain-level data is richest.
3. **Cost-of-virtue probe (~90s).** Stake-laddering auction on one previously stated value. Tracked over time, this is probably the single most useful signal in the whole system.
4. **Reflection (optional, 30s).** "Earlier you chose X. Was that who you want to be?" Captures aspirational overlay in context — far more honest than a separate values survey.
5. **One observation, no score.** Keeps the user curious without teaching what's being measured.

**Rotation:**

- All 10 domains every 2–3 weeks
- Periodic prior-dilemma re-poses with reframing to score consistency
- Occasional anonymous "experimental mode" to compare against default-mode baseline
- Optional real-stakes nights (small actual money or charity donations)

**Anti-gaming:**

- Pure-noise Big-5-style filler items prevent reverse-engineering
- Full profile not shown until ~10–15 sessions in
- Aggressive surface variation; same logical structure across workplace / family / public / anonymous-online settings

### Mechanics worth borrowing

- *Reigns*-style swipe cards for the quick-fire round
- *Choice of Games* / 80 Days for the core narrative
- Auction UI for the cost-of-virtue probe
- **A recurring NPC** the user interacts with over weeks — builds parasocial weight so loyalty/honesty choices toward them carry actual emotional cost. Probably the single highest-leverage mechanic for getting past "it's just a game" surface behavior.

---

## 2. Inventory layer (stated values)

Existing instruments (MFQ, Schwartz PVQ, VIA-IS) under-perform on predictive validity. Three failure modes to avoid:

1. **Everyone endorses everything.** Likert lets users max all values.
2. **No forced tradeoff.** Real ethics is allocation under scarcity.
3. **One-shot intake.** Values drift; aspirations shift as users see their own data.

### Design choices

**Forced-choice pairwise comparison.** 50–100 pairs across the domain taxonomy. Bradley-Terry ranking from the data. Relative comparisons are dramatically more informative than absolute ratings (the same trick that makes ELO work).

**Three separate inventories**, capturing different layers:

- **Current self** — "I am a person who..."
- **Aspirational self** — "I want to be a person who..."
- **Admired other** — "someone I respect is..."

The current↔aspirational gap is the user-chosen growth direction. The admired-other layer is often more honest because it dodges the self-flattery instinct.

**Behavioral anchors over abstractions.** "I keep promises even when it costs me" beats "honesty is important." Force the user to imagine the cost.

**Story prompts with LLM coding.** Free-text "describe a time you were proud / let yourself down." Coded back to taxonomy. What people surface unprompted is more predictive than what they check on a list.

**Identity-level vs. trait-level captured separately.** "I am X" (sticky, behavior-driving) vs. "I value X" (revisable). Identity claims predict behavior change better (Oyserman, Aronson).

**Longitudinal capture.** One or two items per session rather than a big intake. Track inventory drift as a signal: stated values moving *toward* revealed behavior is rationalization; moving *away* is aspiration.

**Card-sort UI** for initial top-N. Fast, forces ranking, game-feel.

The inventory and scenario taxonomy share domain axes 1:1, enabling direct per-domain gap calculation.

---

## 3. Intervention layer (growth strategy)

This is where most self-improvement products fail. The literature is messier than the measurement side; honest framing matters.

### The intervention stack (weakest to strongest)

1. **Insight alone** — small, non-durable effects. Necessary, not sufficient.
2. **Implementation intentions** (Gollwitzer) — "when [cue], I will [behavior]." Robust, replicates. Single highest-leverage software-deliverable intervention.
3. **Scenario rehearsal** — practicing aspirational behavior in low-stakes simulated contexts. Native strength of this product.
4. **Real-world micro-commitments** — scaffold-able, not enforceable in-app.
5. **Identity reinforcement** (Oyserman) — "I am someone who..." beats "I should..."
6. **Social commitment / accountability** — strong but operationally heavy.
7. **Environmental restructuring** — strongest long-term, hardest to deliver in software.

Layers 1–3, 5 are native to the product. 4 and 6 are scaffold-able. 7 is suggest-able.

### Intervention modules

**A. Gap-to-plan translator.** Pulls recurring real-life contexts from earlier story prompts, generates contextual implementation intentions. Generic plans don't work; contextual ones do.

**B. Scenario rehearsal mode.** Once a direction is picked, scenarios weight toward that domain. NPCs parametrize to user's real contexts. Reflection prompts ask comparison to aspirational self — never "the right answer was X."

**C. Daily bookend check-ins.** Morning ("what situation today might test [value]?"); evening ("did it come up?"). The lab-to-life bridge. Noisy, but weeks of self-report reveal signal; the prompt itself primes behavior even before analysis.

**D. Reflective journaling with pattern-mining.** Periodic free-text prompts, LLM-coded back to taxonomy. Output is observations, not advice.

**E. Identity language layer.** "You've chosen X 8 of 12 times this month — what does that say about who you are?" Anchor behavior to identity claims as they accumulate.

**F. Optional costly signaling.** Real-stakes channels — charity allocation, public commitments — for users who want to step from game into life. Strictly opt-in.

### Anti-patterns

- **Don't gamify the values themselves.** Streaks for "honesty days" corrupt motivation via the crowding-out effect (Deci 1971+). Gamify *showing up to the system*; never the moral behavior itself.
- **Don't moralize.** The system never tells the user a choice was wrong. Descriptive, never prescriptive.
- **Don't ship social comparison.** "More honest than 60% of users" is poisonous.
- **Watch for moral self-licensing.** The game must stay tethered to real-life prompts; never function as a closed moral-debit account.
- **Watch for scrupulosity.** Build friction *against* over-engagement. Soft caps, "take a break" nudges, content normalizing imperfection.

### Pacing — the long arc

- **Weeks 1–3:** Pure baseline. No interventions. Trust-building.
- **Week 3–4:** First profile reveal. User picks a growth direction or passes. Passing is fine.
- **Weeks 4–12:** Intervention layer activates for chosen domain.
- **Week 12+:** Maintenance. New gap or deepen current.

**Stage-matching** (Prochaska TTM) matters most. Precontemplation, contemplation, preparation, action, maintenance — different stages need different interventions. Detect stage from engagement signals; modulate accordingly. Action-stage interventions on precontemplation users produce reactance; precontemplation reflection on action-stage users feels patronizing.

### Honest positioning

Realistic effect sizes on the strongest stack — implementation intentions + practice + identity work + accountability — are probably ~0.5–0.8 SD on targeted behavior, with significant attrition. A contemplative practice that may shift behavior over months, not a quick fix.

Working framing: **"a long-form mirror, with optional scaffolding."**

---

## Ethical and design risks

### Intrinsic to the premise (cannot be designed away)

- **Smuggled value claims in the taxonomy.** Every design choice is itself ethical. The set of values you include defines the moral universe for users. *Mitigation:* multiple selectable preset taxonomies (Haidt / Schwartz / Aristotelian / religious / secular humanist), user-editable inventory, transparency about authorship, open-source scenario library so academics and critics can audit.
- **WEIRD bias.** Moral psychology is overwhelmingly Western. Collectivist or honor-based users may "fail" individualist trolley framings in ways that aren't moral failures. *Mitigation:* cultural variant scenarios, explicit acknowledgment, can't fully solve.
- **The mirror itself can harm.** Some users are genuinely worse off knowing their revealed values. *Mitigation:* informed consent, contemplative framing, easy deletion, never make profile feel permanent.
- **False precision.** Single-subject psychometrics on noisy data produce numbers that look more rigorous than they are. *Mitigation:* always show confidence intervals, never a bare number; refuse to ship a single "ethics score" no matter how much users demand it.

### Risks to vulnerable users

- **Scrupulosity / OCD spectrum.** Constant moral self-monitoring is a known symptom. The users most drawn to the product include those least able to tolerate it. *Mitigation:* light onboarding screening, soft caps, content normalizing imperfection, warm offboarding on distress signals.
- **Adolescents.** Identity formation is fragile. *Mitigation:* 18+ minimum.
- **Users in crisis or with moral injuries.** Journaling will surface trauma. *Mitigation:* "this is not therapy" framing throughout, crisis resources at every reflection prompt, light distress detection with handoff to actual resources.

### Risks from misuse and data sensitivity

- **Surveillance / coercion.** A profile of moral compromises is more dangerous in a leak than financial data. Threat model: employers, partners, governments, future-self, ML training. *Mitigation:* local-first by default, E2E encryption for sync, no training on user data ever, working delete, refuse enterprise sales — ideally backed by ownership structure (B-corp / cooperative / foundation), not just policy.
- **Coercive use cases the product enables.** Sharing / comparison features destroy the product. *Mitigation:* refuse to build them even when users request.
- **Manipulation surface.** Engagement-based monetization compromises the trust premise. *Mitigation:* subscription or donation only; no ads, no sponsorships, no data brokerage.

### Risks of substitution

- **Moral self-licensing.** Closed-system risk. *Mitigation:* tight tether to daily-life prompts.
- **Algorithmic moral authority.** Users may outsource judgment. *Mitigation:* descriptive, never prescriptive; no action recommendations in real situations.
- **Substitute for therapy or community.** Explicit complement-not-replace framing.

### Meta-risk

The product attracts exactly the actors who would corrupt it: charismatic-leader types, screening employers, monitoring parents, Social-Credit-curious governments. The product's premise is structurally indistinguishable from the language those bad actors use. *Mitigation:* anti-guru framing, no method-with-a-capital-M, no founder cult, no certifications, ownership structure that legally constrains future bad uses.

---

## Research validation plan

Two claims to validate; different designs.

### Claim 1 — Measurement validity

- **Convergent validity** with existing instruments (MFQ, Schwartz PVQ, HEXACO honesty-humility, VIA-IS, Dark Triad). Moderate correlations expected — perfect correlation means you reinvented something.
- **Discriminant validity** against unrelated constructs.
- **Predictive validity** against real-stakes behavior (Fischbacher die-roll, Mazar/Ariely matrix task, real-money dictator games, charitable giving).
- **Test-retest reliability** over weeks/months (r ≈ 0.6–0.8 over 3 months — stable-ish but not rigid).
- **Ecological validity** — pre-registered studies with real-stakes follow-up; opt-in lab tasks.
- **Informant reports** — partner / coworker / friend ratings (under-used in this field; probably the single most important credibility move).
- **Measurement invariance** across non-WEIRD samples, ages, education, religious backgrounds.

### Claim 2 — Intervention efficacy

- **RCT design** — three arms minimum: full intervention / measurement-only placebo / active control (alternative app: journaling, mindfulness). Pre-registered, IRB-approved, ideally published.
- **Outcome measures in descending credibility:**
  1. Behavioral (lab tasks, economic games)
  2. Informant report (partner/coworker ratings)
  3. Tracked real-world (donations, kept commitments — opt-in)
  4. Self-report scales
- **Timepoints:** baseline, 1m, 3m, 6m, 12m. The 6m and 12m points are what matter — almost all behavior-change interventions show effects at 1m and decay.
- **Mediator measurement** — measure proposed mechanism, not just outcome. Implementation intention formation; identity centrality (Aron IOS scale). Mediation analysis is what turns "found effect" into "know why."
- **Adverse events monitoring** — anxiety, relationship distress, scrupulosity, dropout reasons. Most behavior-change studies don't measure these; this one must.

### Phasing

- **Phase 1 (0–6m):** MVP measurement layer. n≈200. Construct + convergent + test-retest. Cheap and fast.
- **Phase 2 (6–12m):** Behavioral validation via remote economic-game protocols and informant reports. n≈500–1000. The credibility moat.
- **Phase 3 (12–24m):** Pre-registered intervention RCT. n≈400–800 powered for medium effects. Published.
- **Phase 4 (24m+):** Long-term follow-up, cross-cultural replication, mechanism studies.

### Open-science commitments

- Pre-register all confirmatory analyses (OSF)
- Publish protocols and instruments openly
- Release aggregate data for replication
- Open-source scenario library

These map directly onto the trust premise the product is selling.

### Honest acknowledgment

This is academic-grade rigor for what's typically a consumer product. Most apps in this space do none of it. Doing it costs time and money, and the findings might be unflattering — small effect sizes, weaker ecological validity than hoped. The compromise that's both honest and tractable: ship with rigorous Phase 1 validation, run Phase 2 in parallel with the public product, run Phase 3 once there's a user base to recruit from. Be vocal about what's validated and what isn't at each stage. The single most damaging mistake would be claiming validation you don't have.

---

## Open questions

- **Single-platform vs. cross-platform.** Mobile-only loses desk-bound users; web-only loses commute users. Probably both, eventually.
- **NPC implementation.** LLM-driven NPCs are flexible but expensive and inconsistent. Authored NPCs are reliable but rigid. Hybrid likely.
- **Onboarding length.** Inventory + baseline take at minimum 3 sessions. How much can be deferred without losing user trust?
- **Crisis-detection thresholds.** False positives drive users away; false negatives leave users unsupported. Tuning is hard.
- **Inventory taxonomy presets.** Default to Schwartz, Haidt, or a custom blend? Religious and secular variants?
- **Demo / preview without commitment.** A meaningful demo without 3 weeks of data is structurally hard. What's the right "first session" experience?
- **Authorship of dilemmas.** Who writes the scenarios? Single voice → coherence + bias. Crowd → diversity + inconsistency. Editorial board?
- **Effect-size honesty in marketing.** How to communicate realistic outcomes without becoming the depressed-realist app no one downloads?

---

## References

*To be filled and expanded by literature review pass. Anchor sources expected to include:*

**Moral psychology**
- Haidt, J. — Moral Foundations Theory
- Schwartz, S. — Universal Values
- Kohlberg, L. — Stages of Moral Development
- Greene, J. — Dual-process moral cognition
- Cushman, F. — Moral judgment and action

**Behavior change**
- Gollwitzer, P. — Implementation intentions
- Oyserman, D. — Identity-based motivation
- Prochaska, J. — Transtheoretical Model
- Deci, E. & Ryan, R. — Self-Determination Theory; crowding-out effects
- Aronson, E. — Cognitive dissonance
- Wood, W. — Habit formation
- Duckworth, A. — Self-control and behavior change

**Measurement and validation**
- HEXACO (Ashton & Lee) — honesty-humility
- VIA-IS (Peterson & Seligman) — character strengths
- Aron, A. — Inclusion of Other in Self (IOS) scale
- Fischbacher, U. — Die-roll cheating paradigm
- Mazar, Amir, Ariely — Self-concept maintenance / matrix task

**Cross-cultural**
- Henrich, J. — WEIRD samples
- Atari, M. et al. — Moral foundations across cultures

**Virtue ethics**
- Aristotle — Nicomachean Ethics
- MacIntyre, A. — After Virtue
- Annas, J. — Intelligent virtue and habituation
