---
name: lets-document
description: "Use when recording an ADR, documenting APIs or agent guidance, explaining technical material, teaching, preparing exercises or editing prose without changing meaning. 문서·설명·교육·글쓰기."
license: MIT
---

# let's-document

Create the artifact the audience needs while preserving technical truth.

Read the [common contract](../_lets-shared/contracts.md) before acting. Load [advanced modes](../_lets-shared/advanced/document.md) only when the task needs their additional procedure. The [integration decisions](../_lets-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Identify audience, purpose, authoritative facts and established format. Read the code/decision evidence before explaining it.
2. For ADRs, retain consequential context, alternatives, decision and consequences; reuse location/numbering/headings and supersede rather than erase history. Keep glossary terms separate from implementation decisions.
3. For API/README/runbook/agent instructions, provide working contracts, commands, examples and gotchas at the level the reader needs. Verify paths/links/commands; avoid generic instructions already known to the runtime.
4. For teaching, questionnaires, exercises, writing-shape/fragments/beats or prose revision use the advanced mode. Mark experimental source methods as optional. Teach through observable examples and check comprehension without imposing unrelated implementation.
5. During editing preserve names, numbers/units, conditions, trade-offs and uncertainty. Explain necessary why; avoid comments that merely narrate obvious code or blanket deletion of useful comments.
6. Deliver locally unless the user requested a destination and external write. Documentation does not authorize posting, modifying another service or generating production code outside the request.

Return: requested artifact, substantiated examples and any evidence gaps; no invented rationale.
