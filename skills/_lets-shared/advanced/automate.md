# Automation modes

Apply the [common contract](../contracts.md) and [resolved decisions](../decisions.md).
Choose CI, recurring work, webhook UI, sustained task execution, or report intake from the actual request.
Preparing automation is distinct from activating it; existing authorization and native runtime requirements govern each external action.
Never install another agent stack, invoke source skills, scan private transcripts, or infer publication permission from automatic mode.

## Define the operation

Record trigger, scope, inputs, output destination, owner, allowed tools/writes, budgets, stop predicate, and cleanup.
Resolve project commands and supported integrations from the actual environment; do not invent model IDs, endpoints, or capability names.
Keep versioned logic separate from user-owned configuration/maps and secrets; refresh managed files with diff review, preserving local edits.
Live instructions use stable project paths accessible to a fresh checkout, never machine-specific caches or uncommitted-only files.
Inspect existing matching automations before creating one; update rather than duplicate when the requested capability permits it.
Keep unchanged/nonactionable monitoring quiet unless periodic reports were requested; notify meaningful change, failure, completion, or required action.

## Retry and crash semantics

1. Read actual current state, compare with the intended state, and apply only the missing difference.
2. Ask what happens on two runs and after a crash at every interruption point, not only normal completion.
3. Make locks, claimed jobs, temporary files, and partial records recognizably stale from reliable evidence.
4. Use atomic replacement, unique event identity, content comparison, or reconciliation to prevent duplicate effects.
5. Prefer separate owned outputs over shared JSON fields; serialize structurally only when one canonical writer is necessary.

Bound attempts, time, cost, and fan-out. A failed prerequisite produces blocked/unavailable rather than a success-shaped no-op.
Unknown external outcomes require readback before retry, because the first write may have landed.

## CI and deployment preparation

Discover the existing stack, lockfiles, wrappers, merge requirements, and CI provider; preserve required checks.
Order cheap applicable static checks before focused tests, broader integration tests, and build/runtime gates.
Exercise local changes with the same commands used in CI and include service-readiness and isolated test-data setup.
Use test-scoped credentials in the secret facility, separate from production credentials and committed configuration.
When CI fails, read the failing child logs and classify code defect, stale base, environment, or supported flake before retrying.
One bounded fresh run can test an infrastructure hypothesis; the same failure again needs diagnosis, not repeated reruns.
Do not disable a gate, weaken thresholds, or skip tests to turn the pipeline green.
Optimize measured slow CI with sound caches, independent jobs, safe path filters, sharding, and test setup before buying more capacity.
For authorized deployment workflows define staging verification, rollout signals, rollback artifact/action, and flag retirement.
Green CI is an input to readiness, not evidence that production changed or a merge completed.

## Sustained task graph and recovery

Use for an authorized sequence; a single task does not need a standing multi-agent program.
Retain one authoritative task graph/state source with task IDs, dependencies, owner, branch/base, head, evidence, and commit.
[Build](build.md) executes dependency-ready tasks and owns their commits and completion updates.
Pilot one representative end-to-end unit before scaling an unfamiliar recipe; cheap repeated units can use the first normal unit as pilot.
Optional independent workers receive goal, scope, upstream evidence pointers, acceptance, exact checks/revision, budget, forbidden writes, and report shape.
Keep one writer per branch/state object; one designated owner mutates stack topology, and independent outputs merge at a controlled boundary.
Choose independent PRs versus a dependency chain from actual coupling and landing authority; do not silently merge a review-only stack.
Use a bounded rolling queue only when it saves time; no mandatory cloud tree, fixed lane count, model family, or nested coordinator.
Verify reports against actual output, exact revision/method receipts, and relevant required checks; missing slices/dropouts are gaps.
For material high-impact units use authorized independent verification; one cheap deterministic command need not become another agent.
Key verdicts to artifact/head and assumptions, invalidate affected receipts after changes, and recheck the actual merge result when dependencies drift.
After interruption inspect actual commits/evidence and reconcile task state before resuming the first incomplete ready task.
Late worker output must reconcile with the current branch/frontier; never blindly merge stale results.
Judge liveness from real task state, pushed artifacts, or supported process/status tools, not transcript timestamps or reassuring summaries.
Classify failures, retry within the common bound, reduce scope after capacity failures, and stop spawning when upstream acceptance/infrastructure is broken.
An explicit stop propagates to every active writer; preserve a resumable checkpoint rather than claim the predicate was met.

## Decision trail

