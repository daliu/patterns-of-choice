# Pilot Protocol — n=10 Usability and Calibration Study

**Status:** Draft 0.1. Bridges `mvp.md` (build spec) and `pre-registration.md` (n=200 main study). Defines the small-scale study that precedes OSF lock; designed to surface usability problems, calibrate scenario interpretability, and produce baseline data for the LLM story-coding gold standard *before* the main study is committed to.

This pilot is not pre-registered as a test of any validation hypothesis — it's an instrument-shakedown.

---

## Purpose

What the pilot is for:

- Confirm the daily-session flow is actually usable (load-times, friction, drop-off points)
- Confirm scenario prompts are interpretable to non-author readers (no items that consistently confuse users)
- Calibrate onboarding-fatigue threshold (does the ~25-minute inventory load across sessions 1–3 hold up in practice?)
- Get baseline acceptance rates for the cost-of-virtue probe (the most novel-format scenario type; users may skip if framing feels uncomfortable)
- Produce ~50 free-text story-prompt responses per prompt for LLM-coding gold-standard calibration (`scoring.md` requires κ ≥ 0.70 before story data folds into primary analyses)
- Stress-test the candor-moment copy in `onboarding.md` — does it produce excessive attrition, or does the "step away" CTA see meaningful but non-catastrophic use?

What the pilot is **not** for:

- ❌ Testing convergent validity (n=10 is hopelessly underpowered)
- ❌ Testing construct validity (factor structure needs n ≥ 100)
- ❌ Testing intervention efficacy (no intervention in MVP-1)
- ❌ Cross-cultural generalization (n=10 from convenience-recruited)
- ❌ Producing any publishable claim about the instrument

Reporting from the pilot should be carefully framed as *operational* findings: "users tended to skip prompt X" is OK; "the instrument measures Y" is not.

---

## Recruitment

- **n = 10**, convenience-recruited from trusted contacts. No paid panel yet.
- Target composition (not enforced, just sought): roughly 3 confident technical users, 4 mid-comfort knowledge workers, 3 users less comfortable with mobile/web apps. Mixed ages, mixed genders, mixed cultural backgrounds. *Important*: not professional moral psychologists, not professional UX testers — users who'd resemble the eventual main-study sample, just hand-picked rather than panel-recruited.
- **Compensation: $50 per participant for completion of the 4-week protocol** plus the exit interview. Partial compensation prorated by sessions completed (≥14 sessions: full $50; 7–13: $30; <7: $15).
- **Consent**: explicit written consent, signed before session 1. The consent form names the candor-moment framing explicitly: this is a pilot for an unvalidated instrument; the pilot data will not be published; participants can withdraw at any time and their data is deleted upon request.
- **IRB**: usability/quality-improvement pilots are often IRB-exempt; confirm with academic co-PI before recruiting. Defaulting to "submit for exempt determination" is the safe path.

---

## Protocol

