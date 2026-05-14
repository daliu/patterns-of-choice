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

The MVP scopes 4 domains; sample scenarios so far:

| Domain | Quick-fire | Narrative | Cost-of-virtue probe | MVP-1 target |
|---|---|---|---|---|
| Truth-telling under cost | `qf-truth-001`, `qf-truth-003` ✓ | `narr-truth-002`, `narr-truth-004` ✓ | `cov-truth-001`, `cov-truth-002` ✓ | ~12 total |
| Resource allocation | `qf-allocation-001`, `qf-allocation-003` ✓ | `narr-allocation-002`, `narr-allocation-004` ✓ | `cov-allocation-001`, `cov-allocation-002` ✓ (both inverted) | ~12 total |
| In-group / out-group | `qf-ingroup-001`, `qf-ingroup-003` ✓ | `narr-ingroup-002`, `narr-ingroup-004` ✓ | `cov-ingroup-001`, `cov-ingroup-002` ✓ | ~12 total |
| Reciprocity / cooperation | `qf-reciprocity-001`, `qf-reciprocity-003` ✓ | `narr-reciprocity-002` ✓ | `cov-reciprocity-001`, `cov-reciprocity-002` ✓ (inverted) | ~12 total |

All 4 domains have 2 quick-fires + 1 narrative + 2 cost-of-virtue probes = 20 scenarios of ~48 target. Symmetric 5-per-domain coverage. Scale-up authoring pattern is well-established. Remaining: ~28 more scenarios (2nd narratives per domain are the highest-value gap; additional quick-fires and cost-of-virtue probes fill in coverage). Realistically 3–4 weeks of focused authoring once committed.

Setting diversity across narratives:
- `narr-truth-002` — workplace happy hour (peer-to-peer)
- `narr-truth-004` — family, aging parent decision (three decision points across months)
- `narr-allocation-002` — workplace all-hands (subordinate, intangible credit)
- `narr-allocation-004` — family financial dynamics (parents' retirement support, three decisions across a year)
- `narr-ingroup-002` — residential community / neighborhood
- `narr-ingroup-004` — workplace team factionalism (strategic-decision split between social-in-group and technical-judgment positions)
- `narr-reciprocity-002` — creative collaboration / podcast partnership (long-running friendship)

## Open authorship questions

- Single voice vs. editorial board (see `../mvp.md` decision-point §1)
- Whether to ship a content-style guide for future authors
- Localization strategy (post-MVP-1)
