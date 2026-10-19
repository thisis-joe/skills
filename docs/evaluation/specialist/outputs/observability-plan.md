# Diagnose job submission without unbounded labels

Operational questions: are submissions failing or slowing; where did a specific test request fail; did HTTP or worker initiation produce it; would the symptom alert fire? Use existing instrumentation when integrating; this fixture uses an isolated in-memory sink only.

| Question | Signal / query | Privacy and budget |
|---|---|---|
| Failure rate and duration | `job_requests_total{route,method,outcome}`, duration seconds histogram; error/success counts and p50/p95/p99 | 2 route templates × 2 allowed methods × 3 outcomes = 12 label tuples per family before histogram buckets. The local emitter currently emits POST only, so observed envelope ≤6 |
| One failure and entry point | Structured `job.request.completed`, validated `request_id`, initiating `entryPoint=http|worker`, bounded route/outcome | ID is test correlation, never a metric label; no user_id, raw URL, token or payload |
| Causal path | Span `job.request` with same correlation/entryPoint, bounded route/status and seconds | Production cross-service propagation and sampling not verified |
| User symptom deserves attention | Existing-severity error-rate window with on-call owner and runbook | Actual SLO/history absent: production threshold/window remains proposed, not silently invented |

Reject the proposed `user_id` and raw-URL metric dimensions. They are unbounded and may expose private query values. A hashed user_id is still unbounded. Use route templates and allowlisted outcome/method; put necessary request detail only in access-controlled, purpose-limited logs/traces. Proposed local-test receipt retention is seven days; real retention/access policy must be reconciled before publishing telemetry anywhere.

Local test emitted success 0.04s and failure 0.25s, found both event/series/span objects independently in the sink, checked count=1 each and matching request/entryPoint, rejected a raw URL with query token, and evaluated a local error-present alert predicate. This is a toy alert sensitivity check, not evidence of the production error-rate window or real paging. `evidence/observations.json:observe` retains synthetic objects. No notification was sent and no external backend was queried.

Runbook draft: when the approved symptom window fires, on-call first queries error ratio by bounded route and duration percentiles, picks a protected request correlation, follows initiating entryPoint and spans, then holds rollout on the project's error/data-integrity trigger. Owner and escalation destination are unresolved fixture inputs. Backend ingestion, cross-service spans, real alert rule, delivery and working external runbook link are unavailable; they block production telemetry completion. Do not describe these synthetic observations as production visibility.
