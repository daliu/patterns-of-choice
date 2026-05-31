# Pilot Pre-Launch Readiness Checklist

**Status:** Operational reference. The forward-sequence companion to [`PROJECT-STATUS.md`](PROJECT-STATUS.md) (which is current-state) and [`pilot-protocol.md`](pilot-protocol.md) (which is the spec). This document is the do-list: *what has to happen, in what order, by whom, before recruitment opens*.

Items are grouped into phases. Within each phase, items are roughly sequenced; cross-phase dependencies are called out explicitly. Each item names the **output artifact** so progress is observable, not just claimed.

---

## Phase 0 — concept and design (✓ COMPLETE)

These predate the pre-launch sequence; included here for the dependency map.

- [x] Concept document with adjacent literature ([`concept.md`](concept.md))
- [x] MVP-1 build spec ([`mvp.md`](mvp.md))
- [x] Onboarding copy ([`onboarding.md`](onboarding.md))
- [x] Scoring spec ([`scoring.md`](scoring.md), [`interpretation.md`](interpretation.md))
- [x] Pre-registration template ([`pre-registration.md`](pre-registration.md))
- [x] Pilot protocol ([`pilot-protocol.md`](pilot-protocol.md))
- [x] Pilot materials kit ([`pilot-materials/`](pilot-materials/))
- [x] Scenario corpus, schema-validated (48/48 — symmetric 6 QF + 3 Narr + 3 CoV per domain × 4)
- [x] Stated-values inventory module
- [x] Validator + analyzer (6 of 7 pre-reg hypotheses runnable on synthetic data)
- [x] Decision log + status snapshot + walkthroughs

---

## Phase 1 — engineering decisions

**Blocks:** all subsequent phases. The pilot cannot launch without a runtime.

- [ ] **Runtime stack decision.** Per [`DECISIONS.md §14`](DECISIONS.md), tooling line crossed (validator + analyzer shipped) but runtime is still open. Output: an ADR amendment naming the production stack (web framework, persistence, deployment target).
- [ ] **Authentication and identity decision.** Pilot uses Prolific-managed IDs; no user accounts. Document that this is provisional and the main study may need real accounts. Output: brief note in the runtime ADR.
- [ ] **Data-storage decision.** Per [`pilot-materials/data-handling-policy.md`](pilot-materials/data-handling-policy.md), encryption at rest, 90-day deletion, 30-day backup rotation. Output: storage-layer ADR (which DB, how encryption keys are managed, who has access to the production credentials).
- [ ] **Build the runtime.** Implement the screens specified in [`onboarding.md`](onboarding.md), administer scenarios from `scenarios/sample/`, log session entries matching the SessionLogEntry shape in [`types.ts`](types.ts), present the inventory module per [`inventory/`](inventory/). Demo-quality (single-page HTML) does NOT suffice for the pilot. Output: deployed pilot runtime accessible via a URL the recruitment script can link to.
- [ ] **Integrate the analyzer against the runtime's data shape.** Verify that `scripts/analyze.py` runs end-to-end on a hand-authored 1-user session-log export from the runtime (not against the synthetic fixture). Output: integration-test fixture + analyzer green on it.

**Estimated effort:** 4-8 weeks of focused engineering time. The biggest open variable. Could be compressed if a framework like Streamlit or Next.js + Supabase is chosen and the design is kept ascetic.

---

## Phase 2 — academic partnership

**Blocks:** Phase 3 (IRB), and is on the critical path to scientific credibility.

- [ ] **Identify a co-PI.** Pre-registration explicitly names a co-PI gap; this is a real blocker. Candidate areas: moral psychology, behavioral ethics, judgment-and-decision-making. Output: a named co-PI with verbal commitment.
- [ ] **Sign authorship credit agreement.** Output: signed authorship-credit doc per [`pre-registration.md`](pre-registration.md) §10 (mutually agreed contribution split).
- [ ] **Co-PI review of the concept doc and pre-registration.** Output: co-PI sign-off; revisions documented; pre-registration draft pinned at version 1.0 ready for OSF filing.
- [ ] **Co-PI institution selected as IRB-of-record.** Most IRBs require institutional affiliation; this defaults to the co-PI's institution. Output: institutional affiliation locked, IRB liaison contact identified.

**Estimated effort:** 2-6 months elapsed time. Long-tail because co-PI commitment depends on academic schedules; cannot be compressed by working harder.

---

## Phase 3 — IRB protocol

**Blocks:** Phase 5 (pilot pre-registration filing) AND Phase 7 (recruitment).

