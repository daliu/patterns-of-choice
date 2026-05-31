# Narrative Immersion, Transportation, and Parasocial Attachment

Theoretical anchor for **H8** (`pre-registration.md` §6; design in `h8-narrative-immersion-design.md`; scoring in `scoring.md` §9). H8 claims that narrative-embedding with recurring-character attachment functions as a *measure-debiasing* mechanism against socially-desirable responding (H8a) and as a *stake-grounding* mechanism for attachment-laden high-stakes choices (H8b).

This file collects the literature the claim rests on, and — in the house style of this review — flags where that literature does **not** straightforwardly support the claim.

## Narrative transportation

- **Green, M. C., & Brock, T. C. (2000).** *The role of transportation in the persuasiveness of public narratives.* JPSP, 79(5), 701–721. — Defines transportation as absorption into a narrative (attention, imagery, emotion) and introduces the 11-item Transportation Scale. Higher transportation → greater story-consistent belief change and reduced detection of false notes in the text.
- **Green, M. C., & Brock, T. C. (2002).** *In the mind's eye: Transportation-imagery model of narrative persuasion.* In Green, Strange, & Brock (Eds.), *Narrative Impact.* — The mechanism statement: transportation reduces counterarguing and increases the felt realism of narrated events.
- **Appel, M., Gnambs, T., Richter, T., & Green, M. C. (2015).** *The Transportation Scale–Short Form (TS–SF).* Media Psychology, 18(2), 243–266. — Validated 6-item short form; the practical instrument for repeated in-protocol administration.
- **Van Laer, T., de Ruyter, K., Visconti, L. M., & Wetzels, M. (2014).** *The extended transportation-imagery model: A meta-analysis of the antecedents and consequences of consumers' narrative transportation.* Journal of Consumer Research, 40(5), 797–817. — Meta-analytic confirmation that transportation reliably moves attitudes/intentions, with identifiable story and reader moderators.

**Synthesis.** Transportation is a well-measured, meta-analytically supported construct. The mechanism most relevant to H8a — *transportation reduces counterarguing and self-referential editing* — is the same mechanism that, in persuasion, makes transported readers more open to a story's message. H8a's bet is that when there is no message to absorb, only a choice to make, that same lowered self-monitoring surfaces a less curated (less socially-desirable) response.

**Relevance to H8 / direction of the effect.** This is the load-bearing assumption and it is *not* directly established. The entire transportation literature studies persuasion — moving a person toward an attitude the narrative endorses — not measurement fidelity. Repurposing it for debiasing is the novel contribution and the central risk: the very lowering of self-monitoring could equally *introduce* bias (demand characteristics from a sympathetic narrator, story-congruent answering) rather than remove it. H8a is the test that adjudicates this; it is not assumed.

## Entertainment-Education and overcoming resistance (the H8a mechanism)

- **Slater, M. D., & Rouner, D. (2002).** *Entertainment-education and elaboration likelihood: Understanding the processing of narrative persuasion.* Communication Theory, 12(2), 173–191. — The Extended ELM: absorption and identification suppress the message-scrutiny that would otherwise trigger resistance.
- **Moyer-Gusé, E. (2008).** *Toward a theory of entertainment persuasion: Explaining the persuasive effects of entertainment-education messages.* Communication Theory, 18(3), 407–425. — The Entertainment Overcoming Resistance Model (EORM): narrative engagement and parasocial bonds specifically reduce reactance, counterarguing, and **the perceived need to self-present**. The closest existing theoretical statement to H8a.
- **Hinyard, L. J., & Kreuter, M. W. (2007).** *Using narrative communication as a tool for health behavior change: A conceptual, theoretical, and empirical overview.* Health Education & Behavior, 34(5), 777–792. — Reviews narrative's behavior-change advantage over didactic framing in applied settings.

**Relevance to H8.** EORM is the most direct precedent: it names *reduced self-presentation pressure* as a downstream consequence of narrative engagement and parasocial bonding. H8a is, in effect, EORM's "reduced self-presentation" prediction lifted out of the persuasion frame and treated as measurement-quality improvement. Worth stating plainly that EORM was built to explain why entertainment-education *changes* people, so borrowing it as evidence for *measuring* people is an analogical move, not a citation of settled result.

## Parasocial interaction and relationships (the H8b construct)

