---
name: coco-ship
description: "Use when preparing a PR, deciding release readiness, planning a staged launch, or executing an already authorized release."
license: MIT
---

# coco-ship

Produce an evidence-backed readiness decision and distinguish it from actual deployment. Merging an already pushed PR/MR into its target branch without a readiness decision is `coco-merge`.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for PR or version preparation for published consumers, a dependent PR stack, staged rollout with error-budget, SLO or feature-flag gates, rollback and post-deploy proof, and PR supervision (check, threads-only, drive, background). If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/ship.md) before dependent work.

## Procedure and output

1. Identify the exact candidate commit/artifact, acceptance scope, target environment and existing release policy. Read its current review and required test/build/runtime evidence.
2. Aggregate unresolved spec/quality/security findings, dependency/audit evidence, performance/accessibility when relevant, infrastructure, documentation and observability readiness. Missing mandatory evidence blocks readiness.
3. Define staged rollout, owner, measurable success/hold/rollback criteria, error-budget gate and tested recovery commands. Treat data recovery separately from application rollback.
4. For PR preparation, present the concrete behavior change and validation, link authoritative artifacts and preserve feature/work-unit history. Creation, posting and merging follow the requested scope.
5. Execute deployment only when actually authorized through the available runtime. After execution, verify live health and the intended flow; report deploy/rollback state separately from GO/NO-GO.
6. Keep required specialist verdicts distinguishable. When independent reviewers cannot run, state degraded coverage rather than pretending a parallel review happened.

Return: ready/blocked decision with reasons and residual risks, candidate ID, rollout/recovery plan, and actual publication/deployment state if performed.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "It works in staging, it'll work in production": production data and traffic differ; monitor after deploy.
- "Rolling back is admitting failure": shipping a known-broken feature is the failure.
- "The error rate looks fine": check budget burn rate against baseline, not only the current threshold.
- "It's just a small fix, bump the patch": a behavior consumers rely on makes it a breaking change; write the consumer-facing changelog entry with the change.
- Deploying without a tested rollback or monitoring, flags without owner or expiry, or force-pushing shared branches.
