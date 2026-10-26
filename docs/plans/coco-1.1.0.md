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
| F0 Reconcile release compatibility | Release-based branch and compatibility decision; compare released contracts with staged source | Current implementation request; none of F1+ can bypass this | Inventory all 29 entrypoints, direct calls, installer/metadata, manual/automatic defaults, specialist scope, document exceptions, Jira and review/commit boundaries. Compare actual trees. Resolve any incompatible accepted behavior before certifying 1.1.0 | complete for local source and representative calls; no registry-artifact equivalence claim |
| F1 Integrate accepted staged procedure | Selectively carry accepted navigation, transitions, completion and source decisions; owners: shared workflow/contracts/routing, affected entrypoints and references | F0 | C1/C3/C4/C6/C8 agree across owners; initial/full/expert discovery, static-edit bypass, explicit next-skill selection, one-spec resume, exact specialist revoke and before-push stop have behavior evidence. Reconcile README with the release candidate | implemented; five native compatibility calls and supplemental scope/pickup probes recorded below |
| F2 Validate the decision-check instrument | Disposable verification contract with complete owner answers and independent public expected outcomes | F0; may proceed beside F1 in separately owned test/evidence files | Extra real questions reach the owner; matching keys and emitted spelling are distinct if material. Known-choice recovery, unknown safe stop, failure/restore and unchanged unrelated behavior are sensitive. Preserve old invalid pair and frozen studies | complete; frozen at 027e5c3 before primary actors; controls and collector tests pass |
| F3 Repair discovery and final-report adherence | A minimal single change at the actual decision boundary; likely owners build/clarify/shared workflow, not a universal longer interview | F1 and F2 | C2/C7: relevant rule is reached and followed, existing answers are reused, missing business choices precede adoption, concrete asks retain recommendations/effects, final report compares original/actual/reason. Inspect the real entry/read path rather than equating supplied text with use | implemented with focused follow-ups; comparative adoption remains pending F4 |
| F4 Evaluate the repair and record its disposition | Fixed prospective matched cases and a keep/revert/redesign decision | F3 plus frozen inputs/criteria; valid baseline with room for the targeted failure | At least five pairs for a comparative claim; independent actual outcomes, adverse runs, source/adherence audit and blinded controls. Fewer confirmed assumption repairs for a quality-gain claim, with no added owner-control, process, acceptance or operational loss. Preserve safe blocks separately from completion. No favorable-only replacement | incomplete: two of twelve prepared projects started; repeated HTTP429; five-pair gate unmet |
| F5 Inspect actual state duplication | Evidence-backed decision about K3, not another wording-only rewrite; owners spec/plan/context | F4 disposition recorded | If no overlapping mutable state is observed, retain current behavior and close this branch of work. If observed, propose one structural reduction preserving both artifacts, original/superseding decisions, open choices and one state owner; test five fresh pickups. Efficiency claim still requires full process/public guards and median actor ratio <=0.80 | retain / no-op: no observed overlapping mutable-state target; no efficiency claim |
| U1 Assess human presentation need | Determine whether any R7 intervention is warranted; owners workflow/start/discovery | A representative F1 presentation; no need to wait for F5 | Observe actual friction and verify a real baseline/treatment difference. Pilot baseline already omits map; do not fabricate repetition. If no problem/difference, defer with no rewrite. Participant absence remains unavailable, not a model-generated human result | deferred: no observed human selection friction or distinct repeated-map treatment |
| U2 Run a bounded participant pilot | Actual human understanding/selection evidence for an eligible treatment | U1 eligibility, available consenting participants, frozen primary outcome/threshold | At least five unfamiliar participants, same first orientation, counterbalanced equivalent follow-ups; vary repeated-map display only. Preserve recommendation/reason/result/request, full/specialist access and authority. Record selection, explanation, discovery, approval understanding, active time and re-explanation separately. No learning/effort claim without observations | conditional / not started |
| F6 Integrate and review the release candidate | Reviewed combined changed behavior with original attribution and rollback receipts | F1/F4 and the dispositions of F5/U1; U2 only if needed for a claimed human benefit | Check real combined diff and all C1–C8; independently review source/protocol/claims; run required repo checks and actual affected public/runtime/install checks in temporary destinations. Resolve compatibility/version from F0, preserve evidence and work-unit commits, stop before publication | local implementation checks and scoped independent review recorded; final adoption/release certification pending F4 |

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

