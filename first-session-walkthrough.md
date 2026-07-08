# First Session — Walkthrough

**Status:** Reference document. A linear simulation of what a participant sees in their first session of the pilot, pulling actual copy from `onboarding.md` and an actual scenario from `scenarios/sample/`. The point of this document is to make the abstract design concrete — a reviewer can read it straight through and form a felt sense of the experience without having to assemble it from the pieces.

Not a build spec. The runtime engineering would render this dynamically; this document is the static rendering.

---

## Screen 1 — first open

The participant has clicked through from the recruitment email. The app loads. They see:

```
┌──────────────────────────────────────────┐
│                                          │
│         Patterns of Choice               │
│                                          │
│  A mirror for the values you live by,    │
│  alongside the ones you say you live by. │
│                                          │
│  This is a daily practice — five minutes │
│  a session, three to four weeks before   │
│  you'll see anything resembling a        │
│  profile. It will ask you to make small  │
│  choices and to describe what you care   │
│  about. It will then show you where      │
│  those two things line up and where      │
│  they don't. It will not tell you        │
│  whether your patterns are good or bad.  │
│                                          │
│           [        Begin        ]        │
│                                          │
└──────────────────────────────────────────┘
```

---

## Screen 2 — the candor moment

After pressing Begin, the next screen:

```
┌──────────────────────────────────────────┐
│                                          │
│           Before you start               │
│                                          │
│  There's something to be honest about    │
│  up front. The premise of this           │
│  instrument — that small everyday        │
│  choices reveal something useful about   │
│  how you actually live — is not fully    │
│  established in the research literature. │
│  Studies of trolley problems and         │
│  abstract dilemmas have repeatedly       │
│  failed to predict real behavior.        │
│  Studies of mundane stakes (small        │
│  monetary honesty, everyday              │
│  cooperation) have done better, but no   │
│  one has yet validated this specific     │
│  format — a daily-puzzle structure with  │
│  continuing characters and reflection    │
│  over weeks. Whether it works is partly  │
│  what we are figuring out together.      │
│  Your data shapes that.                  │
│                                          │
│  If that uncertainty would make you not  │
│  want to start, this is the right        │
│  moment to step away.                    │
│                                          │
│      [ Continue ]    [ Step away ]       │
│                                          │
└──────────────────────────────────────────┘
```

