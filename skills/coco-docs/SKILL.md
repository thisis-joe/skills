---
name: coco-docs
description: "Use when writing, updating or auditing documents for other readers: an ADR, README, API reference, guide, runbook, changelog, code comments, agent instructions, a discovery questionnaire, course exercises or an article, or editing such prose without changing meaning."
license: MIT
---

# coco-docs

Produce official documents that their readers can rely on: true at the landing revision, consistent with the project's conventions, and owned by the project rather than by one session.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a document type the project has no convention for (default skeletons), a drift audit, an ADR or glossary change, agent-facing instructions or reusable recipes, an async discovery questionnaire, course-exercise scaffolding, and opt-in writing collaboration (fragments, article shaping, beats). If any applies, read the [documentation procedures](../_coco-shared/advanced/docs.md) before dependent work.

## Boundary

- Public developer blog-post selection, evidence-backed editorial transformation and repository publication preparation belong to [coco-blog](../coco-blog/SKILL.md). General project documentation and other articles stay here.

- The readers are others: teammates, users, operators, API callers, future maintainers or agents. The document lives in the project or is delivered to someone.
- Capturing personal TIL notes from the current session belongs to `coco-til`. When that is the requested output, say so in one line and continue with `coco-til` (invoke it, or read its `SKILL.md`) instead of ending with a pointer. Plain chat explanations need no TIL capture unless requested.
- Do not put learning notes, session narrative or a first-person learning diary into project documents.

## Procedure

1. **Frame.** Name the reader, the task the document must let them finish, the document type and the destination path. Infer these from the request and the repository; ask only when a missing choice changes the artifact. Keep one purpose per document.
2. **Follow conventions.** Before writing, find the existing documentation location, file naming and numbering, headings and templates, style guide, docs tooling and language. Continue them and report a conflict instead of starting a parallel structure. Use the default skeletons only when the project has no convention.
3. **Gather evidence.** Read the code, tests, configuration, command help and decision history the document describes. Every behavior, command, flag, path, default, limit and version must trace to that evidence; mark a claim you cannot trace as unverified or leave it out. When the document describes another component's behavior, such as a skill, command or API, read that component's source in full before drafting, not only the part you expect to cite.
4. **Write** once the evidence is gathered. Lead with what the reader needs first: the result, the command or the definition. Name the actor, put conditions before actions and keep one term per concept. Give working contracts, real runnable examples and the gotchas the reader will hit, at the depth the reader needs. When a rewrite grows substantially, state why each added section serves the reader's task, and link exhaustive tables, option lists or logs instead of copying them. Keep an official voice: no session story, no "new" or "currently" without a version or date, no promotional certainty.
5. **Change only what changed.** Update the sections whose underlying behavior changed and preserve the rest, including user edits. For ADRs keep consequential context, alternatives, decision and consequences, supersede rather than rewrite history, and keep glossary terms separate from implementation decisions. Changelog entries state the user-visible impact. While editing prose, preserve names, numbers and units, conditions, trade-offs and uncertainty.
6. **Comments.** Explain nonobvious intent or constraints. Do not narrate obvious code, and do not delete useful comments wholesale.
7. **Verify.** Run documented commands and examples when it is safe and feasible. Check that relative links, anchors, paths and code symbols exist. Run the project's docs lint or build when it has one. Record which claims were executed, which were only read, and which remain unverified. For a new or substantially rewritten document that states behavior you did not execute, have an independent reviewer, when available, check those claims against their sources; give it the recorded results of executed examples instead of having it re-run them, and reconcile each finding.
8. **Deliver locally** unless the user named a destination and authorized the external write. Documentation does not authorize posting, sending a questionnaire, changing another service or writing production code beyond the request.

## Modes

- **Drift audit:** when asked whether documentation is current, list its checkable claims, compare each with the code or an execution, and report stale, broken and unverifiable items with locations and proposed fixes. Edit only within the requested scope.
- **Agent instructions, questionnaires, course exercises and experimental writing collaboration** follow their sections in the documentation procedures. Agent instructions omit generic guidance the runtime already knows. Course material teaches through observable examples and checks comprehension without imposing unrelated implementation. Mark experimental source methods as optional.

## Return

Changed paths with document type and reader; a verification list of claim, evidence and result (executed, read or unverified); preserved uncertainty; follow-ups such as undocumented behavior or a decision that needs an ADR; and, for a rewrite that grew substantially, why each added section is needed. Never invent rationale.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The code is self-documenting": code shows what, not why, rejected alternatives or constraints.
- "ADRs are overhead": a short record prevents re-arguing a costly decision later.
- Documentation that restates code instead of intent, commented-out code, or long-lived TODOs.
- A public interface without its contract, or a README that does not say how to run the project.
- A documented command, path or example you did not trace to evidence, presented as verified.
