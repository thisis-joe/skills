# Bug intake and server-side webhook workflow specification

Status: prepared specification only. No intake, schedule, service, agent, message,
network request, ticket write, repository write, or webhook delivery is activated.
The only authoritative input supplied is `NOTES.md`: it requests this artifact
and leaves source and adapter identities undecided. No operational examples,
existing application commands, provider contracts, or deployment configuration
were supplied. The design below preserves those open decisions.

## Outcome, trigger, ownership, and authority

The intended outcome is one traceable intake verdict for a source report and,
only under separately configured authority, evidence of a reproduced defect,
verified bounded fix, or explicit blocked/nonreproducing result. The webhook is
a server-side delivery boundary for small validated events. Intake is event
triggered; no cadence or polling job is authorized or required by this draft.

One configured coordinator owns source/tracker/external writes. Read-only
assistants receive no messaging credentials or write actions. An active human
implementer owns a fix; a diagnostic bot does not claim ownership. A live PR or
commit selects verification-only mode. No intake operation may merge or deploy.
The local specification author has only artifact-authoring authority.

The following configuration remains unresolved. All operational writes fail
closed until its identities and adapter capabilities are verified:

| Decision | Required value or capability | Why it blocks activation |
| --- | --- | --- |
| Source and destination | Source provider, allowed channel IDs, immutable root/thread coordinates and permalink, thread-only output policy | Prevents guessed or relocated replies |
| Trusted triage identity | Provider-authenticated identity and exactly one verdict-marker format, freshness policy | A body saying ready is not authority |
| Repository | Repository identity, default branch, permitted paths, exact revision and actual launch/test commands | Bounds reproduction and fixes |
| Tracker adapter | Search/read/create/update/link, resolved project/owner/labels/priority, compensation and readback | Prevents duplicates and orphan tickets |
| Control adapter | Launch at revision, real mapped actions, independent reset, read-only inspection, screenshots/recording and cleanup | Establishes discriminating runtime evidence |
| Webhook adapter | Sender/receiver identities, provider envelope, documented authentication and replay defense, timeout, delivery readback | Enables origin and outcome verification |
| Permissions and secrets | Minimum operation grants, distinct test/production secrets, server-side secret facility | Prevents browser or helper credential exposure |
| State and retention | Durable queue/ledger, atomic claim support, dedupe retention across replay/recovery, evidence destination and expiry | Makes retries and recovery safe |
| Operational budgets | Attempt/time/cost/fan-out limits, stale-claim rules and operator | Ensures finite runs and owned recovery |

These are implementation prerequisites, not authorization to select a provider,
install a service, broaden permissions, or run the workflow. Alternative source,
tracker, and runtime adapters remain valid if they meet the same contracts.

## Stages, inputs, outputs, and acceptance

| Stage | Input and owner | Action and output | Acceptance and evidence |
| --- | --- | --- | --- |
| 0. Preflight | Explicit configuration; coordinator | Read selected provider configuration and exact repository revision; verify tool availability and budgets | Each required capability is available; otherwise blocked with zero external writes |
| 1. Freeze source | Allowed source event; source-read adapter | Authenticate origin, read full original thread and attachments, freeze channel/root/permalink and payload hash | Parent exists with certain immutable coordinates; record safe evidence pointers |
| 2. Classify and dedupe | Frozen report; read-only triage judgment plus tracker-search adapter | Classify bug/performance/feature/question/reroute; distinguish facts from hypotheses; search by URL, signature, area/trigger/symptom, version/date and artifacts | A plausible related live issue stops new-ticket creation; unresolved classification stays diagnostic |
| 3. Authorized verdict | Resolved triage and destination; sole coordinator | Recheck original parent immediately before each write; update a confident duplicate or create only a clear new live defect with expected/actual, resolved fields and source link; post one concise original-thread verdict ending in exactly one configured marker | Readback proves correct parent, marker, ticket link and target. No root fallback, cross-post, DM or guessed owner/ping |
| 4. Reproduction gate | Original-thread trusted fresh verdict; coordinator and control adapter | Reject missing/conflicting/expired/untrusted markers into run diagnostics only. Recheck active implementation ownership and PR/commit state | Existing PR/commit means verification-only; missing authorization or ownership uncertainty stops privileged work |
| 5. Reproduce | Exact target revision and route; control adapter | Two independent exact UI reproductions, resetting between them; capture discriminating state/media and expected/actual | Baseline must reproduce; uncertain media or nonreproduction yields could-not-reproduce, never a success claim |
| 6. Bounded fix | Reproduced cause, approved paths/budget and ownership recheck; authorized build owner | Diagnose root cause, make minimum bounded change with equal-input baseline/patched proof and discovered required checks | Writer isolation must prove no messaging actions/credentials; otherwise coordinator/build owner edits. Scope expansion stops for a decision |
| 7. Handoff and cleanup | Verified revision and evidence; coordinator | Only if explicitly authorized, open a draft PR with proof. Preserve evidence, close owned sessions and reconcile job state | Readback verifies any draft PR; no merge/deploy. Failure remains truthful blocked/nonreproducing/verified/draft-open |

