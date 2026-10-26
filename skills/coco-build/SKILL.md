---
name: coco-build
description: "Use when implementing an agreed feature or bug fix, completing one planned task, or executing an authorized sequence."
license: MIT
---

# coco-build

Implement tested work-unit commits, then hand off to formal review through the [staged workflow](../_coco-shared/workflow.md).

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for resuming interrupted work or reconciling a commit missing from task state, strengthened work (uncertain contracts, irreversible effects, shared state or high blast radius), a new domain data or state shape, repeatable mechanical edits or migrations, a TypeScript surface, concurrent or delegated execution, and continuous multi-task execution. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/build.md) before dependent work.

## Feature branch preparation

Before implementation, read project instructions (including AGENTS.md and CLAUDE.md), confirm branch/base and preserve dirty paths. Follow actual project naming rules. Without one use a descriptive feature branch and atomic commits; Jira is not required. Only when the project/team explicitly selects this Jira convention, apply it, including during continuous execution:

```text
type(part)/task-number-exact-summary
feat(be)/123-OAuth2.0_Google
```

- **Type and part:** derive the work type and area from repository rules, the task, and the user request. Do not hardcode the example's `feat` or `be`.
- **Task number:** use the linked Jira task's numeric portion: `TEAM-123` becomes `123`. Retain the full key in the work record to distinguish tasks.
- **Exact summary:** copy that Jira task's Summary/title exactly. Do not substitute the parent epic title or an invented summary from its description. Preserve Korean or other languages, case, punctuation, and underscores; do not translate, abbreviate, or make an English slug. The example task's Summary is `OAuth2.0_Google`.

When that Jira convention applies, reuse ticket details already supplied or retrieve them through an available Jira reader. Do not ask again for settled information. Ask only for required task number, Summary, type, or part that cannot be established; never invent a number or Summary.

Validate the complete candidate with `git check-ref-format --branch`. If the Jira Summary includes spaces or other Git-invalid characters, present the original and the minimum necessary transformation and confirm the spelling with the user. Do not silently replace spaces with underscores or remove characters. Safely quote the complete branch name as one shell argument, including parentheses and non-ASCII text.

Create the valid branch from the confirmed base commit. If it exists, verify it belongs to the same task and is suitable for reuse; never overwrite an unrelated branch. When resuming a suitable same-task branch, keep it unless it conflicts with an actually selected project naming rule; only then explain the conflict and confirm how to proceed. Do not require a Jira-shaped name in a non-Jira project or automatically rename, delete, or reset a branch. Preserve existing user changes and record branch/base, plus Jira key and original Summary only when applicable.

## Procedure and output

1. Read the saved spec and plan before behavior additions/changes; reuse adequate project files or create the brief feature-scoped pair in the shared workflow. Static edits need no pair. Read authoritative task state. Check dependencies and existing dirty paths, then complete the branch preparation above before implementation. Select one dependency-ready task. Before writing its behavioral test or code, apply the [material-choice check](../_coco-shared/workflow.md#questions-delegation-and-reports): recover recorded answers, and check actual input/output for unresolved identity, collision or output choices that affect this slice. Ask only missing material choices; keep dependent behavior pending when unanswered. Continuous mode repeats the same closure standard.
2. Discover actual test/build commands and reuse agreed observable test boundaries. For a behavior change, write one test for the desired behavior, run it and confirm the relevant failure, implement minimal green, and repeat in vertical slices. Run the slice's test file in the loop and the full suite once at closure. Keep tests fast: lower deliberate costs such as hash rounds, sleeps and timeouts through a parameter, keeping one check of the production value. Static changes use appropriate direct checks. If implementation or verification reveals a constraint that would change agreed behavior, reapply the workflow's material-choice check before adopting a new limit or fallback.
3. After green, permit only small local cleanup inside the task and recheck it. Structural refactoring is separate scoped work. Avoid implementation-coupled mocks and expected values copied from the implementation.
4. Run required regression/build checks and the actual UI/API/CLI path; retain discriminating input/output. A feature that never takes effect on default or real input is unmet. Self-inspect the whole actual task diff for correctness, boundary safety and test sensitivity. Strengthened work and dependency/shared-contract changes still apply the [review modes](../_coco-shared/advanced/review.md) and freeze scope with the [review-scope collector](../_coco-shared/tools/review_scope.py); this is not independent formal review. Resolve implementation defects and rerun affected checks. If no adequate automated seam exists, retain an executable reproduction and explain the gap.
5. Commit only this task's owned changes and state update on its feature branch. Record the commit and evidence in authoritative status; reconcile a commit that succeeded before an interrupted status update instead of implementing twice.
6. Report implementation complete/review pending with the commit. Before switching to coco-review or coco-verify apply the manual/spec-local automatic transition in the shared workflow. A newly recommended specialist needs selection. Formal findings return here for follow-up commits. Stop advancement on unresolved required failure, missing material decisions or authorization boundaries; use debug for bounded in-scope diagnosis. Continuous mode resumes at the first incomplete ready task.

Return: current stage, task IDs, checks, self-inspected scope, commit IDs, formal review pending/completed, original expected/actual design and departure reason/effect (including superseding choices), unresolved items and next ready task. The design comparison is mandatory, including no material departure. Omit only inapplicable fields such as tracker task IDs. Do not mark unavailable required checks as passed.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "I'll test it all at the end" or a large batch written without running a check: verify each slice; an early bug makes later slices wrong.
- A new test that passes on its first run: it may not test what you think; see it fail for the intended reason, checking all such tests in one scratch run at closure.
- "All tests pass" with no observed run, or a default command such as `npm test` the repository does not use.
- "This refactor is small enough to include": mixed refactor and feature changes are harder to review and revert.
- An abstraction or new utility file before a real repeated use demands it.
