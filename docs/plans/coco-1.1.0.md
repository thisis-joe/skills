# COCO 1.1.0 integration and improvement plan

Spec: [1.1.0 contract](../specs/coco-1.1.0.md).
Explanation: [purpose, progress and before/after](../coco-1.1.0-rationale.md).
This file is the **sole mutable execution-state owner for this effort**.
Historical plans keep their completed receipts; they do not schedule this work.

## Scope and source identities

- Planning branch: `plan/coco-1.1.0`, starting at `a19c5fb`, in the existing
  managed `coco-staged-workflow/skills` worktree. It began clean.
- Imported handoff: `90edb55` and `5164cd4`, selectively integrated as `ebffb8c`.
  Their old planned-experiment status does not replace completed pilot outcomes.
- Local tagged release baseline: peeled `v1.0.0` commit `84a59a2`; tree equals `88d1c84`.
  Experimental skill reference: `622975e`, also the unchanged skill tree at
  `a19c5fb`. [Machine-readable receipt](../evaluation/coco-1.1.0/baseline.json).
- Implementation authorized on 2026-10-26; branch `feat/coco-1.1.0` starts at
  local tagged release `84a59a2` in the managed `coco-1-1-0/skills` worktree.
  The starting documentation checkout remains clean at `ba596d8`. Historical
  docs/harnesses come from `ba596d8`; the integration audit comes from `6f01c14`.
- The user requested one concrete comparison document: [1.0.0 → 1.1.0](../coco-1.0.0-to-1.1.0.md).
  It owns the detailed before/after instruction map; this plan alone owns task state.
- Authorized scope is specification/plan, actual skills, disposable scenario
  verification and work-unit commits. Temporary installs validate packaging;
  package bumps, personal/global installation, push, PR, merge and deployment
  remain outside this implementation task.

## Current planning work

| Unit | Delivered outcome and check | State |
| --- | --- | --- |
| P1 Reconcile both histories | Import pinned report/reference evidence; distinguish release, staged candidate and follow-up studies; preserve measurements | complete / `ebffb8c`; eight referenced blobs verified |
| P2 Specify behavior and value | Save C1–C8, capabilities, before/after, evidence limits and adoption/stop rules; preserve all accepted decisions | complete / `e099b5a` |
| P3 Independent review and closure | Check claims against actual source/history, resolve findings, verify links and required repository checks, prove documentation-only changes | complete; independent review approves planning, validator and 168 tests pass, documentation-only preservation checks pass; closure commit in branch history |

## Implementation task graph

The task IDs below are authorized acceptance slices. Their state requires actual
evidence and does not imply completion in advance. Use separate work-unit commits. The root
integration writer owns shared rule files; independent inspection can be parallel
without concurrent mutation. Implementation findings belong to build; review
returns issues and verification returns evidence.

