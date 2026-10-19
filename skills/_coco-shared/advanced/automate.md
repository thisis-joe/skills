# Automation modes

Apply the [common contract](../contracts.md) and [resolved decisions](../decisions.md).
Choose CI, recurring work, webhook UI, sustained task execution, or report intake from the actual request.
Preparing automation is distinct from activating it; existing authorization and native runtime requirements govern each external action.
Never install another agent stack, invoke source skills, scan private transcripts, or infer publication permission from automatic mode.

## Mode selection

Keep the common contract and all core sections below active for every operation. Evaluate every
condition independently against the work being designed, prepared, or executed, and load all
matching modules cumulatively before the first action that depends on them. Re-evaluate when new
scope, risk, state, or missing prerequisites are discovered. If applicability is uncertain, read
the relevant modules broadly; if the work cannot be classified, read all automation modules.
If a required reference is unavailable, stop the dependent work and report the missing guidance
rather than infer it. Select internally from the actual request and artifacts; never require the
user to learn or choose source skills or internal mode names.

Loading a module supplies its constraints and dependencies; it does not authorize execution,
activation, messaging, tickets, deployment, or a wider scope. For a specification-only request,
read matching execution modules to preserve their requirements, then return the specification;
do not execute or activate the operation. Existing user authorization and native runtime boundaries
still govern every effect. Intake dependencies below apply even when only a later stage is requested.

| Condition in the requested work or current evidence | Read before dependent work |
| --- | --- |
| CI/CD, build/test gates, pipeline failures, or deployment preparation are involved. | [CI and deployment preparation](automate-ci.md) |
| An authorized task sequence, worker queue, dependency graph, interruption, or sustained recovery needs orchestration. | [Sustained task execution](automate-sustained.md) |
| A requested webhook or bot UI, authenticated event delivery, or its transport is involved. | [Webhook or bot UI](automate-webhook.md) |
| Report intake is configured, prepared, activated, or its integration contracts are designed. | [Report-intake setup](automate-intake-setup.md) |
| Report intake investigates/classifies/deduplicates reports or may write a verdict, reply, or ticket. | [Report-intake setup](automate-intake-setup.md), then [intake triage](automate-intake-triage.md), even for an existing configured intake. |
| Intake reproduces or verifies a report, follows a verdict marker, or attempts a bounded fix or draft PR. | [Report-intake setup](automate-intake-setup.md), [intake triage](automate-intake-triage.md), then [intake reproduction and fix](automate-intake-fix.md); setup and triage remain prerequisites. |
| Explicitly requested repeatable/manual setup needs a person's dashboard access, credential entry, or irreversible choice. | [Human-operated setup wizard](automate-wizard.md) |
| The requested deliverable is a reusable workflow specification, including a workflow-design interview. | [Workflow specification only](automate-specification.md), plus every other matching module for its constraints only. |

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

