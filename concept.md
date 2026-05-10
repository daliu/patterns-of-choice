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

- **Consistency under reframing** — same dilemma flipped positive/negative; in-group/out-group swap [lit: note — moral particularists (Dancy 2004) reject "consistency under reframing" as a moral failure mode; see `literature/ethical-frameworks.md`]
- **Cost-of-virtue curve** — at what stake size does a stated principle break (most useful longitudinal signal) [lit: verified — Crockett et al. 2014 PNAS operationalizes this for harm aversion; Abeler et al. 2019 meta on die-roll honesty (N≈44,000) is the cleanest broader anchor. See `literature/moral-psychology.md`, `literature/ecological-validity.md`.]
- **Speed vs. deliberation** — System 1 vs. reflected response [lit: contested — Bago & De Neys 2019 shows utilitarian responders typically *intuit* the utilitarian answer; the fast=deontological / slow=utilitarian Greene-style mapping does not hold up. See `literature/moral-psychology.md`.]
- **Observed vs. anonymous** — observer effect [lit: verified — robust in die-roll and dictator-game literatures; Rotella et al. 2025 moderation analysis is recent.]
- **Order / anchor effects** — context-dependence of principle [lit: verified for moral-domain choices; do NOT extend to broader social-priming claims, many of which have failed to replicate. See `literature/replication-concerns.md`.]
- **Stated–revealed gap** — joint with inventory layer

**Why this taxonomy rather than Haidt / Kohlberg / Schwartz directly:** each is partial. Foundations describe weighting; stages describe reasoning; values describe stated preferences. The grid captures all three implicitly while forcing the behavioral measurement that none does well alone. [lit: note — MFQ-2 (Atari et al. 2023) supersedes MFQ-30 with six foundations; Kohlberg stage theory is largely abandoned empirically though developmental insight survives; PVQ-RR (Schwartz & Cieciuch 2022) is current. See `literature/measurement.md`.]

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

**Identity-level vs. trait-level captured separately.** "I am X" (sticky, behavior-driving) vs. "I value X" (revisable). Identity claims predict behavior change better (Oyserman, Aronson). [lit: verified — Oyserman & Destin 2010 plus the School-to-Jobs RCT series; effects on academic outcomes persist 2 years post-intervention. Walton & Wilson 2018 "wise interventions" frame is the broader synthesis. See `literature/behavior-change.md`. Note: identity-anchoring may translate awkwardly in role-ethics cultural contexts — see `literature/ethical-frameworks.md`.]

**Longitudinal capture.** One or two items per session rather than a big intake. Track inventory drift as a signal: stated values moving *toward* revealed behavior is rationalization; moving *away* is aspiration.

**Card-sort UI** for initial top-N. Fast, forces ranking, game-feel.

The inventory and scenario taxonomy share domain axes 1:1, enabling direct per-domain gap calculation.

---

## 3. Intervention layer (growth strategy)

This is where most self-improvement products fail. The literature is messier than the measurement side; honest framing matters.

### The intervention stack (weakest to strongest)

1. **Insight alone** — small, non-durable effects. Necessary, not sufficient.
2. **Implementation intentions** (Gollwitzer) — "when [cue], I will [behavior]." Robust, replicates. Single highest-leverage software-deliverable intervention. [lit: verified — Gollwitzer & Sheeran 2006 meta, k=94, N≈8,000, d=0.65 on goal attainment. Effect sizes in recent better-powered work somewhat smaller but still medium. See `literature/behavior-change.md`.]
3. **Scenario rehearsal** — practicing aspirational behavior in low-stakes simulated contexts. Native strength of this product. [lit: note — this is a relatively novel claim; the closest empirical analog is mental-contrasting-with-implementation-intentions (Oettingen) for which there is meta-analytic support, but "moral scenario rehearsal" specifically has no direct literature. Treat as design hypothesis, not validated mechanism.]
4. **Real-world micro-commitments** — scaffold-able, not enforceable in-app.
5. **Identity reinforcement** (Oyserman) — "I am someone who..." beats "I should..." [lit: verified — Oyserman School-to-Jobs RCTs; Walton/Yeager belonging interventions are the strongest adjacent identity-intervention literature; 2023 Walton et al. *Science* multi-site replication shows effects depend on context affordances.]
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

