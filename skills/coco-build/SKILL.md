---
name: coco-build
description: "Use when implementing an agreed feature or bug fix, completing one planned task, or executing an authorized sequence."
license: MIT
---

# coco-build

Own execution from the first ready task through evidence-backed work-unit completion.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for resuming interrupted work or reconciling a commit missing from task state, strengthened work (uncertain contracts, irreversible effects, shared state or high blast radius), a new domain data or state shape, repeatable mechanical edits or migrations, a TypeScript surface, concurrent or delegated execution, and continuous multi-task execution. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/build.md) before dependent work.

## Feature branch preparation

Before implementation, confirm the working branch and base commit. Use this team format for each new feature branch, including during continuous execution:

```text
type(part)/task-number-exact-summary
feat(be)/123-OAuth2.0_Google
```

- **Type and part:** derive the work type and area from repository rules, the task, and the user request. Do not hardcode the example's `feat` or `be`.
- **Task number:** use the linked Jira task's numeric portion: `TEAM-123` becomes `123`. Retain the full key in the work record to distinguish tasks.
- **Exact summary:** copy that Jira task's Summary/title exactly. Do not substitute the parent epic title or an invented summary from its description. Preserve Korean or other languages, case, punctuation, and underscores; do not translate, abbreviate, or make an English slug. The example task's Summary is `OAuth2.0_Google`.

Reuse ticket details already supplied or retrieve them through an available Jira reader. Do not ask again for settled information. Ask only for required task number, Summary, type, or part that cannot be established; never invent a number or Summary.

Validate the complete candidate with `git check-ref-format --branch`. If the Jira Summary includes spaces or other Git-invalid characters, present the original and the minimum necessary transformation and confirm the spelling with the user. Do not silently replace spaces with underscores or remove characters. Safely quote the complete branch name as one shell argument, including parentheses and non-ASCII text.

Create the valid branch from the confirmed base commit. If it exists, verify it belongs to the same task and is suitable for reuse; never overwrite an unrelated branch. When resuming a same-task branch whose name differs from this format, explain the difference and confirm how to proceed; do not automatically rename, delete, or reset it. Preserve existing user changes and record the final branch, base commit, Jira key, and original Summary.

## Procedure and output

1. Read the agreed brief/spec and authoritative task state. Check dependencies and existing dirty paths, then complete the branch preparation above before implementation. Select one dependency-ready task; continuous mode repeats the same closure standard.
2. Discover actual test/build commands and reuse agreed observable test boundaries. For a behavior change, write one test for the desired behavior, run it and confirm the relevant failure, implement minimal green, and repeat in vertical slices. Static changes use appropriate direct checks.
3. After green, permit only small local cleanup inside the task and recheck it. Structural refactoring is separate scoped work. Avoid implementation-coupled mocks and expected values copied from the implementation.
4. Run required regression/build and actual UI/API/CLI acceptance checks. Obtain scoped review findings. Review includes current unstaged/staged/new files, not just HEAD. Resolve required findings and rerun affected checks; keep unchanged valid evidence.
5. Commit only this task's owned changes and state update on its feature branch. Record the commit and evidence in authoritative status; reconcile a commit that succeeded before an interrupted status update instead of implementing twice.
6. Stop advancement on unresolved required failure, missing material decisions or authorization boundaries; use debug for bounded in-scope diagnosis. Continuous mode resumes at the first incomplete ready task.

Return: task IDs, acceptance/check results, actual review scope, commit IDs, updated status, unresolved items and next ready task. Do not mark unavailable required checks as passed.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "I'll test it all at the end" or a large batch written without running a check: verify each slice; an early bug makes later slices wrong.
- A new test that passes on its first run: it may not test what you think; see it fail for the intended reason.
- "All tests pass" with no observed run, or a default command such as `npm test` the repository does not use.
- "This refactor is small enough to include": mixed refactor and feature changes are harder to review and revert.
- An abstraction or new utility file before a real repeated use demands it.
