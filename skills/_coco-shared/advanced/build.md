# Implementation modes

Apply the [common contract](../contracts.md).
Build owns product edits, work-unit commits, and the authoritative completion-state update.
Reuse an existing spec, plan, test-boundary agreement, and execution grant instead of interviewing again.

## Resume the actual task

1. Read the requested task/spec and state its stable ID, intended behavior, preserved behavior, and acceptance.
2. Find the single authoritative task-state location and dependency graph; a copied checklist is not a second tracker.
3. Inspect branch/base, HEAD, relevant dirty paths, prior work-unit commits, and existing verification/review receipts.
4. Reconcile a commit already made but not reflected in task state before selecting new work.
5. Choose one task whose dependencies are actually satisfied; continuous mode repeats this after each completed unit.

Use a feature branch and record pre-existing user changes. Apply the [build entrypoint's Jira branch naming and preparation rules](../../coco-build/SKILL.md#feature-branch-preparation); the entrypoint owns that team convention. Reuse a suitable authorized branch rather than resetting it.
Isolate overlapping hunks; do not stage user work, reset unrelated files, or create a new base merely for procedural neatness.
A blocked dependency does not become ready because a summary or stale checkbox says it is done.

## Choose a proportionate path

- Lightweight: a clear low-impact static edit; inspect the actual result and run applicable project checks.
- Standard: behavior change; use the red-to-green loop and required runtime/regression evidence.
- Strengthened: uncertain contracts, irreversible consequences, shared state, or high blast radius; settle design and add impact/specialist review.
- Single-task versus continuous execution is separate from rigor. A continuous grant changes scheduling, not permissions or evidence.

If a material decision remains unresolved, ask only that decision while continuing independent authorized work.
Scope, glossary, ADRs, and established quality thresholds constrain implementation; source heuristics are not universal quotas.

## Name the shape first

Define the domain data and dominant access paths before writing logic.
Use a state machine for lifecycle, a discriminated model for variants, a registry for repeated dispatch, and one owner for state.
Keep ordinary local code when abstraction does not remove duplicated rules, invalid states, branches, or lifecycle risk.
Parse raw external input at system boundaries, return domain types, and keep framework wiring thin and business transforms pure.
Do not export transport/storage internals as the public domain contract or revalidate already-established internal data everywhere.
Derive schemas/types from their authoritative source and brand semantically different primitives where confusion is possible.
Repeated casts, special-case coordination, or callers knowing internals indicate a missing boundary or wrong sketch.
For a consequential novel design compare distinct shapes before committing; a small edit needs no panel.

## Execute one vertical slice

1. State the smallest complete public behavior this slice adds or corrects and its already-agreed test boundary.
2. Discover the repository's focused-test, typecheck, build, lint, and closure commands; prefer checked-in wrappers.
3. Write a focused behavioral check before changing implementation and run it to observe the intended failure.
4. If it passes or fails for setup reasons, correct the check/reproduction before trusting it as a red signal.
5. Implement only enough to satisfy that behavior, without speculative features or unrelated cleanup.
6. Run the focused check to green, then relevant nearby checks and the real user path when required.
7. After green, allow small in-scope naming/duplication cleanup only; recheck affected behavior after changing it.
8. Obtain the required [review](review.md), resolve findings through this owner, and close the work unit below.

Do not write a whole imagined test suite followed by a whole implementation; each slice uses what the previous one taught.
Tests use public behavior and independent expected values, real local implementations, and controlled external boundaries.
Do not force brittle internal mocks, broad fixture setup, or irrelevant tests for a static change.
If no practical correct test boundary exists, retain the exact executable failing reproduction and explain the gap.
Do not claim automated regression coverage or completion when a required check remains unavailable.
Keep incomplete user-visible features behind an existing suitable safe control when the rollout plan requires it.

## Repeatable edits and migrations

For nontrivial mechanical work, learn one unit then build the smallest deterministic transformation or check that makes the result reviewable.
Prove the tool reproduces the learned unit, handles reruns safely, and preserves excluded paths.
Prefer one deterministic pass to many workers manually repeating the same edit; avoid a framework for a one-off script.
Run each verifiable unit before proceeding. Keep removal, reshape, and behavior addition independently understandable.
Compatibility-sensitive changes prefer expand, migrate callers/data, verify, then contract.
When no external compatibility obligation exists, migrate all internal callers and remove the legacy route in the same coordinated wave.
Search strings, examples, docs, schemas, and backreferences after renames; symbol search alone misses them.
An explicitly scoped integration-only branch can carry necessary temporary breakage, but cannot claim normal done/ship until final integrated checks pass.

## TypeScript condition

Use this section only for a TypeScript surface, respecting the repository's actual schema/logger/test libraries.

- Prefer discriminated unions and constructive types to optional-field bags and synchronized booleans.
- Keep a simple array while operations are total; strengthen to a nonempty/range/paired shape when it removes partial operations.
- Parse unknown boundary values using the existing runtime schema library and infer the domain type from it.
- Verify brands and type-guard claims; a cast does not validate input and a lying guard hides the same bug.
- Narrow with discriminants, property presence, and runtime checks before assertions; exhaust variants with a never check.
- Prefer satisfies for validating literal shape and derived types over parallel handwritten interfaces.
- Object arguments improve semantic clarity except where a measured hot path justifies another representation.
- Exercise real framework lifecycle/disposal where relevant and use structured shipped diagnostics with useful correlation context.

## Optional concurrent execution

Use agents only when authorized and when independent work exceeds coordination cost; one owner is a valid decomposition.
Name blocking prerequisites, independent outputs, shared mutable targets, and the smallest safe decomposition first.
Eliminate shared writes with owned files/branches/state keys; different fields in one mutable file still conflict.
If one shared object is an actual invariant, enforce single-writer/atomic/locking/sequential control structurally.
Every brief names goal, allowed/excluded paths, upstream context pointers, acceptance, exact check, revision, and report shape.
Relate dependent tasks through both ordering and the upstream findings they need; do not assume siblings share context.
One writer owns each branch, a separate authorized owner integrates topology, and final build ownership remains explicit.
For sustained queue/recovery bookkeeping use [automation modes](automate.md), without making a standing program the default.

## Close a work unit

1. Run project-required regression/build/runtime checks at closure; [verify](verify.md) distinguishes pass from unavailable evidence.
2. Reuse unaffected passing receipts and rerun checks whose relevant code, environment, or acceptance changed.
3. Review the actual task changes, including committed/index/worktree/untracked layers, before the work-unit commit.
4. Resolve blocking findings or retain an explicit authorized disposition; a pass on one review axis cannot mask another failure.
5. Inspect the final diff for unrelated work, secrets, obsolete instrumentation, and broken references.
6. Stage only task-owned paths or hunks and create the coherent work-unit commit required by repository policy.
7. Record the actual commit and evidence in the authoritative task state; mark done only after all required conditions hold.
8. In continuous mode refresh the dependency-ready frontier and proceed to the next authorized unit.

Do not commit a speculative fix to make a check quieter, disable failures, or broaden scope to resolve unrelated debt.
After a check fails stop dependent advancement and use [debug](debug.md); repeated unresolved blockers follow the common retry bound.
If interrupted after committing, inspect that commit and reconcile task state instead of implementing or committing the unit twice.
Keep dependent PR bases consistent with the chosen plan. A local commit does not by itself authorize publication, merging, deployment, or tracker writes.

## Return

Report changed behavior, significant choice, failing-before/passing-after evidence, required check/review status, commit, and authoritative task state.
For continuous work include completed units, next ready unit, and genuine blockers; do not present a red integration branch as finished.
