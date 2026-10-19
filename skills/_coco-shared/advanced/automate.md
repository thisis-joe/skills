# Automation modes

Apply the [common contract](../contracts.md).
Choose CI, recurring work, webhook UI, sustained task execution, or report intake from the actual request.
Preparing automation is distinct from activating it; existing authorization and native runtime requirements govern each external action.
Never install another agent stack, invoke source skills, scan private transcripts, or infer publication permission from automatic mode.

## Mode selection

Evaluate each row independently; read all matches before dependent work. Re-evaluate on new scope, risk, state, or missing prerequisites. If uncertain, read relevant modes broadly; if unclassifiable, read all modes. Stop dependent work and report unavailable required guidance.

Apply the common contract and entire core even without matches. Select internally from request/evidence; users need not learn source skills or mode names. Reading grants no wider scope or authority. For specification-only requests, read matching execution modes for constraints; return the specification without executing/activating.

| When | Read |
| --- | --- |
| CI/CD, build/test gates, pipeline failures, or deployment preparation. | [CI](automate-ci.md) |
| Authorized task sequence, worker queue, dependency graph, interruption, or sustained recovery orchestration. | [Sustained](automate-sustained.md) |
| Requested webhook/bot UI, authenticated event delivery, or transport. | [Webhook](automate-webhook.md) |
| Report intake configured/prepared/activated, or its integration contracts designed. | [Setup](automate-intake-setup.md) |
| Intake investigation/classification/deduplication, or possible verdict/reply/ticket writes. | [Setup](automate-intake-setup.md), then [triage](automate-intake-triage.md), even for existing intake. |
| Intake reproduction/verification, verdict-marker following, or bounded fix/draft PR. | [Setup](automate-intake-setup.md), then [triage](automate-intake-triage.md), then [fix](automate-intake-fix.md). |
| Explicitly requested repeatable/manual setup needs dashboard access, credential entry, or irreversible human choice. | [Wizard](automate-wizard.md) |
| Reusable workflow specification, including workflow-design interview. | [Spec](automate-specification.md), plus other matches for constraints only. |

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

## Decision trail

For long/unattended work keep one append-only log with timestamp, phase, decision, reason, evidence pointer, and result.
Log checkpoints, accepted/reverted attempts, pivots, blockers, and repairs; skip obvious individual tool actions.
Keep cells single-line and neutralize spreadsheet-formula prefixes if using TSV/CSV; do not store secrets or raw private transcripts.
Identify run/owner boundaries when several runs append, and correct mistakes with superseding rows rather than rewriting history.
At handoff check claims against real actions/artifacts and add missing influential decisions; commit a trail only when the audit need warrants it.
State the unchanged done predicate and actual verified progress; a plateau or exhausted budget is not a pass.

## Return

Report the prepared or active operation, scope/authority, tested crash/retry behavior, real evidence, persisted state, and exact activation/blocker status.
Do not claim a schedule was created, a webhook delivered, a PR merged, or a deployment succeeded without supported readback.

