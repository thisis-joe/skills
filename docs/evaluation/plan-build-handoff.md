# Planning evidence for implementation

## Basis for the rule

Three historical project tasks each had five paired Codex implementation runs
and five paired fixed-patch reviews. Both arms used `rg`. Each task used the
same brief and starting snapshot, with a single frozen planning memo in the
handoff arm. The table shows selected measurements before and after adding the
memo. Tokens and directory searches are totals across the five runs per arm.

| Task and stage | Directory searches | Tokens | Median seconds | Cache-adjusted estimated credits |
| --- | ---: | ---: | ---: | ---: |
| New backend API, build | 34 → 16 | 1,887,966 → 1,335,521 | 191.6 → 175.9 | 21.067 → 19.656 |
| New frontend feature, build | 40 → 33 | 3,634,961 → 3,018,478 | 292.4 → 279.1 | 34.618 → 32.789 |
| Existing frontend behavior, build | 23 → 7 | 1,372,917 → 1,179,555 | 89.2 → 105.7 | 15.375 → 15.705 |
| New frontend feature, review | 16 → 26 | 574,338 → 728,400 | 39.1 → 45.4 | 9.390 → 11.869 |

All backend checks passed in one of five builds without the memo and all five
with it. Existing behavior checks passed in both frontend arms. Both review
arms found the seeded defects in all five runs for each task. The small,
project-specific sample supports a narrow plan-to-build rule. The experiment
used a frozen memo per task and did not separately test the three-bullet cap.
This rule is a team addition. The frozen upstream evidence and mappings remain
applicable.

## Procedure check

A fresh, read-only Codex session used the amended entrypoints in an isolated
catalog fixture. It evaluated three cases and produced sample handoffs.

| Case | Observed result after revision |
| --- | --- |
| New route and service | Plan passed three confirmed pointers. Build described checking current symbols, using scoped search for a renamed symbol, and running normal implementation checks. It omitted the note from formal review. Without useful evidence, planning could proceed without the note. |
| Existing listing order change across files | Plan kept scope, acceptance and planned checks. Its handoff omitted the planning discoveries. |
| New helper in one implementation file with a separate test | Plan omitted the note. Build kept the normal discovery and checks. |

The first check omitted the note in the last two cases but repeated a prior
test result in the main handoff. The revised rule keeps the extra planning
discoveries inside the qualifying note. The rerun omitted the result from both
handoffs. The fixture checked instruction following and sample outputs. It
did not implement the catalog changes or execute their tests.
