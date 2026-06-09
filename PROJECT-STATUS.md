# Project Status

**Last updated:** 2026-06-09 (the local-first runtime app is now BUILT & shipped on daliu.github.io; corpus grew to 61 + 5 recurring-character arcs + 9 H8 pairs; H9 self-prediction calibration added as the 9th hypothesis; analyzer aligned with the on-device projection + a new cross-implementation parity gate)

A consolidating snapshot of where every track sits right now, what's solid vs. provisional, what's waiting on which kind of human decision, and what's actually needed to launch each phase. Updated when material state changes.

For overview see [`README.md`](README.md). For decisions-made see [`DECISIONS.md`](DECISIONS.md). For design rationale see [`concept.md`](concept.md). This document is the *current state*, not the design.

---

## One-paragraph state

The repo holds a complete pre-launch specification of a longitudinal instrument for revealed-vs-stated ethical values: design, build spec, onboarding copy, pilot protocol, pre-registration template, scoring spec, interpretation guide, **a designed-and-audited runtime architecture**, six pilot-operational documents, decision-log, type definitions, JSON schemas, validator + analyzer covering most of the scoring spec, CI workflow, **61 authored scenarios** (the full 48-scenario MVP-1 corpus + 9 H8 paired narrative-vs-abstract probes + 4 additional rounds) plus **5 recurring-character arcs** across 4 domains × 3 scenario types, complete inventory module, 14 literature notes. The novel 8th hypothesis — **H8 (narrative-immersion as measure-debiasing)** — is specified end-to-end (concept, pre-reg, scoring §9, DECISIONS §17, pilot-protocol calibration, validity-threats CV-1, literature anchor, a 5-character recurring-NPC cast, a paired-probe manifest, 9 authored pairs, and the 5 recurring-character arcs that make the mechanism playable). A **9th hypothesis — H9 (self-prediction calibration)** — is now locked in DECISIONS §19 with scoring math in scoring.md §14 and a design doc (`h9-self-calibration.md`); it reuses the existing corpus (no expansion). A **per-person value-weighting layer** (scoring §13: ipsative ordering + cost-of-virtue price + word/deed concordance) is specified, honesty-audited, and rendered in the profile-reveal page. A **public-facing landing page + interactive demos** ship on `daliu.github.io/patterns-of-choice/`, and — the major change since the last pass — a **working local-first runtime app is now BUILT & shipped** at `daliu.github.io/patterns-of-choice/app.html`: a dependency-free, no-build vanilla-JS PWA with an event-sourced engine (append-only IndexedDB log), a deterministic on-device projection/scorer, an offline service worker, ~170 Node assertions across 4 test files (all green), and user-facing onboarding, the full recurring-character arc player (the H8 mechanism made interactive), card-sort + quick-fire/narrative sessions, an animated reveal, a shareable reveal portrait, and a type-to-confirm profile wipe — everything on-device, nothing sent. As of the 2026-06-09 pass the validator (all 66 scenarios + arcs), the analyzer regression gate (H2–H7), and the new cross-implementation parity gate (JS projection ↔ Python analyzer) all pass green. What remains is real-world execution (recruit a co-PI, IRB submission, build the **separate** multi-user production pilot runtime with encrypted sync + auth + scheduling) plus continued H8 authoring (more paired probes + the attachment instrument) — all needing human decisions and partnerships beyond autonomous work.

---

## Track-by-track state

### Design and rationale: **complete and stable**

- [`concept.md`](concept.md) — Draft 0.3 with both literature passes integrated. Foundational empirical risk explicitly named in the Premise. Effect-size estimates calibrated to ~0.3–0.5 SD per Yeager/Milkman megastudies. Smuggled-values section names the MacIntyre/Confucian role-ethics challenge. TTM stage-matching prescriptive claim removed.
- [`DECISIONS.md`](DECISIONS.md) — 19 ADR-format entries. Load-bearing operating constraints codified. §17 adds H8 + unlocks the corpus; §18 records the designed runtime architecture (revisit of §14); §19 adds H9 (self-prediction calibration) reusing the existing corpus.

These two documents are likely to need only small revisions before any real-world work. They're the load-bearing design.

### Validation plan: **drafted, pending lock**

