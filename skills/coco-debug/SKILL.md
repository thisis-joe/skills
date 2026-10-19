---
name: coco-debug
description: "Use when tests fail unexpectedly, builds break, behavior is wrong, a regression is intermittent, or a performance failure needs root-cause diagnosis. 버그 재현·원인 조사·복구."
license: MIT
---

# coco-debug

Construct a red-capable feedback loop and establish the supported cause.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/debug.md) only when the task needs their additional procedure. The [integration decisions](../_coco-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Stop adding unrelated behavior and preserve relevant error/environment evidence with secrets redacted. Determine whether the failure predates this task.
2. Obtain an agent-runnable symptom-specific red signal: test, HTTP/CLI script, browser action, replay or isolated harness. For nondeterministic faults, pin conditions and raise reproduction rate. Do not confuse a different failure or a mock-only assertion with the reported bug.
3. Minimize the repro while retaining the triggering mechanism. State ranked falsifiable hypotheses and use targeted probes or bisection to distinguish them; change one variable at a time.
4. For performance, measure first rather than guessing from logs. Tag temporary instrumentation so it can be removed.
5. When a correct test surface exists, make the minimized repro fail before applying the fix, then pass; rerun the original full scenario. If no adequate surface exists, retain reproducible evidence and report the architectural gap.
6. Remove owned temporary probes, preserve useful evidence and hand the verified fix to the build owner for review/commit/state. After repeated inconclusive attempts, report what is needed to proceed.

Return: reproducible invocation and observed failure, supported cause, fix/regression evidence, cleanup result and remaining uncertainty.
