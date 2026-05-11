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
| Truth-telling under cost | `qf-truth-001` ✓ | `narr-truth-002` ✓ | `cov-truth-001` ✓ | ~12 total |
| Resource allocation | `qf-allocation-001` ✓ | `narr-allocation-002` ✓ | `cov-allocation-001` ✓ (inverted) | ~12 total |
| In-group / out-group | `qf-ingroup-001` ✓ | — | `cov-ingroup-001` ✓ | ~12 total |
| Reciprocity / cooperation | `qf-reciprocity-001` ✓ | — | `cov-reciprocity-001` ✓ | ~12 total |

All 4 domains have a quick-fire round and a cost-of-virtue probe; 2/4 now have a narrative as well. Two more narratives pending (in-group, reciprocity). Authoring estimate: ~30 min per quick-fire, ~90 min per narrative, ~20 min per cost-of-virtue probe. Full MVP-1 corpus (~12 scenarios per domain) is realistically 3–4 weeks of focused editorial work.

## Open authorship questions

- Single voice vs. editorial board (see `../mvp.md` decision-point §1)
- Whether to ship a content-style guide for future authors
- Localization strategy (post-MVP-1)
