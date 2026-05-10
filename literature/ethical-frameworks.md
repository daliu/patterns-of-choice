# Ethical Frameworks: The Meta-Question of Whose Framework

Concept doc explicitly acknowledges "smuggled value claims in the taxonomy." This file surveys the philosophical literature relevant to that meta-question.

## Virtue ethics (Aristotelian / neo-Aristotelian)

- **Aristotle.** *Nicomachean Ethics.* (c. 350 BCE) — Foundational text. Virtue as a stable disposition (*hexis*) cultivated through habituation toward the mean between extremes; *phronesis* (practical wisdom) as integrative.
- **MacIntyre, A. (1981).** *After Virtue.* Notre Dame UP. — Argues that modern ethics is incoherent absent a teleological framework; calls for return to virtue ethics within "tradition-constituted" practices. Important for the question of whether a free-floating, secular, individual-user values practice (which character-lab is) can coherently support virtue formation at all — MacIntyre's answer is largely no.
- **Annas, J. (2011).** *Intelligent Virtue.* Oxford UP. — Virtue as skill; emphasizes that habituation in the Aristotelian sense is *intelligent practice*, not rote routine. Each virtue exercise should be a fresh judgment, not a reflex.
- **Hursthouse, R. (1999).** *On Virtue Ethics.* Oxford UP. — Canonical contemporary statement; "right action is what a virtuous person would characteristically do."

**Concept-doc relevance — important:** Concept doc's intervention layer (especially identity-anchored, repeated-practice framings) maps onto Aristotelian habituation. Annas's emphasis that virtue-as-skill requires *intelligent* practice (not routine) is directly relevant to the anti-pattern "don't gamify the values themselves." The character-lab system that varies scenarios, requires fresh judgment, and refuses to teach "the right answer" is consistent with Annas-style intelligent habituation.

**MacIntyre challenge:** The doc's individualist, secular, optional framing is precisely what MacIntyre argued is *insufficient* for virtue formation — he requires tradition-constituted communities. Character-lab cannot answer this challenge fully but should not pretend the challenge doesn't exist. Worth a sentence in the "smuggled values" section acknowledging that the very form of an individual app for personal moral self-cultivation is itself a (modern, liberal, individualist) ethical commitment.

## Deontology

- **Kant, I.** *Groundwork of the Metaphysics of Morals* (1785). — Foundational: morality as rule-following derivable from rationality; categorical imperative.
- **Korsgaard, C. M. (1996).** *The Sources of Normativity.* Cambridge UP. — Most influential contemporary Kantian.
- **Scanlon, T. M. (1998).** *What We Owe to Each Other.* Harvard UP. — Contractualism; what is wrong is what cannot be justified to others.

**Concept-doc relevance:** Deontological framings tend to favor stated-values measurement over revealed-behavior — what matters is the principle, not the outcome. Character-lab's revealed/stated *gap* is interesting from a Kantian view because it surfaces hypocrisy (claimed principle, contradicted action). The doc is implicitly compatible with deontology but not derived from it.

## Consequentialism / utilitarianism

- **Mill, J. S.** *Utilitarianism* (1863).
- **Singer, P. (1972).** *Famine, affluence, and morality.* Philosophy and Public Affairs.
- **Parfit, D. (1984).** *Reasons and Persons.* Oxford UP.

**Concept-doc relevance:** The doc's "harm tradeoffs" domain and cost-of-virtue paradigm are most natural in a consequentialist frame: outcomes are units that can be weighed. But the doc explicitly resists telling users *which framework* is right. The taxonomy's allocation domain (resource allocation) embeds a utilitarian-friendly default (more good = better) that should be flagged as not framework-neutral.

## Care ethics and feminist ethics

- **Gilligan, C. (1982).** *In a Different Voice.* Harvard UP. — Care vs. justice frame; argues Kohlberg-style stage models systematically undervalued relational moral reasoning.
- **Held, V. (2006).** *The Ethics of Care.* Oxford UP. — Canonical contemporary statement.
- **Noddings, N. (1984).** *Caring.* University of California Press.

**Concept-doc relevance:** Care-ethics is relevant for the "in-group vs out-group" domain — care ethics rejects the impartialist framing that the gradient measure presumes. A user with strongly relational ethics may rationally weight kin over stranger and this is not a moral failure under care ethics. The concept doc's "in-group vs out-group" framing is closer to a Singerian impartialist baseline than it acknowledges.

## Confucian / role ethics

- **Ames, R. T. (2011).** *Confucian Role Ethics: A Vocabulary.* University of Hawaii Press. — Argues Confucian ethics is fundamentally role-based, not virtue-as-individual-quality. Different ontology of the self.
- **Slingerland, E. (2014).** *Trying Not to Try.* Crown. — Wuwei / spontaneity in Confucian and Daoist ethics; *de* as efficacious virtue.

**Concept-doc relevance:** A non-trivial portion of character-lab's potential global user base (East Asian, including the user's own ancestry per CLAUDE.md notes) operates implicitly from role-ethics rather than virtue-as-personal-quality. The concept doc's identity-anchoring ("I am someone who...") may translate awkwardly. The Confucian alternative would be relational-role anchoring ("As a daughter / colleague / friend, I am someone who...").

## Moral particularism vs. generalism

- **Dancy, J. (2004).** *Ethics Without Principles.* Oxford UP. — Moral particularism: features that are reasons in one context need not be reasons (or may be opposite-valenced reasons) in another.

**Concept-doc relevance:** The concept doc's "Consistency under reframing" signature implicitly assumes a generalist view (the same principle should apply across reframings). A particularist would dispute that this is even a *failure mode* — they would argue contextual sensitivity is *what moral judgment is*. This is a real philosophical objection to the consistency signature. Doesn't undermine the design but should be acknowledged as one philosophical position character-lab is implicitly taking.

## Implications for character-lab's taxonomy choices

Concept doc names "multiple selectable preset taxonomies (Haidt / Schwartz / Aristotelian / religious / secular humanist)" as a mitigation. Reasonable. Some practical notes:

- The **Aristotelian preset** is well-defined (NE Book II–VI) but requires translation work; few existing instruments operationalize it. Annas (2011) and Curzer (2012) are good starting points.
- The **Schwartz preset** is empirically well-validated (PVQ-RR across 49 cultures) but is value-theoretic, not virtue-theoretic — it captures *what people care about*, not *who they are aiming to become*.
- The **Haidt preset** (MFQ-2) is empirically well-validated but politically loaded in WEIRD contexts (the binding/individualizing split tracks political ideology in the U.S.); using it requires care to avoid framing the product as politically partisan.
- The **religious presets** would require denomination-specific work; Christian / Jewish / Buddhist / Hindu / Islamic / Confucian each have distinct virtue / value taxonomies. Concept doc's "religious and secular variants" is the right gesture but is non-trivial.

## What's missing from concept doc

- Acknowledgment that the *form* of the product (individual, optional, secular) is itself an ethical position (MacIntyre challenge).
- Explicit position on the moral-particularism critique of the consistency signature.
- The role-ethics alternative as an identity-anchoring framing (not just "I am X" but "as X-role, I am Y").
