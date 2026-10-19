# Measured performance and benchmark decisions

Use this reference for user-visible slowness, regressions or choosing between measured options.
Apply the [common contract](../contracts.md); build owns changes and commits.
An optimization is a hypothesis until a comparable measurement supports it.

## Inputs and modes

- User-facing symptom, target metric/unit and relevant product budget.
- Code/version, dataset, hardware/runtime, load/concurrency and environment.
- Measurement script, traces, field data and prior experiment ledger.
- Correctness checks and authorized execution/production access.

| Available evidence | Mode | Permitted conclusion |
|---|---|---|
| Source only | Quick inspection | Potential impact, no measured score |
| Trace/report/running reproducible target | Deep measurement | Sourced baseline and bottleneck |
| User requests one rough ballpark | Ballpark | One-run result with limitations |
| Alternatives will determine adoption | Comparative experiment | Comparable tuned runs and correctness |

Do not invent browser metrics for a CLI/library or populate a scorecard from assumptions.
Use available supported tools; a named profiler or browser is not a prerequisite by fiat.

## Establish a valid baseline

1. Write the exact claim to test, including metric, unit, workload and intended scope.
2. Read the harness: what it times, counts, awaits and ignores.
3. Verify the work occurs inside the timed region and outputs are correct.
4. Count errors, rejected requests, retries and timeouts alongside successes.
5. Detect busy-host/load-generator interference and equalize or disclose it.
6. Match production-relevant versions, release flags, data and cache state.
7. Profile in a separate run to identify the limiter without reporting profiler overhead.

Tune both alternatives comparably before declaring one preferable.
Check physical bounds and the changed portion's share of total time.
A helper consuming one percent cannot explain a large end-to-end gain without another effect.
If work did not occur, errors are uncounted or an alternative is untuned, mark inconclusive.
For a ballpark, still verify real work and correctness and label the single run.

## Measure the actual bottleneck

For page load inspect network/TTFB, blocking resources, image priority and rendering.
For sluggish interactions examine long tasks, input delay, rendering and work per event.
For backend latency separate query execution, connection wait, CPU and external calls.
Use representative hardware/networks and pair synthetic traces with field evidence when available.
Do not replace a measured symptom with whichever metric is easiest to improve.

For queries capture before/after execution plans and actual versus estimated rows.
Refresh stale statistics when estimates are wrong; index the query shape, not a lone column.
Consider equality/range/sort order, expressions, selectivity and write overhead.
For pool exhaustion find held/leaked connections before increasing limits.
Bound total instances times pool maximum by database capacity; proxy unbounded instances.

For caches state the expensive reread, layer, full key and acceptable staleness.
Include viewer/tenant/locale/permissions/flags when they change the response.
Choose an invalidation policy, memory ceiling and stampede protection.
Negative-cache absence briefly, never an origin failure; monitor hit rate.
Do not cache a value whose staleness violates correctness.

For frontend work prioritize dimensioned LCP images, modern responsive media and route splitting.
Lazy-load below-fold media; defer noncritical work and split long main-thread tasks.
Memoize only measured expensive work; adding memoization everywhere is not a result.

## Controlled experiment and decision

Change one hypothesis at a time and keep correctness checks unchanged.
Repeat each side, normally at least five alternating runs for an adoption comparison.
Use identical commands, conditions, warmup and fixed work/sample/time budget.
Report median and range and compare the gain with run-to-run variation.
If the comparison remains close, use suitable harness statistics rather than cherry-pick a run.

| Measurement and correctness | Decision |
|---|---|
| Meaningful gain beyond noise, required checks green | Keep |
| Within noise or no measurable improvement | Revert the owned attempt |
| Slower or correctness regressed | Revert the owned attempt |
| Missing limiter, comparable tuning or valid work count | Inconclusive |

Reversion preserves unrelated edits and the evidence explaining the attempt.
Removing required work, assertions or validation cannot create a valid performance win.
Record each kept and reverted idea with baseline/result/conditions/verdict/reason.
Consult that ledger before repeating an earlier failed experiment.

## Conditional sustained tuning

When the user requests a tuning run, agree the metric, direction, workload and stop/budget predicate.
Prove harness sensitivity with realistic contrasting workloads, then freeze the harness and gate.
The fixed command must report metric, work count and errors; do not edit it to make an attempt win.
Run one grounded hypothesis per iteration, record it, and keep/revert before the next attempt.
Independent experiments may use isolated owned workspaces if available and authorized.
Do not stack unmeasured edits or relax the target after a plateau.
Revisit the limiter or pivot hypothesis category when attempts stall.
Stop at the agreed predicate/budget or surface exhausted useful options with the remaining gap.

## Guard and output

Return faster/slower/no measurable difference/inconclusive before interpretation.
Give the primary metric/unit, workload, run count, range, limiter and artifact pointer.
Report micro improvements alongside their share of the end-to-end path.
For web changes, separate controlled synthetic evidence from user-field validation.
Use project-specific synthetic budgets and meaningful field movement to guard the metric.
An inherited baseline may become a [ratchet](start.md) rather than an aspirational failing gate.
Record incomplete field validation or unavailable tools explicitly.
Stop optimization when the requested budget is met or the evidence rejects the hypothesis.
