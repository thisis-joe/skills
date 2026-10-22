---
name: coco-debug
description: "Use when tests fail unexpectedly, builds break, behavior is wrong, a regression is intermittent, or a performance failure needs root-cause diagnosis."
license: MIT
---

# coco-debug

Construct a red-capable feedback loop and establish the supported cause.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a failure without an obvious red signal, an intermittent or nondeterministic fault, a regression that needs bisection, a second failed fix resting on one premise, verification of an existing PR or commit fix, performance or captured-artifact (profile, heap, trace) diagnosis, and configured report intake. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/debug.md) before dependent work.

## Procedure and output

1. Stop adding unrelated behavior and preserve relevant error/environment evidence with secrets redacted. Determine whether the failure predates this task.
2. Obtain an agent-runnable symptom-specific red signal: test, HTTP/CLI script, browser action, replay or isolated harness. For nondeterministic faults, pin conditions and raise reproduction rate. Do not confuse a different failure or a mock-only assertion with the reported bug.
3. Minimize the repro while retaining the triggering mechanism. State ranked falsifiable hypotheses and use targeted probes or bisection to distinguish them; change one variable at a time.
4. For performance, measure first rather than guessing from logs. Tag temporary instrumentation so it can be removed.
5. When a correct test surface exists, make the minimized repro fail before applying the fix, then pass; rerun the original full scenario. If no adequate surface exists, retain reproducible evidence and report the architectural gap.
6. If two fixes sharing one premise fail the same gate, write that premise down and test it with an observation that would differ if it were false before any third fix, following the [premise rule](../_coco-shared/advanced/debug.md#test-competing-causes). Remove owned temporary probes, preserve useful evidence and hand the verified fix to the build owner for review/commit/state. After repeated inconclusive attempts, report what is needed to proceed.

Return: reproducible invocation and observed failure, supported cause, fix/regression evidence, cleanup result and remaining uncertainty.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "I know what the bug is, I'll just fix it": reproduce first; an unreproduced fix is a guess.
- "The failing test is probably wrong": prove it, then fix the test; never skip it.
- "It's flaky, ignore it": measure the failure rate and pin conditions; intermittency hides real defects.
- "It works now" without a supported mechanism, or several unrelated edits made while debugging.
- A third fix resting on a premise two fixes already failed on: test the premise first (step 6).
