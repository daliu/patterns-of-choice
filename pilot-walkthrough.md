# Pilot Walkthrough — 4-Week Experience

**Status:** Reference document. A longitudinal narrative of what a pilot participant experiences across the 4-week protocol specified in [`pilot-protocol.md`](pilot-protocol.md). Complements [`first-session-walkthrough.md`](first-session-walkthrough.md), which is screen-level for session 1; this document is participant-experience-level across the entire arc.

Not a build spec. The runtime engineering would produce this experience dynamically against the JSON content; this document is the synthesized rendering of what the spec produces over time.

---

## Pre-week-1 — recruitment to consent

**Day −7 to Day 0**

A prospective participant sees the Prolific listing per [`pilot-materials/recruitment-script.md`](pilot-materials/recruitment-script.md). The headline is honest about the time commitment ("Daily 5-minute ethics-decisions study (4 weeks, $50 max)") and the unvalidated-instrument framing ("we want to know whether it works as an instrument, not how you compare to anyone").

If they pre-screen through (18+, English-fluent, mid-comfort with daily-cadence apps, no active scrupulosity/OCD, not a moral psychology professional), they receive a welcome email within 48 hours with:
- Confirmation of the compensation structure ($50 / $30 / $15 by completion tier)
- The consent form link ([`pilot-materials/consent-form.md`](pilot-materials/consent-form.md))
- A calendar link to schedule their first weekly check-in
- The app link with onboarding instructions

