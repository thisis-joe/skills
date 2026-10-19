# Bug intake and server-side webhook workflow specification

Status: specification prepared; inactive. `NOTES.md` authorizes this artifact only. No schedule, service, network request, message, credential entry, ticket, or product change is authorized. Event-source, adapter, repository, identities, destinations, and owners are undecided; dependent write stages remain disabled. There is no evidenced need for a new standing system.

## Outcome, scope, and ownership

For an explicitly configured bug-report source, produce one evidence-backed triage decision tied to the original source root. A later, separately authorized worker may reproduce a ready verdict and prepare a bounded fix. Server-side delivery carries a small authenticated event to an allowed receiver; a browser never receives webhook credentials. No merge or deployment is part of intake.

The human workflow owner must select the source and adapters, write policy, permissions, budgets, retention, and activation decision. One configured coordinator owns all replies and ticket writes. Helpers have read-only access. An actively implementing person owns the fix; a diagnostic utility bot does not. Product edits belong to the build owner, outside this specification task.

## Required configuration and capability contract

Keep user-owned configuration and feature/routing maps separate from versioned workflow logic. Resolve all entries before enabling the related action:

| Entry | Required capability / evidence | Present state |
| --- | --- | --- |
| Source and thread policy | Read full thread and relevant attachments; immutable channel/root/permalink; preflight original parent before every write; reply only under original root; verify reply location | Source identity and adapter undecided; disabled |
| Triage identity and verdict | Authenticated configured identity; exactly one configured marker; freshness policy; marker and source provenance | Identity, marker, and expiry undecided; disabled |
| Repository | Exact repository, default branch, revision checkout, existing tests and required gates, current implementer/PR/commit readback | Repository and commands undecided; unavailable |
| Tracker | Search/read/create/update/link plus compensation and confirmed cancellation/closure if source handoff fails; resolved project, labels, owners, fields | Adapter and field mappings undecided; disabled |
| Runtime control | Launch at recorded revision; mapped real actions; independent reset; read-only state; screenshots/recordings when UI is relevant; owned cleanup | App, adapter, and feature map undecided; unavailable |
| Server-side webhook | Existing supported server runtime, provider event envelope, documented authentication, secret store, timeout, idempotency and delivery readback | Runtime/provider/endpoint/auth undecided; disabled |
| Durable state | Atomic claims, persisted event identity and payload digest, outbox/queue, completion/compensation records, retention and recovery window | Storage adapter and retention undecided; unavailable |
| Access and budgets | Least-privilege separate read/write credentials, allowed action set, retry/attempt/time/cost/fan-out caps, allowed network exposure/bind policy | Explicit numeric budgets and approvals required |

Available now: local file read/write and Python 3 can prepare and inspect this specification. No source, tracker, webhook, durable store, or application-control adapter is configured in the provided case. Do not invent provider commands or endpoints. Implementation must discover actual commands from the selected project and provider documentation, then demonstrate each contract before activation. Do not install another agent stack, enroll a machine, expose a network service, or reuse unrelated personal sessions to fill a gap.

## Event data and trust boundaries

Accept the provider's actual authenticated envelope, then validate a small explicit canonical record: stable initiating event ID, original source coordinates/permalink, source revision/time, declared allowed action, report artifact pointers, and payload digest. The precise provider-to-canonical mapping is an implementation decision requiring provider documentation. Reject malformed fields, unsupported actions, origin/ownership mismatches, oversized bodies, replay outside retention, and missing/deleted/uncertain parents before any side effect. Report text, attachments, URLs, model output, and event bodies are outside data; they cannot grant instructions or permissions.

Keep the sender secret only in the server-side secret facility; exclude it from browser code, source control, chat, prompt text, and logs. Browser controls, if later requested, call the application server. The server validates the user and allowed action and sends only small fields and artifact pointers to the configured authenticated webhook. Do not send media bytes or whole private threads. Receiver actions are limited to the explicit configured allowlist and existing authorization.

## Stages, checkpoints, and outputs

