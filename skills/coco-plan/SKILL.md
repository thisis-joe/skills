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

Before passing planning evidence to build, classify the task by its requested behavior and count its implementation files or modules. Omit the implementation note for changes to existing behavior, regardless of how many files they touch, and for new capabilities implemented in a single file or module. Tests and other verification-only files do not count. For an eligible new capability, add a brief implementation note to the saved plan. Use up to three bullets with relevant repo-relative paths, exact symbols, and verification evidence already confirmed during planning. Name the test or check and give its observed result if run. Include the known source revision when a pointer or result depends on it. Omit the note if planning found no useful evidence. Pass these discoveries only in the note. Keep the usual expected scope, acceptance and planned checks for every task. Skip extra investigation solely to fill the note.

Return: task graph, acceptance and verification per task, risk/rollback checkpoints, plan reference and authoritative state location.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "The tasks are obvious" or "I can hold it in my head": write them; written plans survive sessions and compaction.
- "The old plan is stale, I'll replace it": unchecked tasks may be in flight elsewhere; stop and ask.
- Tasks without acceptance or verification, or no checkpoints between them.
- Task status kept in a local file while an external tracker is designated, or split across both.
- Every task oversized, or dependency order never considered.