| Task | Delivered behavior / expected owners | Genuine dependencies | Acceptance and verification | State |
| --- | --- | --- | --- | --- |
| F0 Reconcile release compatibility | Release-based branch and compatibility decision; compare released contracts with staged source | Current implementation request; none of F1+ can bypass this | Inventory all 29 entrypoints, direct calls, installer/metadata, manual/automatic defaults, specialist scope, document exceptions, Jira and review/commit boundaries. Compare actual trees. Resolve any incompatible accepted behavior before certifying 1.1.0 | source audit complete; representative runtime compatibility remains F6 |
| F1 Integrate accepted staged procedure | Selectively carry accepted navigation, transitions, completion and source decisions; owners: shared workflow/contracts/routing, affected entrypoints and references | F0 | C1/C3/C4/C6/C8 agree across owners; initial/full/expert discovery, static-edit bypass, explicit next-skill selection, one-spec resume, exact specialist revoke and before-push stop have behavior evidence. Reconcile README with the release candidate | source applied; native fixtures in progress |
| F2 Validate the decision-check instrument | Disposable verification contract with complete owner answers and independent public expected outcomes | F0; may proceed beside F1 in separately owned test/evidence files | Extra real questions reach the owner; matching keys and emitted spelling are distinct if material. Known-choice recovery, unknown safe stop, failure/restore and unchanged unrelated behavior are sensitive. Preserve old invalid pair and frozen studies | instrument written; sensitivity checks running before freeze |
| F3 Repair discovery and final-report adherence | A minimal single change at the actual decision boundary; likely owners build/clarify/shared workflow, not a universal longer interview | F1 and F2 | C2/C7: relevant rule is reached and followed, existing answers are reused, missing business choices precede adoption, concrete asks retain recommendations/effects, final report compares original/actual/reason. Inspect the real entry/read path rather than equating supplied text with use | candidate applied; F4 adoption decision pending |
| F4 Evaluate the repair and record its disposition | Fixed prospective matched cases and a keep/revert/redesign decision | F3 plus frozen inputs/criteria; valid baseline with room for the targeted failure | At least five pairs for a comparative claim; independent actual outcomes, adverse runs, source/adherence audit and blinded controls. Fewer confirmed assumption repairs for a quality-gain claim, with no added owner-control, process, acceptance or operational loss. Preserve safe blocks separately from completion. No favorable-only replacement | not started |
| F5 Inspect actual state duplication | Evidence-backed decision about K3, not another wording-only rewrite; owners spec/plan/context | F4 disposition recorded | If no overlapping mutable state is observed, retain current behavior and close this branch of work. If observed, propose one structural reduction preserving both artifacts, original/superseding decisions, open choices and one state owner; test five fresh pickups. Efficiency claim still requires full process/public guards and median actor ratio <=0.80 | conditional / not started |
| U1 Assess human presentation need | Determine whether any R7 intervention is warranted; owners workflow/start/discovery | A representative F1 presentation; no need to wait for F5 | Observe actual friction and verify a real baseline/treatment difference. Pilot baseline already omits map; do not fabricate repetition. If no problem/difference, defer with no rewrite. Participant absence remains unavailable, not a model-generated human result | conditional / not started |
| U2 Run a bounded participant pilot | Actual human understanding/selection evidence for an eligible treatment | U1 eligibility, available consenting participants, frozen primary outcome/threshold | At least five unfamiliar participants, same first orientation, counterbalanced equivalent follow-ups; vary repeated-map display only. Preserve recommendation/reason/result/request, full/specialist access and authority. Record selection, explanation, discovery, approval understanding, active time and re-explanation separately. No learning/effort claim without observations | conditional / not started |
| F6 Integrate and review the release candidate | Reviewed combined changed behavior with original attribution and rollback receipts | F1/F4 and the dispositions of F5/U1; U2 only if needed for a claimed human benefit | Check real combined diff and all C1–C8; independently review source/protocol/claims; run required repo checks and actual affected public/runtime/install checks in temporary destinations. Resolve compatibility/version from F0, preserve evidence and work-unit commits, stop before publication | not started |

F0/F1 specifically protect an adequate non-Jira descriptive branch on resume;
the experimental build's residual "this format" wording is an audited risk.
Audit the complete common/build/push rule chain rather than adding another
branch-format policy. Likewise preserve direct WIP review requests and frozen
all-layer review scope when integrating the changed formal-review/commit timing.
Carry explicit source-coverage/team-override links with the workflow, preserving
original source facts and snapshot bytes. Unknown identity or unavailable private
specialist storage must fall back to manual selection, never shared/global defaults.
F0 must also pin/compare the actual registry artifact if making published-npm
compatibility claims; this planning receipt verifies local source trees only.

F2's instrument work and F1's port may be independent once F0 is settled; F3
needs both. R5's disposition precedes any R2 structural efficiency intervention.
Human-study availability is not a prerequisite for correctness/authority work or
for a release making no human-benefit claim. No-op or deferred findings are valid
dispositions, not a reason to invent additional tasks.

## Verification surfaces and retained limitations

| Obligation | Required observation | What it does not prove |
| --- | --- | --- |
| Compatibility | Same supported 1.0.0 requests/installer use remain usable, changed defaults explicitly classified | The old published-0.2.0 comparison is not this check |
| Decision control | Public behavior matches actually settled choices; real unanswered choices remain pending; known facts are recovered | Lucky oracle agreement or a question-count reduction is not consent |
| Handoff | Fresh worker cites surviving actual sources, recovers current and open choices, completes permitted work and preserves unrelated data | New thread technical authority is not proof of cross-chat consent persistence |
| Reporting/review | Original/actual/reason in the exact final report; separate implementation, review and runtime states | A revised spec, check label or self-review does not supply omitted evidence |
| Efficiency | Recorded all-attempt and jointly completed costs, elapsed and token counters separate, fixed guard/gain gate | Actor seconds are not human effort, prices or causal rule costs |
| Human presentation | Actual participant observations for an eligible real treatment, with frozen assessment | Shorter replies and fresh model judges are not human learning evidence |

