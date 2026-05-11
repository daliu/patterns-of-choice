# Inventory JSON Schema

**Version:** 0.1

---

## `values-deck.json`

```jsonc
{
  "version": "0.1",
  "size": 20,
  "card_sort_protocol": "...",            // one-paragraph description of UX
  "design_intent": "...",                  // why this set of values
  "values": [
    {
      "id": "honesty",                     // snake_case stable ID; matches scenario tags
      "label": "Honesty",                  // display name
      "domain": "truth-telling",           // matches scenario taxonomy
      "behavioral_anchor": "...",          // single sentence: value as observable behavior, with cost
      "internal_tensions": ["tact", "discretion"]   // IDs of other values this trades against
    }
  ]
}
```

---

## `pairwise-pairs.json`

```jsonc
{
  "version": "0.1",
  "value_pool_size": 20,
  "pair_count": 30,
  "sampling_strategy": "...",              // how pairs were chosen from the 190 possible
  "pairs": [
    {
      "id": "p01",
      "pair_type": "within-domain",        // within-domain | cross-domain
      "domain": "truth-telling",           // for within-domain pairs only
      "left_id": "honesty",
      "right_id": "tact",
      "tension_anchor": "...",             // 1–2 sentences explaining what's at stake
      "prompt": "Which leans closer to what you actually do, even when it costs you?",
      "left_text": "Tell someone an uncomfortable truth even if it lands badly.",
      "right_text": "Soften a truth to keep it kind."
    }
  ]
}
```

Bradley-Terry analysis uses the `left_id` / `right_id` and user choice; the prompt and option text exists for the user.

---

## `three-layer-prompts.json`

```jsonc
{
  "version": "0.1",
  "layers": {
    "current_self": {
      "label": "How I actually live",
      "anchor_phrase": "I am a person who...",
      "protocol_note": "Captured first — establishes baseline before aspiration colors response."
    },
    "aspirational_self": {
      "label": "Who I want to become",
      "anchor_phrase": "I want to be a person who...",
      "protocol_note": "Captured second — explicitly distinguished from current self."
    },
    "admired_other": {
      "label": "Someone I deeply respect",
      "anchor_phrase": "Someone I deeply respect is...",
      "protocol_note": "Captured third — dodges self-flattery; users often surface traits they won't claim for themselves."
    }
  },
  "presentation_modes": {
    "pairwise": "Run the pairwise protocol once per layer over sessions 1–3.",
    "card_sort": "Run the card-sort once per layer; same deck, different framing each time.",
    "behavioral_anchor_acknowledgment": "When a value card is selected, show the behavioral anchor and ask the user to confirm: 'is this how you'd actually describe yourself?' for current-self layer; 'is this what you'd want?' for aspirational; 'is this what they actually do?' for admired-other."
  }
}
```

---

## `story-prompts.json`

```jsonc
{
  "version": "0.1",
  "protocol": "...",                       // when/how prompts are surfaced
  "coding_strategy": "...",                // how free text gets mapped back to taxonomy
  "prompts": [
    {
      "id": "story-pride",
      "category": "self-evaluation",
      "framing": "Recent moral self-reflection — proud",
      "text": "Tell me about a time, recently, when you were quietly proud of how you handled something. Not a big moment; one of the small ones. Two or three sentences is plenty.",
      "expected_word_count": "30–120",
      "domains_likely_surfaced": ["any"],
      "follow_up": "If you can: what was the alternative — what would the less-proud version of you have done?"
    }
  ]
}
```

LLM coding maps each story to one or more `(domain, value_id)` tags with confidence scores. Human verification for the validation cohort; automated only for the post-validation product.

---

## Cross-file consistency

- `values-deck.json` defines the universe of value IDs; everything else references them
- `pairwise-pairs.json` only uses IDs that exist in the deck
- `three-layer-prompts.json` is layer-orthogonal (applies to any value)
- `story-prompts.json` does not reference specific values; coding is post-hoc

A CI validator should enforce these constraints once the format stabilizes.
