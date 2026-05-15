# Informant-Report Recruitment — Pilot (Template)

**Status:** Draft. Operationalizes the "optional week-4 informant wave" per `../pilot-protocol.md` and `../pre-registration.md`. Informant data is *the* highest-signal validation step in the scoring plan (per Vazire 2010 SOKA and Connelly & Ones 2010 meta), but it's also the most operationally complex single piece of the pilot. This document specifies how to actually do it.

---

## Why this is high-stakes

Per `../pre-registration.md`:
> **Phase 2 (6–12m): Multi-source validation — primarily informant reports (partner/coworker/friend ratings), plus remote economic-game protocols. The credibility moat.**

Per `../literature/ecological-validity-positive.md`:
> Connelly & Ones 2010 meta (N = 44,178) shows informant ratings outperform self-report for evaluative-and-observable traits — honesty-humility being the prototype.

For the pilot specifically, informant data is optional but recommended because:
1. It surfaces operational issues (recruiting informants is harder than the pilot-protocol suggests; running this on n=10 catches the friction before scaling to n=200)
2. It gives the eventual pre-registration writers a real handle on opt-in rates and informant-completion rates
3. It is the most differentiating feature of the validation plan vs. typical consumer-app pilots

If the pilot proceeds without informant data, the Phase-2 plan's credibility-moat claim becomes harder to defend.

---

## Sequencing

Week 1–3: standard pilot, no informant material surfaced to participant.

**Week 4, session 22 onward**: participant sees an opt-in screen offering the informant-report option. Copy:

> *"For research purposes, your data is more meaningful when paired with how people who know you well would describe you on the same dimensions. We'd like to invite two people to fill out a short questionnaire about you — one from your personal life, one from professional. They'll see a different (much shorter) instrument than you do.*
>
> *This is optional. If you say no, you still get the full study compensation. If you say yes, your two informants will be compensated $20 each for completing the questionnaire.*
>
> *We'll send them the invitation; you tell us who, and we handle the rest."*

CTAs:
- "Yes, I'll name two informants" → next screen
- "Not this time" → continue
- "Maybe — tell me more" → expanded explanation

### Expanded explanation (for the "tell me more" branch)

> *"The instrument we're piloting tries to capture how you make small ethical choices — about honesty, fairness, group loyalty, cooperation. Research shows that people who know you well can describe these dimensions of you more accurately than you can describe yourself, for some traits especially.*
>
> *Your informants would fill out a 60-item questionnaire rating you on those dimensions. It takes about 8 minutes for them. They wouldn't see what you've chosen in the app, and you wouldn't see what they reported. We only use their ratings, paired with your scores, to evaluate whether the app's measurements correspond to how people who know you actually describe you.*
>
> *Pick one informant from your personal life (a partner, a close friend, a sibling) and one from a professional context (a current or former coworker, a manager, a collaborator). They'll get the invitation directly from us, with your introduction, within a few days of you naming them."*

### After participant names two informants

The participant fills in:
- Informant 1: name, email, relationship description ("romantic partner of 4 years"), how long they've known
- Informant 2: same fields

System constraint: at minimum one personal-life and one professional informant. The Connelly & Ones meta found the personal-vs-professional pair maximizes evaluative-trait validity, so the system enforces this rather than letting the participant pick two partners (or two coworkers).

---

## Informant invitation email

Sent within 24 hours of participant naming the informant.

