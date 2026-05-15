# Project Status

**Last updated:** 2026-05-15 (after the bootstrap-CI engineering pass)

A consolidating snapshot of where every track sits right now, what's solid vs. provisional, what's waiting on which kind of human decision, and what's actually needed to launch each phase. Updated when material state changes.

For overview see [`README.md`](README.md). For decisions-made see [`DECISIONS.md`](DECISIONS.md). For design rationale see [`concept.md`](concept.md). This document is the *current state*, not the design.

---

## One-paragraph state

The repo holds a complete pre-launch specification of a longitudinal instrument for revealed-vs-stated ethical values: design, build spec, onboarding copy, pilot protocol, pre-registration template, scoring spec, interpretation guide, six pilot-operational documents, decision-log, type definitions, JSON schemas, validator + analyzer covering most of the scoring spec, CI workflow, 36 authored scenarios across 4 domains × 3 scenario types, complete inventory module, 13 literature notes. **Approximately 70 commits of content + spec + engineering over two weeks.** The project is at the gate of "everything needed to start running real-world work has been drafted" — what remains is real-world execution (recruit a co-PI, do an IRB submission, build the runtime app) that needs human decisions and partnerships beyond what can be authored autonomously.

---

## Track-by-track state

### Design and rationale: **complete and stable**

- [`concept.md`](concept.md) — Draft 0.3 with both literature passes integrated. Foundational empirical risk explicitly named in the Premise. Effect-size estimates calibrated to ~0.3–0.5 SD per Yeager/Milkman megastudies. Smuggled-values section names the MacIntyre/Confucian role-ethics challenge. TTM stage-matching prescriptive claim removed.
- [`DECISIONS.md`](DECISIONS.md) — 15 ADR-format entries. Load-bearing operating constraints codified. Engineering decision-point officially "line crossed for tooling, runtime still open."

These two documents are likely to need only small revisions before any real-world work. They're the load-bearing design.

### Validation plan: **drafted, pending lock**

- [`mvp.md`](mvp.md) — MVP-1 build spec. Solid; revisions in place after lit-pass 2 (HEXACO r ≥ 0.25 not 0.30; informant reports as primary Phase-2; die-roll/sender-receiver as truth-telling paradigm).
- [`pre-registration.md`](pre-registration.md) — OSF-filing template. Three primary hypotheses, four secondary. Falsification thresholds explicit. *Does not yet have a co-PI listed or IRB protocol number*; both are bound to the co-PI recruitment step.
- [`pilot-protocol.md`](pilot-protocol.md) — n=10 pilot specification. Pre-registered go/no-go criteria. *Independent of the main-study pre-reg* — the pilot's own criteria could be separately pre-registered before pilot launch.
- [`scoring.md`](scoring.md) — analytical spec. Seven sections implemented in the analyzer (§2-3, §4, §5.1, §5.2, §5.3, §6, §8); one reserved (§7 CFA) for the validation-cohort analyzer, plus §4.3 longitudinal probe trajectories.

These are pre-launch templates. Need final author-pass against the chosen co-PI's institutional IRB.

### Pilot materials: **complete drafts, IRB-ready**

[`pilot-materials/`](pilot-materials/) holds six operational documents:
- Consent form template (with the candor moment built in)
- Recruitment script template (Prolific)
- Weekly interview script (4 week-specific variants)
- Exit interview script (5-section structured 45-min)
- Informant recruitment protocol (HEXACO-60 informant-rated; 30-day withdrawal window)
- Data handling policy (technical and procedural backing for consent commitments)

These need institutional review and customization before use. The candor framing is the most likely point of IRB negotiation; reviewers used to standard IRB consent style may push back. The project's position is that the candor is structurally load-bearing.

### Onboarding / user-facing copy: **complete drafts**

- [`onboarding.md`](onboarding.md) — sessions 1–3 + profile-reveal copy. The candor moment, the card-sort framings, the quick-fire framing, the profile-reveal language.
- [`interpretation.md`](interpretation.md) — what the analyzer's output means for a human reader.
- [`first-session-walkthrough.md`](first-session-walkthrough.md) — linear simulation tying the copy + scenarios + types together.

These are user-facing prose. They will iterate against real pilot participant feedback.

### Scenarios: **75% of target authored, structurally symmetric**

36 of ~48 target scenarios. All 4 domains have 4 quick-fires + 3 narratives + 2 cost-of-virtue probes (= 9 scenarios per domain, 36 total).

| Type | Authored | Target | Authoring cost per scenario |
|---|---|---|---|
| Quick-fire rounds | 16 | ~24 | ~30 min |
| Branching narratives | 12 | ~12 | ~90 min |
| Cost-of-virtue probes | 8 | ~12 | ~20 min |

