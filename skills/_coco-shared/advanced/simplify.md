# Simplification with behavior and contract preservation

Use this reference for reducing complexity without adding behavior.
Apply the [common contract](../contracts.md) and existing project conventions.
Small local cleanup after green is permitted; structural work has its own scoped work unit.
Build owns edits/commits and review returns findings rather than modifying code.

## Inputs and conditional modes

- Target responsibility, current public contract and the reason it is hard to understand.
- Callers, tests, errors/side effects/order and relevant history/ADRs.
- Accepted scope, current passing evidence and pre-existing user changes.
- External compatibility requirements and measured performance constraints.

| Condition | Mode | Action |
|---|---|---|
| Tiny naming/duplication cleanup in changed code after green | Local cleanup | Preserve scope and recheck |
| Structural responsibility change | Separate refactor | Define contract and regression scope first |
| Internal API replacement with coordinated callers | Caller migration | Move all callers before legacy deletion |
| External/independently deployed consumers | Compatibility work | Use the migration sequence |
| Purpose or behavior unclear | Understand first | Read history/callers before editing |

Do not refactor an adjacent system just because the file is open.
Do not simplify code that will be discarded or replace a known fast path without measurement.

## Establish what must remain true

1. Read target and neighboring conventions, glossary and relevant architectural decisions.
2. Inspect public callers and downstream serialization/persistence effects.
3. Read tests and error paths; identify side effects, ordering and timing commitments.
4. Use history to understand platform constraints or a surprising existing structure.
5. State the behavior to preserve and the complexity to remove.
6. Obtain missing acceptance decisions; reuse existing approval for the defined refactor.

Protect observable outputs, errors, state transitions, side effects and execution order.
Preserve external interfaces unless a contract change is explicitly in scope.
Passing unchanged tests is required evidence, not proof of every unknown behavior.
Add a missing public-boundary characterization when it protects a real uncertainty.
Do not copy the implementation into expected assertions or freeze irrelevant internals.

## Choose a concrete simplification

Prefer fewer concepts a reader must hold, not fewer lines at any cost.
Use guard clauses or a named predicate for tangled conditions when that clarifies intent.
Split orchestration from business rules and keep feature policy in its owning module.
Reuse an existing canonical helper rather than inventing a near duplicate.
Delete pass-through wrappers that add no current meaning; keep helpers that name a real concept.
Make invariant/type boundaries explicit instead of layering casts and silent fallbacks.
Preserve useful why/gotcha comments and remove restatements only when their purpose is clear.

For repeated branches, compare one coherent model/dispatcher against duplicated conditionals.
For shared mutable state, first separate owned targets; structurally serialize only real sharing.
For a broad mechanical change, prefer a reviewable codemod/AST transform and inspect its scope.
File/line-count thresholds are signals for investigation, not automatic extraction rules.

## Execute in verifiable steps

Make one coherent change against the recorded current state.
Run the affected behavior checks and required build/types/lint after relevant changes.
If a check fails, preserve failure evidence and revert only the owned attempted edit or debug it.
Keep unrelated working-tree/index changes intact; never reset the entire workspace as cleanup.
When tests must change, explain whether their contract or irrelevant implementation coupling changed.
A test change solely to hide a behavior regression is forbidden by the standing floor.

After each green step compare comprehension and resulting structure with the original.
If the same complexity merely moved files or gained another wrapper, reconsider/revert.
Do not keep an abstraction for a hypothetical future caller.
Keep substantive refactor commits separate from new feature/config behavior.

## Migrate callers before deleting legacy APIs

Use coordinated removal only when all consumers are internal and can move together.
Inventory real callers, generated bindings, tests and less-visible serialization consumers.
Update each to the new contract and run the integration path.
Check for remaining active references and ownership before removing the old implementation.
Delete obsolete adapters/config/docs and tests that only preserve the removed internals.
Retain tests of required public behavior under the new interface.
Do not preserve dead compatibility layers without a real consumer or explicit migration need.
For public or independent consumers, use [expand/migrate/contract](migrate.md) instead.

## Output and stop

Return the removed concepts, preserved contract, affected callers and regression evidence.
Record discarded attempts or remaining complexity when useful to future work.
Present unresolved behavior/performance questions instead of asserting exact equivalence.
Stop when the scoped readability goal is met and required checks pass.
Stop and reframe if the proposed simplification needs new behavior or unapproved removal.
Review the final current diff; prior evidence cannot approve later cleanup edits.
