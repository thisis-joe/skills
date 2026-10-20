---
name: coco-document
description: "Use when recording an ADR, documenting APIs or agent guidance, explaining technical material, teaching, preparing exercises or editing prose without changing meaning."
license: MIT
---

# coco-document

Create the artifact the audience needs while preserving technical truth.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for an ADR or glossary change, agent-facing instructions or reusable recipes, an async discovery questionnaire, teaching or an opt-in multi-session learning workspace, course-exercise scaffolding, and opt-in writing collaboration (fragments, article shaping, beats). If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/document.md) before dependent work.

## Procedure and output

1. Identify audience, purpose, authoritative facts and established format. Read the code/decision evidence before explaining it.
2. For ADRs, retain consequential context, alternatives, decision and consequences; reuse location/numbering/headings and supersede rather than erase history. Keep glossary terms separate from implementation decisions.
3. For API/README/runbook/agent instructions, provide working contracts, commands, examples and gotchas at the level the reader needs. Verify paths/links/commands; avoid generic instructions already known to the runtime.
4. For teaching, questionnaires, exercises, writing-shape/fragments/beats or prose revision use the advanced mode. Mark experimental source methods as optional. Teach through observable examples and check comprehension without imposing unrelated implementation.
5. During editing preserve names, numbers/units, conditions, trade-offs and uncertainty. Explain necessary why; avoid comments that merely narrate obvious code or blanket deletion of useful comments.
6. Deliver locally unless the user requested a destination and external write. Documentation does not authorize posting, modifying another service or generating production code outside the request.

Return: requested artifact, substantiated examples and any evidence gaps; no invented rationale.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The code is self-documenting": code shows what, not why, rejected alternatives or constraints.
- "ADRs are overhead": a short record prevents re-arguing a costly decision later.
- Documentation that restates code instead of intent, commented-out code, or long-lived TODOs.
- A public interface without its contract, or a README that does not say how to run the project.
