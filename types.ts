/**
 * Patterns of Choice — Type definitions for all JSON content schemas.
 *
 * This file is declarative only — no runtime, no framework commitment.
 * It captures the same schemas defined in scenarios/SCHEMA.md and
 * inventory/SCHEMA.md in TypeScript-readable form so engineering work
 * (whenever it starts) has a typechecked contract against the content.
 *
 * Versioning: this file tracks the schemas at v0.1. Bump field-by-field
 * (mark deprecated, add new) rather than rewriting; pre-registration
 * locks the field set at OSF filing time.
 *
 * If you change a schema, change both the .md and this file in the
 * same commit.
 */

// =============================================================================
// Shared / primitive types
// =============================================================================

export type ScenarioId = string; // e.g. "qf-truth-001", "narr-allocation-002"
export type ItemId = string;
export type OptionId = string;
export type SceneId = string;
export type ValueId = string; // matches IDs in inventory/values-deck.json
export type UserId = string; // uuid v4
export type SessionId = string; // uuid v4

export type Domain =
  | "truth-telling"
  | "resource-allocation"
  | "in-group-out-group"
  | "reciprocity-cooperation";

export type Layer = "current_self" | "aspirational_self" | "admired_other";

/**
 * Tag attached to a scenario choice or option.
 * Format: "namespace:value" or single token (legacy).
 * Tags resolve to scoring contributions or metadata stratifiers via
 * analysis/tag_axis_map_v*.csv.
 */
export type Tag = string;

// =============================================================================
// Scenarios — common fields
// =============================================================================

export type ScenarioType =
  | "quick-fire-round"
  | "core-narrative"
  | "cost-of-virtue-probe";

export interface ScenarioMetadata {
  title: string;
  author: string;
  design_intent: string;
  domain_anchor: string;
  estimated_duration_seconds: number;
  content_warnings: string[];
  timer_seconds_per_item?: number; // quick-fire only
}

export interface ScenarioBase {
  id: ScenarioId;
  type: ScenarioType;
  domain: Domain;
  version: string;
  metadata: ScenarioMetadata;
}

// =============================================================================
// Scenario: quick-fire-round
// =============================================================================

export interface QuickFireOption {
  id: OptionId;
  text: string;
  tags: Tag[];
}

export interface QuickFireItem {
  id: ItemId;
  prompt: string;
  options: [QuickFireOption, QuickFireOption]; // binary forced choice
}

export interface QuickFireRound extends ScenarioBase {
  type: "quick-fire-round";
  metadata: ScenarioMetadata & { timer_seconds_per_item: number };
  items: QuickFireItem[];
}

// =============================================================================
// Scenario: core-narrative
// =============================================================================

export interface NarrativeChoice {
  id: OptionId;
  text: string;
  next?: SceneId; // omitted on terminal-leading paths
  tags: Tag[];
}

export interface NarrativeScene {
  id: SceneId;
  text: string;
  choices?: NarrativeChoice[]; // omitted iff terminal
  terminal?: boolean;
  tags?: Tag[]; // present on terminal scenes for resolution coding
}

export interface CoreNarrative extends ScenarioBase {
  type: "core-narrative";
  setup: string;
  scenes: NarrativeScene[];
  reflection_prompt: string;
  domain_signatures_captured: string[];
}

// =============================================================================
// Scenario: cost-of-virtue-probe
// =============================================================================

export interface ProbePreconditions {
  /**
   * Probe surfaces only if user has named this value in their top-5
   * for at least one inventory layer. Can be a single value id or
   * an array of acceptable alternates.
   */
  value_must_be_in_user_top_5_for_at_least_one_layer: ValueId | ValueId[];
  ladder_currency: "user-local" | "USD";
}

export interface LadderRung {
  rung: number; // 1-indexed
  stake: number;
  unit: "USD" | string; // localization-ready
  label: string; // rendered to user
}

export interface ProbeNoOption {
  id: string; // "never" | "always_return" | "always_keep"
  text: string;
}

export interface ProbeAnalysis {
  break_point_field: "first_accept_stake" | "first_return_stake";
  no_break_point_handling: string;
  interpretation_note: string;
  longitudinal_signal: string;
  domain_signature_captured: "cost_of_virtue_curve";
}

export interface CostOfVirtueProbe extends ScenarioBase {
  type: "cost-of-virtue-probe";
  value_slot: ValueId;
  preconditions: ProbePreconditions;
  framing_prompt: string;
  framing_question: string;
  ladder: LadderRung[];
  no_option: ProbeNoOption;
  alternate_no_option?: ProbeNoOption; // present iff inverted probe
  analysis: ProbeAnalysis;
}