- [`mvp.md`](mvp.md) — MVP-1 build spec. Solid; revisions in place after lit-pass 2 (HEXACO r ≥ 0.25 not 0.30; informant reports as primary Phase-2; die-roll/sender-receiver as truth-telling paradigm).
- [`pre-registration.md`](pre-registration.md) — OSF-filing template. Three primary hypotheses, **six secondary (H8 added 2026-05-30 as the 8th hypothesis; H9 self-prediction calibration added as the 9th)**. Falsification thresholds explicit. *Does not yet have a co-PI listed or IRB protocol number*; both are bound to the co-PI recruitment step.
- [`pilot-protocol.md`](pilot-protocol.md) — n=10 pilot specification. Pre-registered go/no-go criteria. *Independent of the main-study pre-reg* — the pilot's own criteria could be separately pre-registered before pilot launch.
- [`scoring.md`](scoring.md) — analytical spec. Sections implemented in the analyzer (§2-3, §4, §5.1, §5.2, §5.3, §6, §8); reserved: §7 CFA (needs lavaan/statsmodels), §4.3 longitudinal trajectories, §9 H8 divergence/attachment (reserved on unresolved design inputs, not a lib gap), §13 the per-person value-weighting layer (specified + honesty-audited + rendered in the profile page; analyzer implementation pending — it's stdlib-feasible and reference-free), and §14 H9 self-prediction calibration (math specified; reserved in the analyzer pending a `prediction` event type). **Six of the nine pre-registered hypotheses** end-to-end runnable: H2, H3, H4, H5, H6, H7. Reserved: H1 (CFA), H8a/H8b (see scoring §9 / §13), and H9 (see scoring §14).

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

### Scenarios: **61 authored (48 MVP-1 + 9 H8 paired probes + 4 rounds) + 5 recurring-character arcs, structurally symmetric**

The 48-scenario MVP-1 base is complete (6 quick-fires + 3 narratives + 3 cost-of-virtue per domain × 4); on top of it, **9 H8 paired narrative-vs-abstract probes** are authored (low-stakes truth-telling for H8a + high-stakes attachment probes for H8b), bundled with their abstract quick-fire twins, and **5 recurring-character arcs** (`scenarios/arcs/`) make the H8 mechanism playable. Validator reports "all 66 scenarios + arcs valid" (61 scenarios + 5 arcs; re-verified 2026-06-09).

| Type | Authored | MVP-1 target | Note |
|---|---|---|---|
| Quick-fire rounds | 28 | 24 | +4 hold the H8 abstract twins |
| Branching narratives | 21 | 12 | +9 H8 paired-probe narratives |
| Cost-of-virtue probes | 12 | 12 | complete |

The MVP-1 base reached full structural symmetry (`DECISIONS.md` §16); §17 unlocked the lock for the H8 paired probes (the one documented construct gap). Remaining scenario work: more paired probes + the attachment-measurement instrument — editorial, benefits from Dave's voice.

**H8 substrate authored:** `scenarios/npc-cast.json` — 5 named characters (close friend, aging family member, evolving new-arrival, adversary-with-redemption, animal companion) spanning all four domains and all five design-doc archetypes, Mode-A/Mode-B deployment encoded — plus `scenarios/h8-probe-pairs.json`, the paired-probe manifest now holding 9 entries linking each narrative signal to its abstract twin, and the 5 recurring-character arcs in `scenarios/arcs/` (arc-biscuit, arc-cole, arc-gran, arc-marisol, arc-nadia) that the runtime plays interactively. The cast and paired-probe manifest live outside `sample/` so the scenario validator skips them; the 5 arcs get arc-specific validation (the "+ 5 arcs" in the "all 66 scenarios + arcs valid" total).

### Inventory module: **complete**

[`inventory/`](inventory/) — values deck (20 values, 5 per domain), pairwise pairs (30 pairs, 16 within-domain + 14 cross-domain), three-layer prompts (current/aspirational/admired-other), story prompts (5 free-text templates), relational variant (11 roles across 5 categories; opt-in for MVP-2). Plus JSON Schema docs in [`inventory/SCHEMA.md`](inventory/SCHEMA.md).

### Tooling: **complete for the pre-launch phase**

[`scripts/`](scripts/) holds the validator + analyzer + two regression gates, all pure-Python, single dependency for the validator:
- `validate.py` — scenario + inventory schema validation with cross-file integrity checks; path reachability; tag-map lookup. Catches drift before merge. Currently reports "all 66 scenarios + arcs valid" (61 scenarios + 5 recurring-character arcs).
- `analyze.py` — implements scoring.md §2-3 (revealed), §4 (probe), §5.1 (card-sort), §5.2 (Bradley-Terry pairwise via Hunter 2004 MM), §5.3 (combined stated), §6 (gap), §8 (bootstrap CIs), plus **six of the nine pre-registered hypotheses** that fit within the stdlib-only constraint (H2 HEXACO self, H3 revealed test-retest per-domain, H4 informant HEXACO, H5 probe test-retest per-domain, H6 stated-revealed range, H7 Big-5 N discriminant). It was just aligned with the on-device JS projection (cov payload, primary-axis scoring, inattentive-RT gate). **Pure Python, no external statistical library.** Reserved: §7 CFA / H1 (needs lavaan/statsmodels), §4.3 longitudinal probe trajectories beyond two windows, §9/§13 H8 + value-weighting (stdlib-feasible but reserved on unresolved design inputs), and §14 / H9 (needs a `prediction` event type) — see the analyzer docstring's reserved section.
- `check_impl_parity.py` (`make check` / `make check-parity`) — a cross-implementation parity gate asserting the JS on-device projection and the Python analyzer agree on item scoring. Green (9 cases, incl. secondary-axis).

Plus [`types.ts`](types.ts) (declarative TypeScript schemas), JSON Schema files in `scenarios/schemas/`, GitHub Actions CI workflow auto-running the validator on push/PR, and synthetic fixture data demonstrating end-to-end runs. The validator + threshold gate + parity gate are all green.

### Literature: **two passes done, 14 area notes**

[`literature/`](literature/) — first pass produced 9 area notes + index. Second pass focused on ecological-validity-positive added a deeper note. A later focused addition, [`narrative-immersion.md`](literature/narrative-immersion.md), anchors H8 (transportation theory, EORM debiasing, parasocial attachment, Paulhus SDR components) and carries the adversarial flag that the cited literature is all *persuasion*, not *measurement* — the analogical leap H8 has to earn. The literature work has saturated for current purposes; further passes would be focused additions on specific questions as they arise.

### Public UI/UX: **complete and live on daliu.github.io**

A public face for the project ships at `daliu.github.io/patterns-of-choice/` (in the separate public repo, not this one):
- Landing page — framing, methodology, the four domains, all 9 hypotheses, a dedicated H8 explainer, and a consolidated "Try it yourself" section.
- Five client-side interactive demos, each ~2 min, nothing recorded, forming a funnel: the **on-ramp** ("Two-Minute Self-Portrait" — a pop-quiz that returns no verdict, teaching the stated-vs-revealed distinction); the **card sort** (real 20-value deck, the stated channel); the **quick-fire** (predict-then-reveal stated-vs-revealed gap, the revealed channel); **"The Weight of a Name"** (the H8 paired abstract-vs-narrative effect, with the honest debiasing-vs-manipulation caveat); and the **sample profile reveal** (the gap across four domains + the §13 ipsative-weighting and word/deed-concordance reads). Cross-linked; all constraint-audited (descriptive-not-prescriptive, no verdict/score/comparison; a11y + link audits green).
- Reachable from the site's homepage hero and the portfolio's featured-projects card. Calm, research-stage aesthetic distinct from the portfolio theme.

This is the public-communication layer — single-file vanilla HTML/JS with reduced/sample content. It is distinct from both (a) the **now-BUILT local-first runtime app** (`app.html`, full content, everything on-device — see Engineering) and (b) the still-unbuilt **multi-user production pilot runtime** (encrypted sync + auth + scheduling for a research cohort, designed in `runtime-architecture.md`).

### Engineering: **tooling crossed; local-first runtime app BUILT & shipped; multi-user pilot runtime still designed-only**

Crossed (tooling track):
- Validator (validate.py, single dependency)
- CI workflow (.github/workflows/validate.yml)
- Analyzer (analyze.py, standard library, scoring-spec subset + hypotheses H2–H7)
- Cross-implementation parity gate (check_impl_parity.py — JS projection ↔ Python analyzer agree)

Crossed (the local-first runtime app — **BUILT & shipped** at `daliu.github.io/patterns-of-choice/app.html`): a dependency-free, no-build vanilla-JS PWA realizing the architecture's event-sourced model on-device. It has an event-sourced engine (append-only IndexedDB log, `runtime/poc-runtime.js`), a deterministic on-device projection/scorer (`runtime/poc-projection.js`), a content bundle, an offline service worker, and ~170 Node assertions across 4 test files (all green). User-facing: a first-run onboarding flow, the full recurring-character arc player (the H8 mechanism made interactive), card-sort + quick-fire/narrative daily sessions, a colorful animated reveal, a shareable reveal portrait (SVG→canvas image), and a cautious type-to-confirm profile-wipe. **Everything on-device; nothing sent — this is the local-first, individual-benefit tool.** (The runtime source lives in the separate public repo, alongside the demos.)

Runtime architecture — **designed and adversarially audited** (`runtime-architecture.md`, `DECISIONS.md §18`): local-first PWA, the `SessionLogEntry` append-only event stream as source of truth, scores as deterministic projections, rewind as replay-to-timestamp, opt-in client-encrypted sync to a ciphertext-only relay; `analyze.py` stays canonical (not ported). The audit was sound-with-fixes (zero load-bearing-constraint violations) and surfaced the load-bearing finding that the gap needs cohort norms (so the reveal is researcher-side or norms-artifact-driven). The single-user on-device portion of this design is now realized by the shipped app (above); the **multi-user production pilot runtime** (the cohort version) is still designed-only. Seven owner decisions remain (see the doc §10).

Public-communication layer shipped (vanilla single-file demos on daliu.github.io) — see the Public UI/UX track. These are the front door, distinct from both the shipped local-first app and the multi-user pilot runtime.

Not crossed (the **multi-user production pilot runtime** for a research cohort — still designed-only):
- The sync infrastructure (opt-in client-encrypted, ciphertext-only relay)
- The auth layer
- The notification / scheduling layer for the longitudinal protocol
- Server-side persistence behind encrypted sync

`mvp.md §"Tech stack proposal"` names React + TypeScript + Vite as the working hypothesis but this is not locked. The shipped local-first app deliberately used dependency-free vanilla JS; the **multi-user pilot runtime** is the next big crossing and deserves Dave's explicit input — particularly on:

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

1. **Multi-user pilot-runtime stack choice.** The local-first app shipped on dependency-free vanilla JS; the *cohort* runtime (with sync/auth/scheduling) still needs a stack call — React, Svelte, or something else. Affects everything downstream for the multi-user build.
2. **Co-PI identification.** Who's the academic partner? Affects IRB timeline (institutional differences are substantial) and pre-registration filing.
3. **Funding / compensation budget.** Pilot needs ~$500 for 10 participants × $50; main study ~$5,000 for 200 × $25; plus informant payments and platform fees.
4. **Hosting decision.** Self-hosted, Vercel, institutional infrastructure?
5. **Open-sourcing / data-release schedule.** The repo is now public (the local-first app and demos ship openly). Still open: when and how to release the pilot/main-study *data* and analysis artifacts — at pilot launch, at main-study launch, at first preprint?
6. **Whether to even continue.** This is the most upstream decision. The repo represents a genuine multi-year commitment to do this seriously. If the answer is "this was a useful design exercise but I'm not going to actually run it," that's a fine answer too — but the design itself doesn't need further iteration.
7. **H8 creative authoring (in progress).** The substrate is complete (cast, manifest, scoring §9/§13) and **9 paired probes + 5 recurring-character arcs are authored** (workflow-generated, adversarially verified) and playable in the shipped app. Remaining: more pairs + the per-NPC attachment instrument. These are pre-registered research artifacts where editorial voice matters — best continued with Dave's review, though the proven author→verify→repair workflow can draft them.

---

## To launch the pilot (n=10) — dependency checklist

What's needed beyond what's currently in the repo:

- [ ] Co-PI identified
- [ ] IRB application submitted (using `pilot-materials/` templates customized to the institution)
- [ ] IRB exemption or approval
- [ ] OSF account set up; pilot's go/no-go criteria pre-registered
- [ ] Recruitment platform account (Prolific or similar)
- [~] Runtime app — **the local-first single-user app is BUILT & shipped** (`app.html`, on-device, ~170 tests green). The *cohort-capable* pilot runtime (adds multi-user sync + scheduling on top) is still designed-only (`runtime-architecture.md`, DECISIONS §18)
- [ ] Sync infrastructure deployed (design: opt-in ciphertext-only relay, per the architecture)
- [x] 48 scenarios authored to MVP-1 target — DONE (full corpus, validator green)
- [~] H8 paired narrative-vs-abstract probes — **9 authored + 5 recurring-character arcs** (validator green, playable in the app); more pairs + attachment instrument are continued editorial work (corpus now 61 + 5 arcs)
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
| Runtime app built | local-first single-user app: **DONE** (shipped). Multi-user cohort runtime: +4 months (parallel to IRB) |
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

Last comprehensive review: 2026-06-09 (local-first runtime app built & shipped; corpus → 61 + 5 recurring-character arcs + 9 H8 pairs; H9 added as the 9th hypothesis; analyzer aligned with the on-device projection + cross-implementation parity gate added).
