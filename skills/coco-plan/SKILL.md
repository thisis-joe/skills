---
name: coco-plan
description: "Use when a spec or clear brief needs dependency-ordered tasks, verifiable slices, ticket publication, or execution checkpoints."
license: MIT
---

# coco-plan

**Contents:** [Procedure and output](#procedure-and-output) · [Stop signals](#stop-signals)

Turn the contract into small verifiable units with unambiguous ownership. Every behavior change needs a saved plan before code; a small task can be one item with acceptance/check. Apply the [transition contract](../_coco-shared/workflow.md) before another skill.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for tracker publication or its recovery, a wide mechanical migration across callers, whole-spec integration or concurrent workers, a huge unclear effort that needs a decision map, and unfamiliar work that needs a bespoke investigation plan. If any applies, read the [advanced modes](../_coco-shared/advanced/plan.md) before dependent work.

## Procedure and output

1. Read the spec and actual code/dependencies. Reuse a sufficient existing plan; never overwrite another unfinished effort.
2. Define vertical behavior slices, each with stable ID, acceptance, verification, genuine blockers, expected scope and risk. Order the dependency-ready frontier rather than forcing a false linear chain.
3. Put prerequisite prefactoring before dependent behavior. A wide mechanical refactor may need expand–migrate–contract; use the explicit integration-only exception rather than falsely promising every intermediate commit is shippable.
4. Keep one authoritative task-state target. A plan may index external issue IDs; it must not duplicate their mutable status. Match the designated tracker/local-file convention.
5. Plan focused loop checks, task closure checks and meaningful integration/risk checkpoints. Task size is judged by comprehensible scope, not a universal file count.
6. State single-task or continuous execution and preserve approval already given. Surface new material decisions and task-state conflicts; publish tickets only within the authorized destination/scope using the [publication protocol](../_coco-shared/advanced/plan.md#tracker-publication-and-recovery).

Classify the task by its requested behavior and count its implementation files or modules. Only a new capability spanning multiple implementation files or modules qualifies for an implementation note. Tests and other verification-only files do not count.

- **All tasks:** Keep expected scope, acceptance criteria and planned checks. Write planned checks as actions to perform, with expected behavior where useful. Add a prior check to that list only if the task independently needs it.
- **Eligible tasks:** Add up to three bullets in an implementation note with useful confirmed paths, exact symbols and verification evidence. For a check already run, record its name and observed result. Include the known revision when a pointer or result depends on it. Keep those observations inside the note. Check the rest of the plan for copies, including its summary and verification steps. Omit the note if no useful evidence exists, and skip extra investigation solely to fill it.
- **Other tasks:** Leave the note and the planning discoveries out of the entire plan, including context, summaries, verification and the final handoff. Leave out prior check commands, outputs and revision details carried only to document those checks, even when explaining an omission. Keep file or symbol names needed to specify the work and checks the implementer must run. Before returning the plan, scan it for copied planning receipts and remove them.

Return: task graph, acceptance and verification per task, risk/rollback checkpoints, plan reference and authoritative state location.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The tasks are obvious" or "I can hold it in my head": write them; written plans survive sessions and compaction.
- "The old plan is stale, I'll replace it": unchecked tasks may be in flight elsewhere; stop and ask.
- Tasks without acceptance or verification, or no checkpoints between them.
- Task status kept in a local file while an external tracker is designated, or split across both.
- Every task oversized, or dependency order never considered.
