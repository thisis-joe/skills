# Workflow value v2 plan

Spec: [workflow value](../specs/workflow-value-v2.md).
Branch: `experiment/coco-workflow-v2`, based on `648283a` (includes `cd132c7`).
Candidate skills remain `622975e`; existing comparison is preserved on
`experiment/coco-collaboration-value`. This is the authoritative task state.

| Unit | Acceptance | State |
| --- | --- | --- |
| V1 Freeze procedure/usability protocol | Three comparable conditions, observable axes, independent design check | complete / `fc97274`; independent blockers repaired before primary |
| V2 Execute matched handoff/selection | Five per condition/family; actual cold successor and CLI checks; retain failures | complete / 30 projects, 45 fresh native contexts; no actor reruns or active-skill changes |
| V3 Blind analysis | Common rubric, independent judgments, negative controls, pairwise findings | complete / `1a01e6d` support; 32 grades, two controls rejected, 30 eligible source audits |
| V4 Report v2 and close | Original preserved; evidence/limits; required tests/validator; independent review; commits | complete / report-v2 and independent final review in this closure commit; evidence in `df6eaba` |

A separate two-arm collaboration experiment was already running when v2 began.
Its source, profiles, records and projects were not altered by this evaluation;
its observations are not pooled into this three-condition report.

## Closure receipts

- [Report v2](../evaluation/staged-development/report-v2.md) evaluates procedure
  clarity, consistency, independent pickup and selection separately from coding
  superiority. Both requested comparator assessments are explicit.
- [Final independent review](../evaluation/workflow-v2/final-review.md) checked
  claims against retained evidence. Framework/table counts and the unquantified
  files-read/reconstruction measures were corrected without changing grades.
- Required validator passed: 29 skills, source checksums, coverage and references.
  All 156 unit tests passed; the complete log is in the evidence commit.
- `git diff --check` passed. `git diff 622975e -- skills sources
  docs/evaluation/staged-development/report.md` was empty: active skills, inert
  source evidence and the original report are preserved.
- Commits: `fc97274` protocol/runner; `1a01e6d` blind analysis and eligibility;
  `df6eaba` measured results and native archive; this commit closes the report.
  No push, publication or global skill installation was performed.
