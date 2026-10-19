# Bug intake and server-side webhook workflow specification

Status: specification only; inactive. Authority comes from `NOTES.md`: no activation,
scheduling, network requests, installation, or messages are authorized. No source,
tracker, control, server, or webhook provider identity has been chosen. This document
specifies contracts and activation gates; it does not provision a standing system.

## Outcome, owner, trigger, and scope

The intended outcome is one evidence-backed bug classification under its original
source thread, followed only when separately authorized by reproduction or a bounded
fix. A configured authenticated event triggers a run; no polling cadence or schedule
is selected. Event source, permitted channels, thread policy, immutable root identity,
repository and default branch, trusted verdict author, marker grammar and expiry,
tracker adapter, control adapter, feature/routing map, destination, operational owner,
retention, retry/time/cost/fan-out budgets all remain UNRESOLVED.

A single configured coordinator owns external writes and the durable run ledger.
Read-only assistants receive no messaging or tracker-write credentials/actions.
Child writers, if any, must demonstrably lack messaging credentials/actions; otherwise
only the coordinator/build owner may edit. Human judgment chooses routing, ownership,
ambiguous duplicate decisions, permission expansion, and any product fix scope. No
owner, priority, label, destination, endpoint, model, or adapter is guessed.

## Sources, destinations, tools, and minimum permissions

| Action | Input/output and required capability | Available state and activation gate |
| --- | --- | --- |
| Read a report | Configured source adapter reads the entire original thread and relevant attachments at immutable channel/root/permalink coordinates | Adapter and source identity UNRESOLVED; disabled |
| Inspect and deduplicate | Repository read access plus tracker search/read by source URL, signature, area/trigger/symptom, version/date, and regression artifacts | Repository/default branch and tracker UNRESOLVED; disabled |
| Write ticket/link/compensation | Tracker search/read/create/update/link and verified cancel/close compensation | Fields/owners/labels and adapter contract UNRESOLVED; no writes |
| Write thread verdict | Source adapter preflights the same existing parent immediately before each write; thread-only reply and delivery readback | Trusted author, root, marker, write authority and adapter UNRESOLVED; no messages |
| Launch and reproduce | Control adapter launches pinned app revision, performs mapped real actions, independent reset, read-only inspection, screenshots/recording and cleanup | Control adapter/feature map and application UNRESOLVED; disabled |
| Deliver webhook | Application server sends a small explicit schema through a configured authenticated provider and reads delivery result | Server, endpoint, provider envelope/auth and secret facility UNRESOLVED; disabled |
| Prepare this specification | Local file inspection and Python-based document consistency checks | Available and used locally; grants no workflow activation |

The application server owns the sender credential in its server-side secret facility.
Never put it in browser code, chat, logs, prompts, or version control. Separate read,
thread-write, tracker-write, and deploy secrets and grant only the action's minimum
scope. No deploy authority is needed for intake. Use an existing identity for private
network access; bind/access restrictions and the real served endpoint must be tested
before any authorized exposure. Network exposure, enrollment, services and credential
changes need their own authorization. Keep user-owned configuration/maps separate
from versioned workflow logic; preserve local edits on managed-file refresh.

## Stable stages and outputs

1. **Configure and preflight.** Resolve every gate above. Freeze immutable source
   coordinates and a stable initiating key. Validate source ownership and the exact
   provider event envelope/authentication. Check budgets, adapter health and allowed
   actions before claiming the job. Missing/deleted/uncertain parent, unresolved
   identity/fields, invalid origin, or deficient adapter means zero external writes.
2. **Claim and normalize.** Atomically claim the stable key in a durable ledger,
   binding it to canonical payload digest, source root, run owner and version. Reject
   malformed/oversized data, unsupported actions, conflicting payloads and replay
   outside policy. Report and webhook bodies are untrusted data, never instructions.
   Normalize only allowed fields; retain small metadata/artifact pointers rather
   than media bytes or copied private transcripts.
3. **Investigate and triage.** Read the full source thread/attachments. Perform a
   bounded cause/history pass and distinguish facts from hypotheses. Classify bug,
   performance, feature, question/feedback, or reroute. Search for duplicates using
   the criteria above. A plausible related live issue stops new-ticket creation;
   ambiguity goes to human judgment. Model judgment proposes classification and
   evidence links; deterministic guards validate authority and write eligibility.
4. **Optional ticket and verdict.** This stage remains disabled without explicit
   external-write authority. A clear new live defect with resolved fields may create
   a self-contained ticket with expected/actual behavior, reproduction evidence and
   source link. A confident duplicate may add recurrence without replacing unrelated
   fields. Preflight the original parent again before every write. Publish one concise
   verdict ending in exactly one configured marker; read back that it landed under
   the same root. Never fall back to channel root, DM or another destination. Bound
   authorized direct-question/correction follow-up; no second marker or side chatter.
   If a created ticket cannot be handed off, compensate by verified cancellation or
   closure; unknown compensation status stops and escalates in run diagnostics.