The "Step away" CTA is real. If the participant clicks it, the app does not nag, retarget, or attempt to reconvert. The event is logged (with the participant's consent from the consent form) so the eventual study analysis can estimate the ecological-validity-related attrition rate.

---

## Screen 3 — today's session

After Continue:

```
┌──────────────────────────────────────────┐
│                                          │
│             Today's session              │
│                                          │
│  • A short sorting task: 20 values,      │
│    pick your top five.                   │
│  • A few quick choices, paired against   │
│    each other.                           │
│  • One free-text question.               │
│                                          │
│  About six minutes. There is no right    │
│  answer to any of it.                    │
│                                          │
│              [   Start   ]               │
│                                          │
└──────────────────────────────────────────┘
```

---

## Screen 4 — the card sort

After Start, the participant sees the 20-value deck. The 20 cards are presented in a randomized order (with the family-category roles' parallel "relational variant" available as a presetable option per `inventory/relational-variant.json` but defaulting OFF in MVP-1). Each card displays the label and the behavioral anchor:

```
┌──────────────────────────────────────────┐
│                                          │
│  Pick your top 5 values                  │
│                                          │
│  Which values most describe how you      │
│  actually act today — not how you want   │
│  to act?                                 │
│                                          │
│  Drag your picks to the top area, or     │
│  tap to select.                          │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Honesty                          │    │
│  │ Saying what's true, even when    │    │
│  │ it's costly for me or            │    │
│  │ uncomfortable for others.        │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Tact                             │    │
│  │ Saying true things in a way that │    │
│  │ protects others' dignity.        │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │ Loyalty                          │    │
│  │ Standing with the people closest │    │
│  │ to me, especially when it costs  │    │
│  │ me.                              │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ... 17 more cards, scrollable           │
│                                          │
│              [Done picking]              │
│                                          │
└──────────────────────────────────────────┘
```

This is the **current self** layer per `inventory/three-layer-prompts.json`. The two other layers — aspirational self, admired other — will be presented in sessions 2 and 3.

If the participant has selected a value, the app subtly shows the behavioral anchor again and asks: *"Is this how you'd actually describe yourself?"* (raising the cost of selecting a value casually). The participant can keep it or swap it.

---

## Screen 5 — first quick-fire scenario

After the participant finishes the card sort (~3 minutes), the app moves to the quick-fire module. The screen briefly explains the task:

```
┌──────────────────────────────────────────┐
│                                          │
│  A new kind of task: you read each       │
│  moment untimed, then reveal two         │
│  answers and a short clock starts.       │
│                                          │
│  It captures which one you reach for     │
│  first — not how fast you read, and      │
│  not what you'd choose on reflection.    │
│  There are no right answers; the clock   │
│  is part of the data, not a test.        │
│                                          │
│              [  Ready  ]                 │
│                                          │
└──────────────────────────────────────────┘
```

After Ready, the first item appears — sampled from one of the four MVP-1 domains. For this walkthrough we'll use `qf-truth-001-i01`. The prompt shows first with no clock, so reading time never eats the decision window:

```
┌──────────────────────────────────────────┐
│                                          │
│  Your housemate asks if you ate the      │
│  leftovers they were saving. You did.    │
│                                          │
│  [  I've read it — show the choices  ]   │
│                                          │
└──────────────────────────────────────────┘
```

When the participant reveals the choices, the decision clock starts — response time is decision latency, not reading speed:

```
┌──────────────────────────────────────────┐
│                                          │
│  ⏱  8 seconds                            │
│                                          │
│  Your housemate asks if you ate the      │
│  leftovers they were saving. You did.    │
│                                          │
│  [        Admit it.        ]             │
│                                          │
│  [    Say you didn't see them.    ]      │
│                                          │
└──────────────────────────────────────────┘
```

The participant taps one within the clock. The next item appears the same way — prompt first and untimed — and the read-then-decide rhythm repeats:

```
┌──────────────────────────────────────────┐
│                                          │
│  ⏱  8 seconds                            │
│                                          │
│  A friend you don't see often asks       │
│  if you liked their painting. You        │
│  didn't.                                 │
│                                          │
│  [    Say you loved it.    ]             │
│                                          │
│  [  Say it wasn't quite your taste.  ]   │
│                                          │
└──────────────────────────────────────────┘
```

And so on for six items total. If the participant doesn't answer within the timer, the item is logged as a timeout and the next item appears.

---

## Screen 6 — first story prompt

After the quick-fire (~60 seconds), the app surfaces one free-text question. For session 1, this is `story-pride` per `inventory/story-prompts.json`:

```
┌──────────────────────────────────────────┐
│                                          │
│  Tell me about a time, recently, when    │
│  you were quietly proud of how you       │
│  handled something. Not a big moment;    │
│  one of the small ones. Two or three     │
│  sentences is plenty.                    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │                                  │    │
│  │                                  │    │
│  │                                  │    │
│  └──────────────────────────────────┘    │
│                                          │
│  [skip]                  [Done]          │
│                                          │
└──────────────────────────────────────────┘
```

The "skip" CTA is real and used without penalty. Declining is itself a signal that gets logged.

If the participant types something, the follow-up appears:

```
If you can: what was the alternative — what
would the less-proud version of you have
done in that moment?
```

(Same free-text textarea below.)

---

## Screen 7 — session-end card

After the story prompt (or skip), the session ends:

```
┌──────────────────────────────────────────┐
│                                          │
│             Done for today.              │
│                                          │
│  One observation — nothing to act on:    │
│                                          │
│  "You picked 'honesty' and 'tact' in     │
│   your top five. Those two are           │
│   sometimes in tension. We'll come back  │
│   to that."                              │
│                                          │
│  See you tomorrow. About the same time,  │
│  if that works.                          │
│                                          │
│         [Set tomorrow reminder]          │
│                                          │
└──────────────────────────────────────────┘
```

**No streak counter.** **No "you're on a roll."** No score. The observation is descriptive (the user's specific selections are mentioned) but does not interpret which value is "better."

The reminder is opt-in. If the participant sets one, the app surfaces a notification at roughly the chosen time the next day. If not, the app does not push at all.

---

## What the participant doesn't see (yet)

- Any score from their card sort. No domain breakdown. No "you're a 4 on honesty" message.
- Any score from the quick-fire round. No "you chose the honest option 4 of 6 times" message.
- Any per-day or longitudinal trend. No charts. No graphs.
- Any comparison to other users (and they won't, ever — see `concept.md` Operating constraints and `DECISIONS.md §9`).

The first observable measurement comes at **session ~15** (week 3), the profile reveal. Until then, every session ends with one descriptive observation.

---

## What gets logged

During this single first session, the app records:

- **20 card-sort observations** (one per value in the deck, with `selected: true` for the 5 picks). Per `inventory/SCHEMA.md` and `types.ts` `CardSortResponse`.
- **6 quick-fire session-log entries** (one per item, with chosen option, tags from the scenario, response time, presented position, timeout boolean). Per `types.ts` `SessionLogEntry`.
- **1 story-prompt response** (free text, LLM-coded post-hoc to taxonomy per `inventory/story-prompts.json` §coding_strategy). LLM coding is run locally on the device for privacy per `pilot-materials/data-handling-policy.md`.
- **Session metadata**: start timestamp, total duration, voluntary skip count, observation shown.

Total data volume from session 1: roughly 30 records, all stored locally first. If sync is opted in, encrypted blob synced to server.

---

## What the researcher does

Within 24 hours of the first session:
- Confirm the session log is well-formed (validator runs in CI)
- Schedule the first weekly check-in for ~7 days later
- Note any flags in the per-participant tracker

The researcher does NOT inspect the participant's session content unless the participant specifically asks (per `pilot-materials/data-handling-policy.md` §"Access controls").

---

## Cross-references

- `onboarding.md` — full session 1–3 + profile-reveal copy
- `scenarios/sample/qf-truth-001.json` — the source of the quick-fire items shown
- `inventory/values-deck.json` — the 20 values shown in the card sort
- `inventory/story-prompts.json` — the source of the story prompt
- `inventory/three-layer-prompts.json` — the protocol for the three-layer card sort
- `types.ts` — the runtime data shapes the app produces
- `pilot-materials/data-handling-policy.md` — what happens to the data after the session ends

---

## Why this walkthrough exists

The repo has a substantial number of documents, each focused on one slice of the project. A reader assembling the full participant experience has to mentally cross-reference at least eight files. This walkthrough is the single document where that cross-referencing is already done — the cost of one read, instead of several.

It is reference, not spec. The runtime engineering would render dynamically against the JSON content; the appearance here uses ASCII boxes for compactness. The actual app would use a clean visual design appropriate to a contemplative-practice rather than a productivity-app aesthetic.

The walkthrough should be updated whenever onboarding.md, the values deck, or the first-session scenario rotation changes.
