# scripts/

Utility scripts. **This is the first executable code in the repo.** Crosses the engineering decision point flagged in `DECISIONS.md §14`; commits to Python as a tooling language but no specific runtime stack for the eventual product. Python was chosen because: (a) `scoring.md` names Python or R as the analyzer language, so this is on-spec; (b) Python is the standard for content-validation scripts; (c) the dependency footprint (`jsonschema`) is minimal.

## Files

- [`validate.py`](validate.py) — validates all scenario JSON files against their JSON Schemas and the cross-file integrity constraints scoring.md and SCHEMA.md require.
- [`analyze.py`](analyze.py) — minimal analyzer implementing scoring.md §2-3 (per-item / per-session / per-user-per-domain revealed scores). Standard library only — no external dependency needed.
- [`requirements.txt`](requirements.txt) — single dependency for `validate.py`: `jsonschema>=4.18`. `analyze.py` is standard library only.

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

## `analyze.py` — minimal scoring-spec analyzer

Implements scoring.md §2-3 (revealed scores), §4 (cost-of-virtue probe scoring), §5.1 (card-sort inventory scoring), §6 (primary gap = z(stated_aspirational) − z(revealed), per-domain standardized), §8 (bootstrap 95% CIs with pre-committed seed). Reserved for the future validation-cohort analyzer: Bradley-Terry pairwise inventory scoring (§5.2), CFA on item-level loadings (§7), longitudinal cost-of-virtue trajectories (§4.3).

```sh
# Revealed scores only
python scripts/analyze.py --log analysis/fixtures/sample-session-log.json

# Revealed + probes + card-sort
python scripts/analyze.py \
  --log analysis/fixtures/sample-session-log.json \
  --probes analysis/fixtures/sample-probe-responses.json \
  --card-sort analysis/fixtures/sample-card-sort.json

python scripts/analyze.py --log <path> --probes <path> --json
```

Output (table by default):

```
user_id                  domain                        mean  sess           95% CI
----------------------------------------------------------------------------------
user-alice               resource-allocation         +0.667     1              nan
user-alice               truth-telling               +0.875     1              nan
user-bob                 truth-telling               -0.396     2   [-0.72, -0.07]
user-carla               truth-telling               +0.200     1              nan

Cost-of-virtue probe break-points (higher = stronger virtue, inv-flipped):
user_id                  domain                     probe_id                log_score  inv
------------------------------------------------------------------------------------------
user-alice               resource-allocation        cov-allocation-001         -1.000    Y
user-alice               truth-telling              cov-truth-001              +5.000    N
user-alice               truth-telling              cov-truth-002              +4.000    N
user-bob                 resource-allocation        cov-allocation-001         -5.000    Y
user-bob                 truth-telling              cov-truth-001              +1.000    N
user-bob                 truth-telling              cov-truth-002              +1.000    N
```

Revealed scores: range `[-1, +1]` per the clamp in scoring.md §2.2. Positive = ethical pole.

Probe scores: `log10` of break-point per scoring.md §4. Forward probes: positive (1 = breaks at $10 = weakest virtue, 5 = never accepts = strongest). Inverted probes: sign-flipped (so within the inverted range, higher = stronger virtue, but the magnitudes don't align with the forward range — per spec §4.2 cross-probe normalization happens at the per-domain CFA aggregation, not here).

## Fixtures

[`analysis/fixtures/sample-session-log.json`](../analysis/fixtures/sample-session-log.json) — synthetic session-log data demonstrating three user profiles (high-honesty, low-honesty, mixed). Used for analyzer development and as a worked example of the runtime data shape.

## Future scripts

- `validate-inventory.py` — once inventory schemas are authored, parallel script for inventory files
- A full validation-cohort analyzer (Python or R) when the cohort produces data. Will use `analyze.py` as a starting point and add inventory scoring, gap computation, bootstrap CIs, CFA.
- `seed-fixtures.py` — programmatic synthesis of session-log entries for stress-testing the scenario engine

Each script should be self-contained, minimally-dependent, and runnable from repo root.
