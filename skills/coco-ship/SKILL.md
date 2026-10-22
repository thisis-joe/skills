---
name: coco-ship
description: "Use when preparing a PR, deciding release readiness, planning a staged launch, or executing an already authorized release."
license: MIT
---

# coco-ship

Produce an evidence-backed readiness decision and distinguish it from actual deployment. Merging an already pushed PR/MR into its target branch without a readiness decision is `coco-merge`.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for PR or version preparation for published consumers, a dependent PR stack, staged rollout with error-budget, SLO or feature-flag gates, rollback and post-deploy proof, and PR supervision (check, threads-only, drive, background). If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/ship.md) before dependent work.

## Procedure and output

1. Identify the exact candidate commit/artifact, acceptance scope, target environment and existing release policy. Read its current review and required test/build/runtime evidence. Verify behavior at runtime, not merely compilation, in every mode including PR preparation: observe the changed path run, for example with a disposable database or service probe; missing runtime evidence stays pending.
2. Aggregate unresolved spec/quality/security findings, dependency/audit evidence, performance/accessibility when relevant, infrastructure, documentation and observability readiness. Missing mandatory evidence blocks readiness. Once a blocker is confirmed, gather only evidence that could change the verdict and reuse CI or recorded results instead of rerunning them.
3. For an authorized deployment or staged release, define staged rollout, owner, measurable success/hold/rollback criteria, error-budget gate and tested recovery commands; otherwise give the revert path in one line. Plan data recovery separately from application rollback whenever data or schema changes.
4. For PR preparation, present the concrete behavior change and validation, link authoritative artifacts and preserve feature/work-unit history. Creation, posting and merging follow the requested scope.
5. Execute deployment only when actually authorized through the available runtime. After execution, verify live health and the intended flow; report deploy/rollback state separately from GO/NO-GO.
6. Keep required specialist verdicts distinguishable. When independent reviewers cannot run, state degraded coverage rather than pretending a parallel review happened. Skip independent specialist fan-out only for a lightweight change: by default at most two files and under 50 changed lines, touching no auth, payments, data access, configuration or environment, migrations or schema, dependencies or lockfiles; project rules may set other limits. Lightweight never skips required checks, the runtime check or the revert line.

Return: ready/blocked decision with reasons and residual risks, one plain sentence on each blocker's consequence, candidate ID, revert path or rollout/recovery plan, and actual publication/deployment state if performed.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "It works in staging, it'll work in production": production data and traffic differ; monitor after deploy.
- "Rolling back is admitting failure": shipping a known-broken feature is the failure.
- "The error rate looks fine": check budget burn rate against baseline, not only the current threshold.
- "It's just a small fix, bump the patch": a behavior consumers rely on makes it a breaking change; write the consumer-facing changelog entry with the change.
- Deploying without a tested rollback or monitoring, flags without owner or expiry, or force-pushing shared branches.