- **Don't gamify the values themselves.** Streaks for "honesty days" corrupt motivation via the crowding-out effect (Deci 1971+). Gamify *showing up to the system*; never the moral behavior itself. [lit: contested — the directional claim (extrinsic rewards can undermine intrinsic motivation in moral domains) has theoretical support (Deci/Koestner/Ryan 1999 meta d≈-0.34; Bénabou & Tirole 2006 signaling model) but the magnitude is disputed (Cameron & Pierce 1994 meta; Peters et al. 2022 failed direct replication of Deci 1971). The design choice is reasonable on precautionary grounds, but should not be framed as established empirical fact. See `literature/replication-concerns.md`.]
- **Don't moralize.** The system never tells the user a choice was wrong. Descriptive, never prescriptive.
- **Don't ship social comparison.** "More honest than 60% of users" is poisonous.
- **Watch for moral self-licensing.** The game must stay tethered to real-life prompts; never function as a closed moral-debit account. [lit: note — moral licensing is real but smaller and more context-dependent than the early Sachdeva/Monin literature suggested; Blanken et al. 2015 meta d=0.31 with publication bias; three direct replications failed (Blanken et al.). Concern is appropriate; magnitude calibration should be modest. See `literature/replication-concerns.md`.]
- **Watch for scrupulosity.** Build friction *against* over-engagement. Soft caps, "take a break" nudges, content normalizing imperfection.

### Pacing — the long arc

- **Weeks 1–3:** Pure baseline. No interventions. Trust-building.
- **Week 3–4:** First profile reveal. User picks a growth direction or passes. Passing is fine.
- **Weeks 4–12:** Intervention layer activates for chosen domain.
- **Week 12+:** Maintenance. New gap or deepen current.

