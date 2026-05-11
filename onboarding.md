# Onboarding copy and sequence — Draft 0.1

User-facing language for sessions 1–3, the "first contact" window. Codifies the candor-without-undersell framing the concept doc flagged as a remaining gap: the user has to understand they are part of an experiment, not the recipient of a verdict, without that framing making the product feel unproven or under-confident.

This document is the source of truth for the actual strings rendered in the app. Engineering reads from here; copy lives versioned with the concept and the validation plan.

---

## Design principles

**Calm, not warm; serious, not academic.** The tone target is a research instrument that respects the user — closer to a clinician's intake than a wellness app. No exclamation marks, no second-person "you can do this!" energy. Equally: no jargon, no field-specific vocabulary that would alienate a layperson.

**Candor as the trust move.** The product is in front of a contested empirical premise. The user-facing copy names this rather than burying it. The thing being asked of the user — daily 5-minute sessions over weeks — is significant enough that hiding the uncertainty would be a worse breach of trust than acknowledging it.

**No promises about outcomes.** Never "this will change you." Never "you'll be more honest in 30 days." The product is a mirror with optional scaffolding; the language should never promise a destination.

**The user is doing the work, not receiving a service.** Frame the user as an active participant whose data shapes what we learn, not as a customer being delivered insight.

**No moralizing.** Never tell the user a value is more important than another. Never tell them their choice was wrong. Never imply that the system knows better than they do what they should care about.

---

## Anti-patterns (do not write these)

- ❌ "Discover the real you."
- ❌ "Become the person you were meant to be."
- ❌ "Most people don't realize…"
- ❌ "Science-backed."
- ❌ Any percentage or score in onboarding.
- ❌ Any comparison to other users in onboarding.
- ❌ Promising a specific outcome (more honest, more present, more aligned).
- ❌ Asking the user to commit to a streak.
- ❌ Calling the system "AI" or invoking the LLM. The LLM is implementation detail; the user shouldn't think about it.
- ❌ Calling this "therapy," "coaching," or anything therapy-adjacent. It is not, and saying it is would be both untrue and legally fraught.

---

## Session 1 — first contact (≈ 6 min)

### Opening screen

**Headline:**
> Patterns of choice

**Subhead:**
> A mirror for the values you live by, alongside the ones you say you live by.

**Body (one paragraph):**
> This is a daily practice — five minutes a session, three to four weeks before you'll see anything resembling a profile. It will ask you to make small choices and to describe what you care about. It will then show you where those two things line up and where they don't. It will not tell you whether your patterns are good or bad.

**Single CTA:**
> Begin

### Second screen — the candor moment

**Headline:**
> Before you start

**Body:**
> There's something to be honest about up front. The premise of this instrument — that small everyday choices reveal something useful about how you actually live — is not fully established in the research literature. Studies of trolley problems and abstract dilemmas have repeatedly failed to predict real behavior. Studies of mundane stakes (small monetary honesty, everyday cooperation) have done better, but no one has yet validated this specific format — a daily-puzzle structure with continuing characters and reflection over weeks. Whether it works is partly what we are figuring out together. Your data shapes that.
>
> If that uncertainty would make you not want to start, this is the right moment to step away.

**CTAs:**
> Continue · Step away

### Third screen — what session 1 contains

**Headline:**
> Today's session

**Body (bulleted):**
> - A short sorting task: 20 values, pick your top five.
> - A few quick choices, paired against each other.
> - One free-text question.
>
> About six minutes. There is no right answer to any of it.

**CTA:**
> Start

### After the card sort

**Inline note rendered after the user finishes the top-5 selection:**
> Thank you. You'll do this same sort two more times this week, with two different framings — the version of you you'd want to be, and someone you deeply respect. The differences between the three are what makes this instrument work.

### Session-end card

**Headline:**
> Done for today.

**Body:**
> One observation — nothing to act on:
>
> *(rendered observation, descriptive only — e.g. "You picked 'honesty' and 'loyalty' in your top five. Those two are sometimes in tension. We'll come back to that.")*
>
> See you tomorrow. About the same time, if that works.

**No streak counter. No "you're on a roll." No notification commitment beyond the user's chosen daily reminder time.**

---

## Session 2 — continuation (≈ 5 min)

### Return screen

**Headline:**
> Welcome back.

