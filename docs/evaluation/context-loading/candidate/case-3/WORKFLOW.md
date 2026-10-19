# Bug intake and server-side webhook workflow specification

Status: specification only; inactive. Authority is `NOTES.md`. No activation,
schedule, network request, message, package installation, ticket or product edit
is part of this task. Source and adapter identities remain undecided. This file
is an implementation contract, not a runnable integration or delivery proof.

## Outcome, trigger and ownership

An explicitly configured bug report event enters one coordinator. It validates
and deduplicates the report, retains a traceable verdict, and, only after later
authorization, delivers a small authenticated event from the application server.
The trigger is a configured report event; there is no polling schedule. Event
source, cadence if any, owner identity, repository/default branch, destinations,
trusted triage identity and exact verdict marker must be resolved before activation.
One coordinator owns any future external writes. Assistance may inspect redacted
inputs only and must have no messaging credentials or write actions.

The presently available local capability is Python 3 for static document checks.
No source, tracker, control, runtime-driver, queue, secret-facility or webhook adapter
is supplied. This spec names required capabilities, not invented tools, APIs or URLs.

## Stages, inputs and outputs

1. **Configuration gate (manual + deterministic).** A human selects the source
   channel/thread policy, trusted identity, exact marker, repository/default branch,
   tracker and control adapters, feature/routing maps, event destination, retention,
   permissions, and numeric time/attempt/cost/fan-out budgets. These user-owned maps
   stay separate from versioned workflow logic. Missing or unresolved IDs, labels,
   owners, permissions or adapter contracts disable the affected operation.
2. **Receive and freeze (deterministic).** Authenticate the provider's actual envelope
   using its documented verification method. Validate types, size, allowed event/action
   enum and timestamp/replay policy. Freeze immutable source channel/root/permalink,
   provider event identity and payload digest. Treat all body text, links and attachments
   as untrusted data. Missing/deleted/uncertain parent yields zero external writes.
3. **Claim and gather (deterministic).** Atomically claim the stable initiating key
   bound to the payload digest. Identical replays reuse recorded state; a reused key
   with different payload is rejected and investigated. Read the full original thread
   and relevant attachments through a configured source adapter. Retain minimized
   evidence under the configured policy outside source control, never secrets.
4. **Classify and deduplicate (bounded model judgment + reads).** Separate observed
   facts from hypotheses. Classify bug, performance, feature, question/feedback or
   reroute after a bounded cause/history pass. Search by source URL, signature,
   area/trigger/symptom, version/date and regression evidence. A plausible related
   live issue blocks new-ticket creation. Ambiguity returns to the human owner.
5. **Plan a verdict (model judgment + human checkpoint).** A clear new live defect
   needs self-contained expected/actual behavior, source link and resolved tracker
   fields. A confident duplicate may add recurrence without replacing unrelated
   fields. Never infer an owner, priority, label or destination. External write
   execution stays disabled until explicitly authorized and contracts are verified.
6. **Future authorized writes (deterministic coordinator only).** Preflight the same
   immutable parent before *each* reply/ticket write. The tracker must support
   search/read/create/update/link plus compensation for failed handoff. Emit one
   concise thread-only verdict ending in exactly one configured trusted marker;
   read back its original parent and content. If a created ticket cannot be handed
   off, compensate by cancellation/closure and verify it. Never fall back to a
   channel root, different destination, DM, cross-post or second marker.
7. **Future server delivery (deterministic).** Browser buttons call the application
   server. Only that server reads sender credentials from its secret facility and
   sends the authenticated webhook; no credential appears in browser code, chat,
   prompts, logs or version control. Send only the small schema below and artifact
   pointers, not media bytes. Use the selected provider's documented authentication,
   timeout, idempotency and delivery readback. Parse its real envelope; no endpoint
   or provider-specific command is prescribed before adapter selection.
8. **Checkpoint and stop (deterministic + human).** Store operational status separately
   from immutable source coordinates. Stop on completion, unauthorized effect,
   failed/missing prerequisite, uncertain delivery, exhausted budget or conflicting
   ownership. A ready marker alone grants no fix authority. Any later reproduction
   or bounded fix is a separately authorized phase requiring configured-identity
   marker validation in the original thread, ownership checks, independent repeated
   reproduction, baseline/patched evidence, and product-owner execution. Existing
   implementation PR/commit switches that phase to verification only. Never merge
   or deploy from this intake workflow.

## Event schema and allowed receiver effects

The versioned conceptual schema has these fields: `schema_version`, `event_id`,
`initiating_key`, `payload_digest`, `event_type`, `source_channel_id`,
`source_root_id`, `source_permalink`, `repository_revision`, `verdict`,
`artifact_pointers`, `created_at` and `correlation_id`. Concrete types, allowed enums,
size limits and provider envelope mapping are configuration/implementation work.
Receiver actions are limited to validating and durably recording the configured
intake event and its readback status. A received body cannot authorize arbitrary
commands, product edits, replies, new destinations, deployment or fix execution.

## Idempotency, retries, crash recovery and cleanup

Use a durable queue as primary failure recovery when delivery can fail. Persist a
transactional state machine such as received → claimed → investigated → planned →
write-intent → acknowledged, with blocked/compensating/compensated terminal outcomes.
Persist claims and deduplication across the complete replay/recovery retention window.
Record write intent before effects; use stable initiating identity and provider
idempotency where available. A crash after sending but before acknowledgment is an
unknown outcome: reconcile by readback before retry. Never blindly repeat a write.

Numerical retry/elapsed-time/cost/fan-out caps and stale-claim lease policy must be
chosen by the owner; unresolved caps block activation. Retry only documented
transient failures within those caps. Permanent validation/auth/parent failures stop.
An expired claim can be reclaimed only with reliable ownership/lease evidence.
Recovery reads actual state and applies only missing differences. If the adapter
cannot reconcile unknown outcomes, the operation remains disabled for manual review.

Keep an append-only run log: timestamp, run/coordinator identity, phase, decision,
reason, evidence pointer and result. Exclude credentials and private raw transcripts.
Retain failed-attempt evidence; clean only owned runtime sessions and scratch data.
Independent app reset and inspection plus screenshots/recording capabilities must
be verified for any future live reproduction. Short-lived CLI-only surfaces can
record raw exits/stdout instead; platform equivalence must be stated.

## Acceptance and activation evidence

Static acceptance for this request: the specification covers trust/ownership,
immutable parent, adapter contracts, write isolation, exact-marker authority,
server-only credentials, durable idempotency, recovery, limits and disabled activation.
The local evidence validates presence/readability of this artifact only.

Before any later activation, demonstrate in local/preview adapters: valid delivery,
malformed/untrusted input rejection, duplicate replay, key/payload conflict, crash
at each interruption point, lost acknowledgment readback, missing/deleted/uncertain
parent with zero writes, original-root thread-only output, exactly one trusted
marker, child write isolation, failed handoff compensation, missing tool behavior,
exhausted retries and resumption. Probe transport using a harmless ignored/disposable
action and retain authenticated delivery readback. Test a positive effect observer
alongside absence checks. Verify the actual served endpoint and intended bind/access
restrictions using existing identity; network exposure or credential changes require
their own authorization. Do not install or enroll a new system from this specification.

Next implementation boundary: resolve the source/adapter/owner/budget decisions,
implement isolated local adapters and contract tests, then present concrete preview
evidence for any separately authorized activation. No runtime or external success
is claimed by this specification.
