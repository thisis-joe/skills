---
name: coco-clarify
description: "Use when requirements, terminology, idea viability, scope or important product decisions remain unsettled, or when the user wants a plan, decision or idea grilled or stress-tested."
license: MIT
---

# coco-clarify

Reach a shared understanding of the behavior and decisions that matter. For a vague unnamed feature, announce this requirements step and start questions; static edits bypass it.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a missing material decision that needs a focused interview, an open direction that needs divergent ideas, a request to grill or stress-test a plan, decision or idea (grill mode), and a domain term with conflicting meanings. If any applies, read the [advanced modes](../_coco-shared/advanced/clarify.md) before dependent work.

## Procedure and output

1. Read the request, existing agreement, relevant code and domain vocabulary. Apply the [material-choice check](../_coco-shared/workflow.md#questions-delegation-and-reports) to concrete input/output: recover settled answers before asking about public results that remain undecided. Separate discoverable facts from decisions the user must make.
2. Build a decision tree. Ask only questions whose prerequisites are settled; independent questions can share a round. Include a concrete situation, understandable alternatives, their behavioral/cost effects and a reasoned recommendation. When the user asks to grill or stress-test, use [grill mode](../_coco-shared/advanced/clarify.md#grill-mode): ask the whole ready frontier each round, numbered and worded so "yes" accepts your recommendation, until the frontier is empty and the user confirms.
3. Use divergent idea exploration only when the direction itself is open; compare options against user goals before converging. Do not re-interview settled acceptance criteria.
4. When a term crystallizes, update the existing glossary if documentation is in scope. Keep implementation decisions out of it. Offer an ADR only for a consequential, surprising trade-off; follow the repository format.
5. Once behavior and failure handling are usable, preview further useful questions with recommended values and effects. Offer more questioning or adoption of those displayed recommendations and the next step. Delegation approves shown defaults, not unknown material choices. Finish when the requested scope has a shared, usable agreement. List genuinely open decisions explicitly. A questionnaire mode can prepare dependency-ordered questions for asynchronous discussion.

Return: agreed behavior, scope, preserved behavior, decisions and acceptance checks; glossary/ADR changes only when needed. For behavior work hand off to saved spec and plan before build, using the [manual/spec-local automatic transition](../_coco-shared/workflow.md). Explanation-only work ends here; do not publish or implement beyond the request.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The ask is clear enough": if you cannot state the desired outcome in one sentence, it is not.
- "Whatever you think" without displayed defaults: offer concrete recommendations and effects; delegation can then accept them.
- A question without your recommended answer, or a "best practice" question instead of what the user actually wants.
- A vague "sounds good" to a vague restatement: restate outcome and out-of-scope concretely and reconfirm.
- Accepting "scalable", "clean" or "modern" unprobed, yes-machining a weak idea, or converging without surfaced assumptions and a Not Doing list.
