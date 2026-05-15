# Data-Handling Policy — Pilot (Template)

**Status:** Draft. Operationalizes the data-handling commitments in `consent-form.md` and `informant-recruitment.md`. This document is internal-facing — it tells the researcher *how* to honor those commitments and *how* their honoring is verifiable. The consent form is the participant-facing version; this is the engineering-and-procedure version.

To be finalized against the chosen hosting provider's specifics and the institutional IRB's data-handling requirements.

---

## What this document is responsible for

The consent form makes specific data-handling promises:

1. Local-first by default — session responses are stored on the participant's device.
2. End-to-end encrypted for opt-in sync.
3. No training on participant data, ever.
4. Pilot data discarded within 90 days of pilot completion.
5. Right to withdraw at any time, including data deletion.
6. No sale, no enterprise sharing, no external party access.

This document specifies the technical and procedural backing for each commitment.

---

## Data categories

The pilot generates several distinct data categories with different sensitivity and retention rules:

| Category | What | Sensitivity | Default retention |
|---|---|---|---|
| Session-log entries | Choices, response times, scenario IDs | High — reveals personal moral patterns | 90 days post-pilot |
| Probe responses | Cost-of-virtue break-points per probe | High — same as above | 90 days post-pilot |
| Inventory responses | Card-sort + pairwise + free-text stories | High — includes participant's own words | 90 days post-pilot |
| Informant ratings | HEXACO-60 facet scores | Medium — third-party-about-participant | 90 days post-pilot, 30-day informant withdrawal window |
| Aggregated quantitative metrics | Completion rates, response-time medians | Low (no individual identification) | Retained for the eventual published findings |
| Anonymized interview transcripts | Weekly + exit conversations | Medium — anonymized, but voice tone / phrasing distinctive | Retained for cross-pilot pattern analysis |
| Raw interview audio | Source recordings | High | Deleted within 30 days of transcription |

---

## Storage

### During the active pilot

- **Participant device**: primary store. The app keeps session data in encrypted local storage (IndexedDB on web; SQLCipher or equivalent on native).
- **Researcher server**: receives sync data only when the participant opted into cloud sync. Server-side data is encrypted at rest with a participant-specific key.

### Encryption at rest

