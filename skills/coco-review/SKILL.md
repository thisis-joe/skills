---
name: coco-review
description: "Use when reviewing committed or work-in-progress changes against requirements, repository standards and quality, or challenging a consequential design claim."
license: MIT
---

# coco-review

Assess the actual change without changing it or hiding a failed review axis. The normal build handoff is formal review after implementation commits; a direct request can review work in progress or an exact revision range without requiring a new commit. Prefer a fresh reviewer seeing requirements/artifacts rather than the author conversation; disclose missing independence for the user's decision. Apply the [transition contract](../_coco-shared/workflow.md) before sending fixes to build.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for freezing scope with the shared review-scope collector, dependency or lockfile changes, a suspicious diff, shared contract change or deletion that needs impact and safety facts, a requested or high-impact adversarial review, automated review comments, and comments or suppressions that encode constraints. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/review.md) before dependent work.

## Procedure and output

1. Freeze the task's base/HEAD, selected paths, staged/unstaged/untracked files and snapshot. For an exact commit or revision range, `git diff <range>` with `git status --porcelain` is that scope. Otherwise run the [review-scope collector](../_coco-shared/tools/review_scope.py) in the same batch as your first reads, `python3 <skill-dir>/../_coco-shared/tools/review_scope.py --repo <repo> --base <base-ref>` with `--path <task-path>` per task path; it compares from the merge-base with HEAD and prints JSON with the comparison commit, HEAD, a snapshot hash and each file's Git layers, so its source need not be read. Inspect actual content including new files. An empty HEAD diff does not mean there is no work to review.
2. Read the originating requirement and repository standards. Missing spec means spec comparison is unavailable, not automatically passed. Read tests and evidence alongside implementation.
3. Keep three independent verdicts: spec/acceptance, standards, and quality/risk (correctness, readability, structure, security, performance). Check threshold reductions, weakened tests, dead code and dependency changes. Distinguish real defects from preference.
4. Write one actionable finding per defect with severity, location, failure mechanism and supporting evidence. Link all affected axes instead of duplicating the same fix or letting one passing axis mask another.
5. For a consequential in-flight claim, give a fresh reviewer the smallest artifact plus contract, not the author's reasoning. Reconcile findings against the code; stop adversarial cycles after three or when only resolved/trivial issues remain. When a required fresh review was unavailable, say so in one line.
6. Return findings and verdicts to the execution owner. Do not modify files or commit during review. Any later code change invalidates the affected portion of this scope's approval.

Return findings first, most severe first; then the frozen scope, one line per axis verdict, the checks actually examined, and only limitations that change how the verdict can be used.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "It works" or "the tests pass, so it's good": tests miss architecture, security and readability; judge every axis.
- "It's just a version bump": read the changelog; one dependency per change keeps cause and revert clean.
- "We'll clean it up later" or a bare "LGTM": required fixes land before merge, with evidence of actual review.
- A refactor that moves code without reducing concepts, or a change that grows an already-large file or duplicates a canonical helper.
- Reviewer output trusted without rereading the artifact, the author's claim passed to the reviewer, or review rerun on an unchanged artifact.
