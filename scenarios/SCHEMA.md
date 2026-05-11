# Scenario JSON Schema

**Version:** 0.1 (draft; will harden once a third domain is authored and edge cases surface)

All scenario files are UTF-8 JSON. Top-level required fields are `id`, `type`, `domain`, `version`, `metadata`. Type-specific fields follow.

---

## Common fields

```jsonc
{
  "id": "narr-truth-002",                  // stable globally-unique identifier
  "type": "core-narrative",                // one of: quick-fire-round | core-narrative | cost-of-virtue-probe
  "domain": "truth-telling",               // one of: truth-telling | resource-allocation | in-group-out-group | reciprocity
  "version": "0.1",                         // semver string; bump on any tag or wording change
  "metadata": {
    "title": "The happy hour",
    "author": "patterns-of-choice editorial draft",
    "design_intent": "...",                // 1–2 sentences on what the scenario is meant to measure
    "domain_anchor": "...",                 // literature anchor (author/year) for the operationalization
    "estimated_duration_seconds": 240,
    "content_warnings": []                  // e.g., ["workplace conflict", "alcohol context"]
  }
}
```

---

## `type: quick-fire-round`

A timed sequence of paired forced choices. ~60 seconds total. Each item is binary, behaviorally framed, and tagged.

```jsonc
{
  // ...common fields...
  "metadata": {
    // ...common metadata...
    "timer_seconds_per_item": 8             // visible countdown per item
  },
  "items": [
    {
      "id": "qf-truth-001-i01",             // unique within the scenario
      "prompt": "Your housemate asks if you ate the leftovers they were saving. You did.",
      "options": [
        {
          "id": "a",
          "text": "Admit it.",
          "tags": ["truth:commission", "counterparty:close", "stake:micro"]
        },
        {
          "id": "b",
          "text": "Say you didn't see them.",
          "tags": ["lie:omission", "counterparty:close", "stake:micro"]
        }
      ]
    }
    // ...5–7 more items
  ]
}
```

---

## `type: core-narrative`

Branching interactive-fiction scene. 4–6 decision points; branches may converge.

```jsonc
{
  // ...common fields...
  "setup": "Multi-paragraph context shown before the first decision.",
  "scenes": [
    {
      "id": "scene-1",
      "text": "Decision-point prose.",
      "choices": [
        {
          "id": "c1",
          "text": "Choice text the user clicks.",
          "next": "scene-2-a",              // ID of the next scene, OR null/absent if terminal
          "tags": ["truth:confront-mild", "counterparty:peer", "stake:medium-social"]
        }
      ]
    },
    {
      "id": "scene-end-a",
      "text": "Closing prose.",
      "terminal": true,                     // marks an endpoint; no choices
      "tags": ["resolution:honest-discomfort"]
    }
  ],
  "reflection_prompt": "Earlier you chose to {chosen_path}. Looking back — was that the choice that fit who you want to be?",
  "domain_signatures_captured": [
    "consistency_under_reframing",
    "cost_of_virtue_curve",
    "in_group_out_group"
  ]
}
```

---

## `type: cost-of-virtue-probe`

Stake-laddering auction on a previously-stated value. The user's prior inventory data fills the slot at runtime.

```jsonc
{
  // ...common fields...
  "value_slot": "honesty",                  // matched to the inventory taxonomy
  "framing_prompt": "You said earlier that {value} matters to you. Suppose you could trade it here:",
  "ladder": [
    { "stake": 5,     "unit": "USD",  "description": "Write a positive review for a product you've never used." },
    { "stake": 50,    "unit": "USD",  "description": "Same — for $50." },
    { "stake": 500,   "unit": "USD",  "description": "Same — for $500." },
    { "stake": 5000,  "unit": "USD",  "description": "Same — for $5,000." }
  ],
  "break_point_field": "first_accept_stake" // analysis field: the smallest stake at which the user accepts
}
```

---

## Tag vocabulary (controlled)

Tags are namespaced `category:value`. The analyzer reads only these tags, never free text, so the controlled vocabulary matters.

| Namespace | Examples |
|---|---|
| `truth:` | `commission`, `omission`, `confront-mild`, `confront-direct`, `partial`, `acknowledge`, `abandon` |
| `lie:` | `omission`, `commission`, `white`, `protective` |
| `counterparty:` | `close`, `peer`, `subordinate`, `senior`, `stranger`, `out-group`, `child` |
| `stake:` | `micro`, `low`, `medium-social`, `medium-financial`, `high-social`, `high-financial` |
| `social-cost:` | `none`, `low`, `medium`, `high` |
| `self-cost:` | `none`, `apologize`, `time`, `money`, `reputation` |
| `resolution:` | `positive`, `ambivalent`, `avoidance`, `loyalty-over-honesty`, `honest-discomfort`, `honest-costly`, `pretend`, `acknowledge` |

New tags can be added but require updating this vocabulary file and the analyzer.

---

## Validation

Each scenario JSON should pass:

- JSON Schema validation (a `schema.json` ships alongside this doc once the format stabilizes)
- ID uniqueness within the corpus
- All `next` references resolve to scene IDs within the same file
- All tags exist in the controlled vocabulary
- At least one terminal scene reachable from every choice path

A `npm run validate-scenarios` CI hook is the right place to enforce this.
