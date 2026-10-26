# COCO 1.1.0: explicit development procedure

Status: implementation authorized, 2026-10-26. Target: **1.1.0**, with the
local-source compatibility classification and checks recorded in the plan. The
user requested concrete instruction changes, specification/plan updates, actual
skill edits, verification and work-unit commits. Package-version changes, personal
installation and publication remain separate release scope. Temporary fixture
installation is part of verification. The single detailed change document is
[1.0.0 → 1.1.0](../coco-1.0.0-to-1.1.0.md), written in Korean for the user.

Execution state has one owner: [1.1.0 plan](../plans/coco-1.1.0.md). The
[rationale](../coco-1.1.0-rationale.md) explains the original purpose, achieved
results and expected user-visible changes. The accepted
[staged-development contract](staged-development.md), based on the user's 38
decisions, remains the behavioral authority; this document integrates its release
scope with subsequent evidence and preservation conditions.

## Objective and release boundary

Deliver a source-accounted team procedure in which people own goals and material
business choices, the agent performs agreed work, and another worker can recover
the agreement and its evidence. Improve observed decision-discovery and adherence
gaps while preserving successful handoff and selection behavior. Faster coding,
fewer questions, more documents or defeating the underlying model are not the
definition of this product's value.

The local tagged 1.0.0 release baseline peels to `84a59a2`; its tree equals
`88d1c84`. The experimental skill snapshot is `622975e`, unchanged in `a19c5fb`.
That tagged baseline does **not** contain the experimental shared four-stage
workflow. This is local source provenance, not a new verification of registry
package contents. Do not describe the experimental implementation or its model
trials as a verified published 1.0.0 feature or a test of the final 1.1.0 package. See the
[baseline receipt](../evaluation/coco-1.1.0/baseline.json).

The planning branch starts at `a19c5fb` to retain the evidence. Implementation uses `feat/coco-1.1.0`, based on `84a59a2`, and selectively
ports reviewed skill paths; historical documents and harnesses are retained as
evidence rather than merged as executable source. A package still declaring 1.0.0 on an experiment branch is not proof that
its skill contents equal the release.

## Preserved decisions and observable behavior

| ID | Required behavior | Concrete acceptance |
| --- | --- | --- |
| C1 Orientation and composition | Introduce requirements → implementation → review/verification → release, with the existing ten introductory skills. Keep all 29 entrypoints, the full catalog, specialists and expert direct invocation | A newcomer can identify the next step; an explicit full-list or specialist request remains available. No catalog deletion to achieve a short menu |
| C2 User-owned decisions | Investigate repository facts; recover settled choices; ask about genuinely missing material behavior using a situation, alternatives, effects, recommendation and reason | A known choice is recovered without re-asking. An unknown choice is asked and may safely remain pending. Technical automation does not approve undisplayed business defaults |
| C3 Scoped execution | Manual awareness is the default for unselected transitions. An explicit next-skill request supplies that selection. Automatic basic flow binds to one spec/scope, announces stages and stops after review/verification/fixes/commits, before push | No duplicate approval for an already requested action; no transfer of automatic authority to another spec or publication. Supporting reads/tests are not new skill switches |
| C4 Specialist boundaries | Introduce a specialist's purpose, expected coverage and cost; preserve exact user/project/skill opt-ins and revocation | Basic automation does not select every specialist. Decline preserves required checks; missing independence/coverage is disclosed. No personal defaults written into shared/global rules |
| C5 Durable intent and state | Behavior changes save/reuse a feature spec and plan using project conventions; one location owns execution status | A fresh worker recovers choices, completed/pending work, evidence, next action and scope from surviving artifacts. Genuine open choices survive. Explanations and clear static edits retain their exceptions |
| C6 Implementation and evidence | Project AGENTS.md/CLAUDE.md and required checks govern. Observe behavioral RED/GREEN or keep an executable reproduction and explain the missing automated seam | Real public behavior is checked. Missing required runtime evidence stays verification-pending. Self-inspection is distinguished from independent review; work-unit commits remain identifiable |
| C7 Honest final reports | Compare original expected design with actual choice, departure reason/effect, evidence and current stage | A corrected spec does not erase the original assumption. The final user-facing report itself contains the comparison, including no material departure when applicable |
| C8 Source ownership | Retain source attribution, essential-rule decisions and the documented reasons for adaptations | A changed integrated rule has an owner, affected source mechanism and rationale. Inert upstream snapshots never become runtime instructions |

The ten introductory skills remain clarify/spec/plan, build/debug, review/verify,
and push/merge/ship. The broader catalog is not ten competing mandatory steps.
Any conflict with an accepted decision needs a concrete user decision rather than
an implicit implementation compromise.

## Planned capabilities and dependencies

| Capability | Planned result | Depends on |
| --- | --- | --- |
| K0 Release integration and compatibility | Reconcile the tagged 1.0.0 baseline with the experimental workflow; preserve existing supported use and declare intentional changes | — |
| K1 Stage guidance and authority | Make the accepted navigation, transition, specialist and completion rules coherent in the release-based candidate | K0 |
| K2 Decision discovery and reporting | Reach the relevant clarification before adopting unknown business behavior; retain concrete questions and original/actual/reason reporting | K1, valid verification contract |
| K3 State reuse | Preserve durable decisions and pickup; reduce actual overlapping mutable state only if demonstrated | K1; structural reduction conditional on observed duplication |
| K4 Returning-user presentation | Preserve correct concise next actions and full discovery; investigate human friction only when observed | K1; a distinct actual presentation problem for a usability intervention |

