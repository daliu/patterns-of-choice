# Runtime Architecture — Patterns of Choice

**Status:** Design proposal, draft 0.1 (2026-06-04). Resolves the open engineering questions in `DECISIONS.md §14` and `PROJECT-STATUS.md` (the "runtime is the next big crossing"). Produced by a structured design pass (three independent architecture stances → synthesis → adversarial constraint+contract audit). Not yet locked; the open decisions in §10 are the project owner's call.

This document is the *current recommended design*, not a commitment. Where the design has an honest gap or a deferred piece, it says so explicitly rather than papering over it — the adversarial audit's job was to find exactly those, and its findings are folded in throughout (and summarized in §11).

---

## 1. One-paragraph summary

Build a **local-first PWA** (React + TypeScript + Vite) whose source of truth is the **`SessionLogEntry` append-only event stream** in IndexedDB — the spine the data contract already half-built (`types.ts`, `scoring.md §1.1`). Scores are **deterministic projections** of that stream; **rewind is replay-to-timestamp**; an **opt-in, client-encrypted** (libsodium / Argon2id) sync layer ships only ciphertext to a dumb relay that can never read a moral choice. The canonical, pre-registered numbers are **always produced by the unchanged Python `scripts/analyze.py`** over a consented export — the device never reproduces a CI-bearing number — because the analyzer's reproducibility rests on CPython's Mersenne Twister + a fixed seed (`BOOTSTRAP_SEED = 20260510`), which a TS port cannot match byte-for-byte without a fragile MT19937 reimplementation. Phasing is pragmatic (a single-device local app is pilot-capable; sync/auth/hardening are a thin tail), but the privacy-maximal end state is pre-wired into the data model so n=200 is a key-management upgrade, not a rewrite.

This honors every load-bearing operating constraint **structurally, not by policy**: no central plaintext honey-pot (`DECISIONS §10`), E2E for opt-in sync, no-training enforced by data flow, descriptive-only (no schema slot for scores-as-verdict / streaks / social comparison), and reproducible seeded scoring.

---

## 2. The load-bearing finding (read this first)

**The headline reveal number — the per-domain gap — is NOT computable from a single user's data alone.** The gap (`scoring.md §6`; `analyze.py` `compute_gaps` + per-domain z-standardization) requires **sample-level z-standardization across users** and returns nothing when fewer than two users are present. The same is true of every standardized or correlational number (revealed-score *z*, the stated–revealed correlation, the H-tests). The analyzer's `--json` output is **cohort-wide arrays with no per-user mode**.

Consequences the rest of this design is built around:

- A device cannot, even in principle, compute a participant's gap from their own event log in isolation. The reveal needs **either** (a) a researcher-side computation over the whole-cohort export with the device rendering its cached per-user slice, **or** (b) a **versioned, seed-locked population-norms artifact** (per-domain mean/SD, stamped with `corpus_version` / `tag_map_version`) that the device standardizes against locally. This design recommends **(a) for the pilot** (simplest, OSF-canonical) and treats (b) as the n=200 option. **This is the single biggest open design decision — see §10.**
- Per-user revealed-score **CIs are cohort-relative**: `analyze.py` consumes one `random.Random(BOOTSTRAP_SEED)` across all `(user, domain)` keys in sorted order, so a user's CI depends on full-cohort composition + sort order. Per-user reproducible rewind CIs would require a refactor to a per-key-seeded RNG (e.g. `random.Random(BOOTSTRAP_SEED ^ hash(user, domain))`) — **recommended in Phase 0 if per-user rewind reproducibility is wanted.**
- What a device *can* reproduce exactly and live: the **RNG-free, associative descriptive surface** — per-item → per-session → per-user-per-domain revealed **means** (`§2–3`) and card-sort fractions (`§5.1`). That, and only that, is the device's live-scoring job.

---

## 3. Stack (resolves the open `PROJECT-STATUS` questions)