- [ ] **Draft the IRB protocol** using the pilot-protocol + pre-registration + consent form as primary inputs. Most US IRBs require: study purpose, design, sample, recruitment, consent process, data handling, risks/benefits, withdrawal procedures, compensation. Output: full IRB submission package.
- [ ] **Specifically address minimal-risk classification.** The pilot is descriptive and self-reflective; should qualify as minimal risk via exempt or expedited review. Output: justification section citing 45 CFR 46.104 exempt category 3 or appropriate equivalent.
- [ ] **Address wellbeing-monitoring provisions.** Per [`pilot-protocol.md`](pilot-protocol.md) Section 4, scrupulosity surveillance + withdrawal-without-penalty are part of the protocol. Output: explicit IRB language on adverse-event reporting.
- [ ] **Submit to co-PI's IRB.** Output: IRB protocol number.
- [ ] **Respond to IRB revisions.** Plan for 1-2 rounds of revisions (typical for descriptive psychometric pilots). Output: IRB approval letter.

**Estimated effort:** 6-12 weeks from submission to approval. Some IRBs faster, some longer.

---

## Phase 4 — content finalization

**Blocks:** Phase 5 (OSF lock requires content frozen). Can run in parallel with Phases 2-3.

- [x] **Author final scenarios** to reach 48 corpus total — DONE. Distribution: 6 QF + 3 Narr + 3 CoV per domain × 4 = 48. All passing validator.
- [x] **H8: author the recurring-NPC cast** (`h8-narrative-immersion-design.md` A1). DONE — `scenarios/npc-cast.json`: 5 named characters spanning all five archetypes and all four domains, with the Mode-A/Mode-B dual-mode deployment encoded.
- [ ] **H8: author the paired narrative-vs-abstract probes** (~8–12, each construct in both a cast-anchored narrative form and a structurally-equivalent abstract form; `scoring.md` §9.1). This is the corpus expansion that unlocks `DECISIONS.md` §16→§17 (48 → ~56-60). The corpus-lock *decision* is made (§17); this is the remaining *authoring*. Output: paired-probe scenarios passing the validator, tag-axis map extended with `recurring_npc:*` markup tags.
- [ ] **H8: build the attachment-measurement instrument** (`h8-narrative-immersion-design.md` A3; `scoring.md` §9.3). Short Tukachinsky-PSR adaptation per recurring NPC + the behavioral latency proxy. Output: instrument items authored; pilot administers near end of week 2 for calibration (`pilot-protocol.md` §H8).
- [ ] **Final editorial review of all scenarios** (including the H8 paired probes). Bias check, semantic-tag check, cross-domain consistency. Output: review-complete sign-off.
- [ ] **Lock the tag-axis map.** Per [`analysis/tag_axis_map_v0.1.csv`](analysis/tag_axis_map_v0.1.csv) versioning policy: bump to v1.0 at OSF filing. Output: v1.0 CSV.
- [ ] **Lock all JSON schemas.** No schema changes after this point without an ADR. Output: schemas tagged as v1.0 in git.
- [ ] **Lock the values deck and pairwise pairs.** Output: inventory module v1.0.

**Estimated effort:** 2-4 weeks. Mostly editorial, no engineering blockers.

---

## Phase 5 — pilot pre-registration

**Blocks:** Phase 7 (recruitment).

- [ ] **Draft a pilot-specific pre-registration** distinct from the main-study pre-registration. The pilot has its own go/no-go criteria per [`pilot-protocol.md`](pilot-protocol.md). Output: pilot-pre-reg draft.
- [ ] **Pilot pre-reg co-PI sign-off.** Output: signed copy.
- [ ] **File the pilot pre-registration at OSF.** Locks the pilot's success/failure criteria before any data is collected. Note: the main-study pre-registration is a *separate* filing that happens *after* the pilot results, contingent on the pilot's go decision. Output: OSF pre-reg DOI for the pilot.

**Estimated effort:** 1-2 weeks elapsed after co-PI commitment.

---

## Phase 6 — recruitment platform setup

**Can run in parallel with Phases 1-5.** Blocks Phase 7.

- [ ] **Prolific account + study posted as draft.** Use [`pilot-materials/recruitment-script.md`](pilot-materials/recruitment-script.md) as the listing copy. Configure pre-screening criteria. Output: draft Prolific study (not yet published).
- [ ] **Payment infrastructure.** Verify the compensation structure ($50 / $30 / $15 by tier) is supported by the platform's bonus mechanism. Output: payment flow tested with the platform's preview tools.
- [ ] **Recruitment language reviewed against the IRB-approved consent.** Output: any necessary edits applied.
- [ ] **Scheduling tool for weekly interviews.** Calendly or equivalent with 30-minute slots and 4 weekly waves. Output: link ready to embed in the welcome email.

**Estimated effort:** 1 week elapsed; can be done during IRB review.

---

## Phase 7 — final pre-launch checks

**Blocks:** the actual go-live. Everything above must be complete.