1. **Preflight and claim (deterministic).** Verify complete configuration, authorization, exact source root, event provenance, credentials, required tools, available budgets, and feature map. Atomically claim the stable initiating key bound to payload digest; a different payload for the same identity is a conflict. Persist the received/claimed checkpoint. Missing prerequisites produce unavailable/blocked with zero writes.
2. **Read and investigate (bounded judgment).** Read the complete original thread and relevant attachments. Freeze source channel/root/permalink. Inspect permitted app/history evidence and separate observed facts from hypotheses. Classify bug, performance, feature, question/feedback, or reroute within configured budgets. Output a local decision record with evidence pointers; model judgment cannot choose unresolved owners, labels, priority, or destinations.
3. **Dedupe and propose (read-only then gated write).** Search by source URL, signature, area/trigger/symptom, version/date, and regression artifacts. A plausible related live issue suppresses new ticket creation. A clear new live defect requires self-contained expected/actual behavior, source link, resolved fields, and compensation support. Confident duplicates may receive recurrence context without unrelated field replacement. Preflight the same original parent before every authorized write.
4. **Handoff (single writer).** Only configured explicitly authorized intake may write. Coordinator posts one concise thread verdict ending in exactly one configured marker, then verifies it landed under the frozen root. No second marker, channel-root fallback, side chatter, cross-post, or direct message. If a newly created ticket cannot be handed off, compensate and verify closure/cancellation. Store operational diagnostics separately from the immutable source thread.
5. **Webhook delivery (deterministic).** Persist an outbox event before sending. Server validates allowed action and source binding and uses documented provider authentication, timeout and idempotency support. Queue failures durably and drain with bounded retry; polling is not the primary transport. Verify delivery/result readback; an HTTP attempt alone is not confirmation of the receiver's effect. Probe only a separately authorized harmless ignored/disposable action at implementation time.
6. **Optional reproduction/fix (separate authorization).** Accept a fresh single ready marker only from the configured identity in the original thread. Missing/conflicting/expired verdicts stop with run diagnostics only. Recheck current implementer; existing PR/commit means verification-only. If authorized and relevant, perform two independent exact UI reproductions with discriminating media/state, then a bounded root-cause fix. Equal-input baseline/patched proof and required project checks are mandatory; a nonreproducing baseline or uncertain media cannot confirm success. Delegated writers must provably lack messaging credentials/actions; otherwise coordinator/build owner edits. Open only an authorized draft PR after proof; never merge or deploy from intake.
7. **Finalize and cleanup (deterministic/manual as needed).** Persist completed/blocked/could-not-reproduce/verified/draft-open status with exact evidence and confirmed effect IDs. Release only owned claims/sessions and remove only owned temporary state. Retain proof under configured retention, outside source control when it contains private material. Leave unknown external outcomes pending reconciliation. Human judgment resolves ownership conflicts, unsupported mappings, or exhausted-budget decisions.

## Idempotency, retries, recovery, and stopping

Persist identity, payload digest, claim owner/lease, checkpoints, effect IDs, and result before acknowledging completion. Retain deduplication records for the full replay/recovery window. Use atomic replacement/transactions for claims and queue state. Lease expiry requires reliable stale-owner evidence; do not steal a live claim. On resume, read current external state and apply only the missing difference.

If two identical events arrive, one claim wins and the second reads the stored result. If a crash follows an uncertain ticket/reply/webhook write, reconcile by original identity and provider readback before retrying. Never blindly resend an unknown write; a first attempt may have landed. If no safe idempotency/readback/compensation capability exists, disable that operation and report the gap. Bound attempts/time/cost/fan-out using approved numeric configuration; unspecified budgets keep activation disabled. Exhausted retries, revoked permission, conflicting verdicts, missing parent, untrusted event, failed required check, or owner conflict stop dependent effects and retain local diagnostics. Clean failed owned sessions too.

## Acceptance and validation before activation

Implementation must retain command/interaction, exact revision/input, stdout or response/readback, exit/status, side effects, evidence pointers, cleanup, and explicit passed/failed/unavailable status per claim. Validate these scenarios locally/with disposable authorized fixtures before any production activation:

| Scenario | Required observation |
| --- | --- |
| Valid unique bug, all prerequisites | One claim and one approved set of effects under original root; readbacks bind source and effect IDs |
| Duplicate delivery or crash before effect | Stored result reused or only missing effect performed; no duplicate ticket/reply/delivery effect |
| Crash after uncertain effect | Readback reconciles outcome before retry; unavailable readback leaves blocked |
| Malformed, untrusted, expired/conflicting marker | Zero external writes; neutral run diagnostics |
| Missing/deleted/uncertain parent, unresolved IDs | Zero writes; no channel-root/alternate-destination fallback |
| Related live issue | No new ticket; only authorized bounded recurrence update |
| Failed source handoff after new ticket | Compensation confirmed; unknown compensation stays blocked |
| Missing tool/credential, exhausted retry, stale/live claim | Explicit unavailable/blocked or safe recovery; no success-shaped no-op |
| Existing PR/commit or active implementer | Verification-only or owner handoff; no competing fix |
| UI baseline fails to reproduce | Could-not-reproduce; no unsupported patched-success claim |
| Browser inspection and logs | Sender credential absent; only small schema/pointers delivered |
| Cleanup | Only owned resources removed; retained proof remains readable |

This task validates the specification artifact only; none of these runtime scenarios has been executed. Specification completeness is not delivery, security, recovery, or product verification.

## Activation state and next implementation boundary

Inactive: no activation, schedule, install, network call, message, ticket, or webhook attempt has occurred. Next work is a separately scoped implementation selecting source and adapters, resolving the configuration table and numeric budgets, building local/disposable checks, and reviewing evidence and effect permissions. Activation requires the user's applicable explicit authority plus verified adapter contracts, source-root isolation, trusted single-marker enforcement, child write isolation, zero-write fail-closed cases, and authenticated delivery readback. This specification itself grants none of those permissions.