// =============================================================================
// Discriminated-union helper
// =============================================================================

export type Scenario = QuickFireRound | CoreNarrative | CostOfVirtueProbe;

// =============================================================================
// Inventory: values deck
// =============================================================================

export interface ValueCard {
  id: ValueId;
  label: string;
  domain: Domain;
  behavioral_anchor: string;
  internal_tensions: ValueId[];
}

export interface ValuesDeck {
  version: string;
  size: number;
  card_sort_protocol: string;
  design_intent: string;
  values: ValueCard[];
}

// =============================================================================
// Inventory: pairwise pairs
// =============================================================================

export interface PairwisePair {
  id: string;
  pair_type: "within-domain" | "cross-domain";
  domain?: Domain; // within-domain pairs only
  left_id: ValueId;
  right_id: ValueId;
  tension_anchor: string;
  prompt: string;
  left_text: string;
  right_text: string;
}

export interface PairwisePairs {
  version: string;
  value_pool_size: number;
  pair_count: number;
  sampling_strategy: string;
  pairs: PairwisePair[];
}

// =============================================================================
// Inventory: three-layer prompts
// =============================================================================

export interface LayerDefinition {
  label: string;
  anchor_phrase: string;
  protocol_note: string;
  ux_pattern?: string;
}

export interface GapAnalysisInterpretation {
  name: string;
  interpretation: string;
}

export interface ThreeLayerPrompts {
  version: string;
  rationale: string;
  layers: Record<Layer, LayerDefinition>;
  gap_analysis: {
    primary_gap: GapAnalysisInterpretation;
    consistency_check: GapAnalysisInterpretation;
    honesty_check: GapAnalysisInterpretation;
  };
  ordering: string;
  presentation_modes: Record<string, string>;
}

// =============================================================================
// Inventory: story prompts
// =============================================================================

export interface StoryPrompt {
  id: string;
  category: string;
  framing: string;
  text: string;
  expected_word_count: string;
  domains_likely_surfaced: (Domain | "any")[];
  follow_up: string | null;
  coding_dimensions: string[];
}

export interface StoryPrompts {
  version: string;
  protocol: string;
  coding_strategy: string;
  design_intent: string;
  prompts: StoryPrompt[];
  ongoing_story_capture: {
    rationale: string;
    rotation_strategy: string;
  };
  what_we_do_not_do: string[];
}

// =============================================================================
// Inventory: relational variant
// =============================================================================

export type RoleCategory =
  | "family"
  | "work"
  | "social"
  | "civic"
  | "tradition";

export interface RoleOption {
  id: string;
  label: string;
  category: RoleCategory;
}

export interface FramingWrapper {
  default_anchor_phrase: string;
  relational_anchor_phrase: string; // contains `{role}` for templating
  card_sort_prompt: string;
  pairwise_prompt: string;
}

export interface StoryPromptOverride {
  default: string;
  relational: string;
}

export interface RelationalVariant {
  version: string;
  status: string;
  rationale: string;
  philosophical_anchor: {
    primary: string;
    supporting: string[];
    literature_note: string;
  };
  role_taxonomy: {
    selection_protocol: string;
    roles: RoleOption[];
    ux_notes: string;
  };
  framing_wrappers: Record<Layer, FramingWrapper>;
  story_prompt_overrides: Record<string, StoryPromptOverride>;
  scoring_implications: {
    summary: string;
    primary_revealed_score: string;
    stated_scores: string;
    gap_calculation: string;
    validation_caveat: string;
  };
  implementation_notes: Record<string, string>;
  open_questions: string[];
}

// =============================================================================
// Session log — runtime data captured per choice
// =============================================================================

export interface SessionLogEntry {
  session_id: SessionId;
  user_id: UserId;
  timestamp_iso: string;
  scenario_id: ScenarioId;
  scenario_type: ScenarioType;
  domain: Domain;
  item_id: ItemId;
  option_id: OptionId;
  tags: Tag[]; // denormalized at log-write time from scenario JSON
  response_time_ms: number;
  presented_position: number;
  was_timeout: boolean;
}

// =============================================================================
// Cost-of-virtue probe response — runtime data
// =============================================================================

export interface ProbeResponse {
  user_id: UserId;
  session_id: SessionId;
  probe_id: ScenarioId; // cov-*-001 id
  domain: Domain;
  value_slot: ValueId;
  first_accept_rung: number | "never";
  first_accept_stake: number | null; // null iff "never"
  is_inverted: boolean;
}

