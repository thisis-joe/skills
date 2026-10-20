---
name: coco-observe
description: "Use when adding or repairing logs, metrics, tracing, alerts, runbooks or operational visibility for a feature."
license: MIT
---

# coco-observe

Make real user failures diagnosable with bounded, privacy-conscious signals.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for one opaque failure path, a new production boundary or queue that needs full-path signals, metric-label cardinality decisions, distributed tracing, alert or runbook review, verification of the telemetry itself, and an unavailable sink or backend. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/observe.md) before dependent work.

## Procedure and output

1. State the operational questions and what working means before adding telemetry. Reuse existing correlation and instrumentation conventions.
2. Choose logs for events/detail, bounded-label metrics for trends, traces for causal timing. Propagate request/correlation IDs across relevant boundaries; keep unbounded IDs out of metric labels.
3. Allowlist fields and redact secrets/PII. Record distributions and relevant percentiles; an average alone can hide harmed users.
4. Define symptom-based, actionable alerts with owners, thresholds/windows and runbooks. Match existing incident severity policy rather than creating a competing scheme.
5. Verify telemetry itself: trigger a controlled success/failure, locate the expected event/series/span, check correlation and exercise alert delivery where authorized. Synthetic evidence must not be described as production observation.
6. Connect validated signals and release/rollback criteria to ship. Publishing alert rules or sending notifications follows existing authorization.

Return: operational question-to-signal map, schema/cardinality/privacy decisions, verification evidence and runbook links.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "I'll add logging after it works": the first incident is the most expensive time to find you are blind.
- "More logs means more observability" or "console.log for now": emit a few structured, queryable events instead.
- User IDs, raw URLs or error text as metric labels.
- Latency as an average without percentiles, or paging on causes such as CPU while user-facing errors go unwatched.
- Alerts acknowledged daily without action, or secrets, tokens or full request bodies in logs.
