# analysis/

Versioned data files that the analyzer consumes. These files are *part of the pre-registration* — they lock at OSF filing time and any post-lock change is reported as a deviation.

## Files

- [`tag_axis_map_v0.1.csv`](tag_axis_map_v0.1.csv) — maps each scenario-tag to the scoring axis it contributes to, with signed weight in [−1, +1]. The analyzer reads only rows where `axis != metadata`. Metadata tags are stratifiers (counterparty, stake, social-cost, resolution) — they're not part of scoring but the analyzer uses them for subgroup analyses.

## Versioning

The `_v0.1` in the filename is intentional. The file is in two regimes:

**Pre-OSF-lock (now).** The file is mutable. New tags get added, weights get revised, axes get re-thought. Filename stays at v0.1 until the next OSF lock event. Discipline: commit each material change with a clear message describing what changed and why.

**Post-OSF-lock.** When the pre-registration is filed at OSF, the tag-axis map that the pre-reg analysis depends on is locked at its filing version (becoming the locked v0.1 / v0.2 / etc.). After that point, any changes get a version bump rather than an in-place edit; the previous version remains in the repo so post-hoc analyses can be re-run against the locked map.

The version of the file used in the final write-up is reported alongside the results.

## How a tag enters the map

1. A scenario author tags an option in a JSON file
2. CI validates the tag against this map (`axis = metadata` is acceptable but logged for review)
3. If the tag is genuinely new and scoring-relevant, it gets reviewed and added (in-place pre-OSF-lock; via version bump post-lock)
4. The previous version stays in the repo for reproducibility

This discipline prevents drift between authored content and analyzer behavior.

## Open scoring question — cross-domain value tags

When a `value:X` tag appears in a scenario whose primary domain is *not* the value's home domain (e.g. `value:loyalty` appearing in a truth-telling item), how should it contribute to scoring?

Two reasonable models:

- **Per-scenario-domain only (current MVP-1 model).** Each item scores only on its parent scenario's primary axis. Cross-domain value tags are descriptive metadata; the analyzer skips them for scoring. Simpler; matches the per-domain CFA pre-registered for MVP-1.
- **Cross-domain scoring.** `value:X` always scores on X's home-domain axis regardless of scenario context. More informative; produces noisier per-domain estimates because each user's per-domain score draws from items in many scenarios. Would change the factor structure pre-registered.

Decision for MVP-1: per-scenario-domain only. Cross-domain `value:X` tags entered in this map as `*,metadata,value:X,,note` rows so the analyzer treats them as intentional metadata rather than typos. Cross-domain scoring is a candidate revision for MVP-2 once measurement validation is established.

## Open

- An automated CI hook that fails the build on tag mismatch is TODO.
- The full enumeration of metadata-stratifier tags is incomplete in v0.1 — adequate for MVP-1 piloting; full lock requires sweeping the entire scenario corpus.
