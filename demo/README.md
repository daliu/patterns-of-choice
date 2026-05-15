# demo/

**Demo only.** A single self-contained HTML file that renders one quick-fire scenario as an interactive flow. Vanilla JavaScript, no build tooling, no framework, no hosting required — open `first-session.html` in a browser.

## What this is

- A real-rendering version of the screens described in [`../first-session-walkthrough.md`](../first-session-walkthrough.md)
- The opening screen, the candor moment (including a real "step away" branch), the quick-fire instructions, six binary forced-choice items under an 8-second timer, and a session-end observation
- Embedded scenario data sourced from [`../scenarios/sample/qf-truth-001.json`](../scenarios/sample/qf-truth-001.json)

## What this is NOT

- **Not the production runtime.** Per [`../DECISIONS.md §14`](../DECISIONS.md), the runtime stack decision remains open. This demo is a measured step across the runtime line in the smallest possible way — vanilla HTML + JS — that does not commit to React, Svelte, or any specific framework.
- **Not a full session.** A real first session per [`../first-session-walkthrough.md`](../first-session-walkthrough.md) also includes the 20-value card sort and a story prompt. Those are omitted here for compactness.
- **Not persistent.** Session data is logged to the browser console (open DevTools). Production would use IndexedDB locally with opt-in encrypted sync per [`../pilot-materials/data-handling-policy.md`](../pilot-materials/data-handling-policy.md).
- **Not validated.** The candor moment in the demo names this; the production app uses the same framing.

## Run it

```sh
# macOS / Linux
open demo/first-session.html

# Or just double-click the file in a file explorer.
```

No `npm install`. No server needed. Single file.

## What the demo demonstrates

- The JSON scenario format actually renders to a working UI
- The candor moment can be implemented without making the product feel unproven
- The 8-second-per-item timer feels like the right pace (you can validate against your own experience)
- The "step away" CTA actually works as a real branch, not just copy
- The session-end observation is descriptive, never evaluative

## What gets logged

Open the browser DevTools console after completing the demo. The session log object has:
- Scenario ID, start / end timestamps
- Per-item: item ID, chosen option (or `null` for timeout), response time in ms, timeout boolean

This matches the `SessionLogEntry` shape in [`../types.ts`](../types.ts), modulo the production-side fields like `user_id` and `session_id` that this demo doesn't generate.

## Why a demo file at all

The repo has a substantial set of documents describing the system. Several reviewers (potential co-PI, grant reviewer, future contributor) would benefit from seeing the design actually render to a working interaction rather than reading about it. The walkthrough document is one bridge; this demo is the other.

## Why not React / Vite / a real runtime

Per [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) §"Open decisions waiting on Dave," the runtime stack choice is on the open-decision list. Building anything that commits to React would foreclose that decision. A vanilla HTML demo doesn't.

If Dave decides to go with React + TypeScript + Vite per `mvp.md` §"Tech stack proposal," this demo file gets deleted and replaced. If Dave decides on something else, this demo file still gets deleted but the alternative stack proceeds independently. The demo is intentionally reversible.

## Limitations / known issues

- No keyboard navigation — click only. Production would handle this.
- No accessibility audit. Production would.
- No analytics. Production has explicit opt-in only.
- The "session log" is in-memory and lost on refresh. Production persists locally.
- The session-end observation is hardcoded; production uses the tag-axis map.
- No localization. The pilot is English-only per `pilot-protocol.md`.