- **4 weeks** of daily sessions (vs. 8 weeks for the main study — compressed because the pilot's goal is operational shake-down, not longitudinal signal estimation)
- Same content as the main study would deploy: full inventory module, all 12 minimum-viable scenarios in rotation, all four cost-of-virtue probes
- **Weekly 30-minute semi-structured interview with researcher** (sessions 7, 14, 21, 28 approximately) — not part of the main study; pilot-specific
- **End-of-pilot exit interview**: 45 minutes, structured around specific evaluation questions (below)
- Participants kept in a private channel (Slack / Discord / email thread) for low-friction bug reports during the pilot

---

## Specific evaluations

### Quantitative (passively logged)

| Metric | Source | Target |
|---|---|---|
| Time-to-first-session-complete (median) | Session log timestamps | ≤ 10 min |
| Time-to-week-3-profile-reveal (proportion reaching session 15) | Session log | ≥ 7/10 |
| Drop-off points (sessions where median ≥ 2 users churn) | Session log per user × session | flag any |
| Inventory-onboarding completion rate by session 3 | Inventory response presence | ≥ 8/10 |
| Cost-of-virtue probe skip rate (per-probe) | Probe response code | ≤ 20% per probe |
| Reflection prompt completion rate | Reflection text presence | ≥ 25% |
| Story prompt completion rate (sessions 3 batch) | Story response presence | ≥ 7/10 per prompt |
| Median story prompt word count | Story text length | 30–120 (matches design target) |
| Mean session duration | Session log | 5–10 min |
| Median response time on quick-fire items | Choice timestamps | 2–8 seconds |

### Qualitative (from interviews + exit)

- Did the candor moment in onboarding land? (Did anyone "step away"? Did the framing feel honest or apologetic?)
- Which scenarios confused users? Which felt unrealistic? Which felt too on-the-nose?
- Did the cost-of-virtue probe feel uncomfortable / acceptable / interesting?
- Did the inventory feel like work or like reflection?
- How did the user describe the experience to a friend? (asked at exit; surfaces the user's mental model)
- Was the profile reveal at session 15 informative / surprising / underwhelming / unsettling?
- Anyone become more anxious / preoccupied with self-monitoring? (scrupulosity risk signal)

### Editorial review

After the pilot, the author of any scenario flagged by ≥ 2 users as confusing, misleading, or biased rewrites it. Tag-mapping CSV updated if needed.

---

## Interview structure

### Weekly check-in (30 min)

- Bug / friction report (5 min)
- Pick one scenario from the past week the participant most remembers (10 min): why does that one stand out? does the choice they made still feel right?
- One free-form question of the week, rotating across topics (10 min):
  - Week 1: "What did the candor moment make you think when you read it?"
  - Week 2: "Has using this changed how you notice your daily decisions, if at all?"
  - Week 3 (just before profile reveal): "What do you expect to see when the profile shows up?"
  - Week 4 (after reveal): "What did the profile actually tell you that you didn't already know?"
- Operational handoff for the week ahead (5 min)

### Exit interview (45 min)

Section 1 — Usability (10 min)
- Walk through their typical session pattern; surface friction
- What's the smallest thing that would have made you quit?

Section 2 — Scenario interpretability (15 min)
- Pick 3 scenarios at random from their history; ask them to re-read and re-narrate the choice they were making

Section 3 — Honesty of self-reporting (10 min)
- Were there moments you picked an option that wasn't really what you'd do? Why? (probes for social-desirability bias in the gamified format)
- Were there moments you felt the system "wanted" a particular answer?

Section 4 — Wellbeing check (5 min)
- Has using this affected your mood / anxiety / self-perception in any way?
- If yes: how, and would you still recommend it to a friend?

Section 5 — Open (5 min)
- Anything you wished I'd asked that I didn't?

---

## H8 narrative-immersion calibration

The pilot does **not** test H8 (`pre-registration.md` §6; `h8-narrative-immersion-design.md`). At n=10 it is nowhere near powered for the within-subject divergence statistics of `scoring.md` §9. Its H8 job is purely to **de-risk and calibrate** the design before the main study commits to it.

**Three calibration goals.**
1. **Do the recurring characters feel real?** The whole H8 mechanism rests on parasocial attachment forming across sessions. If exit interviews reveal the NPCs read as cardboard, H8 is not viable as designed and the main study should not carry it.
2. **Does the attachment instrument behave?** Administer the short Tukachinsky-PSR adaptation (`scoring.md` §9.3) once near the end of week 2 and sanity-check it: range, ceiling/floor, whether participants can answer it about a two-week-old character without confusion. The behavioral latency proxy is logged but treated as exploratory until self-report is shown to vary.
3. **Do the paired probes feel artificial?** Each H8 construct is probed in both narrative and abstract form (`scoring.md` §9.1). If participants notice and resent the repetition ("you already asked me this"), the pairing is burned and needs redesign before scale.

**Dual-mode split-sample (resolves design-doc Q2).** The n=10 is split, randomized, into two authoring modes so the main study can lock the winner:
- **Mode A — central-buddy** (~5 participants): one recurring dependent figure (e.g. an animal-companion NPC) appears across many sessions; the high-stakes attachment probe consistently features this figure.
- **Mode B — flat-ensemble** (~5 participants): 5–7 named NPCs as a flat cast; the high-stakes probe uses whichever NPC that participant bonded with most.

The exit interview asks, in both arms, a decision question: *"which moment felt most like the choice was about a real person you actually knew?"* The mode that more consistently produces that response becomes the locked design for the n=200 study; the other is deprecated post-pilot. This is honest deferral — design both, test both, decide before the main-study OSF lock.

**Where this lands in the rest of the protocol.**
- *Recruitment* gains a randomized Mode A / Mode B assignment at enrollment (~5 each).
- *Protocol* schedules the attachment instrument once near the end of week 2 (before the profile reveal); narrative and abstract members of each paired probe fall on well-separated days, order counterbalanced across participants.
- *Interview structure* already probes adjacent ground — the weekly check-in's "one scenario you most remember" and the exit interview's Section 3 ("did you feel the system wanted a particular answer?") are natural places to surface NPC-realness without leading the participant.
- *Open questions* gains: do the NPCs feel like real people? does naming/continuity deepen across the two weeks? does the paired-probe repetition feel like a glitch or pass unnoticed?

A NO on goal 1 or 3 is a legitimate reason to drop H8 from the main study while keeping the rest of the instrument — H8 is secondary by design and severable.

---

## Decision criteria for proceeding to OSF lock

The pilot is a go/no-go gate for the main study. Specific criteria:

**Go conditions (all must hold):**
- ≥ 7/10 complete the 4-week protocol
- ≥ 7/10 reach the session-15 profile reveal
- No serious adverse events (relationship distress; scrupulosity escalation; voluntary withdrawal citing the product)
- Cost-of-virtue probe skip rate ≤ 30% per probe (slightly looser than target)
- ≤ 2 scenarios flagged for confusion or bias (out of 12)
- Self-reported "this felt like an experiment, not a verdict" ≥ 6/10
- Exit-interview honesty-of-self-report findings: no systematic bias surfaced that would invalidate the construct

**No-go conditions (any single one):**
- Serious adverse event in ≥ 1 participant
- Drop-off > 40% by session 14
- ≥ 3 scenarios flagged for confusion or bias
- ≥ 2 participants describe the experience as "manipulative" or similar at exit
- Cost-of-virtue probe skipped by > 50% of participants on any single probe

**Mixed: revise and re-pilot.** If 1–2 conditions are mid-range (not clear go, not clear no-go), pilot revision and a second n=10 run is the right move rather than committing to the main study.

---

## Adjustments to make based on pilot results

Pre-decided contingent revisions, so the pilot-to-main-study revision isn't ad-hoc:

| Pilot finding | Pre-decided response |
|---|---|
| Onboarding load > tolerable | Split inventory across sessions 1–4 instead of 1–3 |
| Reflection fill-rate < 20% | Revise reflection prompt copy; consider skipping by default |
| Probe skip rate > 30% (single probe) | Revise framing of that probe; check whether stakes ladder is plausible |
| Probe skip rate > 30% (across all probes) | Revisit probe-format design entirely; pre-reg may need to drop cost-of-virtue from primary indicators |
| Scenario flagged as confusing | Editorial rewrite; re-test on ≥ 2 pilot participants if budget allows |
| Scenario flagged as biased | Editorial rewrite + commit reasoning to `DECISIONS.md` |
| Profile-reveal received as "underwhelming" | Revisit reveal-screen copy; do not add metrics or scores |
| Profile-reveal received as "unsettling" | Strengthen pre-reveal candor framing; do not soften the content |
| Candor moment "step away" used by > 1 user | Useful signal; not a problem. Record and proceed. |
| Candor moment "step away" used by 0 users | Possible signal that the framing isn't real enough; user-test the candor copy with non-pilot readers |

---

## Timeline

- **Pre-pilot prep**: editorial review of all 12 scenarios; consent form drafting; IRB exempt-determination if applicable; recruitment outreach (~1 week)
- **Pilot run**: 4 weeks
- **Analysis + revision decisions**: 1 week (interview transcripts coded; quantitative metrics computed; go/no-go decision)
- **Total before OSF lock**: ~6 weeks

The OSF lock for the main study cannot happen before this gate is cleared. If the pilot triggers a "revise and re-pilot" mixed result, add another 5 weeks before lock.

---

## Open questions

- **Compensation for the LLM story-coding gold standard.** The pilot produces ~50 stories per prompt; calibrating κ ≥ 0.70 between two human raters requires manual coding of all of them, plus a separate set of ~100 stories for held-out evaluation. That's ~750 human-coding events. Decision: pay raters per-story or hourly; budget needed.
- **Who is the second human rater?** Co-PI or external grad student. Single-coder reliability is not enough for the LLM-coding pipeline calibration `scoring.md` requires.
- **Pre-registration of the pilot's own analyses.** Pilot is not pre-registered as a validation test, but the *go/no-go criteria above* could themselves be pre-registered to prevent ad-hoc adjustment. Recommended: yes, pre-register these criteria before the pilot starts, separately from the main-study pre-reg.
- **Pilot data fate.** Discarded after analysis, or retained as covariate/comparison material in the main study writeup? Default discard for privacy; reconsider only if the academic co-PI strongly prefers retention with explicit re-consent.

---

## Cross-references

- `mvp.md` §Recruitment — main-study recruitment plan (Prolific, n=200)
- `onboarding.md` §The candor moment — the copy this pilot stress-tests
- `pre-registration.md` — what gets locked at OSF after this pilot clears
- `scoring.md` §5.4 — LLM story-coding requirement (κ ≥ 0.70 gates story data into primary analyses)
- `DECISIONS.md` §2 — MVP-1 scope rationale
- `DECISIONS.md` §13 — pre-registration as structural commitment