The local-source compatibility audit supports a 1.1.0 candidate; published-artifact
equivalence was not tested. F4 still lacks its required completed comparison.
A genuine structural duplication target needs new observed evidence; a primary human
outcome and numerical acceptance threshold need U1's observed problem and a
concrete participant protocol. These do not reopen the 38 accepted decisions or
reopen already authorized implementation. Routine steps reuse the current request.
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
1.1.0 local-source candidate classification with the representative calls recorded
below; no registry-distribution equivalence or universal compatibility is claimed.

F1's structural/install regression was observed failing on the release baseline
because workflow.md was absent; after the port both tests pass. This is packaging
and structure evidence, not native behavioral proof. The validator and existing
hot-path size caps pass without raising thresholds. Actual native and supplemental
observations follow; they have different scopes and do not fill missing pairs.

A real F1 static-edit fixture at candidate `9949121` completed the authorized
work but its final report said only the correction and no departure from the
spec, with the original expectation only implicit through the spec. Before primary F4
actors, commit 17e3425 moved the existing mandatory comparison into common's
actual final-report paragraph and removed its ownership-summary duplicate. The
original observation remains; a fresh equivalent static task explicitly reported
the agreed scope, correction and no departure. Independent semantic review
confirmed this distinction without requiring fixed labels. This
does not change C7 or the comparison rubric. No primary actor used `9949121`.

F5 source inspection found separate existing ownership in spec/plan/context and
no evidenced overlapping mutable-state target. Preserve this structure; do not
claim the C7 history clarification is a state-reduction or speed intervention.
U1 retains the existing concise returning-user behavior. The earlier model advice
baseline already omitted repeated maps; no actual human selection-friction
observation or distinct treatment is available, so U2 remains unexecuted.


### Recorded behavior, with evidence limits

- **F1 compatibility:** five completed native calls exercised bare start, a static
  correction on an adequate non-Jira branch, push to a disposable local bare
  remote, direct WIP review including an untracked file, and exact-range review.
  The reviews found seeded defects and an additional real parsing defect. The
  local push read back the expected commit and retained the old remote branch.
  The static task reused its documents/grants and stopped before push. Initial
  sandbox startup failures and an extra policy probe that timed out on HTTP429
  remain in the [receipt](../evaluation/coco-1.1.0/implementation/evidence/compatibility.json)
  and [raw archive](../evaluation/coco-1.1.0/implementation/evidence/compatibility.tar.gz).
  This does not exercise every possible project convention, real Jira writes,
  active required Git hooks, or a published registry artifact.
- **C7 reporting follow-up:** the fresh static task reported its agreed unchanged
  wording, actual typo correction and no departure. The original partial report
  is retained; neither a fixed label nor an extra report file is required.
  [Native follow-up](../evaluation/coco-1.1.0/implementation/evidence/report-followup.json),
  [independent source/report review](../evaluation/coco-1.1.0/implementation/evidence/source-review.json).
- **C3/C4 boundaries:** a fresh supplemental worker actually revoked one exact
  specialist preference while preserving another, rejected a copied record for
  a different project, and used a manual fallback without confirmed identity.
  Synthetic fixture identity and local private-file protection were inspected.
  Read-only policy probes also kept missing required browser execution pending
  and rejected scope expansion. These are not native paired observations or real
  external-service calls. [Receipt](../evaluation/coco-1.1.0/implementation/evidence/boundary-probes.json).
