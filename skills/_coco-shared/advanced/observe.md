# Logs, metrics, traces and operational proof

Use this reference for production instrumentation and visibility gaps.
Apply the [common contract](../contracts.md) and [security policy](security.md).
Instrumentation is developed with the feature, not deferred until its first incident.

## Inputs and modes

- Critical feature flow, endpoints/dependencies, workers and failure/retry paths.
- On-call questions, existing signals, SLOs, privacy policy and retention limits.
- Available logger, metric/tracing backend, staging traffic and alert destinations.
- Authorized changes and test traffic/failure-injection scope.

| Need | Mode | Deliverable |
|---|---|---|
| One opaque failure path | Narrow instrumentation | A few queryable events and correlation |
| New production boundary/queue | Full path | RED/USE, cross-boundary trace and signals |
| Pager noise or missing incident signal | Alert review | Actionable symptom rule and runbook |
| Sink/backend unavailable | Design plus gap | Schema/query plan with unverified runtime state |

A current incident belongs to debugging; this reference supplies its observation mechanism.

## Start from operational questions

1. Write two to four questions an on-call person will need to answer.
2. For each question choose log, metric or trace and the exact fields/query.
3. Map permanent-failure, timeout, retry, queue/replay and success outcomes.
4. Define expected traffic/latency/error observations and a bounded cost/cardinality budget.
5. Reuse existing platform instrumentation instead of creating a parallel telemetry system.

Metrics show that something changed, traces locate the path, logs explain one case.
Each emitted field must support a real question or operational correlation.

## Structured logs and attribution

Use stable event names and structured fields rather than interpolated prose.
Generate or validate a correlation/request/run ID at the boundary.
Propagate that ID in outbound HTTP, queue metadata, logs and spans.
If scheduler, replay endpoint and CLI share a sink, stamp `entryPoint` at initiation.
Propagate entry point alongside correlation; do not infer it later from timing or process state.
A correlated hint is not proof of which entry point executed the operation.

Use consistent levels: error for broken invariants, warn for handled degradation,
info for significant events and debug off by default in production.
Allowlist fields and redact secrets, tokens, auth headers and personal payloads.
Log external-call metadata such as provider/status/latency/attempt rather than full bodies.
Honor purpose, access and retention rules for identifiers that remain necessary.

## Metrics and cardinality

For request endpoints and external dependencies measure Rate, Errors and Duration.
For queues, pools and hosts measure Utilization, Saturation and Errors where useful.
Use latency histograms with p50/p95/p99 rather than an average alone.
Track worker queue age/depth and processing duration separately.

Metric labels come from bounded sets: route template, operation, provider and status class.
Never use raw URLs, emails, request IDs, user/tenant IDs or error messages as labels.
Estimate series count from label combinations before introducing a dimension.
Move high-cardinality case detail to appropriately protected logs/traces.
Choose useful buckets and units and verify that instrumentation measures the intended interval.

## Tracing

Use the existing tracing stack or an available vendor-neutral implementation.
Initialize instrumentation early enough to observe actual libraries and calls.
Propagate inbound/outbound trace context through HTTP and asynchronous queue boundaries.
Add manual spans around meaningful internal units, with bounded non-sensitive attributes.
Use a justified sampling policy; retain errors with tail sampling if supported.
Record a broken span/context gap as a verification failure, not an acceptable screenshot.

## Alerts and runbooks

Page on symptoms users feel: error rate, tail latency or queue age with impact.
Keep causes such as CPU/restarts on dashboards unless their policy identifies actual impact.
Each alert needs a threshold and duration justified by SLO/history.
Use actionable severities and owners; page/ticket is a useful starting distinction.
Attach a runbook with meaning, first query/check and escalation owner.
Delete or tune a repeatedly ignored alert rather than train people to ignore the pager.
Record incident-learned corrections before closing the incident.

## Test the telemetry itself

Under the authorized test scope, force a representative error in staging.
Find it using correlation/entry-point fields without relying on source inspection.
Send test traffic and confirm expected metric names, labels, counts and duration units.
Follow one request across every service/queue and check for broken spans.
Test-fire each new alert safely and verify destination and working runbook link.
Restore any temporary test threshold immediately and record the restoration.
If external notification is not authorized, test locally and leave delivery unverified.

## Output and stop

Return the on-call question-to-signal map, schemas/queries and retention/cardinality decisions.
Include actual log/metric/trace/alert evidence and target/version.
Keep unavailable backend, test traffic or delivery evidence explicitly pending.
Stop completion when required signals cannot be found or attribution is ambiguous.
Feed launch monitoring and recovery criteria into [release readiness](ship.md).
