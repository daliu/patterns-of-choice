# Recurring-character arcs — data model (v0.1)

Status: draft 0.1 (2026-06-05). Canonical model for multi-session NPC arcs. The
runtime (`daliu.github.io/patterns-of-choice/runtime/`) and the analyzer both
consume this; keep one source of truth here so they cannot drift.

## Why arcs exist

H8 (narrative-immersion-as-debiasing) is the project's novel claim: that a
choice about a character you have *come to know* across sessions is measured
with less social-desirability distortion than the same choice posed abstractly.
The H8b high-stakes probe (`pp-allocation-001`, narrative form
`narr-allocation-008` "High water") is the headline test — but its own setup
*references* months of attachment ("You named the dog yourself, the first
week... Across these months that has turned out to be a great deal") that, until
now, the participant never actually lived. Without that lived accrual the climax
is just a trolley problem with a dog sticker, and H8 is untestable.

**An arc is the lived accrual.** It is an ordered sequence of short *beats*
featuring one recurring character, played one beat per session, where the early
beats are deliberately mundane acts of care (ecological-validity register) and
attachment builds through ordinary recurrence — so that the eventual
high-stakes beat lands on a relationship the participant has, not one they were
told about. The high-stakes beat is *gated* behind a minimum number of prior
encounters, so it cannot fire before the attachment is real.

## Register discipline (load-bearing)

The corpus principle is **mundane over dramatic** for ecological validity. Arcs
keep that for the *build-up*: meeting, naming, routine care, a small ordinary
sacrifice — no melodrama. The single sanctioned dramatic exception remains the
H8b high-stakes climax beat (see `narr-allocation-008` metadata.design_intent
and `h8-narrative-immersion-design.md`). A build-up beat that reaches for
tension or peril is a defect: the whole point is that attachment accrues through
the unremarkable, which is what makes the later forced trade cost something.

## Schema

```jsonc
{
  "arc_id": "arc-biscuit",                 // stable id, kebab-case
  "version": "0.1",
  "npc_ref": "npc-biscuit",                // -> scenarios/npc-cast.json id
  "npc_default_name": "Biscuit",           // shown if participant declines to name
  "name_is_participant_supplied": true,    // if true, b1 captures a name
  "name_token": "{dog_name}",              // substituted with the supplied (or default) name everywhere
  "recurring_npc_tag": "recurring_npc:biscuit", // the tag that marks an event as an encounter with this npc
  "primary_domain": "resource-allocation", // the axis the climax scores on
  "premise": "...",                        // one-paragraph editorial frame (not shown to participant)
  "design_refs": ["h8-narrative-immersion-design.md", "npc-cast.json#npc-biscuit"],
  "beats": [ /* ordered; see beat schema */ ]
}
```

### Beat

```jsonc
{
  "beat_id": "arc-biscuit-b1",
  "order": 1,                              // 1-based play order
  "kind": "naming",                        // naming | encounter | attachment_probe | high_stakes
  "min_prior_encounters": 0,               // gate: # of completed encounter/naming beats required before this beat unlocks
  "title": "The first week",               // short, shown as the session header
  "intro": "...",                          // continuity bridge shown before the scene ("You've had {dog_name} a few weeks now.")
  "captures_name": true,                    // naming beat only: prompt the participant to name the companion

  // EITHER an inline scene graph (build-up beats) ...
  "setup": "...",
  "scenes": [ /* core-narrative scene graph, see below */ ],
  "reflection_prompt": "...",

  // ... OR a reference to an existing canonical scenario (the reused climax)
  "scenario_ref": "narr-allocation-008",   // mutually exclusive with inline scenes
  "pairs_with": "pp-allocation-001"        // the H8 pair this beat's signal feeds
}
```

`kind`:
- **naming** — first appearance; introduces the character and (if
  `name_is_participant_supplied`) captures the participant's chosen name.
- **encounter** — an ordinary care beat; the workhorse of attachment accrual.
- **attachment_probe** — administers the parasocial-relationship self-report
  (see attachment instrument) instead of a scene; logged as an `instrument`
  event. Used to *measure* accrued attachment at a milestone.
- **high_stakes** — the sanctioned dramatic beat; references a canonical
  high-stakes scenario via `scenario_ref` and is gated by `min_prior_encounters`.

### Scene graph (unchanged from core-narrative)

Inline beat scenes use the existing core-narrative shape so the runtime's
scene-walker and the analyzer's tag reader work without special-casing:

```jsonc
// branching scene
{ "id": "scene-1", "text": "...", "choices": [
    { "id": "c1", "text": "...", "next": "scene-2", "tags": ["recurring_npc:biscuit", "care:routine", "value:..."] }
]}
// terminal scene
{ "id": "scene-end", "text": "...", "terminal": true, "tags": ["recurring_npc:biscuit", ...] }
```

Every choice and every terminal scene in an arc beat MUST carry the arc's
`recurring_npc_tag` — that tag is how the runtime counts encounters and how the
projection attributes attachment. Build-up beats are low-stakes, so their tags
lean on relationship texture (`care:routine`, `self-cost:minor`,
`presence:*`) rather than the heavy `stake:high-emotional` of the climax.

## Name substitution

The runtime stores the participant's chosen name as setting
`npc_name:<npc_ref>` at the naming beat. Wherever `name_token` appears in beat
text — and in the reused climax, whose canonical copy still reads "Biscuit" —
the runtime substitutes the stored name (falling back to `npc_default_name`).
The canonical climax is NOT rewritten; substitution is a render-time concern so
the corpus stays stable and analyzer-readable.

## Attachment accrual & gating (runtime projection)

Derived from the append-only event log, never stored as mutable state:

- `encounters(npc)` = count of completed beats (kind `naming`/`encounter`)
  whose logged choice tags include the `recurring_npc_tag`.
- A `high_stakes` beat is *playable* iff `encounters(npc) >= min_prior_encounters`.
- The reveal's H8b read compares the participant's **abstract** choice
  (`qf-allocation-013-i01`, `counterparty:anonymous`) against their **narrative**
  choice (`narr-allocation-008` signal, `counterparty:animal-dependent`) — the
  same indivisible trade, one stripped of attachment and one grounded in it.
  Divergence is reported descriptively (reference-free, no verdict), per the
  no-forced-single-subject-statistic rule.

## First arcs (H8b — attachment-laden stakes)

`arc-biscuit` and `arc-gran` are **H8b** arcs (`mode: "h8b"`, the default): build-up
beats accrue attachment, then a single *gated dramatic climax* poses a high-stakes
trade whose abstract twin (a generic version) is the comparison. Only the cast's
`attachment-laden-stakes` figures (Biscuit, Gran) fit this shape.

- `arc-biscuit` — the "imaginary buddy dog": naming → routine care → small
  sacrifice → (gated) "High water" climax (`narr-allocation-008`).
- `arc-gran` — an aging grandmother (human, non-named): three escalating-dependency
  encounters → (gated) "The near bed" climax (`narr-ingroup-010`).

## H8a arcs (debiasing-companion — accumulation, no climax)

The remaining cast (`npc-nadia`, `npc-marisol`, `npc-cole`) are **H8a**
debiasing-companions (`h8_role: "debiasing-companion"`). Their specs are explicit:
attachment accrues *by accumulation, not by any single dramatic beat*. So an H8a
arc has a different shape and a different read — and it implements the H8a half of
the hypothesis (the H8b runtime above measures only the high-stakes half).

```jsonc
{
  "arc_id": "arc-nadia",
  "mode": "h8a",                          // distinguishes from the h8b climax arcs
  "npc_ref": "npc-nadia",
  "npc_default_name": "Nadia",
  "name_is_participant_supplied": false,
  "recurring_npc_tag": "recurring_npc:nadia",
  "primary_domain": "truth-telling",       // the value axis the pairs score on
  "evolves": false,                        // true for marisol/cole (trajectory IS the signal)
  "beats": [ /* ordered low-stakes "encounter" beats, each with an abstract_twin */ ]
}
```

H8a beat = an ordinary, **low-stakes** encounter (no peril, no climax) whose signal
choice is a truth / reciprocity / in-group choice made ABOUT the known figure,
PLUS an inline **abstract twin** — the same choice posed generically (about an
acquaintance / a stranger / "someone"), which "invites a tidier, more performed
answer" (npc-cast h8_role_note). The twin is presented separately in time.

```jsonc
{
  "beat_id": "arc-nadia-b1",
  "order": 1,
  "kind": "encounter",
  "min_prior_encounters": 0,
  "title": "...", "intro": "...",
  "setup": "...", "scenes": [ /* core-narrative scene graph; the SIGNAL choice carries
                                a value-axis tag, e.g. honesty / lie:white */ ],
  "reflection_prompt": "...",
  "signal": "scene-id-of-the-choice",     // which scene's choice is the measured one
  "abstract_twin": {                       // the generic, performed-answer version
    "item_id": "arc-nadia-b1-twin",
    "prompt": "...about an acquaintance...",
    "options": [ { "id":"a","text":"...","tags":["..."] }, { "id":"b","text":"...","tags":["..."] } ]
  }
}
```

**The H8a read (debiasing):** for each beat, compare the participant's *narrative*
signal choice (about the figure) with their *abstract twin* answer on the value
axis (via the tag map's signed contribution). A systematic gap — typically a
tidier/more-virtuous abstract answer vs. a more candid one about the friend — is
the H8a debiasing signal. Reported per-pair and as a pattern, descriptively, with
NO aggregate score (the no-forced-single-subject-statistic rule). For `evolves`
arcs the *trajectory* of the gap across the ordered beats is the signal (e.g.
marisol's circle-membership widening; cole's trust returning after repair).
H8a arcs have no `high_stakes` beat and no single `pairs_with`.
