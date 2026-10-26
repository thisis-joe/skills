# Procedure refinement execution plan

Spec: [authorized scope](../specs/procedure-refinement.md).
Branch: `experiment/coco-procedure-refinement`; base `f458420`, with completed
collaboration evidence integrated at `3123487`. Active candidate: `622975e`.
This file is the sole execution state for this documentation/experiment task.

| Unit | Acceptance | State |
| --- | --- | --- |
| D1 Integrate completed evidence | Preserve both studies and their distinct scopes; no active skill change | complete / `3123487` |
| D2 Freeze isolated comparisons | R5/R2/R7 single-factor copies, five pairs each, held-out discovery domains, guards and independent review | complete / `d524ec9`; independent actor blockers closed before execution |
| D3 Execute and audit | Real CLI development and fresh pickup; advice read-only; failures, costs, source reads and controls retained | complete / `a79bb7d`; 30 attempts, 40 actor contexts, 32 native grades. R5 has four usable pairs and one retained unresolved pair; R2/R7 valid. Collection-only correction `1aa9060` preserves original grades |
| D4 Update report and reduction plan | Bound v2 claims, retain 0.2.0 evidence, strengthen preservation gates, report candidates separately | complete; interpretation/gates `52cbe73`, final outcomes and independent review in the closing documentation commit |
| D5 Close | Independent claim review, required checks, links, active/source immutability, work-unit commits | complete; validator and 168 tests pass; independent review approves bounded claims, links and preserved-source checks pass; closing commit recorded in branch history |

The comparison uses the decision-bearing development snapshot in both earlier
reports, not another release branch. Existing untracked reference archives in
the separate collaboration worktree are unrelated and remain untouched.

## Closure receipts

- [Sandbox report](../evaluation/procedure-refinement/report.md) and
  [independent final review](../evaluation/procedure-refinement/final-review.md).
- [Required checks](../evaluation/procedure-refinement/evidence/required-tests.log):
  package validation and 168 tests pass. The full suite ran again after the
  collection-only correction; no actor or judge was replaced.
- Archive digest, original actor/judgment bytes, all eight frozen actor
  dependencies and both analysis epochs independently verified. R5 measurement
  limitations remain unresolved, rather than being counted as valid completions.
- `git diff --exit-code 622975e -- skills sources` and the original staged-report
  preservation check pass. No untracked skill/source additions, installation,
  push or release. The primary checkout remains on `release/npm-1.0.0`.
- Work units are separately committed: integration `3123487`, frozen actor
  design `d524ec9`, interpretation/acceptance `52cbe73`, analysis support `8c0a1a4`,
  transparent collection correction `1aa9060`, results `a79bb7d`, then the final
  documentation/closure commit on `experiment/coco-procedure-refinement`.