- [ ] **End-to-end dry run of the runtime.** Walk through the entire week-1 onboarding flow as a researcher would, including the inventory module and at least one of each scenario type. Output: dry-run notes; any bugs filed and fixed.
- [ ] **End-to-end dry run of the analyzer against runtime-exported data.** Output: per-domain revealed scores + per-domain gaps + all six hypothesis-test outputs produced for the dry-run session.
- [ ] **End-to-end dry run of the consent → recruitment-script → first-session funnel.** Read the consent as a participant would; check the candor moment is in the consent itself. Output: walk-through notes.
- [ ] **Informant invitation email tested.** Send a test email to a researcher account; verify the HEXACO informant link works, completion is logged. Output: tested informant pipeline.
- [ ] **Data-deletion procedure rehearsed.** Run the 90-day deletion procedure against the dry-run user data; verify it actually drops everything per the policy. Output: deletion log + auditable record.
- [ ] **Wellbeing-monitoring procedures briefed.** Researcher has read [`pilot-protocol.md`](pilot-protocol.md) Section 4 and knows the language for the wellbeing prompts. Output: brief sign-off note.
- [ ] **Pilot pre-registration linked from the README.** Output: README updated.

**Estimated effort:** 1 week elapsed. The dry-run is the most critical item — if anything in the funnel breaks during the actual pilot, the n=10 sample may be too small to recover from.

---

## Phase 8 — go-live and during-pilot monitoring

- [ ] **Open the Prolific study.** Output: recruitment posting live.
- [ ] **Monitor signup queue.** Aim for n=10 enrolled within 1-2 weeks of opening.
- [ ] **Weekly check-in interviews on schedule** per [`pilot-materials/weekly-interview-script.md`](pilot-materials/weekly-interview-script.md). Output: 4 interview transcripts per participant.
- [ ] **Adverse-event watch.** Any wellbeing concern surfaced in a session or interview gets logged and (if material) reported to the IRB per protocol. Output: adverse-event log (likely empty for an n=10 minimal-risk pilot, but the log itself is required).
- [ ] **Informant wave at session 22.** Output: informant invitations sent + completed.
- [ ] **Exit interviews** per [`pilot-materials/exit-interview-script.md`](pilot-materials/exit-interview-script.md). Output: 10 exit-interview transcripts.
- [ ] **Compensation processed within 14 days.** Output: payment confirmations.

---

## Phase 9 — post-pilot decision + main-study setup

- [ ] **Compile pilot data into the analyzer.** Output: per-participant + per-domain results across all six hypotheses.
- [ ] **Decision document.** Per [`pilot-protocol.md`](pilot-protocol.md) "Decision criteria for proceeding to OSF lock," classify as GO / NO-GO / MIXED. Output: signed decision document with rationale.
- [ ] **If GO:** finalize main-study pre-registration; file at OSF; open MVP-1 recruitment per the n=200 main-study plan.
- [ ] **If NO-GO:** publish the methodological findings (the instrument failed in specific identified ways); pause the project for redesign.
- [ ] **If MIXED:** revise per [`pilot-protocol.md`](pilot-protocol.md) "contingent-revision table"; plan a second n=10 pilot.
- [ ] **90-day pilot data deletion.** Output: deletion log per the rehearsal in Phase 7.

---

## Critical-path summary

The longest-pole items, in order:
1. **Phase 2 (co-PI recruitment)** — 2-6 months elapsed
2. **Phase 1 (runtime engineering)** — 4-8 weeks, parallelizable with Phase 2
3. **Phase 3 (IRB)** — 6-12 weeks from submission, parallelizable with Phase 1
4. **Phase 8 (pilot run itself)** — 5 weeks from go-live to last exit interview

End-to-end realistic timeline from today to a GO decision: **9-15 months.** Compressing this further requires either an unusually fast co-PI commitment or a parallel-track IRB submission with provisional approval pending co-PI sign-off (some institutions allow this).

---

## What this document does NOT cover

- The main-study (MVP-1) launch itself — that's a separate readiness checklist for a future document, contingent on the pilot's GO outcome
- The MVP-2 intervention layer — measurement-first; intervention deferred
- Detailed runtime engineering decisions — those belong in ADRs as they're made

---

## Cross-references

- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current-state snapshot (what's solid vs provisional now)
- [`pilot-protocol.md`](pilot-protocol.md) — the protocol this checklist operationalizes
- [`pilot-walkthrough.md`](pilot-walkthrough.md) — the participant-experience narrative this checklist enables
- [`pre-registration.md`](pre-registration.md) — main-study pre-reg template (filed *after* the pilot succeeds)
- [`DECISIONS.md`](DECISIONS.md) — design ADRs already made; new ones from Phase 1 should be appended here
