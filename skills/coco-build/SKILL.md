---
name: coco-build
description: "Use when implementing an agreed feature or bug fix, completing one planned task, or executing an authorized sequence. 구현·TDD·작업별 커밋·연속 실행."
license: MIT
---

# coco-build

Own execution from the first ready task through evidence-backed work-unit completion.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/build.md) only when the task needs their additional procedure. The [integration decisions](../_coco-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Read the agreed brief/spec and authoritative task state. Check dependencies, feature branch/base and existing dirty paths. Select one dependency-ready task; continuous mode repeats the same closure standard.
2. Discover actual test/build commands and reuse agreed observable test boundaries. For a behavior change, write one test for the desired behavior, run it and confirm the relevant failure, implement minimal green, and repeat in vertical slices. Static changes use appropriate direct checks.
3. After green, permit only small local cleanup inside the task and recheck it. Structural refactoring is separate scoped work. Avoid implementation-coupled mocks and expected values copied from the implementation.
4. Run required regression/build and actual UI/API/CLI acceptance checks. Obtain scoped review findings. Review includes current unstaged/staged/new files, not just HEAD. Resolve required findings and rerun affected checks; keep unchanged valid evidence.
5. Commit only this task's owned changes and state update on its feature branch. Record the commit and evidence in authoritative status; reconcile a commit that succeeded before an interrupted status update instead of implementing twice.
6. Stop advancement on unresolved required failure, missing material decisions or authorization boundaries; use debug for bounded in-scope diagnosis. Continuous mode resumes at the first incomplete ready task.

Return: task IDs, acceptance/check results, actual review scope, commit IDs, updated status, unresolved items and next ready task. Do not mark unavailable required checks as passed.
