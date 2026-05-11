# scenarios/

Authored scenario library for the patterns-of-choice measurement layer.

**Status:** Two sample scenarios in `sample/` exemplify the format. The MVP-1 target is ~48 authored scenarios across 4 domains (see [`../mvp.md`](../mvp.md)).

## Format

Scenarios are authored as JSON files. Three scenario *types* correspond to the three core session modules in `concept.md`:

| Type | Filename prefix | Schema | Purpose |
|---|---|---|---|
| Quick-fire round | `qf-` | `quick-fire-round` | 5–8 paired forced choices under a visible timer; captures System 1 |
| Core narrative | `narr-` | `core-narrative` | Branching interactive-fiction scene with 4–6 decisions; richest domain-level data |
| Cost-of-virtue probe | `cov-` | `cost-of-virtue-probe` | Stake-laddering auction on a previously-stated value; the longitudinal signal |

See [`SCHEMA.md`](SCHEMA.md) for full field definitions.

## Authoring principles

- **Behavioral anchors, not abstractions.** Scenarios describe concrete situations with stakes; they do not ask "how much do you value honesty?"
- **Pre-registerable.** Each authored scenario has a fixed ID, version, and tag set so the analysis plan can reference them before data collection.
- **Mundane over dramatic.** Per Hofmann et al. 2014 *Science* and the post-Bostyn 2018 ecological-validity literature, everyday moral situations have better lab-to-life correspondence than trolley-class dilemmas. The bar exists low.
- **No "right answer."** Tags describe what each choice reveals (which signature, which counterparty, what stake level); they do not score one choice as better than another.
- **Multiple framings of the same logical structure.** For each domain, we want scenarios that vary surface (workplace / family / anonymous online) while preserving the underlying choice structure — this is how the *consistency under reframing* signature gets measured.

## Domain coverage (MVP-1)

The MVP scopes 4 domains; sample scenarios currently illustrate only `truth-telling`:

- [ ] Truth-telling under cost — 2 samples (this directory)
- [ ] Resource allocation — pending
- [ ] In-group / out-group — pending
- [ ] Reciprocity / cooperation — pending

Each domain needs ~12 scenarios at MVP-1 scale, mixed across the three types.

## Open authorship questions

- Single voice vs. editorial board (see `../mvp.md` decision-point §1)
- Whether to ship a content-style guide for future authors
- Localization strategy (post-MVP-1)