// =============================================================================
// Self-prediction beat — runtime data (H9 self-calibration; scoring.md §14,
// h9-self-calibration.md, DECISIONS §19)
// =============================================================================
//
// Append-only, user-keyed, timestamped log of the "prediction beat": on a
// designated calibration probe the participant records a NON-BINDING prediction
// of their own choice BEFORE resolving it (h9-self-calibration.md §1.1). Each
// entry captures only the prediction; the realized choice is joined afterward on
// `target_scenario_id` (+ `item_id` for a quick-fire item) against the choice
// log — SessionLogEntry for the axis channel, ProbeResponse for the cost-of-
// virtue channel. The analyzer then forms e = pred − rev per §14.
//
// The two channels resolve on DIFFERENT scales and are NEVER pooled (§14.7):
//   channel "axis" → predicted primary-axis choice (tags → [−1,+1], §2.2)
//   channel "cov"  → predicted break-point rung (log-dollar, §4); a predicted
//                    OR realized "never" is right-censored and is NEVER priced
//                    (the §14.1 lock — reported categorically only).
//
// Not yet consumed by the on-device projection (poc-projection.js) — the H9
// personal reveal is a later increment. Field shapes mirror SessionLogEntry
// (denormalized `predicted_tags`, `response_time_ms`, `was_timeout`) and
// ProbeResponse (`predicted_rung`) so the join is a straight scale-share.

export type PredictionChannel = "axis" | "cov";

export interface PredictionLogEntry {
  user_id: UserId;
  session_id: SessionId;
  timestamp_iso: string;
  target_scenario_id: ScenarioId; // the choice this predicts — the join key
  item_id?: ItemId; // present when the target is a quick-fire item
  domain: Domain;
  channel: PredictionChannel;

  // Axis channel: the option the participant predicts they will choose,
  // with its tags denormalized at write-time exactly like SessionLogEntry.tags.
  predicted_option_id?: OptionId;
  predicted_tags?: Tag[];

  // Cost-of-virtue channel: the break-point rung the participant predicts.
  predicted_rung?: number | "never";

  // Counterbalanced reactivity control (§14.6, DECISIONS §19 — mandatory, not
  // optional): on control trials the prediction beat is WITHHELD so downstream
  // scoring can net out the question–behavior effect of predicting. When true,
  // this entry marks a control (no prediction elicited); defaults to false.
  prediction_withheld?: boolean;

  response_time_ms: number;
  was_timeout: boolean;
}

// =============================================================================
// Inventory responses — runtime data
// =============================================================================

export interface CardSortResponse {
  user_id: UserId;
  layer: Layer;
  value_id: ValueId;
  selected: boolean;
  sort_order?: number;
  timestamp_iso: string;
}

export interface PairwiseResponse {
  user_id: UserId;
  layer: Layer;
  pair_id: string;
  left_id: ValueId;
  right_id: ValueId;
  choice: "left" | "right" | "skip";
  response_time_ms: number;
  timestamp_iso: string;
}

export interface StoryResponse {
  user_id: UserId;
  prompt_id: string;
  text: string;
  llm_coded_tags: Array<{
    domain: Domain;
    value_id: ValueId;
    confidence: number; // 0-1
  }>;
  timestamp_iso: string;
}

// =============================================================================
// Derived / analyzer types — per scoring.md
// =============================================================================

export interface PerDomainRevealedScore {
  user_id: UserId;
  domain: Domain;
  primary_axis: string; // e.g. "honesty"
  score: number; // [-1, +1]
  sessions_contributing: number;
  items_contributing: number;
  ci_lower_95: number;
  ci_upper_95: number;
}

export interface PerDomainStatedScore {
  user_id: UserId;
  domain: Domain;
  layer: Layer;
  score: number; // standardized
  source: "card_sort_only" | "pairwise_only" | "combined";
  ci_lower_90: number;
  ci_upper_90: number;
}

export interface GapEstimate {
  user_id: UserId;
  domain: Domain;
  primary_gap: number; // aspirational - revealed, standardized
  consistency_check: number; // admired_other - aspirational
  honesty_check: number; // current - admired_other
  ci_lower_95: number;
  ci_upper_95: number;
}

// =============================================================================
// Compile-time exhaustiveness helper
// =============================================================================

/**
 * Use in `switch (scenario.type)` blocks to enforce that every scenario
 * type is handled. The TypeScript compiler will surface a type error if
 * a new scenario type is added but not handled.
 */
export function assertNever(x: never): never {
  throw new Error(`Unhandled scenario type: ${JSON.stringify(x)}`);
}