| Question | Decision | Note |
|---|---|---|
| Framework | **React 18 + TS + Vite**, installable PWA | Reversible — the spine is framework-agnostic plain-TS modules; React is load-bearing nowhere. Chosen for talent-pool depth on a multi-year artifact + the existing `types.ts` contract. *Audit note: vanilla/Svelte would ship the pilot faster; React is defensible, not free.* |
| Local store | **IndexedDB via Dexie.js**, insert-only event stores | Source of truth on device |
| Sync (streams) | **Plain append-only encrypted-batch sync**, deterministic union-merge | NOT a CRDT — the streams are conflict-free by construction (§5) |
| Sync (settings) | **Yjs** for the one small mutable settings doc *only* | **Deferred out of the pilot** per audit — single-device pilot has no concurrency; use last-writer-wins-by-timestamp until n=200 |
| Server (pilot) | **Thin Fastify + SQLite (Litestream)**, ciphertext-only relay | SQLite not Postgres (n=10–200 is tens of thousands of small rows). PocketBase is the documented fallback (§10) |
| Auth | **Magic-link** (pilot) → **passkey/WebAuthn-PRF** (n=200) | Magic-link = recoverable Prolific handle, simpler lost-device story |
| Crypto | **libsodium-wrappers (WASM)** — XChaCha20-Poly1305 / `crypto_secretbox`, Argon2id KDF | Exactly as `pilot-materials/data-handling-policy.md` names |
| Canonical scorer | **`scripts/analyze.py`, unchanged** | Device never reproduces its CI-bearing numbers (§6) |

---

## 4. Data model — events on top of the existing contract

Events build directly on the five runtime shapes `types.ts` already defines (`SessionLogEntry`, `ProbeResponse`, `CardSortResponse`, `PairwiseResponse`, `StoryResponse`). Each is wrapped in a thin storage envelope **without touching its payload**:

```
Envelope {
  event_id:       string   // routing id — see security note below
  kind:           "session_log" | "probe" | "card_sort" | "pairwise" | "story" | "instrument"
  schema_version: "0.1"
  tag_map_version: string   // which analysis/tag_axis_map_vX.csv was effective
  corpus_version:  string   // which scenario/inventory bundle was effective
  device_id:      string
  local_seq:      number    // monotonic per device
  payload:        <one of the types.ts shapes, verbatim>
}
```

- **Immutability:** the data layer exposes **no update or delete** path on the event stores (enforced in code, not convention). Corrections (double-tap, late `was_timeout`, clock skew) are **compensating events** referencing the superseded `event_id`; the projector applies supersedes during the fold. Per-event deletion is never a feature — deletion is whole-user (a hard drop), matching the data-handling-policy withdrawal semantics.
- **Total order for replay:** `(timestamp_iso, device_id, local_seq)` — deterministic, so every device replays identically and matches what `analyze.py` sees.
- **Versioned content bundle:** the corpus + inventory + **all historical `tag_axis_map_vX.csv`** ship with the build; each event re-scores under the tag map stamped on it (`scoring.md §1.1` denormalized-tags discipline). *Audit note: `analyze.py` currently loads a single `--tag-map` per run, so a mixed-version export needs either per-version scoring passes or a documented single-version-per-export rule.*

### Two corrections the audit required to the naive "export is just envelope-strip" claim

1. **Pairwise needs a transform, not an envelope strip.** `analyze.py`'s pairwise path ingests a compact `{user_id, layer, choices:[[winner,loser],…]}` shape, **not** the `types.ts` `PairwiseResponse {pair_id,left_id,right_id,choice,response_time_ms}`. The export adapter must resolve `left/right + choice → winner/loser` and **drop `skip`s**. (Session-log and probe match `types.ts` verbatim; card-sort also matches.)
2. **Analyzer JSON keys ≠ `types.ts` derived-type keys.** The analyzer emits `revealed_score_mean` / `ci_95_low` / `ci_95_high` / `n_sessions_contributing` and gaps as `z_revealed` / `z_stated_aspirational` / `gap` (no gap CI). `types.ts` `PerDomainRevealedScore` / `GapEstimate` use different names and include fields the analyzer doesn't emit. **Phase 0's round-trip CI must reconcile these names — it is not a no-op.**

`event_id` (security): do **not** transmit a deterministic plaintext-derived content hash to the relay as routing metadata — it is a confirmation/dedup oracle over identical choices ("hash a guessed payload, look it up"). **Route by random per-event UUID**, or HMAC the id under a per-user key the server never sees. (Content-addressing for idempotent local dedup can still be used *on-device*; it just must not leave as cleartext metadata.)

---

## 5. Rewind — replay-to-timestamp

Rewind is the strongest argument for the event-sourced spine: it is **one predicate over an immutable list**, not a feature with its own storage. "Step my profile back to before last Tuesday" = filter events to `{ e : e.timestamp_iso ≤ T }`, run the identical projection over that prefix, render. No undo log, no rollback machinery, no destructive edit.

- **Descriptive surface** (per-session observation, running per-domain means): rewinds **instantly on-device** by re-folding the RNG-free `§2–3` projection over the prefix — months of daily sessions is still only thousands of events (sub-millisecond, offline).
- **Canonical rewound reveal** (with CIs / Bradley-Terry / gap): produced by exporting the prefix through `analyze.py` — the same path that produces the live reveal — so a rewound profile is reproducible by a reviewer. (Subject to §2: the gap needs cohort norms.)
- **Versioning interacts cleanly:** each event stamps `tag_map_version`/`corpus_version`, so an old event always re-scores under the rules in force when made — the OSF reproducibility discipline of `DECISIONS §13/§16`. Rewind is read-only and side-effect-free.