Every write repeats the original-parent preflight. Missing, deleted, or uncertain
parent means zero writes, including cancellation/handoff attempts that would
need that parent. Operational status lives in the ledger, separate from the
immutable source thread. If a newly created ticket cannot be handed off, invoke
and verify the tracker's configured cancellation/closure compensation; never
retry a reply at channel root or another destination. A failed compensation is
recorded for the configured operator without claiming cleanup succeeded.

## Webhook boundary and minimal event schema

A browser button calls the application's own server. The server reads a sender
credential from its secret facility and calls the configured authenticated
webhook. Credentials never enter browser code, chat, model prompts, logs, or
version control. No endpoint or provider-specific command is invented here.

The selected adapter must parse its documented envelope and verify sender
origin, signature/authentication, freshness and replay policy before interpreting
fields. Body identity fields alone are untrusted. Restrict sizes, field types,
allowed actions and artifact destinations; reject malformed, unknown or
out-of-policy input before any effect. Log only safe identifiers and pointers.

The internal schema must include a schema version, stable initiating event ID,
action from a configured allowlist, authenticated sender reference, immutable
source channel/root/permalink references, payload digest, event timestamp,
exact target revision when applicable, and small bounded artifact pointers.
Do not transmit screenshots/media bytes, secrets, or whole private transcripts.
The receiver's action list must explicitly map each action to an authorized
operation; a ready field cannot authorize arbitrary code or external writes.

Before any real activation, verify the real server binding/access restrictions
and intended identity. Probe delivery only with a separately authorized harmless
ignored/disposable action and verify receipt/readback. This specification has
not performed that probe or exposed any network endpoint.

## Idempotency, retries, crash recovery, and stop rules

Use a durable event queue when delivery can fail. Drain it safely using provider
events rather than polling as the primary transport. Keep event identity stable
through retries. In one atomic transaction, claim a ledger key bound to source
coordinates, operation, event ID and payload digest. A same-key/different-payload
conflict stops; a replay of a completed event returns the retained result.
Retain dedupe records for the configured maximum replay and recovery window.

The ledger stores received/validated/claimed/effect-pending/effect-confirmed/
compensation-pending/completed/blocked states, owner/lease, attempt count,
revision, result and evidence pointers. A worker reads actual state and applies
only missing differences. A crash before claim leaves a retriable received
item; a crash after claim requires lease/ownership reconciliation; a crash after
an external call but before receipt requires readback before retry. Unknown
external outcomes never trigger blind replays. If a provider cannot locate the
prior effect, stop for operator resolution rather than risk duplication.

Retries obey the configured attempt/time/cost limits, with no more than three
unsuccessful attempts at the same unresolved blocker. Missing configuration,
parent uncertainty, trust failure, conflicting verdict, stale ownership,
unavailable tools, exhausted budgets or out-of-scope work stop the relevant
operation. No success-shaped no-op. Stale locks are reclaimed only with reliable
lease/process/state evidence. Cleanup owns only this run's sessions and scratch
state; durable evidence and user work survive.

## Deterministic mechanics, judgment, and manual boundaries

Deterministic mechanics: schema/origin checks, immutable-coordinate comparisons,
atomic dedupe/claims, exact revision launch, command exits, queue state,
readback, retention and cleanup. Implement these with the selected adapters and
local application code, not model assertions.

Model judgment: bounded classification, related-issue assessment, cause
hypotheses and evidence interpretation. Keep fact/hypothesis separation and
attach source pointers; model output never grants authority. Human decisions:
resolve provider/owner/routing/budgets, any material requirement or scope change,
identity/credential/network setup and explicit permission for each external
effect class. Current authorization ends with this local document.

## Verification plan and evidence contract

Before activation, a local fake-adapter suite must exercise duplicate delivery,
same ID with altered payload, simultaneous claims, each crash boundary,
malformed/untrusted/expired events, wrong/deleted/uncertain parents, competing
markers, active implementation and existing PR routes, missing tools, exhausted
retries, failed handoff/compensation, resumption, and cleanup. Assert zero writes
on every failed gate and exact one authorized effect on valid replay. Pair
absence checks with positive cases proving the effect observer works.

The server adapter must then pass an authorized disposable end-to-end test of
browser-to-server-to-receiver flow, credential separation, actual delivery
readback and restart recovery. Reproduction acceptance requires independent
baseline and equal-input patched evidence. Logs must retain target snapshot,
input/action, expected/actual, exit/result, sanitized receipt and resolvable
artifact pointers. Never equate a static spec check with these runtime tests.

Available now: local files and Python standard-library commands for reading and
checking this document. Missing now: all operational identities, adapters,
application launch/test instructions, credentials and runtime evidence. Only
local document completeness checks were run; no workflow behavior, crash
recovery, provider delivery, message, ticket or fix has been executed.

## Next implementation boundary

Resolve the configuration table against a concrete repeated-work example,
confirm scope and effect permissions, select adapters, and implement a local
fake-adapter pilot. Verify all failure gates and recovery before seeking the
separately authorized disposable integration probe. No standing system,
activation, installation, scheduling, messaging, deployment or external service
call follows from this document alone.