Server-side data is encrypted using authenticated symmetric encryption (AES-256-GCM, libsodium's `crypto_secretbox`, or equivalent). Keys are derived from a participant-specific secret generated client-side at first sync; the server stores only the ciphertext.

The encryption key derivation:
- Derived via Argon2id from the participant's authentication credential
- Never transmitted to the server in raw form
- Lost if the participant loses their device AND has not enabled key escrow (an opt-in feature; not default)

If the participant loses their key, their server-side data becomes unreadable to anyone, including the researcher. This is a feature: it implements "no external party access" structurally rather than via policy.

### What is NOT stored

- No participant phone numbers, email addresses, or government IDs paired to session data on the server
- No "real name" linkage — participants are referenced by a UUID throughout
- Compensation processing (Prolific or equivalent) is the only system that touches PII; researcher does not maintain a separate identity database

### Backups

The encrypted server-side data has daily backups for operational reliability (recover from accidental deletion within 7 days). Backups are also encrypted; the same key-loss property applies. Backups older than 30 days are automatically purged.

---

## Access controls

- **Researcher access**: aggregated metrics only, by default. Individual-participant inspection requires logging the access (timestamp, participant UUID, justification) for the eventual study write-up's audit trail.
- **No third-party processor reads the data.** Hosting providers, transcription services, and compensation platforms see only encrypted blobs or non-PII metadata.
- **Two-person rule for individual-participant inspection**: any view of an individual participant's session log requires either (a) the participant's explicit request (e.g. they're asking about a specific data point) or (b) a co-PI sign-off documented in the audit log.

### Specifically forbidden access

- Querying the database to find participants matching specific demographic or behavioral criteria (no profile-building)
- Linking participant data to any external dataset (HEXACO is collected within the study; not joined to outside sources)
- Sharing identified participant data with anyone outside the named research team

---

## Deletion process

### Default 90-day post-pilot deletion

90 days after the last exit interview:

1. **Drop the encrypted user-data tables.** This is the primary deletion; renders the data unrecoverable even with the encryption keys.
2. **Verify against the backup retention.** Confirm that no backup older than 30 days exists at the verification moment (the 30-day backup-rotation policy enforces this; this is a check, not an action).
3. **Audit-log the deletion event.** Timestamp, scope, verification signature from the co-PI.
4. **Notify participants** (if they consented to closure notification). Brief email: *"The pilot ended on [date]. Your data has been deleted as committed. Thank you for participating."*

### Active withdrawal

Participant emails withdrawal request to the published contact:

1. Within 7 days: participant-specific tables purged. Receipt confirmed by reply email.
2. Within 30 days: any backup containing the participant's data has rotated out per the backup retention policy.
3. Notify the participant within 14 days: *"Your data has been deleted. You will not be contacted again unless you initiate contact."*

### Informant withdrawal

Informant emails withdrawal request within 30 days of their questionnaire completion:

1. Their HEXACO-60 ratings are removed from the analysis dataset.
2. Their pairing with the participant is dropped.
3. The participant's data is unaffected (they retain their own data and the rest of their informant pair if both were collected).

After 30 days from informant completion, the informant's contribution is anonymized (informant identity stripped; only the pairing hash and ratings remain); withdrawal of the specific contribution is no longer possible. This is disclosed in the informant consent screen.

---

## What we never do

The consent form lists prohibitions. This document operationalizes them:

| Commitment | Operational backing |
|---|---|
| No training on user data | No data routed to any LLM provider, OpenAI/Anthropic/Google API, or local model training pipeline. The LLM in the analyzer is for prompt-coding free-text using locally-running inference only; no participant data leaves the encryption boundary. |
| No sale | No commercial database access agreements exist. The data is not for sale at any price; no sales process is even possible. |
| No enterprise sharing | No B2B product. No data-licensing arrangements. |
| No employer access | Even with court order, the data is encrypted such that researcher cannot decrypt individual records without the participant's key. Court-orders are resolved through this technical impossibility, not through compliance. (Caveat: not legal advice; co-PI's institutional legal counsel handles real-world court-order scenarios.) |
| No partner / family access | Same. |
| No advertising | No advertising network has any connection to the app. No third-party analytics packages are included. |

---

## Edge cases

### Participant loses their device mid-pilot

Their local data is unrecoverable. If they had enabled sync, they can re-authenticate and recover from server. If they had not enabled sync, their accumulated session data is lost. Researcher notes the gap; participant continues from week 1 (resetting their pilot clock).

### Participant changes their mind mid-pilot about sync

Allowed. If they turn off sync, server-side data is deleted within 7 days of the change. The local data persists.

### Researcher loses their administrative key

This is operationally bad but doesn't compromise participants: participant data is encrypted with participant keys, not the researcher's administrative key. The researcher loses their ability to administer the system but the participants' privacy is unaffected.

### Co-PI changes mid-pilot

Update audit-log entries. Notify participants of the change in writing within 14 days. Allow participants to withdraw without prejudice if they have concerns about the change.

### Audit request from IRB

Researcher provides:
- Aggregated metrics (always)
- Audit-log of individual-record access (always)
- Encrypted database snapshot (only if IRB has compelling reason; participant data remains encrypted)

### Subpoena or court order

Researcher consults co-PI's institutional legal counsel. The encryption design means there is often nothing technical to comply with at the record level. If aggregated data is requested, that can be provided. Individual records are technically inaccessible.

---

## Verification and audit

The pilot's data-handling commitments are verifiable by:

1. Code audit of the sync server (open-sourced; anyone can inspect)
2. Periodic third-party security audit before scaling to MVP-1 main study (recommended before n=200 recruitment; not required for pilot)
3. Pre-registered analysis code (published at OSF lock per pre-registration.md); the analyzer cannot access raw data outside the audit-logged paths
4. Public reporting of deletion events (aggregated)

---

## Updates

This policy is versioned. Material changes require:
- Co-PI sign-off
- Notification to all active participants within 14 days
- Participants given option to withdraw without prejudice in response to the change

Minor updates (typographical, clarifying language) don't require notification but are logged in the document's revision history.

---

## Cross-references

- `consent-form.md` — participant-facing data-handling commitments
- `informant-recruitment.md` — informant-specific data-handling
- `../mvp.md` §"Tech stack proposal" — Y.js + CRDT sync is the proposed implementation; the data-handling specifics in this document assume that or similar
- `../DECISIONS.md §10` — Local-first data architecture as a load-bearing project constraint