- **C2/C7 pickup:** fresh supplemental workers resumed existing saved spec/plan.
  The known-choice worker implemented the settled contract without re-questioning,
  passed seven real CLI tests including exact large integers/rollback, committed
  implementation and review closure separately, and reported original versus
  superseding choices. The unanswered-choice worker asked concretely, retained
  the unresolved identity/output choice and changed no files or commits. Root
  checks confirmed public outcomes and unrelated data preservation. This tests
  model-worker pickup, not human learning, and does not replace the unstarted
  native preservation probes. [Receipt](../evaluation/coco-1.1.0/implementation/evidence/pickup-probes.json).
- **F4 comparison:** only profile 0 in each condition started; the remaining eight
  primary projects plus two preservation probes were not attempted. Repeated
  HTTP429 after cooldown prevented a complete cohort. Raw emitted finals,
  provisional commentary, missing process-exit metadata and post-stop public
  observations are distinguished. Independent blinded grading retained all
  missing outcomes and rejected both false-completion controls. No five-pair,
  quality, speed, human-effort or easier-selection claim is supported.
  [Frozen protocol](../evaluation/coco-1.1.0/implementation/protocol.md),
  [observations and durable raw receipts](../evaluation/coco-1.1.0/implementation/observations.md).
- **F3 follow-up from the blind finding:** both observed implementations introduced
  an unapproved SQLite price cap. The candidate's final question correctly left
  acceptance pending but arrived after the cap was committed. Commit 1250ffd adds a recheck when
  implementation/verification reveals a constraint that would alter agreed
  behavior; preserve the contract with an in-scope solution or settle the new
  material choice before adopting a limit. The original grades remain unchanged.
  This is a focused redesign of the trigger, not a successful replacement cohort.
  A fresh supplementary worker reproduced the binding overflow and preserved the
  agreed contract via internal exact storage, without asking to narrow prices. Six
  tests passed; independent CLI calls confirmed exact `2^100 + 17`, a legacy maximum
  INTEGER row and unchanged data after a rejected batch. No product departure,
  unrelated file change or push occurred. The impossible-constraint/unanswered-new-
  choice branch was not executed in this follow-up; newer Python conversion-guard
  behavior was source-reviewed only.
  [Focused receipt](../evaluation/coco-1.1.0/implementation/evidence/constraint-followup.json).

### Disposition and next boundary

The implemented source remains reviewable on the feature branch. F5 is closed as
retain/no-op; U1 is deferred and U2 unexecuted. The evidence supports these specific
procedure repairs and their bounded local observations. It does **not** certify
final F3/F4 adoption or release readiness: the frozen five-pair gate remains unmet,
and the passing focused constraint-follow-up is separate from that cohort. A later comparison needs an available environment and a recorded recovery
plan, preserving all original attempts rather than replacing them with successes.

All 38 user decisions, all 29 skill names/discovery metadata, installer interfaces,
original source facts and source snapshots remain. The maintained guidance stays
English; the user-facing change map is Korean. Package versions, personal/global
installs and remote publication are unchanged. Temporary Codex/Claude installation
checks are separate from the user's installed skill state.


### Source and verification closure

- Required validator passes: 29 skills, source checksums, coverage and references.
  All **179 tests pass** in the final source checkout (54.542 seconds).
  [Full log](../evaluation/coco-1.1.0/implementation/evidence/final-tests.log).
- A clean release-based clone exposed a historical fixture test depending on
  unrelated Git object `622975e`. Commit `f6336e0` uses the already committed,
  checksum-verified historical snapshot instead. The test still checks the same
  historical proposals and active-source preservation; no frozen study was changed.
  The original clean-clone failure and the post-fix result are retained separately.
  At `1250ffd`, the clone still lacks `622975e` and passes the validator and all
  179 tests (54.148 seconds), with a clean worktree.
  [Receipt and log pointers](../evaluation/coco-1.1.0/implementation/evidence/clean-clone.json),
  [original failure](../evaluation/coco-1.1.0/implementation/evidence/clean-clone-before.log),
  [passing full suite](../evaluation/coco-1.1.0/implementation/evidence/clean-clone-after.log).