Standing commands come from AGENTS.md: `python3 scripts/validate.py` and
`python3 -m unittest discover -s tests -v`. Focused native comparisons now belong to F2–F4 under the frozen implementation
protocol. The earlier documentation closure did not execute them. Reuse unchanged historical evidence;
run only affected/regression/integration checks justified by actual changes.
Keep scoring anchors distinct from behavioral repair counts: later confirmation
of a matching default without a behavior change is not a repair episode, even
when its original adoption lacked demonstrated owner agreement.

## Keep, rollback and stop conditions

- Freeze each future experiment's exact input, source, owner/oracle, applicable
  rubric, cost formula and budget before its actors. Keep original failures and
  all attempts. An invalid measure is inconclusive; never patch an old result
  into a success. Report loaded-but-unfollowed and unexposed rules separately.
- A real owner-control, authority, provenance, public-behavior or required-process
  regression blocks adoption. Preserve the obligation and revert the isolated
  candidate or redesign its trigger. A passing check on one slice is not release
  readiness. New material user decisions remain user-owned.
- No effect on a working baseline means keep it. A missed efficiency gate rejects
  that claim. Another cohort needs a consequential changed hypothesis or repaired
  instrument recorded in advance; do not rerun until a win appears.
- Keep per-slice work-unit commits so a rejected change can be reverted without
  deleting evidence. Reconcile task status with actual commits. No destructive
  reset, broad rewrite, invented tracker, first-orientation deletion or hidden
  simplification of consent/data checks.
- R1/R3 removal remains deferred; R4 evidence reuse and R6 independent/diverse
  review or executed sensitivity are separate future hypotheses. Do not treat
  post-trial judges as development interventions or schedule them to justify
  their original authors' reputations.

## Decisions remaining for later dependent work

Final compatibility/version classification needs F0's concrete before/after
audit. A genuine structural duplication target needs F5's trace; a primary human
outcome and numerical acceptance threshold need U1's observed problem and a
concrete participant protocol. These do not reopen the 38 accepted decisions or
block completion of this planning request. Implementation is now authorized; routine steps reuse the current request.
Any genuinely incompatible concrete change still requires the user’s decision.

## Planning closure

The [independent review](../evaluation/coco-1.1.0/plan-review.md) approves the
specification, task graph and rationale at `e099b5a`. This final update records
planning status/receipts only; future task acceptance and authority are unchanged.
The [check log](../evaluation/coco-1.1.0/planning-checks.log) retains the actual
validator result and all 168 passing tests (41.996 seconds). These unchanged-code
repository checks do not certify the unimplemented release or human outcomes.

All task changes are documentation. Protected tracked/untracked skill, source,
runtime-script/test, installer and metadata paths match `a19c5fb`; original
native evidence, grades and frozen cohorts are unchanged. The primary checkout
and other evaluation worktree remain untouched. No active implementation,
new actor/participant experiment, package bump, installation or publication ran.
The above paragraph records the earlier planning closure. Current implementation
state is recorded in the task table and closure receipts below.

## Implementation receipts (2026-10-26)

F0 compared `84a59a2` with `622975e`: all 29 entrypoint registrations and
frontmatter, package/install interfaces and inert source snapshots match. The
19 experimental active paths (18 edits plus workflow) were inspected and
selectively ported. The 64 coverage rows retain their original essential-rule
facts and add explicit workflow adaptation references. The source audit identified
five compatibility repairs: conditional Jira on resumed build and push entry,
direct WIP/exact-range review, bare start routing, and preservation of explicit
same-spec stage grants. The single change map records their exact locations.

Saved documents before behavior changes, manual awareness for unselected stages,
and separate post-commit formal review are deliberate defaults selected by the
user. Existing explicit stage selections and direct calls stay usable. This is a
1.1.0 local-source candidate classification, conditional on F6 representative
calls; no registry-distribution equivalence or universal compatibility is claimed.

F1's structural/install regression was observed failing on the release baseline
because workflow.md was absent; after the port both tests pass. This is packaging
and structure evidence, not native behavioral proof. The validator and existing
hot-path size caps pass without raising thresholds. Native fixture and comparison
results remain pending until their actual execution and independent review.