5. **Optional reproduction and fix.** A ready marker alone does not authorize work.
   Accept only an unexpired, nonconflicting marker from the configured trusted author
   in the original thread after setup/triage contracts pass. Missing or conflicting
   markers stop silently outside run diagnostics. A person actively implementing
   owns the fix; diagnostic utility bots do not. An existing concrete PR/commit
   changes the operation to verification-only. Perform two independent exact
   user-interface reproductions with reset and discriminating media/state evidence,
   recheck ownership, and allow only the separately authorized bounded root-cause
   edit. Compare baseline and patched behavior with equal inputs and identical
   after-proof plus required checks. Uncertain media or a nonreproducing baseline
   cannot establish success. A separately authorized draft PR may be opened with
   evidence; never merge or deploy from intake. Report blocked, could-not-reproduce,
   verified, or draft-open according to the actual result.
6. **Record and clean.** Keep operational status separate from immutable source
   coordinates. Append timestamp, run/owner, phase, decision, reason, evidence pointer
   and result to the run trail. Keep evidence outside source control under the
   configured retention policy; redact secrets/private payloads. Clean only owned
   sessions and scratch state, including failed attempts, preserving proof. Return
   actual state and the first unmet gate; no success-shaped no-op.

## Server-side webhook contract

A browser button, if present, calls the application server; only that server may
send to the configured authenticated webhook. The explicit logical payload contains
schema version, stable event ID, allowed action, immutable source coordinates,
artifact pointers and minimal nonsecret result fields. Provider-specific envelope,
field encoding, authentication/signature verification, timestamp/replay window,
timeout, size limits and allowed receiver actions remain UNRESOLVED until the actual
provider documentation and adapter are selected. Do not invent an endpoint or protocol.

Validate every field and action on the receiver. The receiver may only perform
explicitly configured actions, with independent ownership/authority guards. Retain
a durable event queue when delivery can fail, drain safely, and use stable keys and
delivery readback to avoid duplicate effects. Do not use polling as the primary
transport. Before activation, test a harmless ignored/disposable action against the
real served endpoint with authorized delivery/readback; this document performs none.

## Idempotency, interruption, retries, and recovery

The persistent ledger records claimed, validated, triaged, effect-intent,
effect-observed, compensated, completed, blocked and unknown-outcome phases. The
stable initiating key survives replay/recovery and is bound to payload and result.
Use atomic claim/replace or transactional compare-and-set with one canonical writer.
Retain deduplication state beyond the configured replay/recovery window. A duplicate
with the same digest reads/reconciles the previous result; a conflicting digest
stops for inspection.

Record an effect intent before a permitted external write and delivery/ticket ID
only after readback. If a crash occurs between them, read actual external state by
stable identity before retrying: the first write may have landed. Apply only the
missing difference. Never blindly retry a create, reply or delivery. Locks/claims
become stale only from reliable owner/lease evidence, not elapsed guessing. A stale
claim resumes from its last verified checkpoint after ownership reconciliation.

All attempt counts, time, cost and fan-out limits must be configured before
activation. Retry only classified transient failures within those limits; exhausted
retries stop as blocked/unknown with evidence. Missing tools/auth, malformed data,
permission failures, uncertain parent/ownership and unresolved fields fail closed.
No retry redirects the destination or broadens permissions. Reversion/compensation
and delivery reconciliation need verifiable readback. Stop on budget exhaustion,
human ownership, unavailable prerequisite or permission boundary.

## Acceptance, evidence, and scenario checks before activation

| Scenario | Required observable result |
| --- | --- |
| Valid unique trusted report | One claim, bounded triage, evidence-backed result; effects only if separately authorized |
| Duplicate delivery or concurrent workers | One owner/effect; prior result read back, same source root preserved |
| Same key with altered payload | Conflict recorded; zero new effects |
| Crash before/after external response | Reconcile actual state by key, no blind resend/create |
| Malformed, spoofed or instruction-bearing body | Reject/ignore as data; zero privileged effects |
| Missing/deleted/uncertain parent | Zero replies/tickets; run diagnostics only |
| Trusted identity absent, conflicting or expired marker | Stop reproduction/fix without source messages |
| Related live issue or active human implementation | No new duplicate ticket/fix; concrete PR/commit means verification-only |
| Tracker handoff fails | Compensate new ticket and verify closure, or mark unknown and stop |
| Missing tool/adapter/secret or exhausted budget | Blocked/unavailable with exact unmet gate; no success claim |
| Resumption and cleanup | Continue only missing stages; owned scratch removed, retained proof accessible |

Before activation demonstrate immutable root coordinates, thread-only output, one
trusted marker, isolated child write capabilities, missing-parent zero writes,
duplicate/crash/malformed-input/retry/recovery semantics, real control reset/proof,
and harmless webhook delivery/readback. Record target revisions, exact inputs,
actions, return/exit/readback values and evidence pointers for each. Local document
checks validate specification coverage only; they are not live workflow tests.

## Open decisions and next implementation boundary

Choose source/adapter identities, repository/default branch, coordinator, immutable
root policy, trusted marker contract, routing map, budgets/retention, server/provider
and secret/access facilities. Preserve provider/adapter alternatives until those
choices are supported. No experimental agent stack or standing service is prescribed.
The next boundary is a separately authorized local implementation/adapter contract
validation with disposable fixtures. Live activation, scheduling, installation,
messages, ticket/PR writes and network delivery each remain disabled pending their
required authority and passing acceptance evidence.
