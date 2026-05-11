# analysis/

Versioned data files that the analyzer consumes. These files are *part of the pre-registration* — they lock at OSF filing time and any post-lock change is reported as a deviation.

## Files

- [`tag_axis_map_v0.1.csv`](tag_axis_map_v0.1.csv) — maps each scenario-tag to the scoring axis it contributes to, with signed weight in [−1, +1]. The analyzer reads only rows where `axis != metadata`. Metadata tags are stratifiers (counterparty, stake, social-cost, resolution) — they're not part of scoring but the analyzer uses them for subgroup analyses.

## Versioning

The `_v0.1` in the filename is intentional. When the tag-to-axis mapping changes (a new tag is added; an existing tag's weight is revised; a scoring axis is added), bump to `_v0.2` rather than overwriting. The pre-registration locks a specific version; future analyzers can run either version against the data.

The version of the file used in the final write-up is reported alongside the results.

## How a tag enters the map

1. A scenario author tags an option in a JSON file
2. CI validates the tag against this map (`axis = metadata` is acceptable but logged for review)
3. If the tag is genuinely new and scoring-relevant, it gets reviewed and added to a new version of this file
4. The previous version stays in the repo for reproducibility

This discipline prevents drift between authored content and analyzer behavior.

## Open

- An automated CI hook that fails the build on tag mismatch is TODO.
- The full enumeration of metadata-stratifier tags is incomplete in v0.1 — adequate for MVP-1 piloting; full lock requires sweeping the entire scenario corpus.