To complete to 48: ~8 more quick-fires, ~4 more probes. Roughly 5–6 hours of editorial work, or 1 quick-fire per remaining iteration if the slow pace continues.

The corpus has reached editorial stability — validator now passes most new scenarios on first run without tag-map drift. New tags introduced are mostly metadata stratifiers.

### Inventory module: **complete**

[`inventory/`](inventory/) — values deck (20 values, 5 per domain), pairwise pairs (30 pairs, 16 within-domain + 14 cross-domain), three-layer prompts (current/aspirational/admired-other), story prompts (5 free-text templates), relational variant (11 roles across 5 categories; opt-in for MVP-2). Plus JSON Schema docs in [`inventory/SCHEMA.md`](inventory/SCHEMA.md).

### Tooling: **complete for the pre-launch phase**

[`scripts/`](scripts/) holds two scripts, both pure-Python, single dependency for the validator:
- `validate.py` — scenario + inventory schema validation with cross-file integrity checks; path reachability; tag-map lookup. Catches drift before merge. Currently 36 scenarios validate cleanly.
- `analyze.py` — implements scoring.md §2-3 (revealed), §4 (probe), §5.1 (card-sort), §5.2 (Bradley-Terry pairwise via Hunter 2004 MM), §5.3 (combined stated), §6 (gap), §8 (bootstrap CIs). **Pure Python, no external statistical library.** Seven of the scoring spec's sections; the genuinely reserved ones (§7 CFA, §4.3 longitudinal probe trajectories) need either external statistical libraries or longer-running cohort data than synthetic fixtures can provide.

Plus [`types.ts`](types.ts) (declarative TypeScript schemas), JSON Schema files in `scenarios/schemas/`, GitHub Actions CI workflow auto-running the validator on push/PR, and synthetic fixture data demonstrating end-to-end runs.

### Literature: **two passes done, 13 area notes**

[`literature/`](literature/) — first pass produced 9 area notes + index. Second pass focused on ecological-validity-positive added a deeper note. Plus the `ecological-validity-positive.md` note that landed the second pass. The literature work has saturated for current purposes; further passes would be focused additions on specific questions as they arise.

### Engineering: **tooling line crossed; runtime line touched at minimum-step**

Crossed (tooling track):
- Validator (validate.py, single dependency)
- CI workflow (.github/workflows/validate.yml)
- Analyzer (analyze.py, standard library, seven scoring-spec sections)

Smallest possible runtime step taken:
- `demo/first-session.html` — single-file vanilla JS demo of one quick-fire scenario. Demonstrates the format renders interactively, includes the candor moment + step-away branch + timer + session-end observation. Does not commit to React / Svelte / any specific stack; the production runtime decision genuinely remains open.

Not crossed (production runtime):
- The product app itself with full session orchestration (multiple scenarios, three-layer card sort, story prompt, profile reveal)
- The sync infrastructure
- The auth layer
- The notification / scheduling layer
- The persistence layer (IndexedDB locally, encrypted sync)

`mvp.md §"Tech stack proposal"` names React + TypeScript + Vite as the working hypothesis but this is not locked. The runtime is genuinely the next big crossing and deserves Dave's explicit input — particularly on:

- React vs. Svelte vs. vanilla HTML
- Y.js + CRDT vs. PocketBase vs. custom backend sync
- Passkey vs. magic-link auth
- Postgres vs. SQLite-on-server for the centralized data

These choices have downstream consequences (developer talent pool, hosting cost, maintenance burden) that the autonomous iteration shouldn't make unilaterally.

---

## What's solid vs. provisional

**Solid (low chance of needing rework):**
- The 3-layer × 4-domain × 3-type scenario taxonomy
- The forced-choice pairwise inventory format
- The descriptive-not-prescriptive operating constraint
- The local-first + no-engagement-monetization commitments
- The DECISIONS.md log of choices made
- The validator
- The analyzer's §2-3, §4, §5.1, §5.2, §5.3, §6, §8 implementations (the pure-Python-tractable portion of the scoring spec is essentially complete)
- The pilot-materials' candor framing

**Provisional (likely to iterate with real-world feedback):**
- Specific scenario wordings — many will need editorial revision against pilot participants' actual responses
- Effect-size estimates — Yeager/Milkman-anchored guesses, not yet calibrated
- The cost-of-virtue probes' ladder ceilings (currently $10K base; cov-ingroup-002 is $100K) — may need revision based on real participant tolerance
- The convergent validity threshold r ≥ 0.25 — calibrated to literature meta but only the validation cohort will tell us if it's achievable
- The relational variant — content drafted but not yet user-tested for translation accuracy
- The candor moment copy — IRB negotiation is likely

