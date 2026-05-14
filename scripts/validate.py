#!/usr/bin/env python3
"""
Validate patterns-of-choice JSON content against its schemas and cross-file
integrity constraints.

Usage:
    python scripts/validate.py
    python scripts/validate.py --quiet     # only print failures
    python scripts/validate.py --strict    # treat warnings as errors

Exits 0 on success, 1 on any validation failure, 2 on script error.

Checks performed:
- Each scenario JSON validates against its type-specific JSON Schema
  (scenarios/schemas/*.schema.json).
- Narrative choice.next references resolve to scene IDs within the same file.
- Narrative scenes are either decision-points OR terminal (schema enforces
  this; rechecked here for clearer error messages).
- Cost-of-virtue probe value_slot references an existing value ID in
  inventory/values-deck.json.
- Cost-of-virtue probe preconditions.value_must_be_in_user_top_5... ditto.
- All tags in scenario options/choices appear in
  analysis/tag_axis_map_v0.1.csv.
- Scenario IDs are unique across the corpus.

Out of scope (not yet validated here):
- Inventory file structure (pairwise-pairs.json, three-layer-prompts.json,
  story-prompts.json, relational-variant.json). JSON Schemas for these
  don't exist yet; types.ts is the only typed contract.
- Every narrative path eventually reaches a terminal scene. The current
  checks catch unreachable next-ids but not orphan terminals or cyclic
  paths. Adding path-reachability is a TODO.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:
    print(
        "ERROR: jsonschema not installed. Run: pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_DIR = REPO_ROOT / "scenarios" / "sample"
SCHEMAS_DIR = REPO_ROOT / "scenarios" / "schemas"
INVENTORY_DIR = REPO_ROOT / "inventory"
ANALYSIS_DIR = REPO_ROOT / "analysis"


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def load_schemas() -> dict[str, dict]:
    return {
        "quick-fire-round": load_json(SCHEMAS_DIR / "quick-fire-round.schema.json"),
        "core-narrative": load_json(SCHEMAS_DIR / "core-narrative.schema.json"),
        "cost-of-virtue-probe": load_json(
            SCHEMAS_DIR / "cost-of-virtue-probe.schema.json"
        ),
    }


def load_tag_map() -> set[str]:
    """Read column 'tag' from the tag-axis CSV; return the set."""
    csv_path = ANALYSIS_DIR / "tag_axis_map_v0.1.csv"
    tags: set[str] = set()
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row.get("tag")
            if tag:
                tags.add(tag.strip())
    return tags


def load_value_ids() -> set[str]:
    deck = load_json(INVENTORY_DIR / "values-deck.json")
    return {v["id"] for v in deck["values"]}


def validate_schema(data: dict, schema: dict) -> list[str]:
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(data):
        path = "/".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"schema: {err.message} @ {path}")
    return errors


def validate_narrative_paths(data: dict) -> list[str]:
    """
    For a core-narrative scenario, verify:
      (1) every choice.next resolves to a scene ID within the file,
      (2) every choice path eventually reaches a terminal scene,
      (3) every scene is reachable from some starting scene (no orphans).
    """
    errors = []
    scenes_list = data.get("scenes", [])
    scenes = {s["id"]: s for s in scenes_list}
    terminals = {sid for sid, s in scenes.items() if s.get("terminal")}

    # (1) choice.next references resolve
    for scene in scenes_list:
        sid = scene["id"]
        if scene.get("terminal"):
            continue
        for choice in scene.get("choices") or []:
            nxt = choice.get("next")
            if nxt is None:
                errors.append(
                    f"narrative-paths: scene {sid} choice {choice.get('id')} "
                    f"has no 'next' and parent scene is not terminal"
                )
            elif nxt not in scenes:
                errors.append(
                    f"narrative-paths: scene {sid} choice {choice.get('id')} "
                    f"references unknown scene '{nxt}'"
                )

    # (2) every choice path reaches a terminal scene
    def reaches_terminal(start_id: str) -> bool:
        if start_id not in scenes:
            return False
        visited = set()
        stack = [start_id]
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            if cur in terminals:
                return True
            scene = scenes.get(cur)
            if not scene:
                return False
            for choice in scene.get("choices") or []:
                nxt = choice.get("next")
                if nxt and nxt != cur:
                    stack.append(nxt)
        return False

    for scene in scenes_list:
        sid = scene["id"]
        if scene.get("terminal"):
            continue
        for choice in scene.get("choices") or []:
            nxt = choice.get("next")
            if nxt and nxt in scenes and not reaches_terminal(nxt):
                errors.append(
                    f"narrative-paths: scene {sid} choice {choice.get('id')} → "
                    f"{nxt} leads to a path that never reaches a terminal scene"
                )

    # (3) every scene reachable from some root
    # Roots = scenes that are not the target of any choice.next
    targets = {
        choice["next"]
        for s in scenes_list
        for choice in (s.get("choices") or [])
        if choice.get("next")
    }
    roots = [sid for sid in scenes if sid not in targets]

    reachable: set[str] = set()
    stack: list[str] = list(roots)
    while stack:
        cur = stack.pop()
        if cur in reachable:
            continue
        reachable.add(cur)
        scene = scenes.get(cur)
        if not scene:
            continue
        for choice in scene.get("choices") or []:
            nxt = choice.get("next")
            if nxt:
                stack.append(nxt)

    orphans = set(scenes) - reachable
    for sid in sorted(orphans):
        errors.append(
            f"narrative-paths: scene {sid} is unreachable from any starting scene"
        )

    return errors


def validate_probe_values(data: dict, value_ids: set[str]) -> list[str]:
    errors = []
    slot = data.get("value_slot")
    if slot and slot not in value_ids:
        errors.append(
            f"probe-values: value_slot '{slot}' not in inventory/values-deck.json"
        )
    precond = (
        data.get("preconditions", {})
        .get("value_must_be_in_user_top_5_for_at_least_one_layer", None)
    )
    refs = precond if isinstance(precond, list) else ([precond] if precond else [])
    for ref in refs:
        if ref not in value_ids:
            errors.append(
                f"probe-values: precondition value '{ref}' not in "
                f"inventory/values-deck.json"
            )
    return errors


def validate_inventory() -> list[str]:
    """
    Structural integrity checks for inventory files. Done at the Python level
    rather than via JSON Schema — the inventory module is small and rarely
    authored by multiple people; full Schema files would be defense-in-depth
    rather than catching real drift.

    Checks:
    - values-deck: value IDs are unique, internal_tensions references resolve,
      declared `size` matches actual count, all values have a `domain` from
      the canonical enum.
    - pairwise-pairs: pair IDs are unique; left_id/right_id resolve in
      values-deck; left_id != right_id; within-domain pairs declare a domain;
      within-domain pairs have both values in that domain; declared pair_count
      matches.
    """
    errors: list[str] = []
    valid_domains = {
        "truth-telling",
        "resource-allocation",
        "in-group-out-group",
        "reciprocity-cooperation",
    }

    # ----- values-deck -----
    try:
        deck = load_json(INVENTORY_DIR / "values-deck.json")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return [f"values-deck.json: cannot load ({e})"]

    seen_ids: set[str] = set()
    for v in deck.get("values", []):
        vid = v.get("id")
        if not vid:
            errors.append("values-deck: value missing 'id'")
            continue
        if vid in seen_ids:
            errors.append(f"values-deck: duplicate value id '{vid}'")
        seen_ids.add(vid)
        dom = v.get("domain")
        if dom and dom not in valid_domains:
            errors.append(
                f"values-deck: value '{vid}' has invalid domain '{dom}' "
                f"(must be one of {sorted(valid_domains)})"
            )

    for v in deck.get("values", []):
        for ref in v.get("internal_tensions", []) or []:
            if ref not in seen_ids:
                errors.append(
                    f"values-deck: value '{v.get('id')}' references unknown "
                    f"internal_tensions value '{ref}'"
                )

    declared_size = deck.get("size")
    actual_size = len(deck.get("values", []))
    if declared_size is not None and declared_size != actual_size:
        errors.append(
            f"values-deck: declared size={declared_size}, actual count={actual_size}"
        )

    # ----- pairwise-pairs -----
    try:
        pairs = load_json(INVENTORY_DIR / "pairwise-pairs.json")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return errors + [f"pairwise-pairs.json: cannot load ({e})"]

    value_domain_lookup = {v["id"]: v.get("domain") for v in deck.get("values", [])}

    seen_pair_ids: set[str] = set()
    for p in pairs.get("pairs", []):
        pid = p.get("id", "<missing>")
        if pid in seen_pair_ids:
            errors.append(f"pairwise-pairs: duplicate pair id '{pid}'")
        seen_pair_ids.add(pid)

        for ref_field in ("left_id", "right_id"):
            ref = p.get(ref_field)
            if ref and ref not in seen_ids:
                errors.append(
                    f"pairwise-pairs: pair {pid} {ref_field}='{ref}' not in values-deck"
                )

        if p.get("left_id") and p.get("left_id") == p.get("right_id"):
            errors.append(
                f"pairwise-pairs: pair {pid} has identical left_id and right_id"
            )

        pair_type = p.get("pair_type")
        if pair_type not in {"within-domain", "cross-domain"}:
            errors.append(
                f"pairwise-pairs: pair {pid} has invalid pair_type '{pair_type}'"
            )

        if pair_type == "within-domain":
            decl_domain = p.get("domain")
            if not decl_domain:
                errors.append(
                    f"pairwise-pairs: pair {pid} is within-domain but missing 'domain' field"
                )
            elif decl_domain not in valid_domains:
                errors.append(
                    f"pairwise-pairs: pair {pid} declared domain '{decl_domain}' not in canonical enum"
                )
            else:
                for ref_field in ("left_id", "right_id"):
                    ref = p.get(ref_field)
                    if ref:
                        actual_domain = value_domain_lookup.get(ref)
                        if actual_domain and actual_domain != decl_domain:
                            errors.append(
                                f"pairwise-pairs: pair {pid} within-domain='{decl_domain}' "
                                f"but {ref_field}='{ref}' has domain '{actual_domain}'"
                            )

    declared_count = pairs.get("pair_count")
    actual_count = len(pairs.get("pairs", []))
    if declared_count is not None and declared_count != actual_count:
        errors.append(
            f"pairwise-pairs: declared pair_count={declared_count}, actual count={actual_count}"
        )

    return errors


def validate_tags(data: dict, known_tags: set[str]) -> list[str]:
    """Find all 'tags' arrays in the data tree; check each tag is in the map."""
    errors = []
    bad_tags: set[str] = set()

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            tags = obj.get("tags")
            if isinstance(tags, list):
                for t in tags:
                    if isinstance(t, str) and t not in known_tags:
                        bad_tags.add(t)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    for t in sorted(bad_tags):
        errors.append(f"tags: '{t}' not in analysis/tag_axis_map_v0.1.csv")
    return errors


def validate_scenario_file(
    path: Path,
    schemas: dict[str, dict],
    known_tags: set[str],
    value_ids: set[str],
    seen_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        data = load_json(path)
    except json.JSONDecodeError as e:
        return [f"json: malformed — {e.msg} at line {e.lineno} col {e.colno}"]

    sid = data.get("id")
    if not sid:
        errors.append("structure: missing top-level 'id'")
    elif sid in seen_ids:
        errors.append(f"structure: duplicate scenario id '{sid}'")
    else:
        seen_ids.add(sid)

    stype = data.get("type")
    schema = schemas.get(stype)
    if not schema:
        errors.append(f"structure: unknown scenario type '{stype}'")
        return errors

    errors.extend(validate_schema(data, schema))
    errors.extend(validate_tags(data, known_tags))

    if stype == "core-narrative":
        errors.extend(validate_narrative_paths(data))
    elif stype == "cost-of-virtue-probe":
        errors.extend(validate_probe_values(data, value_ids))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors (no warnings exist yet)"
    )
    args = parser.parse_args()

    try:
        schemas = load_schemas()
        known_tags = load_tag_map()
        value_ids = load_value_ids()
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"ERROR loading dependencies: {e}", file=sys.stderr)
        return 2

    seen_ids: set[str] = set()
    file_errors: dict[str, list[str]] = {}

    # Inventory structural integrity (separate pass; not per-file)
    inv_errors = validate_inventory()
    if inv_errors:
        file_errors["inventory/"] = inv_errors

    scenario_paths = sorted(SCENARIOS_DIR.glob("*.json"))
    if not args.quiet:
        print(f"Validating inventory + {len(scenario_paths)} scenarios...")

    for path in scenario_paths:
        errors = validate_scenario_file(path, schemas, known_tags, value_ids, seen_ids)
        if errors:
            file_errors[path.name] = errors

    if file_errors:
        total = sum(len(e) for e in file_errors.values())
        print(
            f"\nFAILED: {total} errors in {len(file_errors)} of {len(scenario_paths)} files\n",
            file=sys.stderr,
        )
        for fname, errs in file_errors.items():
            print(f"  {fname}:", file=sys.stderr)
            for err in errs:
                print(f"    - {err}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"OK: all {len(seen_ids)} scenarios valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
