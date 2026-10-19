---
name: coco-observe
description: "Use when adding or repairing logs, metrics, tracing, alerts, runbooks or operational visibility for a feature. 관측·계측·알림·운영 진단."
license: MIT
---

# coco-observe

Make real user failures diagnosable with bounded, privacy-conscious signals.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/observe.md) only when the task needs their additional procedure. The [integration decisions](../_coco-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. State the operational questions and what working means before adding telemetry. Reuse existing correlation and instrumentation conventions.
2. Choose logs for events/detail, bounded-label metrics for trends, traces for causal timing. Propagate request/correlation IDs across relevant boundaries; keep unbounded IDs out of metric labels.
3. Allowlist fields and redact secrets/PII. Record distributions and relevant percentiles; an average alone can hide harmed users.
4. Define symptom-based, actionable alerts with owners, thresholds/windows and runbooks. Match existing incident severity policy rather than creating a competing scheme.
5. Verify telemetry itself: trigger a controlled success/failure, locate the expected event/series/span, check correlation and exercise alert delivery where authorized. Synthetic evidence must not be described as production observation.
6. Connect validated signals and release/rollback criteria to ship. Publishing alert rules or sending notifications follows existing authorization.

Return: operational question-to-signal map, schema/cardinality/privacy decisions, verification evidence and runbook links.
