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

**Scenarios:**

- Schema violations (each scenario file matched against the appropriate JSON Schema in `scenarios/schemas/`)
- Duplicate scenario IDs across the corpus
- Tags not in `analysis/tag_axis_map_v0.1.csv` (catches typos and undocumented additions)
- Narrative `choice.next` references that don't resolve to a scene ID in the same file
- Cost-of-virtue probe `value_slot` and `preconditions` that don't reference a value in `inventory/values-deck.json`
- Choices without `next` whose parent scene isn't terminal
- Every choice path eventually reaches a terminal scene (no infinite loops, no dead-end branches)
- No orphan scenes (every scene reachable from some starting scene)

**Inventory (structural Python-level checks; no JSON Schema):**

- `values-deck.json`: value IDs unique; `internal_tensions` references resolve; declared `size` matches actual count; all values have a valid `domain`
- `pairwise-pairs.json`: pair IDs unique; `left_id`/`right_id` resolve in the values-deck; `left_id != right_id`; `pair_type` in canonical enum; within-domain pairs declare `domain`; within-domain pairs have both values in that domain; declared `pair_count` matches actual

## What it doesn't catch yet

- Three-layer prompts, story prompts, and relational-variant inventory files — no structural checks; only `types.ts` types exist as a contract
- Semantic validity — a `truth:` tag on a `lie:`-marked option would parse but should be flagged by editorial review
- Cross-domain tag consistency — e.g., flagging when a tag's scoring direction would conflict with the scenario's domain

## What it catches now (narratives, in addition to schema)

- `choice.next` references resolve to an in-file scene ID
- Every choice path eventually reaches a terminal scene (no infinite loops, no dead-end branches)
- No orphan scenes (every scene reachable from some starting scene)

## CI integration

Active at [`.github/workflows/validate.yml`](../.github/workflows/validate.yml). Runs on push to `main` and on every pull request, but only when files under `scenarios/`, `inventory/`, `analysis/`, `scripts/`, or the workflow itself change. Path-filtering keeps the actions-minutes cost negligible (a validation run takes ~10 seconds; the filter skips it on most pushes).

Triggers:
- `push` to `main` (filtered)
- `pull_request` (filtered)
- `workflow_dispatch` (manual run from the GitHub UI)

The workflow can be deleted without affecting the validator itself — `scripts/validate.py` runs identically locally.

## Future scripts

- `validate-inventory.py` — once inventory schemas are authored, parallel script for inventory files
- `analyze.py` (or `.R`) — the scoring-spec analyzer; out-of-scope for MVP-1 content validation, in-scope when the validation cohort produces data
- `seed-fixtures.py` — generate synthetic session-log entries for testing the eventual scenario engine

Each script should be self-contained, minimally-dependent, and runnable from repo root.