**Body:**
> Today is the second sorting task. Same 20 values, different framing: not how you live, but who you'd want to become.
>
> After that, ten quick comparisons.

**CTA:**
> Start

### Aspirational-self framing prompt

Surfaced before the aspirational card sort:

> Try to think about who you want to be in a year. Not in terms of achievements — in terms of character. The version of yourself you would, on reflection, most respect.

### Pairwise comparison framing

Surfaced before the 10-pair sequence:

> Each pair shows two things people often value. When you can't fully have both — which do you actually lean toward?

(Pair text follows the JSON format from `inventory/pairwise-pairs.json`.)

---

## Session 3 — admired other + first scenarios (≈ 7 min)

### Admired-other setup

> One last sort. This time bring someone specific to mind — a person you deeply respect. Not for their achievements. For their character.
>
> Just their initials, if you want to write them down somewhere.

After initials entry (optional, never required):

> Now: how would *you* describe what they actually do, day to day?

### Story prompts

Two free-text prompts surface here. Rendered with no character minimum, no maximum word limit:

1. *"Tell me about a time, recently, when you were quietly proud of how you handled something. Not a big moment; one of the small ones. Two or three sentences is plenty."*
2. *"Tell me about a time, recently, when you let yourself down — not catastrophically, just a small moment when you knew you didn't act like the person you want to be."*

### First quick-fire round

Surfaced as the closing module of session 3:

> A new kind of task: rapid choices under a timer. Each one is between two options, eight seconds each. The point is to capture what you reach for first — not what you'd choose on reflection. There are no right answers and the timer is part of the data, not part of a test.

(Quick-fire content follows the JSON format from `scenarios/sample/qf-truth-001.json` or rotation-equivalent.)

---

## Profile reveal (session ≈ 15, end of week ~3)

This is the highest-stakes copy in the product. The user has done three weeks of work for it.

### Pre-reveal screen

**Headline:**
> Today is different.

**Body:**
> You've done about fifteen sessions. Enough that what you've shown us has settled into something measurable. We can show you the early shape of your profile.
>
> Two cautions before you see it.
>
> First — this is early. The numbers will move as you keep doing sessions. Treat what you see as a hypothesis about yourself, not a conclusion.
>
> Second — there is no good or bad here. The point of the profile is not whether you scored high or low on anything. The point is the gap — the places where the version of yourself you say you want to be doesn't quite match the version your everyday choices reveal. That gap is yours to do something about, or to leave alone. We have no opinion on which.

**CTA:**
> Show me

### After the reveal

Single observation, never a score. Confidence intervals always shown. Per-domain breakdown is optional, off by default — the user can opt into details.

### Closing — the open door

**Body:**
> You can keep going as you have been. You can pick one of the gaps to focus on. You can also do neither and just keep observing.
>
> None of those is the right one. Tomorrow's session is the same length as today's, regardless of which you pick.

**CTAs:**
> Keep observing · Focus on one gap · Take a break

---

## Engineering notes

- Every string above is content; ship as JSON or YAML in a copy file (e.g. `copy/onboarding-en.yaml`) so editorial review is decoupled from deploy.
- Localization is post-MVP-1; English-only is acceptable through Phase-1.
- "Step away" CTA on the candor screen is real — clicking it should not nag, retarget, or attempt to reconvert. Log the event for the validation cohort (with consent) so we can estimate ecological-validity-related attrition.
- A11y: minimum 16pt body type, no animation on copy reveal, no time-pressure on any onboarding screen except the explicit quick-fire round.

---

## Open questions

- Whether to surface the per-session "one observation" line in the validation cohort during the baseline 3-week period. Arguments either way: surfacing it makes the experience feel reciprocal; suppressing it gives a cleaner pre-intervention baseline. **Decision deferred until pre-registration locks in MVP-1.**
- Whether to require the user to type a name into the "admired other" prompt or accept initials only. The literature suggests *some* concreteness matters (Vazire 2010 on informant specificity); requiring full names introduces a privacy ask the candor framing has not yet earned. Initials-only is the conservative MVP-1 default.
- The exact word "experiment" vs. "calibration period" vs. "study" in the candor moment. Current draft uses none of them by name in user-visible copy — the explanation is given without the label. If user-testing shows confusion, "we are figuring out together" can become "this is a study you are part of." Defer to pilot.
