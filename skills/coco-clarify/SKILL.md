---
name: coco-clarify
description: "Use when requirements, terminology, idea viability, scope or important product decisions remain unsettled."
license: MIT
---

# coco-clarify

Reach a shared understanding of the behavior and decisions that matter.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for a missing material decision that needs a focused interview, an open direction that needs divergent ideas, a request to grill or stress-test a plan, decision or idea, and a domain term with conflicting meanings. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/clarify.md) before dependent work.

## Procedure and output

1. Read the request, existing agreement, relevant code and domain vocabulary. Separate discoverable facts from decisions the user must make.
2. Build a decision tree. Ask only questions whose prerequisites are settled; independent questions can share a round. Include the decision, meaningful alternatives and a reasoned recommendation.
3. Use divergent idea exploration only when the direction itself is open; compare options against user goals before converging. Do not re-interview settled acceptance criteria.
4. When a term crystallizes, update the existing glossary if documentation is in scope. Keep implementation decisions out of it. Offer an ADR only for a consequential, surprising trade-off; follow the repository format.
5. Finish when the requested scope has a shared, usable agreement. List genuinely open decisions explicitly. A questionnaire mode can prepare dependency-ordered questions for asynchronous discussion.

Return: agreed behavior, scope, preserved behavior, decisions and acceptance checks; glossary/ADR changes only when needed. Hand off to spec or build according to artifact needs, without automatically publishing or implementing.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The ask is clear enough": if you cannot state the desired outcome in one sentence, it is not.
- "Whatever you think": that is delegation, not a decision; offer concrete options with your recommendation.
- A question without your recommended answer, or a "best practice" question instead of what the user actually wants.
- A vague "sounds good" to a vague restatement: restate outcome and out-of-scope concretely and reconfirm.
- Accepting "scalable", "clean" or "modern" unprobed, yes-machining a weak idea, or converging without surfaced assumptions and a Not Doing list.