> Subject: [First name] asked you to participate in a brief research study about them
>
> Hi [Informant name],
>
> [Participant first name] is taking part in a pilot study about how people make small ethical choices in daily life. They specifically nominated you as someone who knows them well, and they'd like your help completing a small but important piece of the research.
>
> The ask is straightforward: an 8-minute online questionnaire where you rate [Participant first name] on a series of personality traits — how you would describe them based on what you've observed. There are no right or wrong answers. You won't see their responses; they won't see yours.
>
> Your time is paid: $20 for completing the questionnaire, sent through [platform — typically the same as the participant's payment platform].
>
> The link below takes you to the consent form, then to the questionnaire. You can stop at any time. Your data is encrypted and not shared with [Participant first name] or anyone outside our small research team.
>
> [Personal one-line consent form link]
>
> If you'd rather not participate, the simplest thing is to delete this email. [Participant first name] won't be told whether you completed it or not unless they specifically ask, and we'll honor your decision either way.
>
> Questions: [Co-PI name and contact]
>
> Thanks for considering it,
> [Researcher name]
> [Institution]

---

## Informant's own consent

The informant clicks the link in the invitation and lands on a consent screen — separate from the participant's. Key sections:

### What you're being asked to do
> *Fill out a brief questionnaire (about 8 minutes) about [Participant first name]. The questionnaire is a standardized personality inventory called HEXACO-60. You'll rate how strongly you agree with statements like "[Participant] usually keeps quiet about their own concerns" on a 1–5 scale. There are 60 items.*

### What we do with your data
> *Your ratings are paired with [Participant first name]'s app data for the research analysis. Your individual responses are not shared with [Participant first name] under any circumstance during the active pilot. Your responses are stored encrypted, retained for analysis, then deleted within 90 days of pilot end.*

### Compensation
> *$20 for completing the questionnaire, paid within 14 days of completion through [platform].*

### Right to decline / withdraw
> *You can decline this invitation by closing this page. If you start and want to stop, you can. If you complete it and later want your data deleted, email [contact] within 30 days and we'll remove it. After 30 days the data is anonymized and we cannot identify your individual contribution to remove it.*

Consent button: "I agree, take me to the questionnaire."

Decline button: "No thanks." (Closes the tab; no follow-up.)

---

## The instrument

For MVP-1 pilot, informants complete the **HEXACO-60 informant-rated version** (Lee & Ashton 2018; standardized inventory). Honesty-humility subscale scored at the facet level (sincerity, fairness, greed-avoidance, modesty).

For MVP-2 / Phase-2 (when the patterns-of-choice domain taxonomy has demonstrated convergent validity with HEXACO H), an additional 12-item domain-rating instrument can be added — 3 items per MVP-1 domain — where the informant rates the user on the patterns-of-choice domain anchors directly. This is **not** added for the pilot; HEXACO-60 alone is the right anchor.

The full HEXACO-60 with informant-version wording is available from Lee & Ashton (http://hexaco.org/scales) under public-domain research license. Not reproduced in this document; the researcher running the pilot should download the canonical version.

---

## Informant follow-up

Day 3 after invitation, if no completion: gentle reminder email.

Day 7 after invitation, if no completion: final reminder, with a "we won't bother you again after this" framing.

Day 14 after invitation, if no completion: silent close-out. The participant is not told the informant didn't complete; we simply don't have data from that informant.

If a participant nominates a third informant (e.g. after the second decline), allowed without penalty up to one additional swap.

---

## Data handling specifics

- **No cross-talk between participant and informant data during pilot.** The participant cannot see their informant's responses; the informant cannot see the participant's session data.
- **Pairing for analysis only.** When the analyzer runs, the participant's HEXACO H facet-level scores and the informant's HEXACO H facet-level ratings are joined on the participant-ID hash. Both are stored separately and the join happens at analysis time, not at storage time.
- **30-day informant-data withdrawal window.** After 30 days post-completion, informant data is anonymized (informant identity stripped); only the pairing-hash remains. Informant can no longer withdraw their specific contribution after that point.
- **Deletion timeline.** All informant data deleted within 90 days of pilot end, alongside participant data per consent form.

---

## What we measure operationally

Per pilot-protocol.md, the informant wave gives us operational data for the eventual Phase-2 scale-up:

| Metric | Target (per Connelly & Ones meta) |
|---|---|
| Opt-in rate (participants accepting informant wave) | ≥ 60% |
| Informant invitation → completion rate | ≥ 50% |
| Per-participant informant completion (≥ 1 of 2 informants completes) | ≥ 70% |
| Median time invitation → completion | ≤ 5 days |
| Informant qualitative feedback "experience was positive / neutral" | ≥ 80% |

The pilot's n=10 means each metric is noisy; the point is to surface operational issues (people-named-don't-respond patterns, informant types that work, friction points in the email flow) before scaling.

---

## Open operational questions

- **Two-informant minimum vs. one acceptable**: pilot-protocol.md says "≥2 informants per user, aim for 3." Should we accept participants whose only one informant completes? Probably yes for pilot data-collection purposes (don't throw out partial data) but flag in the per-participant tracker.
- **Informant who's connected to multiple participants**: in a small pilot recruited via co-PI network, two participants might name the same informant. Handle by: separate invitations, separate consents, informant chooses whether to complete one, both, or neither.
- **Cultural variants of HEXACO-60**: the canonical instrument has been validated in many languages but the pilot is English-only. If the chosen platform has non-English speakers, exclude (don't translate ad hoc) at pre-screening.
- **What to do when an informant emails back with concerns about the participant**: rare but real. Pre-decide: do not share informant communications with participant unless informant explicitly authorizes. Treat as a research-ethics edge case requiring co-PI judgment in real-time.

---

## Cross-references

- `../pilot-protocol.md` §"Recruitment" — opt-in framing
- `../pre-registration.md` H4 — informant H rating correlates with revealed truth-telling (r ≥ 0.20)
- `../scoring.md` §7 — informant ratings as a CFA convergent-validity anchor
- `../literature/ecological-validity-positive.md` — Connelly & Ones meta, Vazire SOKA, why informants matter
- `consent-form.md` — participant's informant-wave opt-in language
