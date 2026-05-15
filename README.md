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
- [`demo/`](demo/) — single self-contained HTML demo file that renders one quick-fire scenario interactively. Vanilla JS, no build tooling. Demo only; runtime stack decision still open per DECISIONS §14
- [`analysis/`](analysis/) — versioned data files the analyzer consumes (currently: the tag-to-axis mapping). Part of the pre-registration; locked at OSF filing
- [`types.ts`](types.ts) — TypeScript type definitions for all the JSON content schemas. Declarative only; no runtime or framework commitment. Schema-in-code complement to `scenarios/SCHEMA.md` and `inventory/SCHEMA.md`. Any future implementation can typecheck against this contract.
- [`DECISIONS.md`](DECISIONS.md) — running log of load-bearing design choices with rationale; lightweight ADR format. Append-only.
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current state snapshot across every track. Solid vs provisional, open decisions waiting on the owner, dependency checklists to launch each phase, realistic timeline.
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