**Still open as design questions** (would benefit from research):
- LLM story-coding inter-rater calibration target (κ ≥ 0.70 in scoring.md) — operationally how to achieve
- Cross-domain `value:X` scoring (DECISIONS.md §15 locked to no for MVP-1; MVP-2 may revisit)
- Identity-level vs. trait-level claim separation in the inventory (mentioned in scoring.md §5 open questions)

---

## Open decisions waiting on Dave

These are choices that need human judgment from the project owner and shouldn't be made autonomously:

1. **Runtime stack choice.** React, Svelte, vanilla, or something else. Affects everything downstream.
2. **Co-PI identification.** Who's the academic partner? Affects IRB timeline (institutional differences are substantial) and pre-registration filing.
3. **Funding / compensation budget.** Pilot needs ~$500 for 10 participants × $50; main study ~$5,000 for 200 × $25; plus informant payments and platform fees.
4. **Hosting decision.** Self-hosted, Vercel, institutional infrastructure?
5. **Open-sourcing schedule.** The repo is currently private. When does it go public — at pilot launch, at main-study launch, at first preprint?
6. **Whether to even continue.** This is the most upstream decision. The repo represents a genuine multi-year commitment to do this seriously. If the answer is "this was a useful design exercise but I'm not going to actually run it," that's a fine answer too — but the design itself doesn't need further iteration.

---

## To launch the pilot (n=10) — dependency checklist

What's needed beyond what's currently in the repo:

- [ ] Co-PI identified
- [ ] IRB application submitted (using `pilot-materials/` templates customized to the institution)
- [ ] IRB exemption or approval
- [ ] OSF account set up; pilot's go/no-go criteria pre-registered
- [ ] Recruitment platform account (Prolific or similar)
- [ ] Runtime app built (React + TypeScript per mvp.md, OR alternative)
- [ ] Sync infrastructure deployed
- [ ] 48 scenarios authored to MVP-1 target (currently 36)
- [ ] Pilot scheduling: 10 participants × 4 weeks + 1 week analysis = ~5 weeks active
- [ ] $500 in compensation budget + platform fees

Approximate timeline from "co-PI identified" to "first pilot participant signs consent": 8–12 weeks (dominated by IRB submission + app build, which can run in parallel).

## To launch MVP-1 main study (n=200) — dependency checklist

Beyond pilot launch:

- [ ] Pilot completes; go/no-go decision arrives at GO per pilot-protocol.md decision criteria
- [ ] Any scenario / copy revisions surfaced by pilot incorporated
- [ ] Main-study pre-registration filed at OSF (the template at pre-registration.md, finalized)
- [ ] Statistical analysis code finalized in R (lavaan for CFA) or Python (statsmodels) — the validation analyzer beyond what `analyze.py` covers
- [ ] HEXACO-60 administration integrated into the protocol
- [ ] Informant infrastructure scaled (multiple informants per user, separate consents)
- [ ] $5,000 in participant compensation + ~$2,000 informant compensation + platform fees + hosting
- [ ] Main-study scheduling: 8-week active study + ~6-week analysis + ~3-month preprint cycle

Approximate timeline from pilot end to first preprint: 6–9 months.

## Long-term (MVP-2 / intervention)

Reserved. Per `pre-registration.md` §"Out of scope," MVP-2 (the intervention layer that nudges users toward closing self-identified gaps) is contingent on MVP-1's measurement validation succeeding. Designing MVP-2 in detail now is premature — the design depends on what MVP-1 reveals about which measurement signals are real.

---

## Realistic timeline if everything went well

| Milestone | Earliest realistic |
|---|---|
| Co-PI recruited | +2 months from "decide to do this" |
| IRB approval | +4 months |
| Runtime app built | +4 months (parallel to IRB) |
| Pilot starts | +5 months |
| Pilot ends, go/no-go decision | +7 months |
| Main study starts | +9 months |
| Main study ends | +11 months |
| First preprint | +14 months |
| Validation status established | +18 months |

This is the **optimistic** path. Most projects with this profile take 50–100% longer due to delays at each step (IRB revisions, recruitment shortfall, analysis re-runs, manuscript revisions).

## What "not continuing" looks like

If Dave decides not to actually run this, the repo still has value as:
- A complete worked example of designing a research instrument from concept to pre-registration
- A reusable scenario corpus for any subsequent ethics-decision research
- A validator + analyzer pattern that's reusable for similar instruments
- A literature review on moral psychology's replication crisis with specific entry points

The design work is not wasted regardless of the launch decision.

---

## How this document gets updated

When a material state change happens — new commit landing a substantive artifact, a track flipping from "provisional" to "solid," an open question getting resolved — update the relevant section here. The document's value is in being current.

Last comprehensive review: 2026-05-15.
