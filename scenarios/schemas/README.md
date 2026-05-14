# scenarios/schemas/

JSON Schema (draft 2020-12) definitions for the three scenario types. Language-agnostic; any validator in any language can consume these. Complements `types.ts` (TypeScript-specific) and `SCHEMA.md` (human-readable).

## Files

| Schema | Validates |
|---|---|
| [`quick-fire-round.schema.json`](quick-fire-round.schema.json) | `sample/qf-*.json` files |
| [`core-narrative.schema.json`](core-narrative.schema.json) | `sample/narr-*.json` files |
| [`cost-of-virtue-probe.schema.json`](cost-of-virtue-probe.schema.json) | `sample/cov-*.json` files |

## What the JSON Schemas catch

- Required fields present
- Types and value ranges correct (e.g., timer_seconds_per_item between 3 and 30; minimum 4 items per quick-fire)
- ID format conventions (e.g., `qf-{domain-slug}-{nnn}`; matching item IDs)
- Tag format (`namespace:value` or single lowercase-underscored token)
- Field length minimums (e.g., metadata.design_intent ≥ 20 chars — catches placeholder content)
- Enum constraints on domain, domain_signature, ladder_currency, break_point_field
- Quick-fire option count is exactly 2 (binary forced-choice)
- Narrative scenes are either decision-points OR terminal but not both
- Cost-of-virtue probe ladder rungs are 3–6 (matches pre-registration's stake-range design)

## What the JSON Schemas do NOT catch

These need a custom validator (not in this directory yet):

- `choice.next` references resolve to a scene ID within the same file
- All choice paths eventually reach a terminal scene (no infinite loops, no dead ends)
- Every tag in every option/choice/scene resolves in `../../analysis/tag_axis_map_v*.csv`
- `value_slot` in a probe references an existing value in `inventory/values-deck.json`
- `preconditions.value_must_be_in_user_top_5_for_at_least_one_layer` references existing value IDs
- Scenario ID is globally unique across the entire corpus (these schemas check format, not uniqueness)
- Tag-scoring direction (a `truth:` tag on a `lie:`-marked choice would parse but should be flagged by editorial review)

## Running validation

```sh
# Using ajv-cli (Node)
npm install -g ajv-cli ajv-formats
ajv validate \
  -s scenarios/schemas/quick-fire-round.schema.json \
  -d "scenarios/sample/qf-*.json" \
  --spec=draft2020

# Using check-jsonschema (Python)
pip install check-jsonschema
check-jsonschema \
  --schemafile scenarios/schemas/quick-fire-round.schema.json \
  scenarios/sample/qf-*.json
```

The custom-validator script that handles the cross-file integrity checks (`choice.next` resolution, tag-map lookup, etc.) is a TODO; recommended as the next engineering artifact after these schemas land.

## Versioning

Schemas follow the same pre-OSF-lock policy as the tag-axis map: in-place mutable until pre-registration is filed, then bump-rather-than-overwrite. The `$id` in each schema is the canonical URL for the locked version once filed.
