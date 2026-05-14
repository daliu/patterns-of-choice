# scripts/

Utility scripts. **This is the first executable code in the repo.** Crosses the engineering decision point flagged in `DECISIONS.md §14`; commits to Python as a tooling language but no specific runtime stack for the eventual product. Python was chosen because: (a) `scoring.md` names Python or R as the analyzer language, so this is on-spec; (b) Python is the standard for content-validation scripts; (c) the dependency footprint (`jsonschema`) is minimal.

## Files

- [`validate.py`](validate.py) — validates all scenario JSON files against their JSON Schemas and the cross-file integrity constraints scoring.md and SCHEMA.md require.
- [`requirements.txt`](requirements.txt) — single dependency: `jsonschema>=4.18`.

## Usage

```sh
# One-time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt

# Validate
python scripts/validate.py
python scripts/validate.py --quiet     # only print failures
```

Exits 0 on success, 1 on validation failure, 2 on script error.

## What `validate.py` catches

- Schema violations (each scenario file matched against the appropriate JSON Schema in `scenarios/schemas/`)
- Duplicate scenario IDs across the corpus
- Tags not in `analysis/tag_axis_map_v0.1.csv` (catches typos and undocumented additions)
- Narrative `choice.next` references that don't resolve to a scene ID in the same file
- Cost-of-virtue probe `value_slot` and `preconditions` that don't reference a value in `inventory/values-deck.json`
- Choices without `next` whose parent scene isn't terminal

## What it doesn't catch yet

- Inventory JSON files (pairwise-pairs.json, three-layer-prompts.json, story-prompts.json, relational-variant.json) — no JSON Schemas authored for inventory yet; only `types.ts` types exist
- Path reachability — does every choice path eventually reach a terminal scene? Catches dangling `next`-IDs but not orphan terminals or cycles
- Semantic validity — a `truth:` tag on a `lie:`-marked option would parse but should be flagged by editorial review
- Cross-domain tag consistency — e.g., flagging when a tag's scoring direction would conflict with the scenario's domain

## CI integration

Recommended pre-commit / PR hook:

```yaml
# .github/workflows/validate.yml
name: validate scenarios
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r scripts/requirements.txt
      - run: python scripts/validate.py --quiet
```

Not yet committed as a workflow file; this README documents the intended pattern.

## Future scripts

- `validate-inventory.py` — once inventory schemas are authored, parallel script for inventory files
- `analyze.py` (or `.R`) — the scoring-spec analyzer; out-of-scope for MVP-1 content validation, in-scope when the validation cohort produces data
- `seed-fixtures.py` — generate synthetic session-log entries for testing the eventual scenario engine

Each script should be self-contained, minimally-dependent, and runnable from repo root.
