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

A stake-laddered probe that locates the user's break-point on a previously-stated value. Concrete framing of the trade-off plus a 4-rung amount ladder plus an explicit no-option; the user picks the smallest rung at which they'd act (or `never`). UI renders amount buttons after the framing.

```jsonc
{
  // ...common fields...
  "value_slot": "honesty",                  // matches an ID from inventory/values-deck.json
  "preconditions": {
    "value_must_be_in_user_top_5_for_at_least_one_layer": "honesty",
                                            // probe surfaces only if user has named this value;
                                            // can be a single string or an array of acceptable values
    "ladder_currency": "user-local"         // future i18n hook; "USD" until localization ships
  },
  "framing_prompt": "Multi-sentence concrete scenario describing the action and removing escape valves (no one would know; no realistic consequences).",
  "framing_question": "What's the smallest amount at which you'd say yes?",
  "ladder": [
    { "rung": 1, "stake": 10,    "unit": "USD", "label": "$10" },
    { "rung": 2, "stake": 100,   "unit": "USD", "label": "$100" },
    { "rung": 3, "stake": 1000,  "unit": "USD", "label": "$1,000" },
    { "rung": 4, "stake": 10000, "unit": "USD", "label": "$10,000" }
  ],
  "no_option": {
    "id": "never",
    "text": "I wouldn't do this at any of these amounts."
  },
  "alternate_no_option": {                  // optional — used by inverted probes (e.g.
                                            // cov-allocation-001 asks "at what stake would you
                                            // RETURN the overpayment" rather than accept the trade)
    "id": "always_keep",
    "text": "I'd keep it at any of these amounts."
  },
  "analysis": {
    "break_point_field": "first_accept_stake",
    "no_break_point_handling": "Code as Inf for break-point analysis; report separately as 'integrity ceiling above probe range'",
    "interpretation_note": "...",            // per-probe nuance for the analyst
    "longitudinal_signal": "...",            // what within-user trajectory means
    "domain_signature_captured": "cost_of_virtue_curve"
  }
}
```

### Probe-format design choices

- **Same ladder scale across probes ($10 → $10,000) by default** so within-user break-points are cross-domain comparable, except where a domain's realistic stake floor is higher (loyalty/career-opportunity probes use $100 → $100,000).
- **Explicit `framing_question` always present.** Users break their hypothetical action down into "would I do it for X?"; the question wording matters and gets pre-registered.
- **`no_option` is mandatory; `alternate_no_option` is used only for inverted probes** where the ladder asks at what stake the user does the *ethical* action rather than the *unethical* one.
- **Preconditions gate probe surfacing.** The probe is meaningful only if the user has stated the value matters; otherwise it tests an aspiration the user doesn't claim, which conflates revealed-vs-stated.

### Inverted probes

`cov-allocation-001` is the first inverted probe: the ladder asks at what overpayment the user would *return* it (ethical action), not accept the trade (unethical action). Analysis pipeline must read `break_point_field` together with direction-of-action from `analysis` to score correctly.

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
