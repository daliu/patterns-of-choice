# Patterns of Choice

A longitudinal instrument for measuring revealed ethical preferences, comparing them against stated values, and offering opt-in scaffolding for user-defined growth.

**Status:** Concept stage. No code yet. See [`concept.md`](concept.md) for the working design (Draft 0.2) and [`mvp.md`](mvp.md) for the proposed first build spec.

## What this is

Not a personality quiz. Not a self-improvement app. A research-grade instrument delivered as software, framed as a contemplative practice — *a long-form mirror with optional scaffolding*.

The actionable signal is the **gap** between two separately-captured layers:

- **Revealed values** — extracted from behavioral choices in repeated low-stakes scenarios over weeks
- **Stated values** — captured via forced-choice inventory across three layers (current self, aspirational self, admired other)

Existing instruments measure one side or the other. None systematically operationalize the gap. The gap is what makes growth concrete.

## Repo layout

- [`concept.md`](concept.md) — the working concept document (Draft 0.2)
- [`mvp.md`](mvp.md) — proposed scope for the first measurement-validation build (MVP-1)
- [`onboarding.md`](onboarding.md) — user-facing copy and sequence for the first 3 sessions and the profile reveal
- [`pre-registration.md`](pre-registration.md) — OSF-filing-ready template for MVP-1's measurement-validation study, with pre-specified hypotheses, analysis plan, and falsification thresholds
- [`pilot-protocol.md`](pilot-protocol.md) — n=10 usability/calibration pilot that precedes the OSF lock; defines go/no-go criteria for the main study
- [`pilot-materials/`](pilot-materials/) — operational documents the pilot needs before launching (consent form template, recruitment script template). Drafts, not IRB-final
- [`scoring.md`](scoring.md) — analytical specification: how raw session-log and inventory data become the revealed / stated / gap / cost-of-virtue scores referenced by the pre-registration
- [`interpretation.md`](interpretation.md) — what the analyzer's output numbers actually mean for a user, a researcher, or a future engineer reading them. Companion to `scoring.md` (which says *how*) explaining *what they mean*
- [`first-session-walkthrough.md`](first-session-walkthrough.md) — linear simulation of what a participant sees, screen by screen, in their first session. Cross-references the actual onboarding copy, values deck, scenario corpus, and types into a single read-through
- [`pilot-walkthrough.md`](pilot-walkthrough.md) — companion to the first-session walkthrough at the longitudinal level. Traces the full 4-week pilot arc: pre-week-1 recruitment / consent, weeks 1-4 of sessions and check-ins, profile reveal at week 3, optional informant wave at week 4, exit interview, post-pilot deletion timeline
- [`pilot-pre-launch-checklist.md`](pilot-pre-launch-checklist.md) — operational forward-sequence: what has to happen, in what order, by whom, before recruitment opens. Phases 0-9 from concept-complete through GO/NO-GO decision. Companion to PROJECT-STATUS (current-state) and pilot-protocol (spec); this one is the do-list with output artifacts named per item. End-to-end realistic timeline: 9-15 months
- [`validity-threats.md`](validity-threats.md) — adversarial audit. Construct / internal / external / reliability / statistical validity threats categorized; mitigation traces; residual-risk ratings; detection method via pilot or main study. Surfaces four concrete recommended additions to the pre-registration that aren't currently scheduled (inter-rater tag-axis agreement, financial-situation sensitivity, familywise-corrected hypothesis reporting, CI-aware SEM-fit reporting). Audience: prospective co-PI, grant reviewer, or replication-extension researcher
- [`h8-narrative-immersion-design.md`](h8-narrative-immersion-design.md) — design proposal for H8: narrative-immersion-with-recurring-character-attachment as a measure-debiasing mechanism against social-desirability response. NOVEL methodological claim (not a psychometric import). H8a tests debiasing; H8b tests attachment-grounding. Source document for downstream multi-iteration changes to concept / pre-reg / scoring / DECISIONS / pilot-protocol; outlines instrument modifications needed (recurring NPC cast, paired narrative-vs-abstract probes, immersion instrument). Per Dave's direction 2026-05-30
- [`demo/`](demo/) — single self-contained HTML demo file that renders one quick-fire scenario interactively. Vanilla JS, no build tooling. Demo only; runtime stack decision still open per DECISIONS §14
- [`analysis/`](analysis/) — versioned data files the analyzer consumes (currently: the tag-to-axis mapping). Part of the pre-registration; locked at OSF filing
- [`types.ts`](types.ts) — TypeScript type definitions for all the JSON content schemas. Declarative only; no runtime or framework commitment. Schema-in-code complement to `scenarios/SCHEMA.md` and `inventory/SCHEMA.md`. Any future implementation can typecheck against this contract.
- [`DECISIONS.md`](DECISIONS.md) — running log of load-bearing design choices with rationale; lightweight ADR format. Append-only.
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current state snapshot across every track. Solid vs provisional, open decisions waiting on the owner, dependency checklists to launch each phase, realistic timeline.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — five-minute orientation for any new contributor. What to read first, by-goal entry points, conventions, what kinds of contributions are in/out of scope.
- [`Makefile`](Makefile) — `make setup` / `make validate` / `make analyze` / `make demo` — the common-task entry points.
- [`scripts/`](scripts/) — utility scripts. Currently: `validate.py` (content-validation, Python, single dependency `jsonschema`). The first executable code in the repo. See [`scripts/README.md`](scripts/README.md) for the engineering-line-crossing rationale.
- [`scenarios/`](scenarios/) — authored-scenario corpus and JSON schema (4 quick-fires, 4 cost-of-virtue probes, 1 branching narrative)
- [`inventory/`](inventory/) — stated-values inventory module: values deck, forced-choice pairs, three-layer prompts, story prompts
- [`literature/`](literature/) — literature notes and citations (iterated by research agents)

## Operating constraints

These are design commitments, not nice-to-haves. They follow from the trust premise the product depends on.

- Descriptive, never prescriptive. The system never tells the user a choice was wrong.
- No social comparison features. No leaderboards. No "more honest than X% of users."
- No engagement-based monetization. No ads, no sponsorships, no data brokerage.
- Local-first by default; E2E encrypted sync; no training on user data.
- No enterprise / employer-screening product, ever.
- Pre-registered validation studies. Open-source instrument. Published findings.

## Status

Concept Draft 0.2 (incorporates first literature review pass). MVP-1 spec drafted. Not yet validated, not yet built.