---

## 6. Scoring projection — one canonical scorer, a cheap live cache

A deliberate, contract-driven split:

- **Class A (cheap, associative, RNG-free):** per-item → per-session → per-domain revealed **means** (`§2–3`), card-sort fractions (`§5.1`). Tracked **incrementally on-device** (O(1) per appended event) so the session-end "one observation" renders instantly, offline. Because mean is associative, incremental == replay exactly. *Audit note: to actually match `analyze.py`, the on-device projector must replicate the versioned tag-map lookup, the ≥3-items-per-session NA rule, NA-item exclusion, and the `§10` inattentive-session drop (quick-fire median RT < 2s). A bare running sum/count will diverge.*
- **Class B (sample-relative / global / RNG-bound):** bootstrap CIs (`§8`), per-domain z-standardization (`§5.3/§6`), the gap, the H-tests. **Not** reproduced on-device for any canonical number. **Correction from the audit:** the Bradley-Terry **point estimate** (`fit_bradley_terry`, Hunter 2004 MM) is **deterministic and RNG-free** → it *is* portable (Class A-eligible); only its **bootstrap CI** is RNG-bound. The "don't port" argument applies strictly to the **bootstrap percentile CIs** (and per-hypothesis `seed_offset`), not to BT, means, or z-standardization.

**Why Python stays canonical:** `_bootstrap_ci_*` use `rng.choice` / `rng.randrange` over `random.Random(20260510 + offset)`. Byte-identical CIs from TS would require a bit-exact MT19937 + CPython's `_randbelow`/`choice` index mapping — a perpetual reproducibility liability for a pre-registered instrument. Keeping Python canonical is both less work and *more* rigorous: the number a user sees is the number a reviewer reproduces.

**Safety nets:** (a) whenever `analyze.py` runs over an export, diff its revealed means against the device Class-A projection — a mismatch beyond float tolerance is a projector-drift bug (and the diff must apply identical exclusion semantics, else it trips on definitions not bugs); (b) keep `check_analyzer_thresholds.py` as the regression gate; (c) add a CI job asserting the export adapter round-trips a fixture into the exact arrays `analyze.py` ingests. The incremental projection is **always a disposable cache** (`drop proj_*; replay` fixes any projector bug).

*Audit note — latency is not a compute problem:* a full `analyze.py` run over the fixtures is ~0.25s wall; per-user reveal numbers are a fraction of that. The **Web-Worker JS bootstrap is cut from the pilot** — it can only produce non-canonical numbers and adds a second divergent CI implementation (a reproducibility liability) to solve latency that doesn't exist.

---

## 7. Latency

- **Daily session: instant and offline** because it touches no scores on the critical path. Content is a static versioned bundle served by the service worker; orchestration (8s quick-fire timer, branching narrative, cost-of-virtue ladder, reflection) is pure client state; writing a choice is one idempotent IndexedDB append off the render path; the session-end observation reads the O(1) Class-A projection. No network is ever on the interaction path. (Matches the proven feel of `demo/first-session.html`, persisted.)
- **Profile reveal: a precomputed cached artifact, not an on-tap compute.** After the reveal-threshold session ends, an export → canonical analyzer run is triggered (researcher-side in the pilot) and cached as an immutable `profile_snapshot` keyed by `(corpus_version, tag_map_version, last_event_id)` — so "Show me" paints from cache. The `onboarding.md` pre-reveal choreography ("Today is different", the two cautions) is an honest beat that also covers a cold compute.
- **Reveal-threshold predicate must be defined and shared with the analyzer's exclusion set** (`onboarding.md` fires at session ~15; `scoring.md §10` excludes <14 completed sessions and drops inattentive sessions) so the reveal and the OSF numbers agree. *Currently unspecified — see §10.*

---

## 8. Storage, backup, sync, security

Three tiers mapping 1:1 to `data-handling-policy.md`:

1. **Device (primary):** five event streams in IndexedDB, **sealed at rest** with `crypto_secretbox` under a per-user key `K_data` derived client-side via Argon2id from the auth secret and never transmitted. A stolen device yields only ciphertext. *Audit note: per-event at-rest sealing + Argon2id-unlock-on-open is heavier than an in-person n=10 pilot needs; OS-disk-encryption + a single sealed export meets the policy for the pilot — gate per-event sealing to when ciphertext actually leaves the device (Phase 4).*
2. **Server (ciphertext-only, opt-in):** each synced batch is an opaque `crypto_secretbox` blob + non-secret routing metadata (random UUID, `device_id`, `local_seq` range, nonce, receive timestamp). No tags/option_ids/scenario_ids/scores/free-text in cleartext; the relay cannot read a single choice and has **no query surface** over choices. No PII paired server-side (compensation via Prolific only).
3. **Backup:** because all derived state rebuilds by replay, only the **event log** needs durability. (a) **Local export** — one-tap encrypted `.pocbak` (sealed event blobs); restore = import-and-replay; satisfies the policy for a single-device pilot before any server exists. (b) **Server backup** (sync cohort) — Litestream streams the SQLite WAL to object storage; a nightly cron prunes generations >30 days (the policy's rotation) and the 90-day post-pilot deletion is a `DROP` + verify-no-backup-older-than-30-days + audit row. *Audit note: with Litestream, an active-withdrawal "drop" is itself a WAL op and prior generations hold rows until pruned — so "within 7 days" purge is true at the live DB, **30 days at backups**; keep that distinction explicit and make the prune verifiable.*

**Security posture** (threat model from `DECISIONS §10` — moral-compromise data leaks worse than financial; adversaries include employers, partners, a fragile future self, ML trainers). Structural-now: no plaintext honey-pot; operator/subpoena cannot read data (no keys, no query surface); no-training enforced by data flow; device-theft yields ciphertext; no schema slot for engagement/social-comparison dark patterns; reproducibility gated by the seeded canonical analyzer.

**The one honest gap (owner sign-off required):** web-delivered E2E is **trust-on-first-load** — a compromised origin could ship key-exfiltrating JS, and **SRI protects sub-resources, not the served `index.html`/service worker itself**. Not eliminated in the pilot. Pilot mitigations: open-source the relay (the policy's audit clause), installable PWA, SRI-pin sub-resources, tiny audited surface. Full closure is the n=200 upgrade (per-device keypairs, passkey-bound unwrap, optional Shamir escrow). Other disclosed residuals: device loss without sync/export = data loss (consent-disclosed); sync timing/size metadata visible to the relay (mitigation: size-padding + jittered sync, n=200).

---

## 9. Phased build

| Phase | Deliverable | Why |
|---|---|---|
| **0 — lock the scoring contract (no UI)** | Freeze the event envelope + five `types.ts` payloads as v0.1. Build the **export adapter** (incl. the pairwise winner/loser transform + the key reconciliation from §4) and a CI job round-tripping `analysis/fixtures/*` so `analyze.py` + `check_analyzer_thresholds.py` still pass. Decide the per-key-seeded-RNG refactor if per-user rewind reproducibility is wanted (§2). | De-risks the only hard correctness claim before any UI; bakes in "Python stays canonical." |
| **1 — local-only spine (pilot-capable)** | Vite+React+TS PWA importing `types.ts`; versioned 48-scenario+inventory+tag-map bundle; lift `demo/first-session.html` into a real Session component; Dexie insert-only stores; full daily session appends events; render the Class-A "one observation". Copy from `copy/onboarding-en.yaml`. No sync, no crypto, no server. | A single-device app already does the pilot's job (does the instrument measure anything; Mode A vs B; usability). |
| **2 — full protocol + reveal + rewind** | Full orchestration (quick-fire + narrative + cost-of-virtue + reflection) and three-layer card-sort/pairwise/story onboarding; wire the reveal (export prefix → `analyze.py` researcher-side → cache `profile_snapshot` → render behind the choreography); rewind as timestamp-filter replay. **Resolve the gap-norms decision (§2) and the probe-precondition projection** (top-5 membership from card-sort gates the cost-of-virtue probe — a cross-stream derived view). | Reveal + rewind are pure consumers of the Phase-1 log; add no new storage. |
| **3 — durability without a server** | Encrypt local store at rest (libsodium + Argon2id) and the one-tap encrypted export/import = backup + restore-by-replay. | Meets the at-rest + backup policy commitments before any relay exists. |
| **4 — auth + opt-in thin sync (pilot-ready)** | Magic-link; ~300-line Fastify+SQLite ciphertext-blob relay; client seals each batch; Litestream + retention/deletion cron (30-day rotation, 90-day drop); open-source server + SRI-pin. | A thin encrypted tail on a complete product — Phases 1–3 remain whole if sync is never enabled. |
| **5 — cohort hardening (pre n=200)** | Passkey/WebAuthn-PRF; per-device-key multi-device E2E; optional escrow; size-padding + jittered sync; the Yjs settings doc; audit-logged export feeding `analyze.py`; stand up the reserved lavaan/statsmodels CFA (H1); third-party security audit. | Moves to the privacy-maximal end state (closes the web-E2E gap) + the one genuinely-reserved scoring piece, without touching the storage model or the canonical analyzer. |

*Audit note: Phases 0–2 + the Phase-3 encrypted export are the actual pilot; 4–5 are main-study (n=200) scope. Defer out of the pilot: Yjs/CRDT, per-event at-rest sealing, `prev_hash` hash-chains, content-addressed event_ids as routing metadata, passkey pre-wiring. For n=10: random UUID per event, monotonic `local_seq`, union-merge, settings as plain LWW, one-tap encrypted export.*

---

## 10. Open decisions for the owner

1. **Where the canonical reveal is computed (the §2 decision — biggest one).** Recommend: **researcher-side over a consented whole-cohort export** for the pilot (keeps Python off the device, OSF-canonical); a versioned population-norms artifact is the n=200 alternative for on-device standardization. Also decide **whether the pilot even shows the gap** — with n≈10 there is barely a sample to standardize against.
2. **Pilot auth:** magic-link (recommended) vs passkey-from-day-one. Reversible; changes key management only.
3. **Accept the named web-E2E trust-on-first-load gap for n=10** (mitigated by open-source + SRI + PWA; fully closed by per-device keys at n=200). Explicit sign-off needed — it's the one place the privacy-maximal end state isn't yet met.
4. **Per-session "one observation" during the cohort's baseline 3 weeks** (`onboarding.md` open question). Recommend keep for the pilot; defer the cohort decision to pre-reg lock.
5. **Server:** hand-rolled Fastify+SQLite (recommended, one clean encrypted-blob contract) vs **PocketBase** (batteries-included fallback) — both ciphertext-only.
6. **H8 in the pilot runtime (audit-surfaced):** the n=10 pilot runs the H8 Mode-A/B split, which needs the Tukachinsky **PSR-PRD attachment self-report** captured at sessions 8/16/24 — but there is **no runtime type for it** (the five event kinds don't include an instrument-response). Either **add a sixth `instrument` event kind** (recommended — the envelope already reserves the `"instrument"` kind for this) or **scope H8 out of the pilot runtime**. Don't claim "exactly five runtime types" while committing H8 to the pilot.
7. **Informant HEXACO + interview audio/transcripts** have distinct sensitivity/retention/withdrawal flows in the policy but **no home in this data model**. Either extend storage/retention to cover them or state explicitly they're managed outside the app (and how the deletion/withdrawal guarantees are met).

---

## 11. What the adversarial audit changed (for the record)

The audit verdict was **sound-with-fixes: zero load-bearing-constraint violations**, but it corrected seven contract claims now folded into this doc:

- **The gap is not single-user-computable** (§2) — the central data-flow fix.
- **Per-user CIs are cohort-relative** (§2) — recommend per-key-seeded RNG refactor.
- **Bradley-Terry point estimate is deterministic/portable**; only its bootstrap CI is RNG-bound (§6).
- **Export is not "envelope-strip-only"** — pairwise transform + analyzer-key reconciliation required (§4).
- **Class-A incremental must replicate the analyzer's exclusion/NA semantics** to match (§6).
- **Cut the Web-Worker JS bootstrap** — latency isn't a real problem; it's a reproducibility liability (§6).
- **H8 attachment capture and informant/audio data have no model slot** — resolve in §10.

Plus de-scoping of Yjs / per-event sealing / hash-chains / passkeys / content-addressed routing-ids out of the n=10 pilot (§9).

---

## Cross-references

- [`DECISIONS.md`](DECISIONS.md) §10 (no honey-pot / privacy posture), §13/§16 (versioning + OSF reproducibility), §14 (engineering line — this doc closes the "runtime open" item)
- [`scoring.md`](scoring.md) §1 (event input shapes), §2–3 (Class-A means), §5–6 (stated/gap, sample-relative), §8 (bootstrap CIs), §9 (H8), §10 (exclusions)
- [`types.ts`](types.ts) — the five runtime event shapes + derived score types
- [`scripts/analyze.py`](scripts/analyze.py) — the canonical scorer (stays canonical; never ported)
- [`pilot-materials/data-handling-policy.md`](pilot-materials/data-handling-policy.md) — encryption/retention/deletion this design implements
- [`onboarding.md`](onboarding.md) — reveal + rewind UX; the "one observation" + reveal-threshold open questions
- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — the engineering section whose open stack questions §3 resolves