K2 is the first outcome repair. K3's possible efficiency change follows its
recorded disposition. K4 is separate and may remain unchanged. The deferred
R1/R3 removal proposals and R4/R6 interventions are not bundled into this release.

## Evidence and adoption rules

Existing studies retain their original inputs, denominators, errors, exclusions
and judgments. The [workflow-v2 report](../evaluation/staged-development/report-v2.md),
[collaboration report](../evaluation/collaboration-value/report.md) and
[isolated pilot](../evaluation/procedure-refinement/report.md) answer different
questions. None supplies a population success rate, a direct original-tree
comparison, or measured human learning/effort. The initial clear-task study and
its later reporting repairs remain separate historical observations.

- **R5:** retain the incomplete contact pair and its null comparative repair
  counts; do not adopt the tested frontier wording as a proven repair. Before a
  future trial, make owner answers cover every oracle-required business choice,
  let actual extra questions reach the owner, and verify rule loading and execution
  separately. Include both known-choice recovery and truthful unknown-choice
  pending cases. Expected RED and completion of blocked work are not policy repairs.
- **R2:** both pilot arms already recovered and completed all five pickups.
  Stronger reuse wording missed the 20% time reduction gate; it did not test
  structural duplicate removal. A fresh structural proposal requires an actual
  duplicated-state trace, keeps both saved artifacts and pending choices, and
  passes every applicable clarity/consistency/provenance/pickup/reporting guard.
  Retain the frozen <= 0.80 median actor-time ratio for an efficiency claim;
  it is not a universal gate for the existence of a shared procedure.
- **R7:** the pilot's current arm already omitted the repeated map; the proposal
  was longer. Keep this result. Do not manufacture a verbose control. A human
  study requires an observed problem and a real presentation difference; otherwise
  defer the intervention. The participant design in the integrated reduction plan
  remains unexecuted. Model advice checks cannot prove human ease or substitute
  for a sequence of actual participant interactions.

A future comparative claim uses at least five fixed matched pairs per relevant
procedure arm, equal capabilities/authority/budgets, independent public outcomes,
source/adherence audits and blinded grading with grounded negative controls.
Freeze outcome, questions/owner contract, thresholds and stopping conditions before
execution. Preserve all attempts; an invalid instrument yields an inconclusive
result. A follow-up needs a recorded measurement/input change and its rationale,
not a search for favorable samples. Reuse valid unchanged evidence.

## Compatibility and version acceptance

1. Keep entrypoint names, installation scope/ownership protection, full discovery
   and existing explicit user authorizations usable.
2. Audit changed defaults as observable contracts, especially manual transitions,
   saved-document requirements, review/commit timing and conditional Jira rules.
   Merely preserving skill names does not establish compatibility.
   Preserve an adequate descriptive branch in a non-Jira project: the candidate's
   residual build phrase about a branch differing from "this format" must not
   reintroduce an unrelated Jira confirmation. Keep configured Jira summaries and
   Git validation when that project actually requires them.
3. Exercise representative existing 1.0.0 invocations under the release candidate;
   do not treat 622975e-versus-0.2.0 results as 1.0.0 compatibility evidence.
   Pin and compare the registry artifact if making a claim about published npm
   consumers; local tag equality alone does not verify that distribution.
4. If preserving the accepted behavior requires an incompatible change, present
   its concrete before/after use and migration cost. Resolve the choice to retain
   compatible behavior or target a major release; do not silently relax a user
   decision to fit 1.1.0. This is a future release gate, not a blocker to this plan.

`1.1.0` is therefore the target, not a compatibility certification or permission
to change package metadata. Pre-release packaging and publication belong to a
later authorized release task.

The future port also carries source-accounting metadata: `coverage.json` adds
workflow reference/team-override links for 64 of 131 items. Original essential
rules, adaptation facts and inert upstream snapshot bytes remain preserved. The
planning request changes none of that metadata.

## Historical planning closure

Done means the two chats' settled decisions, source histories, release/experiment
distinction, evidence limits, prospective acceptance and dependency-ready tasks
are written, independently reviewed and checked. Active `skills/`, inert
`sources/`, runtime scripts/tests, installers and version metadata remain byte
identical to `a19c5fb`. Only documentation/evidence integration changes here.

That planning-only boundary applied to the earlier request. On 2026-10-26 the
user authorized implementation. The plan owns current task state. Human
participants and a frozen human outcome remain prerequisites only for U2; they
do not block correctness work and no human-benefit claim is made here.

## Concrete implementation acceptance

The single change document maps each edited owner to its release wording,
replacement, example, reason and check. F1 carries the accepted four-stage rules
and resolves the project-conditional branch/Jira chain, bare start routing and
direct WIP review. Existing explicit same-spec implementation/review/verification
grants remain usable; continuous scheduling alone does not choose missing stages.
F3 tests a narrow pre-expectation decision check in the always-read common
contract, referenced from build and clarify, plus preservation of original and
superseding design choices for final reports. It asks only when a real public
result depends on an unresolved material choice; it does not introduce a universal
questionnaire. F4 determines whether that isolated repair is retained, reverted
or needs redesign. F5 and U1 may close unchanged when no real target exists.