The consent process is intentionally not frictionless. The candor moment is in the consent itself: *"You are not being measured; you are helping us figure out whether the instrument works."* About 5–10% of accepted participants are expected to step away at this point (per the consent's "step away" CTA design); this is logged for the eventual estimate of ecological-validity-related attrition.

Signed consent triggers Day 1.

---

## Week 1 — sessions 1 through 7

### Sessions 1–3 — onboarding (longer than typical sessions)

The first three sessions are longer than the daily-rhythm sessions that follow because the inventory module needs administration:

- **Session 1** (~10 min): the screens covered in [`first-session-walkthrough.md`](first-session-walkthrough.md) — opening, candor moment, current-self card sort (20 values, pick top 5), one quick-fire round, one story prompt ("Tell me about a time, recently, when you were quietly proud of how you handled something").
- **Session 2** (~7 min): aspirational-self card sort (same 20 values, different framing — "who you want to become"); first batch of forced-choice pairwise items (10 of 30); one quick-fire round.
- **Session 3** (~7 min): admired-other card sort (the user is asked to bring a specific person to mind); pairwise items 11–20; the second story prompt ("a time you let yourself down"); first cost-of-virtue probe (if their stated values include one of the probed slots — `honesty` / `fairness` / `loyalty` / `cooperation`).

By the end of session 3 the inventory side is substantially complete; the user has cared and stated where they care.

### Sessions 4–7 — established daily rhythm begins

Sessions get shorter — about 5 minutes each. The user sees one quick-fire round per session, occasionally interleaved with the third scenario type (branching narrative, ~3 min). The four domains rotate so by week's end the user has been exposed to truth-telling, resource-allocation, in-group/out-group, and reciprocity scenarios.

A meaningful detail: the recurring NPC (per `concept.md` §"Mechanics worth borrowing") becomes a continuing character. By session 7 the participant has seen the same colleague/friend/family-member figure appear across multiple scenarios; their parasocial weight starts to make subsequent choices about that character feel more like choices about a real person.

### Week 1 check-in interview — end of week 1

A 30-minute call per [`pilot-materials/weekly-interview-script.md`](pilot-materials/weekly-interview-script.md). The week-specific question is about the candor moment: *"Do you remember the screen during your first session that said something like — this is a pilot, the instrument isn't validated, you might step away? What did you think when you read that?"*

What the researcher learns: whether the candor framing is being read as honesty or as cynicism / defensive lawyering. Both are real possibilities.

---

## Week 2 — sessions 8 through 14

### The daily rhythm establishes

By week 2 the participant has a routine. Sessions take 5–10 minutes; they fit into the daily slot that emerges naturally (morning coffee, post-commute, before bed). The participant starts to recognize the scenario formats — quick-fire under timer, branching narrative, cost-of-virtue probe — and develops their own implicit pacing strategy.

The inventory item-drift hits this week: 1–2 ongoing inventory items per session, rotating across the 4 domains × 3 layers (current / aspirational / admired-other). The user re-rates a value periodically; the analyzer logs whether their stated rating has moved.

### Mid-week — first reflection emerges

By session 10–11 some participants report (in the eventual exit interview) that they've started noticing daily-life decisions they wouldn't have noticed before. This is the intended effect — the reflective consciousness about everyday ethics that the design hopes for. Other participants report no such effect; that's also data.

### Week 2 check-in interview

The week-specific question is about whether using the app has changed anything about how the participant notices their daily decisions: *"Not in a 'I'm a better person now' way — just whether you've found yourself thinking about choices you wouldn't have thought about before."*

Two failure modes the researcher listens for:
1. **No effect at all** — participant is going through the motions; the app isn't catching anything that matters to them. This raises a question about whether the scenarios fit the participant or whether the participant's actual ethical life happens at scales the app doesn't capture.
2. **Anxiety / scrupulosity emerging** — participant has started self-monitoring in a way that exceeds the design intent. The researcher uses Section 4-style wellbeing-check language and offers withdrawal without compensation penalty.

---

## Week 3 — sessions 15 through 21 — the profile reveal

### Pre-reveal — sessions 15 builds up

By session 15 the participant has completed enough sessions for the analyzer to compute a real per-domain revealed score plus the gap against their stated values. The app's session-15 screen surfaces the explicit framing per [`onboarding.md`](onboarding.md) §"Profile reveal":

> *"Today is different. You've done about fifteen sessions. Enough that what you've shown us has settled into something measurable. We can show you the early shape of your profile."*

The two cautions are real:
1. *"This is early. The numbers will move as you keep doing sessions. Treat what you see as a hypothesis about yourself, not a conclusion."*
2. *"There is no good or bad here. The point of the profile is not whether you scored high or low on anything. The point is the gap — the places where the version of yourself you say you want to be doesn't quite match the version your everyday choices reveal."*

### The reveal itself

The participant sees their per-domain revealed score, their aspirational stated score, and the gap. Per [`interpretation.md`](interpretation.md), the scores are presented with explicit confidence intervals (no bare numbers); the per-domain breakdown is opt-in (off by default).

The closing CTA is the open door:
> *"You can keep going as you have been. You can pick one of the gaps to focus on. You can also do neither and just keep observing."*

None of those is presented as the right one.

### Sessions 16–21 — post-reveal

Some participants pick a gap and engage; some don't; some explicitly opt to keep observing without engaging the growth scaffolding. The analyzer logs this engagement choice.

For participants who picked a growth direction, the rest of the week's scenarios rotate slightly more heavily toward that domain (per `concept.md` §"Intervention modules" item B, "Scenario rehearsal mode"). This is **NOT MVP-1 intervention efficacy testing** — that's MVP-2. For MVP-1 the rotation shift is recorded but not measured for behavior-change effect.

### Week 3 check-in interview

The week-specific question, asked just before the profile reveal: *"Tomorrow or the day after — depending on your session cadence — the app is going to show you a profile for the first time. What do you expect to see? What do you hope to see? What are you nervous about?"*

The researcher's listening focus is on anticipatory anxiety and on whether the participant has formed accurate or inaccurate expectations.

---

## Week 4 — sessions 22 through 28 — informant wave + closing

### Sessions 22–25 — informant opt-in

At session 22 the participant sees the optional informant-wave opt-in screen per [`pilot-materials/informant-recruitment.md`](pilot-materials/informant-recruitment.md). The framing names that informant ratings are research-relevant ("your data is more meaningful when paired with how people who know you well would describe you"), explicitly allows declining ("if you say no, you still get the full study compensation"), and surfaces the third party's separate consent obligation.

Participants who opt in name two informants (one personal-life, one professional). The informants receive separate invitation emails with a brief explanation and a link to the HEXACO-60 informant-rated form. They have 14 days to complete; day-3 and day-7 reminders follow if needed.

### Sessions 26–28 — the arc closes

The final week of sessions has its own texture. By session 27 the participant has been doing this for nearly four weeks; the daily rhythm is by now genuinely habit-forming or genuinely tedious. The story prompts that surface this week ask about anticipated tests in the participant's near-future ("Is there a situation coming up that you think will test you in some way?").

The final session is session 28, but it isn't marked as the final session. The participant doesn't see "you've finished." They see the same session-end card they've seen all four weeks. The closing happens in the exit interview.

### Week 4 check-in interview — pre-exit-interview

The week-specific question: *"You've seen the profile now. What did it tell you that you didn't already know?"*

The researcher's listening: surprise (which is where the instrument is informative beyond self-knowledge), mismatches (which read as the app being wrong about the user vs. catching something the user hadn't noticed), and forward intention (whether the participant would welcome the MVP-2 intervention layer).

