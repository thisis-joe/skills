---
name: lets-review
description: "Use when reviewing committed or work-in-progress changes against requirements, repository standards and quality, or challenging a consequential design claim. 코드 리뷰·중요 판단 검토."
license: MIT
---

# let's-review

Assess the actual change without changing it or hiding a failed review axis.

Read the [common contract](../_lets-shared/contracts.md) before acting. Load [advanced modes](../_lets-shared/advanced/review.md) only when the task needs their additional procedure. The [integration decisions](../_lets-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Freeze the task's base/HEAD, selected paths, staged/unstaged/untracked files and snapshot. Use the shared review-scope tool when available; inspect actual content including new files. An empty HEAD diff does not mean there is no work to review.
2. Read the originating requirement and repository standards. Missing spec means spec comparison is unavailable, not automatically passed. Read tests and evidence alongside implementation.
3. Keep three independent verdicts: spec/acceptance, standards, and quality/risk (correctness, readability, structure, security, performance). Check threshold reductions, weakened tests, dead code and dependency changes. Distinguish real defects from preference.
4. Write one actionable finding per defect with severity, location, failure mechanism and supporting evidence. Link all affected axes instead of duplicating the same fix or letting one passing axis mask another.
5. For a consequential in-flight claim, give a fresh reviewer the smallest artifact plus contract, not the author's reasoning. Reconcile findings against the code; stop adversarial cycles after three or when only resolved/trivial issues remain. Report degraded independence where applicable.
6. Return findings and verdicts to the execution owner. Do not modify files or commit during review. Any later code change invalidates the affected portion of this scope's approval.

Return: frozen scope, per-axis verdicts/findings, checks actually examined and remaining limitations.
