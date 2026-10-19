---
name: lets-ship
description: "Use when preparing a PR, deciding release readiness, planning a staged launch, or executing an already authorized release. PR·출시 판단·롤백 준비."
license: MIT
---

# let's-ship

Produce an evidence-backed readiness decision and distinguish it from actual deployment.

Read the [common contract](../_lets-shared/contracts.md) before acting. Load [advanced modes](../_lets-shared/advanced/ship.md) only when the task needs their additional procedure. The [integration decisions](../_lets-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Identify the exact candidate commit/artifact, acceptance scope, target environment and existing release policy. Read its current review and required test/build/runtime evidence.
2. Aggregate unresolved spec/quality/security findings, dependency/audit evidence, performance/accessibility when relevant, infrastructure, documentation and observability readiness. Missing mandatory evidence blocks readiness.
3. Define staged rollout, owner, measurable success/hold/rollback criteria, error-budget gate and tested recovery commands. Treat data recovery separately from application rollback.
4. For PR preparation, present the concrete behavior change and validation, link authoritative artifacts and preserve feature/work-unit history. Creation, posting and merging follow the requested scope.
5. Execute deployment only when actually authorized through the available runtime. After execution, verify live health and the intended flow; report deploy/rollback state separately from GO/NO-GO.
6. Keep required specialist verdicts distinguishable. When independent reviewers cannot run, state degraded coverage rather than pretending a parallel review happened.

Return: ready/blocked decision with reasons and residual risks, candidate ID, rollout/recovery plan, and actual publication/deployment state if performed.