For long/unattended work keep one append-only log with timestamp, phase, decision, reason, evidence pointer, and result.
Log checkpoints, accepted/reverted attempts, pivots, blockers, and repairs; skip obvious individual tool actions.
Keep cells single-line and neutralize spreadsheet-formula prefixes if using TSV/CSV; do not store secrets or raw private transcripts.
Identify run/owner boundaries when several runs append, and correct mistakes with superseding rows rather than rewriting history.
At handoff check claims against real actions/artifacts and add missing influential decisions; commit a trail only when the audit need warrants it.
State the unchanged done predicate and actual verified progress; a plateau or exhausted budget is not a pass.

## Webhook or bot UI

Use only when requested; provider-specific routine/secret-card/mesh commands are not prerequisites.
Keep the sender credential in the server-side secret facility, never browser code, chat, logs, prompt text, or version control.
Browser buttons call the application server; that server sends a small explicit schema to the configured authenticated webhook.
Treat event bodies as outside data, validate fields/allowed actions, and parse the provider's actual event envelope.
Use documented authentication, timeout, idempotency/retry behavior, and delivery readback; probe with a harmless ignored/disposable action.
If delivery can fail, retain a durable event queue and drain safely rather than polling as the primary transport or duplicating effects.
Send small event fields and artifact pointers rather than media bytes; document exactly which actions the receiver may perform.
For private network access reuse existing identity, choose intended bind/access restrictions, and verify the real served endpoint.
Network exposure, machine enrollment, new services, or credential changes follow their own user/runtime authorization; never install them from a source recipe.

## Report-intake setup

Configure explicit source channel/thread policy, trusted triage identity, repository/default branch, tracker adapter, control adapter, feature map, and budgets.
Require tracker search/read/create/update/link and compensation for a failed source handoff; unresolved IDs/labels/owners fail closed for writes.
Require app launch at a revision, mapped real actions, independent reset, read-only inspection, screenshots, recording, and cleanup.
Keep user-POV feature/routing maps outside managed automation logic; defaults never guess owners or broad on-call pings.
Before activation prove immutable root coordinates, thread-only output, one trusted verdict marker, child write isolation, and zero writes on missing/deleted/uncertain parent.
Keep operational status separate from the immutable source thread, and retain evidence outside source control according to configured retention.
If an adapter cannot meet the required contract, leave that operation disabled and report the missing capability.

## Intake triage condition

Only an explicitly authorized configured intake may write replies/tickets. One coordinator owns writes; assistance is read-only with no credentials/write actions.
Freeze source channel/root/permalink, read the full thread and relevant attachments, and preflight that same parent before every write.
Classify bug, performance, feature, question/feedback, or reroute after a bounded cause/history pass; separate facts from hypotheses.
Dedupe by source URL, signature, area/trigger/symptom, version/date, and regression artifacts. A plausible related live issue means no new ticket.
Create only a clear new live defect with resolved fields, source link, self-contained expected/actual behavior, and compensation support.
Update confident duplicates with recurrence without unrelated field replacement; never guess owner, priority, labels, or destination.
Post one concise authorized thread verdict ending in exactly one configured marker and verify the reply landed under the original root.
If a newly created ticket cannot be handed off, compensate and verify cancellation/closure; never retry at channel root or another destination.
Bound direct-question/correction follow-up; no second marker, unsolicited cross-post, DM, or side chatter.

## Intake reproduction and bounded fix

Accept a marker only from the configured identity in the original thread; missing/conflicting/expired verdicts stop silently outside run diagnostics.
A person actively implementing owns the fix; diagnostic utility bots do not. A concrete existing PR/commit switches to verification-only.
Follow [debug](debug.md) for two independent exact UI reproductions, discriminating media/state proof, ownership recheck, and bounded root-cause fix.
Use [verify](verify.md) for equal-input baseline/patched proof; uncertain media or a nonreproducing baseline cannot confirm success.
Delegated writers must provably lack messaging credentials/actions; otherwise the coordinator/build owner performs the edit.
After identical after-proof and required checks, open only an authorized draft PR with evidence; never merge or deploy from intake.
Clean every owned session and failed attempt, preserve proof under retention policy, and report truthful blocked/could-not-reproduce/verified/draft-open outcomes.

## Return

Report the prepared or active operation, scope/authority, tested crash/retry behavior, real evidence, persisted state, and exact activation/blocker status.
Do not claim a schedule was created, a webhook delivered, a PR merged, or a deployment succeeded without supported readback.
