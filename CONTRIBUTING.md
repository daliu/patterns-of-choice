# Contributing

The repo accumulated substantial surface area during its design phase — about 80 commits across spec docs, content, tooling, pilot operational materials, and a small interactive demo. This file is the "first thing a new contributor should do" entry point. For why anything is structured the way it is, see [`DECISIONS.md`](DECISIONS.md); for what the project is, see [`README.md`](README.md); for where every track sits right now, see [`PROJECT-STATUS.md`](PROJECT-STATUS.md).

## Five-minute orientation

```sh
# Get the tooling working
make setup

# Confirm the corpus is well-formed (should pass with no errors)
make validate

# See what the analyzer produces against synthetic fixtures
make analyze

# Click through a working demo of one quick-fire scenario
make demo
```

If all four succeeded, you've verified the validator, the analyzer, the fixture data, and the demo all hang together. You're ready to contribute.

## Where to start, by goal

**Reading the project for the first time.** Read in this order: `README.md` → `concept.md` → `PROJECT-STATUS.md` → `first-session-walkthrough.md` → `interpretation.md`. Then open `demo/first-session.html` in a browser. Total: about 90 minutes.

**Adding a scenario.** See [`scenarios/README.md`](scenarios/README.md) for the format. Author your scenario file as JSON, then run `make validate`. The validator catches schema errors, dangling references, missing tags, and a handful of other authoring mistakes. If the validator surfaces an unknown tag, add it to [`analysis/tag_axis_map_v0.1.csv`](analysis/tag_axis_map_v0.1.csv) (metadata stratifier by default; new scoring axes need design review).

**Reviewing the spec.** The load-bearing design is in `concept.md`. The validation plan is in `mvp.md` and `pre-registration.md`. The scoring spec is `scoring.md`; the analyzer implements its pure-Python-tractable subset.

**Running an actual pilot.** This is where the project moves from "designed and specified" to "executed in the real world." The dependency chain in `PROJECT-STATUS.md §"To launch the pilot"` is the canonical path: recruit an academic co-PI; submit IRB using the `pilot-materials/` templates; build the production runtime app; complete scenario authoring to MVP-1 target.

## What to expect

**The project is not in active development.** It was a multi-day design exercise resulting in a substantial pre-launch specification. Whether it gets executed depends on decisions outside this repo (see `PROJECT-STATUS.md §"Open decisions waiting on Dave"`). If you've arrived here expecting an active research project, ask before assuming.

**The code is intentionally minimal.** Two pure-Python scripts (one validator, one analyzer) and one single-file HTML demo. No build tooling, no framework lock-in. This is by design — the production runtime stack remains an open decision.

**The corpus is provisional.** 55 scenarios are authored (the full 48-scenario MVP-1 base + the first 5 H8 paired probes). They will get editorial revision against actual pilot participant feedback. Treat scenario wordings as drafts, not as a locked instrument.

**The candor moment is structurally load-bearing.** The recurring "this instrument is unvalidated; you might step away" framing in `onboarding.md`, the consent form, and the demo is not rhetorical. It's the project's response to the contested-ecological-validity premise. Reviewers used to standard consumer-app or research framings will sometimes object to it. Don't soften without reading the rationale.

## What kind of contributions

**Welcome:**
- More authored scenarios (in any of the four MVP-1 domains)
- Editorial review of existing scenarios for clarity / bias / interpretability
- Literature additions in areas already covered in `literature/`
- Bug fixes in the validator / analyzer
- Improvements to the demo's accessibility, keyboard navigation, mobile rendering
- Translations of scenario / inventory content (post-MVP-1)

**Discuss first:**
- New scoring axes (would change the tag-axis map and the analyzer; affects pre-registration)
- New domains beyond the four MVP-1 set (changes the validation plan substantively)
- Changes to load-bearing operating constraints (see `DECISIONS.md`)
- Production-runtime engineering (changes the open-decision landscape)

**Probably not in scope here:**
- Marketing copy
- Branding / logo
- B2B / enterprise features (would conflict with `DECISIONS.md §7`)
- Social comparison features (would conflict with `DECISIONS.md §9`)
- Anything that gamifies the moral behavior itself (would conflict with `DECISIONS.md §8`)

## Conventions

- **Files.** UTF-8, LF line endings, two-space JSON indentation, no trailing whitespace.
- **Commits.** Subject lines under 72 chars, present tense ("scenarios: add fifth truth-telling quick-fire"). Bodies wrap at 72 chars. Each commit should be coherent on its own; squash before opening a PR.
- **Tags in scenarios.** All-lowercase, hyphens or underscores within tokens, single or no colon separator (`namespace:value` or `bare-token`). Pattern: `^[a-z_-]+(:[a-z_-]+)*$`. The validator enforces this.
- **New tags.** Add to the tag-axis map in the same commit as the scenario introducing them. The pre-OSF-lock policy permits in-place edits to the map; post-lock requires version bumps.
- **No emojis in code or content** unless explicitly user-requested. The aesthetic is calm, not warm.

## Questions

Repo issues are the right channel for design questions and operational questions. For questions about the underlying design rationale, read `DECISIONS.md` first — most foundational questions are already answered there.
