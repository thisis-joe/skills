# Compatibility, migration and retirement

Use this reference for schema/API replacement, broad renames and removal of active systems.
Apply the [common contract](../contracts.md) and [security boundaries](security.md).
The output is a verifiable migration sequence; build owns changes, commits and task state.

## Inputs

- Old/new contracts and behavior, including undocumented observable dependencies.
- Consumer inventory, owners, usage evidence and rollout/deployment topology.
- Data volume, write paths, retry/replay windows and current compatibility guarantees.
- Approved scope, release constraints, backup/recovery capability and required checks.

## Choose the mode

| Condition | Mode | Safety condition |
|---|---|---|
| External or independently deployed consumers | Compatibility migration | Old/new remain valid during transition |
| Internal callers under one coordinated release | Coordinated refactor | Every caller moves before legacy deletion |
| Production data shape changes | Expand/migrate/contract | Additive phases and verified recovery |
| Replacement is not production-proven | Prove replacement first | No premature retirement claim |
| Green intermediate batches impossible | Integration-only branch | Explicit pending state and final integrated gate |

Do not treat a small rename as harmless when its contract is shared.
Advisory deprecation is the default; a compulsory deadline needs a justified reason,
consumer migration support and authority for the affected users/systems.

## Establish the contract and blast radius

1. Read the old behavior, replacement and historical rationale where accessible.
2. Find callers plus API payloads, persisted columns, wire formats and other languages.
3. Quantify active use with code, logs, metrics or consumer-owner evidence.
4. Name the one or two facts that make transition safe.
5. Exercise those facts through real code or a small compatibility harness.
6. Record unproven consumers/behavior as open; an empty search alone proves only its scope.

Compare replacement coverage and migration cost with ongoing maintenance/security cost.
Infrastructure owners migrate users or supply compatibility tooling and documentation.
Do not announce deprecation and leave consumers without a working alternative.

## Expand and migrate

Define the new contract and verification before implementation.
Add the new form alongside the old with safe defaults and explicit ownership.
Use an adapter, strangler routing or cohort flag where it keeps both forms valid.
Give each dependency-ready consumer batch its own acceptance, verification and work unit.
Test representative consumers, errors, retries, serialization and mixed-version operation.
For shared state prefer separate owned targets before introducing structural serialization.
Where one shared writer is necessary use a lock, transaction, single owner or compare-and-swap.

Keep normal batches green and independently reversible.
If that is impossible, record the integration-only branch and affected dependent tasks.
Red intermediate work is integration pending, never normal done or ready to ship.
The final integration task owns full compatibility/regression proof before release.

## Production schema sequence

1. **Expand:** add the new nullable column/table/index without removing the old form.
2. **Dual-write:** deploy all relevant insert/update paths writing old and new forms.
3. **Backfill:** migrate existing data in bounded, throttled batches off the hot path.
4. **Verify:** compare counts, missing values and representative transformed records.
5. **Switch reads:** move consumers to the new form while preserving old writes.
6. **Bake:** observe mixed-version behavior, lag, errors and data consistency.
7. **Stop old writes:** confirm no still-running consumer depends on them.
8. **Contract:** remove the old form in a separate later deployment.

Track a resumable backfill cursor and make reruns idempotent.
Define concurrent-write handling so backfill cannot overwrite newer application data.
Measure batch duration, lock contention, replication lag and error/retry counts.
Build large indexes with the database's appropriate nonblocking mechanism.
Pause backfill when operational guardrails fail; retain progress and evidence.
Do not bundle a safe additive change with a destructive drop in one migration.

## Recovery and destructive phase

Test the down path where reversal is meaningful before merging migration changes.
Distinguish reversible DDL from restoration of overwritten or deleted data.
Record backup/restore or forward-repair procedure and verify the recovery assumptions.
State what new data is preserved and what loss window recovery would impose.
Existing sign-off must cover the destructive action and actual data impact.
A code revert alone is not a production data rollback.

Contract only after measured zero active use and all known callers have migrated.
For coordinated internal API changes, migrate callers/tests in the same planned wave.
Delete the obsolete implementation and tests that only encode its internals.
Keep behavioral coverage for the new public contract; do not delete failing behavior tests.
Remove retired configuration/docs/notices and assign ownership for any remaining legacy path.

## Output and stop

Return old/new contract, consumer map, ordered phases and each phase's proof/recovery gate.
Include cutover criteria, active-use evidence, backfill reconciliation and unresolved consumers.
Keep rollback commands/runbooks explicit and tied to the target/version.
Stop cutover for failed compatibility, unknown data state or absent required authority.
Mark migration complete only when the chosen final contract and required integrated checks hold.

## Conditional TypeScript fixture migration

Use for an explicit request to replace test-only assertions or adopt `@total-typescript/shoehorn`.
Inventory requested `.test.ts`/`.spec.ts` fixtures and classify partial valid data versus intentionally
invalid input. Preserve existing good typed builders; this is not a production-code cast replacement.
Verify the installed/requested library version against its official API and the project's package manager.
If adding it is in scope, add a development dependency using the dependency execution gate in
[security](security.md); otherwise prepare the concrete proposed migration without installing it.

- Replace a test-only `value as Request` partial fixture with `fromPartial(value)` where the consumer
  infers the intended type; keep every field the exercised code path actually reads.
- Replace an intentional `as unknown as Request` bad-input fixture with `fromAny(value)` while retaining
  the invalid value and the assertion that it is rejected. Do not convert it into valid happy-path data.
- Use `fromExact(value)` when the complete fixture shape is the point of the test.
- Import the selected helper from the verified package API and remove obsolete casts/imports.

For example, an existing `getUser({body: {id: '123'}} as Request)` test may become
`getUser(fromPartial({body: {id: '123'}}))`; this does not authorize dropping required test setup.
Run the actual typecheck and affected tests, then required closure checks; inspect that negative tests
still fail when the invalid-input defense is broken in a disposable copy.
Keep all helper usage in tests, preserve user edits, and hand the migration to build for its scoped commit.