### Exit interview — week 5

The 45-minute exit interview per [`pilot-materials/exit-interview-script.md`](pilot-materials/exit-interview-script.md). Five sections: usability, scenario interpretability (re-narration test on three pre-selected scenarios), honesty-of-self-reporting (the most delicate section — social-desirability bias acknowledgment), wellbeing, open.

The "wished I'd asked" prompt at the end is the highest-signal moment of the entire pilot. Most participants will hesitate; the researcher resists filling the silence.

---

## Post-pilot — Day 33 onward

### Compensation

Within 14 days of the exit interview, compensation processes through the platform (Prolific or equivalent):
- ≥ 14 sessions + exit interview = $50
- 7–13 sessions = $30
- 1–6 sessions = $15

Informants get $20 each on completion.

### Data deletion

Per [`pilot-materials/data-handling-policy.md`](pilot-materials/data-handling-policy.md), the default 90-day post-pilot deletion timeline starts. At day 60–90 the researcher:
1. Drops the encrypted user-data tables
2. Verifies against backup retention (30-day rotation enforces no older backups)
3. Audit-logs the deletion
4. Optionally notifies participants

The aggregated quantitative metrics (completion rates, response-time medians, scenario-flag counts) are retained for the eventual published findings. Anonymized interview transcripts are retained for cross-pilot pattern analysis.

### Decision document

Within 30 days of all exit interviews complete, the researcher compiles a GO / NO-GO / MIXED decision per [`pilot-protocol.md`](pilot-protocol.md) §"Decision criteria for proceeding to OSF lock." If GO, the main-study OSF pre-registration is finalized and recruitment opens; if NO-GO, the project's measurement validation has surfaced an issue; if MIXED, revise per the contingent-revision table and run a second n=10 pilot.

---

## What this walkthrough demonstrates that other docs don't

The repo's documents each cover one slice of the project. The **temporal arc** — the felt experience of a participant moving through 4 weeks of daily 5-minute sessions, with weekly researcher calls, a profile reveal at week 3, an optional informant wave at week 4, and a structured exit at week 5 — is hard to assemble from any single document. This walkthrough is the synthesis.

It is also reference, not spec. The runtime engineering would deliver this experience dynamically against the JSON content. The participant-facing words shown in screens come from `onboarding.md`. The pacing comes from `pilot-protocol.md`. The interview structure comes from `pilot-materials/weekly-interview-script.md` and `exit-interview-script.md`. The data handling comes from `pilot-materials/data-handling-policy.md`. This walkthrough threads them.

---

## What this walkthrough does NOT cover

- The screen-level experience of any single session (see [`first-session-walkthrough.md`](first-session-walkthrough.md))
- The technical specification of any single component
- The MVP-1 main study (n=200, 8-week protocol) which scales this same arc to a much larger cohort with a richer scenario corpus
- The MVP-2 intervention layer (whose efficacy depends on MVP-1's measurement validation succeeding first)

For those, see the corresponding documents in the cross-references.

---

## Cross-references

- [`pilot-protocol.md`](pilot-protocol.md) — the specification this walkthrough renders
- [`first-session-walkthrough.md`](first-session-walkthrough.md) — screen-level for session 1
- [`onboarding.md`](onboarding.md) — the actual copy the participant sees on each screen
- [`pilot-materials/`](pilot-materials/) — operational documents (consent, recruitment, interviews, informant protocol, data handling)
- [`scenarios/`](scenarios/) — the authored scenario corpus (40 of ~48 target)
- [`interpretation.md`](interpretation.md) — what the analyzer's profile-reveal numbers actually mean
- [`scoring.md`](scoring.md) — how the analyzer computes the numbers shown at session 15