- Both public Codex and Claude project installers were run in temporary projects.
  All 117 final skill/support files match source; the unrelated skill and project
  exclusions remain. The first observer wrongly treated the installer's own receipt
  as unrelated; that observer assertion and correction are disclosed. No installer
  or personal/global installation change was made for that observation.
  [Final install receipt](../evaluation/coco-1.1.0/implementation/evidence/final-install-checks.json).
- Independent read-only review found no actionable source/spec defect in the
  initial integration, reporting repair or emerging-constraint recheck. This is
  scoped source review, not certification of the incomplete experiment.
  [Review](../evaluation/coco-1.1.0/implementation/evidence/source-review.json),
  [source and link preservation](../evaluation/coco-1.1.0/implementation/evidence/final-source-checks.json).

| Work unit | Local commit |
| --- | --- |
| One concrete 1.0.0-to-1.1.0 change map and accepted plan | `d0ef906` |
| Staged workflow and release compatibility repairs | `9949121` |
| Frozen decision-discovery/preservation instrument | `544cf3b` |
| Original/actual/reason at the final-report boundary | `17e3425` |
| Delivered versus actually settled owner answers | `027e5c3` |
| Interrupted/unstarted evidence collection | `7f34713` |
| Portable historical fixture in fresh clones | `f6336e0` |
| Unchanged blind judgments and incomplete comparison | `1126909` |
| Recheck new constraints before changing agreed behavior | `1250ffd` |

The final evidence/status commit is recorded in branch history. The starting
`docs/coco-1.1.0-clarity` checkout is still clean at `ba596d8`. Source changes and
verification are local; no package version bump, push, PR, merge, publication or
personal/global installation has occurred.


## Authorized release continuation (2026-10-26)

The user now explicitly requests the full comparison, operational installation,
Git push and merge, npm publication and README update. This supersedes the earlier
publication/install exclusion for this continuation, without erasing that historical
closure. Keep the same feature branch and work-unit commits. Existing managed
Codex and Claude global installations are the operational targets; preserve other
skills and user modifications. The current remote default is `main` at `84a59a2`,
with no `dev`/`develop`; use the ship release path into the confirmed default,
not an invented coco-push development base. Preserve work-unit history by merge.

| Release unit | Acceptance | State |
| --- | --- | --- |
| R1 Complete prospective recovery | Freeze new candidate and necessary instrument repair; all five matched profiles and two preservation probes, actual owner routing, independent public outcomes and blinded controls; retain the old incomplete cohort | prior attempts sealed; waited cohort frozen at 7582101; actual Sol/high native controls started, first passed without 429 |
| R2 Prepare consumer artifact | Package 1.1.0, concrete README/distribution notes, exact packed payload, required checks, rollback install and scoped independent review | corrected cd728cd artifact passed: 200 tests, 466 packed/118 active files, eight exact-baseline install/rollback steps |
| R3 Land release branch | Secret/provenance inspection, verified normal push, one PR attached to this chat, all forge checks/review gates, pinned-head merge and target readback | corrected source pushed as 2f8b11d; all ten CI jobs passed; final evidence head checks and R1 remain |
| R4 Publish and install | Annotated release tag, npm exact artifact and registry integrity/readback; install to existing managed Codex/Claude locations and verify source agreement/other skills; preserve a tested rollback path | npm authentication recovered; pending readiness |

Release does not require a superiority claim. Do not fabricate a favorable outcome;
record the absence of a demonstrated gain honestly. A real owner-control, required-process,
public-behavior or operational regression still blocks the affected adoption.
Service capacity or missing authentication is unavailable, never passed. A
published version cannot be overwritten; hold before publish on an unmet gate.
Rollback uses each runtime's exact prior installation (Codex `0b110c0`, Claude
registry 1.0.0) and npm latest-tag restoration when needed; verify the package/commands
and preserve installed ownership before operational writes. No live service database
or migration is involved in this skill bundle.


