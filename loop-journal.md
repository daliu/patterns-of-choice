# Patterns of Choice — extension-loop journal (sidecar)

**Why this file exists.** The canonical loop journal lives in the Obsidian vault
(`wiki/conversations/2026-06-09 - Patterns of Choice — Extension Loop.md`). That
vault is iCloud-synced and the note is a dataless/evicted placeholder, so the
iCloud File Provider denies raw uncoordinated writes (`PermissionError`, errno 1)
while still allowing reads and new-file creation. Rather than lose the per-iteration
log, the loop mirrors entries here, in-repo and non-iCloud. **Reconcile into the
vault** once it is materialized (move the vault off "Optimize Mac Storage", or
download the note) — these entries are the source for that back-fill.

Newest first. Each entry: what branch, what it adds, what it honors, what shipped.

---

## Checkpoint — 2026-06-28 (after iteration 16): planned roadmap complete, Round 3 opened (not exhausted)

Both planned rounds of `measurement-avenues.md` are now drafted: Round 1 (10 items,
H10/H12/H11/H-A1 · H-A2 · H-A3 · C1 · A4/A5 · B4 · C2) and Round 2 (R1–R5). ~17
measurement branches exist.

**Honest status (the important part).** The *marginal* value of one more design doc
has genuinely fallen — the binding constraint is now **build-and-validate** (co-PI,
IRB, multi-user runtime, the κ-validation that ungates the language channel), not
design. **But** a disciplined re-scan of the literature still surfaces genuinely
distinct, validated, measurable constructs the map does not cover, so this is **not**
the loop's stop condition ("genuinely run out of novel, rigorous branches"). Opening
**Round 3**, held to a strictly higher bar (distinct from all ~17 AND validated AND
measurable here):

- **R6. Moral conviction / metaethical objectivism** (Skitka 2010; Goodwin & Darley
  2008) — do you hold a moral position as an objective *fact* or a *preference*? The
  meta-stance toward one's own values; distinct from content (inventory), tradeability
  (R2), centrality (R1). Predicts intolerance of dissent / refusal to compromise /
  any-means acceptance. **HIGH — next iteration.**
- **R7. Moral self-regulation dynamics (licensing)** (Blanken/van de Ven/Zeelenberg
  2015 meta, d≈0.31) — within-sequence: does a virtuous choice at *t* raise the odds
  of a lapse at *t+1*? Distinct from B4's slow drift; the choice stream already exists.
  Replication discipline load-bearing: license only the surviving *licensing* half;
  exclude/caveat the "Macbeth-effect" *cleansing* (Earp et al. 2014 failure). **MEDIUM.**
- **R8. Shame- vs guilt-proneness** (Tangney et al. 2007) — the *form* of moral emotion
  (guilt→repair vs. shame→withdraw) vs. A5's *magnitude*. Overlaps A5 — flagged for a
  discriminant check first; fold in if it doesn't cleanly stand apart. **LOW.**

If a future scan yields nothing that clears this bar, *that* is the genuine stop.
Corrected the premature "flag-and-stop, exhausted" note that had conflated
"planned roadmap done" with "no rigorous branches remain." Loop cron `8819f3b8`
(15-min, session-only) continues into R6 on its next fire unless redirected.

---

## Iteration 16 — 2026-06-28 — R5 · Moral typecasting / dyadic structure (Round 2's last)

- **Branch.** `r5-moral-typecasting.md` — how a person *parses* a moral scene into the
  **agent** (the doer: responsibility, intent, blame) vs. the **patient** (the done-to:
  harm, suffering, need): `dyadic_emphasis = agent_focus − patient_focus`, a justice-vs-
  care emphasis. R5a reliable dyadic emphasis; R5b harm-centrality (do you need a victim
  to moralize?); R5c typecasting (agent XOR patient — exploratory, needs dedicated items).
- **Grounding.** Gray & Wegner 2009 (typecasting); Schein & Gray 2018 (Theory of Dyadic
  Morality); Gilligan 1982 (the care/justice *emphasis* — explicitly not the discredited
  gender claims; already a repo reference).
- **Honesty (load-bearing).** The **weakest operationalization on the map** — detection is
  indirect (κ-gated A3 agent/patient language + inferential intent-vs-harm choice-weighting);
  R5c's clean probe needs role-assignment items the corpus lacks. Reported **exploratory**;
  R5a's reliability is itself contingent on the indirect channels carrying signal (a pilot
  question). Value-neutral (justice/care, neither better). Names exactly the dedicated items
  that would measure it cleanly — closes the map by marking where the next real work is, not
  by overclaiming.
- **Card.** Yes — "Doer or done-to / Whose side of a moral scene do you see first?"
  (design-stage, exploratory). Manifest → 13 cards.
- **Shipped.** poc `86a1fd2` (r5 doc + map R5✓ + research-program.json). Site regenerated
  12→13 cards, `--check` green, R5 link 200, daliu `3fa5d70` (master). DECISIONS entry
  proposed (pending Dave's lock), not auto-locked.

## Iteration 15 — 2026-06-28 — R4 · Moral attentiveness (do you even notice?)

- **Branch.** `r4-moral-attentiveness.md` — Reynolds 2008 moral attentiveness as the
  **perceptual front-end**: `perceptual_i` (do you *see* the ethical dimension?) and
  `reflective_i` (do you *think* about ethics?). The trait-level version of Rest's (1986)
  component-1 *moral sensitivity* — the construct upstream of every other branch (you can't
  show a cost-of-virtue, an A5 pull, or an R3 disengagement on stakes you never perceived).
- **Grounding.** Reynolds 2008 (JAP); Rest 1986 (four-component model); Gantman & Van Bavel
  2014 (the "moral pop-out" effect → the non-reactive incidental-salience read).
- **Honesty (load-bearing).** The **reactivity problem** is the central methodological burden:
  asking "is this a moral situation?" *manufactures* the attention it measures, so R4 uses
  **non-reactive** channels primarily (spontaneous moral-framing *rate* in the A3 corpus —
  distinct from A3's *content*; incidental moral salience) and treats any dedicated probe as
  reactive + educational, never primary. Value-neutral with **extra-force scrupulosity
  guardrails** at the high end (high attention = perceptiveness *or* over-moralizing). R4b: the
  upstream gate, discriminant from value-importance and from R1 centrality (the four corners,
  incl. low-attentive/high-central "well-meaning-but-oblivious").
- **Card.** Yes — "Moral attention / Do you see the moral dimension, or walk past it?"
  (design-stage). Manifest → 12 cards.
- **Shipped.** poc + site (12-card grid) committed/pushed earlier this session. DECISIONS entry
  proposed (pending Dave's lock).

---

*Earlier iterations (1–14) are logged in the vault note; this sidecar begins at 15, the
point the vault became iCloud-gated.*
