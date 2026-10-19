---
name: coco-plan
description: "Use when a spec or clear brief needs dependency-ordered tasks, verifiable slices, ticket publication, or execution checkpoints. 계획·작업 분해·티켓."
license: MIT
---

# coco-plan

Turn the contract into small verifiable units with unambiguous ownership.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/plan.md) only when the task needs their additional procedure.

## Procedure and output

1. Read the spec and actual code/dependencies. Reuse a sufficient existing plan; never overwrite another unfinished effort.
2. Define vertical behavior slices, each with stable ID, acceptance, verification, genuine blockers, expected scope and risk. Order the dependency-ready frontier rather than forcing a false linear chain.
3. Put prerequisite prefactoring before dependent behavior. A wide mechanical refactor may need expand–migrate–contract; use the explicit integration-only exception rather than falsely promising every intermediate commit is shippable.
4. Keep one authoritative task-state target. A plan may index external issue IDs; it must not duplicate their mutable status. Match the designated tracker/local-file convention.
5. Plan focused loop checks, task closure checks and meaningful integration/risk checkpoints. Task size is judged by comprehensible scope, not a universal file count.
6. State single-task or continuous execution and preserve approval already given. Surface new material decisions and task-state conflicts; publish tickets only within the authorized destination/scope.

Return: task graph, acceptance and verification per task, risk/rollback checkpoints, plan reference and authoritative state location.