Release preparation receipts: [packed artifact and rollback checks](../evaluation/coco-1.1.0/release/artifact-readiness.json)
and [independent preparation/public-evidence review](../evaluation/coco-1.1.0/release/independent-review.json).
Normal `npm pack` ran the validator and all 179 tests (57.999 seconds). The artifact
has 465 files; evaluation/test data are excluded. Actual registry 1.0.0 skill bytes
match the tagged local baseline. Both temporary runtime installations passed
1.0.0 -> 1.1.0 -> 1.0.0 -> 1.1.0, including removal of the new workflow on rollback
and preservation of an unrelated skill. Operational installs remain unchanged.
The initial receipt collector failed parsing prepack text before npm's JSON; its
metadata parser was corrected and the identical installation sequence recorded.
`npm whoami` returned E401. A browser login attempt fell back to an interactive
username prompt and was cancelled without collecting credentials; user login in
their own terminal is pending. This does not block preparation or draft review.


Release branch `8689721` was normally pushed and read back, and draft
[PR #28](https://github.com/thisis-joe/skills/pull/28) targets `main`. Its two
required Linux checks and six shell checks passed, but both Windows test jobs
failed five subcases in a historical oracle test. The test setup wrote CRLF on
Windows where the fixed preserved-note fixture requires LF bytes. The fixture now
writes explicit bytes; the historical observer and archived experiment remain
unchanged. A controlled CRLF/LF reproduction distinguishes this cause in all five
profiles, and the validator plus all 179 local tests pass after the fix. The actual
Windows CI recheck passed on `be3a89f`, along with both Linux jobs and all six
shell jobs ([Check](https://github.com/thisis-joe/skills/actions/runs/40306808911),
[shell checks](https://github.com/thisis-joe/skills/actions/runs/40306808966)).
At that revision, the test-only fix left the initial archive's 465 included files
unchanged. Later operational preservation changes require a new artifact and new
CI; the earlier green jobs do not approve those changes.
[Failure and repair receipt](../evaluation/coco-1.1.0/release/windows-fixture-fix.json).


### Recovery outcome and actual operational baseline

The [new recovery report](../evaluation/coco-1.1.0/implementation/recovery/observations.md)
retains two distinct stopped attempts: 14 native calls in total, zero stable trials
and zero valid matched pairs; 10 and then 11 projects were not admitted. Both
attempts honored their original per-call limits. A strict-integer oracle defect
was prospectively repaired and independently reviewed; the first frozen instrument
remains archived. After the actual provider cooldown, one-worker pacing still met
HTTP429. No further native retry or substituted development engine is scheduled.
The blind packet is retained ungraded. The full comparison remains unavailable;
no candidate superiority or no-regression conclusion follows from these attempts.

Actual installation inspection also changed the operational compatibility scope.
Claude matches registry 1.0.0, but the 117 managed Codex files exactly match
`fix/skill-runtime-evidence` at `0b110c0`. This is a known source-version difference,
not an unowned-file conflict. Both installations were left unchanged and private
backups were made during that inspection. The exact Codex rollback source was reconstructed and validated;
registry 1.0.0 alone would not restore that installation.
[Baseline receipt](../evaluation/coco-1.1.0/release/operational-baseline.json),
[source identification](../evaluation/coco-1.1.0/release/operational-source-identification.json).

The previously user-requested operational repairs were preserved under the existing
instruction to retain decisions and behavior. They are helper bug fixes and
clarifications of existing rules, not new product requirements. Seven groups were
absent from the release-based candidate: genuine/project-scoped recent use, actual
merge target identity, request-mode notices, tracker write recovery, obsolete
private-test handling, literal Markdown parsing and owned intake compensation.
The bare-start repair was already integrated. The corresponding fixes were ported
with provenance and original regression tests, preserving the 1.1.0 stage,
authority and reporting contracts. The single change map records exact locations
and examples. No existing installed repair is silently discarded.

This final combined skill tree differs from the pinned recovery candidate
`42f6c58`; the stopped observations cannot approve later changes. The final artifact,
both runtime installations, exact operational rollback targets and final source
review/CI need their own evidence. No merge, tag, npm publication or global
installation had occurred at this checkpoint. Registry authentication still
returned E401 at 10:30 UTC; the later successful retry is recorded below.

### Final artifact preparation and npm authentication retry (2026-10-26)

The user requested an npm retry and completed the new browser login.
`npm login --auth-type=web` exited successfully; `npm whoami` returned `thisis-joe`.
The registry still reported `latest: 1.0.0`. Authentication is resolved; this is not
publication. No secret or authentication code was collected in chat or committed.

| Preserved operational behavior | Work-unit commit |
| --- | --- |
| Genuine recent use and workspace isolation | `6411f8a` |
| Actual fork/base identity and retarget checks | `669d570` |
| Literal Markdown examples | `fe0cc68` |
| Wording-only versus execution notices | `84a345f` |
| Tracker publication and uncertain-write recovery | `6b8e6b0` |
| Public-contract tests and limited private-structure exception | `b132919` |
| Owned intake compensation and reconciliation | `d92a57f` |
| Keep the merge safeguards within the existing guidance budget | `80b8ef2` |

The preserved tests first exposed the omitted helper behavior. After the fixes,
the merge guide exceeded its existing 27,400-character bound by 50 characters;
redundant wording was removed without raising the bound. Normal final `npm pack`
then passed package validation and **all 200 tests in 65.557 seconds**, with no
skips. Its source is `80b8ef2` plus the recorded README/distribution additions.
The initial 117-file skill artifact is superseded for release by this combined
118-file skill artifact. The earlier archive remains historical evidence.

An [independent final source review](../evaluation/coco-1.1.0/release/final-source-review.json)
found no actionable source integration issue. Common authority/stage/reporting
rules were unchanged by the operational ports; source facts and snapshots remain
preserved. Three new recovery archives passed hash/mode inspection and a bounded
public-evidence scan. Two stale plan statements (old backups and prior Windows CI)
were corrected. This review does not replace the missing paired comparison.

The prior temporary release directory was absent after interruption/restart.
Historical receipts remain as records of their original runs; they are not claims
that those scratch files still exist. Reconstruct exact rollback sources and make
fresh private backups before any operational write. Keep those private backups
outside Git. The original full-comparison gate remains unmet and has not been
silently waived by the successful npm login.

[Final artifact receipt](../evaluation/coco-1.1.0/release/final-artifact-readiness.json)
and [rollback records](../evaluation/coco-1.1.0/release/final-rollback-records.json)
confirm all 466 packed files match the checkout, including the 118 active files;
test/evaluation data are excluded. Registry 1.0.0 was downloaded and its original
integrity verified. Existing global managed files still exactly match the identified
baselines. Both temporary destinations passed all eight install/upgrade/rollback/
re-upgrade steps with unrelated content intact. Fresh managed-only private backups
were created and read back; neither global destination was changed.

The exact final archive has SHA-1 `d9e4dfbc87969fa22260e65394fcc395e36fc760` and
SHA-256 `ae49ca6f8028d65ae5fd083926809fc5e515689a3d0fdf94119325f751ac78e9`.
Publish this verified archive only after the remaining readiness decision and
forge checks; do not substitute the superseded initial artifact. These checks
establish package/install compatibility, not the unavailable behavioral comparison.

### User-directed waiting and final Windows finding

After the authentication retry, the user questioned why the provider's requested
wait had not simply been honored. This selects another properly recorded recovery,
not a waiver of the comparison gate. The previous revision-2 rule explicitly
stopped on any recurring 429; it must not be described as permanent provider
unavailability. Its stderr said Codex would retry sampling in 340.999900833 seconds
(attempt 1/5). It did not identify account quota versus service capacity.

Prepare a new cohort on the final corrected source. Retain the 420-second actor
and 90-second classifier budgets, with provider-announced retry intervals recorded
separately and allowed up to 30 minutes per call (wall caps 2220/1890 seconds).
Apply identical accounting to both arms, one project at a time, at least 30 seconds
between call starts, with a 90-minute cumulative provider-wait ceiling for this
cohort. Advertised waiting is an estimate, not measured productive-model time;
always report total elapsed time. Let the same CLI process retry; do not restart
failed product trials to replace results. Freeze and test the new wrapper before
dispatch. Existing attempts and their outcomes stay unchanged.

Remote `3a866db` passed both Linux checks, six shell checks and Windows Python 3.9.
Windows Python 3.x (3.15.1) failed two runtime subcases of the invalid-workspace
regression: a NUL-containing path allowed `coco-ship` to enter another workspace's
recent-use result. This real platform difference must be fixed, not waived. Keep
the failure evidence and the test expectation; the final comparison source and
publishable artifact must include the repair and pass subsequent CI.

Commit `cd728cd` explicitly rejects NUL-containing/non-string record paths before
platform normalization. Existing test expectations are unchanged. Both-runtime
controlled reproduction fails before the guard and passes after; 17 focused tests,
the validator and all 200 tests (61.520 seconds) pass locally. The root separately
reviewed the three-line code change against both JSON-metadata call sites and found
no issue. Actual Windows 3.15.1 confirmation still requires the new pushed CI.
[Repair receipt](../evaluation/coco-1.1.0/release/windows-path-fix.json).
The new comparison candidate is `cd728cd1cbf8afe4740f68a8bf91a924fee574c4`; subsequent
documentation-only commits do not change that active payload. The previously
verified `d9e4dfbc` npm archive omits this repair and must not be published.

The [corrected artifact](../evaluation/coco-1.1.0/release/corrected-artifact-readiness.json)
supersedes that archive with SHA-1 `1c48845fd95e1a276605f4048b89b804ac98f6bb`
and SHA-256 `6d117151412b9ba4b8f3f20e00f70cce7117934ea85113367eb9c40fe6331e9e`.
Normal npm prepack passed the validator and all 200 tests in 63.944 seconds with no
skips. All 466 packed files and 118 active files match source; both exact-baseline
temporary upgrade/rollback/re-upgrade sequences pass. The archive is retained in
the ignored persistent `dist/release-1.1.0/corrected/` directory. Prior archives
and receipts remain unchanged. Global installations are still untouched.

The user delegated model choice, allowed reasoning-only adjustments to preserve
context, then explicitly prohibited Luna: use Sol or above. Keep this conversation
and existing workers' context; choose models for new work without claiming the
main chat's setting was changed. Before any waited-cohort native call, pin both
arms and all owner classifiers to `gpt-6.1-sol` with `high` reasoning and record
the actual model/effort. Use `gpt-6-astra` with `high` reasoning for the new narrow
model-wrapper review and later independent outcome judgment. Do not change model
or effort mid-cohort or pool results with the older unspecified-default cohorts.
This selection follows the user's instruction before outcomes, not a favorable
result search. No Luna worker is authorized.

The Windows repair is now confirmed on the actual remote Windows Python 3.x job,
as well as Windows 3.9, both Linux versions and all six shell jobs at `2f8b11d`.
[Exact CI receipt](../evaluation/coco-1.1.0/release/corrected-source-ci.json).
The active payload is the frozen `cd728cd` candidate; later evidence-only commits
still require their own forge checks before landing. This resolves the platform
failure without weakening or changing the original regression test.

The [waited protocol](../evaluation/coco-1.1.0/implementation/recovery/waited/protocol.md)
and its exact source/input manifests were frozen at `7582101`; the root reread
all 16 file hashes with no mismatch. Ten focused instrument tests passed. The
[preexecution reviews](../evaluation/coco-1.1.0/release/waited-preexecution-review.json)
closed the timing, cancelled-success, partial-collector and stale-model-context
findings before dispatch. The first native control then passed without 429 and
verified a fresh `gpt-6.1-sol`/`high` turn context. This is availability/model
evidence only; it is not a completed development pair or a release verdict.