**Stage-matching** (Prochaska TTM) matters most. Precontemplation, contemplation, preparation, action, maintenance — different stages need different interventions. Detect stage from engagement signals; modulate accordingly. Action-stage interventions on precontemplation users produce reactance; precontemplation reflection on action-stage users feels patronizing. [lit: contested — the descriptive stage distinction (TTM) is widely used, but the prescriptive claim that stage-matched interventions outperform non-matched controls is empirically weak. Aveyard et al. 2009 found no benefit for smoking cessation; West 2005 *Addiction* called for retiring the model. The doc's qualitative claim (different users at different stages need different framings) is intuitive; the strong "stage-matching matters most" framing overstates the evidence. See `literature/behavior-change.md`.]

### Honest positioning

Realistic effect sizes on the strongest stack — implementation intentions + practice + identity work + accountability — are probably ~0.5–0.8 SD on targeted behavior, with significant attrition. A contemplative practice that may shift behavior over months, not a quick fix. [lit: caution — individual component effects support this range (II d≈0.65; identity-belonging d≈0.35; prosocial-spending effects modest), but *no meta-analysis of this combination exists*, and Yeager et al. 2019 *Nature* growth-mindset (d≈0.03 average with large context heterogeneity) and Milkman et al. 2021 *Nature* gym megastudy show that stacking interventions does not necessarily produce additive effects. Calibrate downward; ~0.3–0.5 SD on the strongest measurable outcomes, with substantial heterogeneity, is the more defensible expectation. See `literature/behavior-change.md`.]

Working framing: **"a long-form mirror, with optional scaffolding."**

---

## Ethical and design risks

### Intrinsic to the premise (cannot be designed away)

- **Smuggled value claims in the taxonomy.** Every design choice is itself ethical. The set of values you include defines the moral universe for users. *Mitigation:* multiple selectable preset taxonomies (Haidt / Schwartz / Aristotelian / religious / secular humanist), user-editable inventory, transparency about authorship, open-source scenario library so academics and critics can audit.
- **WEIRD bias.** Moral psychology is overwhelmingly Western. Collectivist or honor-based users may "fail" individualist trolley framings in ways that aren't moral failures. *Mitigation:* cultural variant scenarios, explicit acknowledgment, can't fully solve. [lit: verified and stronger — Atari et al. 2023 *JPSP* shows the *nomological network* of morality (how foundations correlate with outcomes) varies across 25 populations, not just the levels. MFQ-30 shows measurement non-invariance across most country pairs (Iurino & Saucier 2020). Practical: cross-cultural comparison of absolute scores is not statistically defensible without invariance testing. See `literature/cross-cultural.md`.]
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
- **Predictive validity** against real-stakes behavior (Fischbacher die-roll, Mazar/Ariely matrix task, real-money dictator games, charitable giving). [lit: caution — Mazar/Ariely 2008 Ten Commandments effect *did not replicate* in 2018 RRR (Verschuere et al., 25 labs, N=5,786). The task itself produces real cheating behavior and is fine for measurement; the moral-priming finding using it is not. Also: Ariely's broader honesty-research program is partially compromised by the Gino fraud case. See `literature/replication-concerns.md`, `literature/ecological-validity.md`. Fischbacher die-roll and Abeler et al. 2019 meta (N≈44,000) are the better-replicated honesty paradigms.]
- **Test-retest reliability** over weeks/months (r ≈ 0.6–0.8 over 3 months — stable-ish but not rigid). [lit: verified — this range is consistent with HEXACO test-retest (Henry & Mõttus 2022: 13-day median r = 0.88 domains, 0.81 facets, 0.65 items), MFQ-30 (typically 0.6–0.8 over weeks-to-months), and VIA-IS (9-month median r = 0.73). 3-month r ≈ 0.6–0.8 is a reasonable target.]
- **Ecological validity** — pre-registered studies with real-stakes follow-up; opt-in lab tasks. [lit: critical — Bostyn et al. 2018 *Psychological Science* showed hypothetical trolley responses do not predict real-stakes trolley behavior; FeldmanHall et al. 2012 found similar divergence. The doc's measurement premise (low-stakes choices reveal real character) is *contested* in the literature; the burden of empirical proof is on character-lab. See `literature/ecological-validity.md`. Hofmann et al. 2014 *Science* experience-sampling work supports the design choice to use mundane scenarios over dramatic ones.]
- **Informant reports** — partner / coworker / friend ratings (under-used in this field; probably the single most important credibility move). [lit: strongly verified — Vazire 2010 SOKA model shows informants are *more* accurate than selves on observable evaluative traits including honesty; Connelly & Ones 2010 meta-analysis shows multi-informant ratings outperform self-report for predicting honest/conscientious/agreeable behavior. The doc's intuition here is correct and well-supported. See `literature/ecological-validity.md`.]
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

## Literature gaps identified

Areas where the literature supports additions or rebalancings that draft 0.1 doesn't yet incorporate. For the next revision.

1. **Hofmann et al. 2014 *Science* experience-sampling work** is the strongest empirical justification for the doc's design choice of mundane-daily over dramatic-dilemma scenarios. Should be cited directly. Real moral life is dominated by gossip, fairness, loyalty in mundane contexts, not trolley choices.

2. **Bostyn et al. 2018 (and FeldmanHall et al. 2012)** on hypothetical-vs-real moral choice divergence is *the* key empirical concern for character-lab. The doc treats ecological validity as a Phase-2 validation question; the literature suggests it should be elevated to a foundational empirical premise the project must prove, not assume. The "is the gap from low-stakes-game to real-life behavior tractable at all?" question is the project's central empirical risk.

3. **Atari et al. 2023 *JPSP*** on nomological-network variation across cultures is stronger than the doc's current "WEIRD bias" framing. Even when the *structure* of moral foundations is measurable across cultures, the *correlates* of those foundations with outcomes shift. This complicates the gap-analysis output ("you scored low on Loyalty") — what Loyalty *predicts* depends on the user's cultural context.

4. **Vazire 2010 SOKA model and Connelly & Ones 2010 meta-analysis** on informant validity. The doc's intuition that informant reports are the single most important credibility move is correct; the literature support is stronger than the doc currently invokes. Honesty-humility is *the* most-evaluative personality trait — exactly where informants outperform selves.

5. **Walton & Wilson 2018 "wise interventions" framework and the recent multi-site replications (Walton et al. 2023 *Science*; Yeager et al. 2019 *Nature*).** These are the single most relevant analogous-intervention literature for character-lab. Both show: real effects, modest sizes, large heterogeneity, context-affordances matter enormously. Direct implication for marketing-honesty: claim small average effects with meaningful subgroup heterogeneity, not large effects.

6. **Self-efficacy (Bandura).** Not currently cited. Implicit throughout the intervention layer; should be made explicit as the mediator linking "I am someone who..." → action initiation → persistence.

7. **Bénabou & Tirole 2006 *AER* on incentives and prosocial behavior.** Provides a formal signaling-model basis for the "don't gamify the values themselves" anti-pattern. Stronger theoretical foundation than the Deci-1971 citation.

8. **Crockett et al. 2014 PNAS harm-magnitude paradigm.** Existing, validated, computationally tractable operationalization of "cost-of-virtue curve." The doc reinvents the stake-laddering wheel; should be designed to inherit Crockett's parameter-space.

9. **Abeler et al. 2019 *Econometrica* meta-analysis on dishonesty games (N≈44,000).** Single best empirical anchor for cost-of-virtue / honesty-under-stakes calibration. Cleaner numbers than Mazar/Ariely 2008.

10. **Aknin et al. 2013, 2022 on prosocial spending and well-being.** Robustly replicated cross-cultural finding. Relevant for the doc's "Effort and self-sacrifice" domain — the underlying mechanism (prosocial action → affective benefit) is one of the few solidly-replicated moral-psychology findings.

11. **Bago & De Neys 2019** finding that utilitarian responses are typically intuitive, not deliberative. The doc's speed-vs-deliberation signature should be measured but interpreted with explicit awareness that the Greene-style mapping (fast=deontological/slow=utilitarian) does not hold.

12. **Cikara parochial-empathy work.** Relevant for the in-group/out-group domain — measurable as a behavioral signature, not just a domain axis.

13. **MacIntyre / Annas / Confucian role-ethics positioning.** The doc's individualist-secular-optional framing is itself an ethical position that should be explicitly acknowledged. Identity-anchoring may translate awkwardly in role-ethics contexts (East Asian, religious users).

14. **Name collision: Angela Duckworth's "Character Lab"** (characterlab.org) is a separate nonprofit doing character-education research. Public-facing branding will need to differentiate.

15. **The post-Gino landscape.** Doc's emphasis on pre-registration, open-source, published findings is the correct response to the credibility crisis in moral psychology; naming this rationale explicitly (rather than presenting it as generic open-science commitment) would strengthen the trust premise.

See `literature/_index.md` and the area-specific files for sources and citations.

---

## References

Compiled from the first literature review pass. Format: `Author (Year). *Title*. Venue. — One-line note on relevance.`

### Moral psychology

- Aristotle (c. 350 BCE). *Nicomachean Ethics.* — Virtue as cultivated disposition; *phronesis* as practical wisdom integrating virtues.
- Atari, M., Haidt, J., Graham, J., Koleva, S., Stevens, S. T., & Dehghani, M. (2023). *Morality beyond the WEIRD: How the nomological network of morality varies across cultures.* JPSP, 125(5), 1157–1188. — MFQ-2 across 25 populations; foundations measurable but network varies.
- Bago, B., & De Neys, W. (2019). *The intuitive greater good: Testing the corrective dual process model of moral cognition.* JEP:General, 148, 1782–1801. — Utilitarian responses typically intuitive, not deliberative; revises Greene model.
- Cikara, M., Bruneau, E. G., & Saxe, R. R. (2011). *Us and them: Intergroup failures of empathy.* CDPS, 20, 149–153. — Empathy reduced for outgroup targets.
- Bruneau, E. G., Cikara, M., & Saxe, R. (2017). *Parochial empathy predicts reduced altruism and the endorsement of passive harm.* SPPS, 8, 934–942.
- Crockett, M. J., Kurth-Nelson, Z., Siegel, J. Z., Dayan, P., & Dolan, R. J. (2014). *Harm to others outweighs harm to self in moral decision making.* PNAS, 111, 17320–17325. — Computational cost-of-virtue operationalization.
- Cushman, F. (2013). *Action, outcome, and value: A dual-system framework for morality.* PSPR, 17, 273–292. — Model-free / model-based moral learning.
- Greene, J. D., Sommerville, R. B., Nystrom, L. E., Darley, J. M., & Cohen, J. D. (2001). *An fMRI investigation of emotional engagement in moral judgment.* Science, 293, 2105–2108. — Foundational dual-process moral fMRI.
- Greene, J. D. (2013). *Moral Tribes.* Penguin. — Trade synthesis on intergroup moral conflict.
- Graham, J., Haidt, J., & Nosek, B. A. (2009). *Liberals and conservatives rely on different sets of moral foundations.* JPSP, 96, 1029–1046. — Original MFQ-30.
- Hofmann, W., Wisneski, D. C., Brandt, M. J., & Skitka, L. J. (2014). *Morality in everyday life.* Science, 345, 1340–1343. — Experience sampling; everyday morality is mundane, not dramatic.
- Kohlberg, L. (1969). *Stage and sequence: The cognitive-developmental approach to socialization.* — Six-stage model.
- Snarey, J. R. (1985). *Cross-cultural universality of social-moral development.* Psychological Bulletin, 97, 202–232. — Found stages 5–6 non-universal.

### Behavior change

- Bandura, A. (1977). *Self-efficacy: Toward a unifying theory of behavioral change.* Psychological Review, 84, 191–215. — Foundational; mediator linking identity claim to action.
- Bandura, A. (1997). *Self-efficacy: The exercise of control.* Freeman.
- Bénabou, R., & Tirole, J. (2006). *Incentives and prosocial behavior.* AER, 96, 1652–1678. — Signaling model of crowding-out; formal basis for "don't gamify values."
- Deci, E. L., Koestner, R., & Ryan, R. M. (1999). *A meta-analytic review of experiments examining the effects of extrinsic rewards on intrinsic motivation.* Psychological Bulletin, 125, 627–668. — d ≈ -0.34 crowding-out; contested by Cameron & Pierce 1994.
- Cameron, J., & Pierce, W. D. (1994). *Reinforcement, reward, and intrinsic motivation: A meta-analysis.* Review of Educational Research, 64, 363–423. — Counter-meta arguing crowding-out is small.
- Peters, J. R., et al. (2022). *An evaluation of the overjustification hypothesis: A replication of Deci (1971).* — Failed direct replication.
- Gollwitzer, P. M. (1999). *Implementation intentions: Strong effects of simple plans.* American Psychologist, 54, 493–503.
- Gollwitzer, P. M., & Sheeran, P. (2006). *Implementation intentions and goal achievement: A meta-analysis of effects and processes.* AESP, 38, 69–119. — k=94, N≈8000, d=0.65.
- Hagger, M. S., et al. (2016). *A multilab preregistered replication of the ego-depletion effect.* PPS, 11, 546–573. — Ego depletion fails to replicate.
- Lally, P., Van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). *How are habits formed: Modelling habit formation in the real world.* EJSP, 40, 998–1009. — Median 66 days to automaticity.
- Milkman, K. L., et al. (2021). *Megastudy.* Nature, 597, 481–486. — 53 nudges tested for gym attendance; most small or null.
- Oyserman, D., & Destin, M. (2010). *Identity-based motivation: Implications for intervention.* Counseling Psychologist, 38, 1001–1043.
- Oyserman, D., Bybee, D., & Terry, K. (2006). *Possible selves and academic outcomes.* JPSP, 91, 188–204. — School-to-Jobs RCT.
- Prochaska, J. O., & Velicer, W. F. (1997). *The transtheoretical model of health behavior change.* AJHP, 12, 38–48.
- West, R. (2005). *Time for a change: Putting the transtheoretical model to rest.* Addiction, 100, 1036–1039. — Critique of TTM stage-matching.
- Walton, G. M., & Cohen, G. L. (2011). *A brief social-belonging intervention improves academic and health outcomes of minority students.* Science, 331, 1447–1451.
- Walton, G. M., & Wilson, T. D. (2018). *Wise interventions: Psychological remedies for social and personal problems.* Psychological Review, 125, 617–655. — Theoretical synthesis.
- Walton, G. M., et al. (2023). *Where and with whom does a brief social-belonging intervention promote progress in college?* Science, 380, 499–505. — Multi-site, context-dependent effects.
- Yeager, D. S., Hanselman, P., Walton, G. M., et al. (2019). *A national experiment reveals where a growth mindset improves achievement.* Nature, 573, 364–369. — d ≈ 0.03 average, heterogeneous.
- Wood, W., & Neal, D. T. (2007). *A new look at habits and the habit–goal interface.* Psychological Review, 114, 843–863.
- Wood, W., & Rünger, D. (2016). *Psychology of habit.* Annual Review of Psychology, 67, 289–314.

### Measurement and validation

- Abeler, J., Nosenzo, D., & Raymond, C. (2019). *Preferences for truth-telling.* Econometrica, 87, 1115–1153. — Meta of 90 dishonesty games, N≈44,000.
- Aquino, K., & Reed, A. (2002). *The self-importance of moral identity.* JPSP, 83, 1423–1440. — Moral Identity Scale.
- Aron, A., Aron, E. N., & Smollan, D. (1992). *Inclusion of Other in the Self Scale and the structure of interpersonal closeness.* JPSP, 63, 596–612.
- Ashton, M. C., & Lee, K. (2007). *Empirical, theoretical, and practical advantages of the HEXACO model of personality structure.* PSPR, 11, 150–166.
- Brown, A., & Maydeu-Olivares, A. (2011). *Item response modeling of forced-choice questionnaires.* EPM, 71, 460–502. — Methodological reference for forced-choice inventories.
- Connelly, B. S., & Ones, D. S. (2010). *An other perspective on personality: Meta-analytic integration of observers' accuracy and predictive validity.* Psychological Bulletin, 136, 1092–1122.
- Fischbacher, U., & Föllmi-Heusi, F. (2013). *Lies in disguise—An experimental study on cheating.* JEEA, 11, 525–547. — Die-roll paradigm.
- Henry, S., & Mõttus, R. (2022). *Test-retest reliability of the HEXACO-100.* PLOS ONE. — 13-day median r = 0.88 domains.
- Jones, D. N., & Paulhus, D. L. (2014). *Introducing the Short Dark Triad (SD3).* Assessment, 21, 28–41.
- Lee, K., & Ashton, M. C. (2018). *Psychometric properties of the HEXACO-100.* Assessment, 25, 543–556.
- Mazar, N., Amir, O., & Ariely, D. (2008). *The dishonesty of honest people.* JMR, 45, 633–644. — Matrix task; moral-priming effect not replicated.
- McGrath, R. E. (2014). *Scale- and item-level factor analyses of the VIA Inventory of Strengths.* Assessment, 21, 4–14.
- Peterson, C., & Seligman, M. E. P. (2004). *Character Strengths and Virtues: A Handbook and Classification.* Oxford UP. — VIA classification.
- Schwartz, S. H. (1992). *Universals in the content and structure of values.* AESP, 25, 1–65.
- Schwartz, S. H., & Cieciuch, J. (2022). *Measuring the refined theory of individual values in 49 cultural groups: Psychometrics of the revised Portrait Value Questionnaire.* Assessment, 29, 1005–1019. — PVQ-RR validation.
- Vazire, S. (2010). *Who knows what about a person? The self-other knowledge asymmetry (SOKA) model.* JPSP, 98, 281–300.
- Verschuere, B., Meijer, E. H., Jim, A., et al. (2018). *Registered Replication Report on Mazar, Amir, and Ariely (2008).* AMPPS, 1, 299–317. — Failed replication of moral-priming effect.

### Ecological validity

- Bauman, C. W., McGraw, A. P., Bartels, D. M., & Warren, C. (2014). *Revisiting external validity: Concerns about trolley problems and other sacrificial dilemmas in moral psychology.* SPPC, 8, 536–554.
- Bostyn, D. H., Sevenhant, S., & Roets, A. (2018). *Of mice, men, and trolleys: Hypothetical judgment versus real-life behavior in trolley-style moral dilemmas.* Psychological Science, 29, 1084–1093.
- FeldmanHall, O., Mobbs, D., Evans, D., Hiscox, L., Navrady, L., & Dalgleish, T. (2012). *What we say and what we do: The relationship between real and hypothetical moral choices.* Cognition, 123, 434–441.
- Funder, D. C. (2012). *Accurate personality judgment.* CDPS, 21, 177–182.

### Cross-cultural

- Henrich, J., Heine, S. J., & Norenzayan, A. (2010). *The weirdest people in the world?* BBS, 33, 61–135. — Foundational WEIRD critique.
- Henrich, J. (2020). *The WEIRDest People in the World.* FSG.
- Iurino, K., & Saucier, G. (2020). *Testing measurement invariance of the Moral Foundations Questionnaire across 27 countries.* Assessment, 27, 365–372. — Non-invariance across most country pairs.
- Leung, A. K.-y., & Cohen, D. (2011). *Within- and between-culture variation: Individual differences and the cultural logics of honor, face, and dignity cultures.* JPSP, 100, 507–526.
- Nisbett, R. E., & Cohen, D. (1996). *Culture of Honor.* Westview.
- Markus, H. R., & Kitayama, S. (1991). *Culture and the self.* Psychological Review, 98, 224–253.

### Replication and credibility

- Blanken, I., van de Ven, N., & Zeelenberg, M. (2015). *A meta-analytic review of moral licensing.* PSPB, 41, 540–558. — d = 0.31; replication concerns.
- Doyen, S., Klein, O., Pichon, C.-L., & Cleeremans, A. (2012). *Behavioral priming: It's all in the mind, but whose mind?* PLOS ONE, 7, e29081. — Bargh elderly-priming fails to replicate.
- Mullen, E., & Monin, B. (2016). *Consistency versus licensing effects of past moral behavior.* Annual Review of Psychology, 67, 363–385.
- Rotella, A., Jung, J., Chinn, C., & Barclay, P. (2025). *Observation moderates the moral licensing effect.* PSPB.
- Data Colada (Simonsohn, Nelson, Simmons). (2021–2023). *Series on Francesca Gino.* https://datacolada.org/

### Prosocial behavior and well-being

- Aknin, L. B., Barrington-Leigh, C. P., Dunn, E. W., et al. (2013). *Prosocial spending and well-being: Cross-cultural evidence for a psychological universal.* JPSP, 104, 635–652.
- Aknin, L. B., Dunn, E. W., & Whillans, A. V. (2022). *The emotional rewards of prosocial spending are robust and replicable in large samples.* CDPS, 31, 536–545.

### Virtue ethics and ethical frameworks

- Annas, J. (2011). *Intelligent Virtue.* Oxford UP. — Virtue-as-skill; intelligent habituation.
- Ames, R. T. (2011). *Confucian Role Ethics: A Vocabulary.* University of Hawaii Press.
- Dancy, J. (2004). *Ethics Without Principles.* Oxford UP. — Moral particularism.
- Gilligan, C. (1982). *In a Different Voice.* Harvard UP. — Care ethics; Kohlberg critique.
- Hursthouse, R. (1999). *On Virtue Ethics.* Oxford UP.
- MacIntyre, A. (1981). *After Virtue.* Notre Dame UP. — Tradition-constituted virtue formation; challenge to individualist secular framings.
- Scanlon, T. M. (1998). *What We Owe to Each Other.* Harvard UP. — Contractualism.
- Singer, P. (1972). *Famine, affluence, and morality.* Philosophy and Public Affairs.

### Clinical / risk-relevant

- Abramowitz, J. S., et al. (2002). *Religious obsessions and compulsions in a non-clinical sample.* Behaviour Research and Therapy, 40, 825–838. — Scrupulosity in non-clinical populations.
