# Initial independent procedure review

Reviewer: fresh `workflow_review` agent; no author conversation was inherited.
Scope: `0839e35fc346187a1525390c0c26c220135817fd` through
`243a406da3318b1e1f8fc4f376231e162bd1e10a`; later evaluation code excluded.

The reviewer ran package validation, all 129 unit tests and diff whitespace
checks successfully, and confirmed preservation of the original 131 coverage
entries/fields with 64 added workflow mappings. These are structural results,
not proof that an agent follows the policy.

## Finding P2: continuous scheduling bypasses manual transitions

`skills/_coco-shared/advanced/spec.md:79` still instructed an agent with continuous
authorization to proceed to planning without a new gate; `advanced/plan.md:79`
similarly proceeded into build. Those statements conflict with S4 and the common
workflow, which separate scheduling from spec-local automatic skill consent.

Disposition: replace both instructions and the corresponding spec entrypoint
return text with explicit transition-contract handoffs. Add a directed cold
scenario for continuous scheduling with manual skill mode. The repair is a
follow-up work unit; the original failed verdict is retained here.

Initial verdicts: spec changes required (S4), standards passed within the stated
scope, quality changes required for the reachable handoff contradiction. Actual
comparative execution and the final workflow review were still pending.

## Targeted independent recheck

The same independent reviewer reread only `fbe87ea` and its three changed rule
locations. The original P2 is cleared: spec, advanced spec and advanced plan now
separate continuous task scheduling from automatic skill selection. No residual
direct conflict was found in those changes; package and diff checks passed.
This recheck did not include the scenario harness or certify agent compliance.

## Final active-policy review and driver follow-up

The independent reviewer examined base `0839e35` through `dadacf0`, including the
concrete preference fallback. No new direct contradiction was found in stage
selection, consent scope, pre-code spec/plan, implementation-before-formal-review,
runtime-pending rules or provenance. All original 131 coverage entries and fields
were preserved. The six staged tests and whitespace checks passed.

A second P2 affected the experiment driver: `Formal review is pending.` was not
recognized, while `Formal review completed. No review pending.` was recognized
as an unresolved handoff. The driver now recognizes the first and removes the
explicit negation before triage. Both exact reproductions were added to the
existing final-response regression. The reviewer independently reproduced the
corrected True/False values and cleared the finding; all six staged tests and
whitespace checks passed. Text matching remains a triage heuristic. The reviewer
did not include the results collector or later report-strengthening delta in
that targeted clearance.