- **Horton, D., & Wohl, R. R. (1956).** *Mass communication and para-social interaction.* Psychiatry, 19(3), 215–229. — Originates parasocial interaction: the one-sided sense of relationship a viewer forms with a media figure.
- **Rubin, A. M., Perse, E. M., & Powell, R. A. (1985).** *Loneliness, parasocial interaction, and local television news viewing.* Human Communication Research, 12(2), 155–180. — The widely-used PSI scale.
- **Tukachinsky, R. (2010).** *Para-romantic love and para-friendships: Development and assessment of a multiple-parasocial relationships scale (MPRS).* American Journal of Media Psychology, 3, 73–94. — The PSR scale H8b adapts; distinguishes para-friendship from para-romantic dimensions, supporting per-character measurement.
- **Cohen, J. (2001).** *Defining identification: A theoretical look at the identification of audiences with media characters.* Mass Communication & Society, 4(3), 245–264. — Separates *identification* (becoming the character) from *parasocial relationship* (relating to the character as other). H8b's "welfare of a character you've come to know" is a PSR construct, not identification — the distinction matters for which scale is correct.

**Relevance to H8.** H8b's `attachment_strength` (`scoring.md` §9.3) operationalizes exactly this: a Tukachinsky-derived self-report per recurring NPC, paired with a behavioral latency proxy. Measuring per-character (not globally) is consistent with the MPRS's multiple-relationships structure and with the dual-mode design (`h8-narrative-immersion-design.md` Q2/Q4).

**Critical caveat (house-style flag).**
- **Dibble, J. L., Hartmann, T., & Rosaen, S. F. (2016).** *Parasocial interaction and parasocial relationship: Conceptual clarification and a critical assessment of measures.* Human Communication Research, 42(1), 21–44. — Shows that the most-used PSI/PSR scales conflate the two constructs and have shaky discriminant validity. **Implication for H8b:** the attachment instrument must be pinned to PSR (enduring cross-session bond), not PSI (in-the-moment interaction), or `attachment_strength` will be measuring the wrong thing. The pilot's attachment-instrument calibration step (`pilot-protocol.md`) should include a discriminant check, not just reliability.

## Social-desirability responding (the threat H8a addresses)

- **Crowne, D. P., & Marlowe, D. (1960).** *A new scale of social desirability independent of psychopathology.* Journal of Consulting Psychology, 24(4), 349–354. — The Marlowe-Crowne scale; the classic operationalization of the threat.
- **Paulhus, D. L. (1984).** *Two-component models of socially desirable responding.* JPSP, 46(3), 598–609. — Separates *impression management* (deliberate, audience-facing) from *self-deceptive enhancement* (honest but inflated self-view) — the BIDR. The distinction is decisive for H8.

**Relevance to H8 — which component narrative can plausibly touch.** Narrative immersion can credibly reduce *impression management*: lowered self-monitoring under transportation means less audience-facing editing. It is far less plausible that narrative touches *self-deceptive enhancement* — if a participant genuinely believes they are more honest than they act, no amount of story dissolves that, because there is no deliberate editing to suppress. H8a should therefore be read as a claim about the impression-management component specifically. This is a sharper, more falsifiable, and more honest framing than "narrative reduces social-desirability bias" wholesale, and it predicts the ceiling on the H8a effect size (hence the deliberately modest lower-CI threshold of 0.15 in `scoring.md` §9.2).

## What's missing / open lines

- **No measurement-context precedent.** Every source here studies narrative as an *intervention* (persuasion, education, behavior change). H8's use of narrative as *instrumentation* appears genuinely novel — which is the contribution, but means there is no prior effect size to power against. The n=200 thresholds are directional, not benchmarked.
- **Demand-characteristic confound.** A sympathetic recurring character may induce story-congruent answering (a demand effect) that mimics debiasing. The paired narrative-vs-abstract within-subject design (`scoring.md` §9) partially controls this, but an exploratory check for character-valence effects (does attachment to a *virtuous* NPC shift answers differently than attachment to a morally-flawed one?) should be pre-registered as exploratory.
- **Latency-as-attachment is unvalidated.** The behavioral channel in §9.3 (increasing RT-gap on NPC-mentioning items) is a plausible but unestablished proxy. Treat self-report as primary until the pilot shows the two channels converge.
- **Transportation-scale administration burden.** TS–SF is 6 items; administering it per arc across a 4-week protocol adds up. Pilot should confirm it doesn't itself break immersion (measurement-reactivity).

## Cross-references

- [`h8-narrative-immersion-design.md`](../h8-narrative-immersion-design.md) — the hypothesis, instrument modifications, and resolved design questions
- [`scoring.md`](../scoring.md) §9 — operationalization of `D_i^p` and `attachment_strength`
- [`validity-threats.md`](../validity-threats.md) §CV-1 — the social-desirability threat H8a proposes to mitigate
- [`measurement.md`](measurement.md) — HEXACO honesty-humility (H2 convergent anchor) and forced-choice IRT
- [`ecological-validity.md`](ecological-validity.md) — the lab-vs-life gap H8b's stake-grounding speaks to
