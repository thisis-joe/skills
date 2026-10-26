# Staged development contract

Status: accepted from the user's 38 decisions, 2026-10-23.
Feature: `staged-development`. Execution plan: [plan](../plans/staged-development.md).

## Objective and users

Help a team working like the maintainer choose fewer procedures without reducing
behavioral correctness. Users learn the four development stages, choose skills
by purpose, then discover and compose specialist skills. Preserve all installed
capabilities and upstream attribution; default guidance is not the full catalog.

The philosophy is: people own goals and material decisions; the agent implements
small agreed changes and reports observable evidence. Faster execution, fewer
questions, or more documents alone do not establish improvement.

## Capabilities and ownership

| ID | Responsibility | Depends on |
| --- | --- | --- |
| navigation | Four stages, ten introductory skills, complete discovery | — |
| transitions | Manual handoffs, spec-local automatic flow, specialist preferences | navigation |
| execution | Written contracts, project rules, TDD, commits and separate review | transitions |
| evidence | Independent checks, preserved provenance, controlled comparison | execution |

Common rules have one owner in `skills/_coco-shared/contracts.md`; conditional
transition details live in `skills/_coco-shared/workflow.md`. Entrypoints and
advanced procedures reference these rules rather than owning competing policy.

## Navigation and selection

1. Requirements: `coco-clarify`, `coco-spec`, `coco-plan`.
2. Implementation: `coco-build`, `coco-debug`.
3. Review and verification: `coco-review`, `coco-verify`.
4. Release: `coco-push`, `coco-merge`, `coco-ship`.

Install every existing skill. Show specialists and help/learning tools through
purpose-specific discovery; an explicit complete-list request still lists all.
For a vague new feature without a skill name, announce requirements/clarify and
start the first grounded questions. A clear static edit needs no interview or
spec/plan pair. Existing adequate agreements are reused, not rewritten.

## Clarification and decision contract

Read discoverable facts before asking. Each material question uses a concrete
situation, understandable alternatives and consequences, and a recommendation
with its reason. Explicit grill retains dependency-ready numbered rounds.
Once current behavior and failure cases are settled, preview useful additional
questions with proposed answers and effects. Offer more questioning or adoption
of the displayed recommendations and the next step. Delegation accepts displayed
defaults only; it never grants unknown product choices or external operations.

For reversible in-scope implementation choices, proceed and report original
expectation, actual choice, reason for departure, and effect. New material
behavior, compatibility or costly/irreversible choices still require the user.

## Transition and preference contract

The default is manual: before switching skills (including a return to build),
explain the next skill's purpose, expected result and why it is needed. Offer
one next-skill execution or automatic basic transitions for this spec. Do not
ask a separate repeated automatic-mode question. An explicitly requested next
skill already supplies that choice; do not ask permission again for it.

Automatic basic transitions are bound to one identified spec and approved scope.
Record the spec reference, current skill/stage, mode, approvals, open decisions
and evidence in the existing authoritative work record. Preserve that binding
on resume; never carry it to a different spec. Automatic flow stops after
implementation, review, verification, fixes and commits, immediately before push.
Publishing, merging and deploying require their own requested purpose/scope.

Specialist consent is separate. Introduce a proposed specialist and pause even
during automatic basic flow unless that user explicitly opted into that exact
skill for this project. Project-local personal preferences are not team policy,
do not apply to another project/skill/user, and yield to repository instructions.
Do not silently create global preferences or modify shared agent rules to store
a personal choice. A declined specialist leaves required behavior and ordinary
checks intact; disclose the omitted specialist coverage.

## Documents, execution and completion

Behavior additions/changes require an authoritative saved spec and plan before
implementation; use the project's conventions. With none, use feature-scoped
files under `docs/specs/` and `docs/plans/`. Small work can have a brief contract
and one planned task/check. Pure explanations and clear static edits are exempt.

Follow project instructions (`AGENTS.md`, `CLAUDE.md`, existing checks). Without
them, retain feature branches, atomic commits and behavior checks; do not require
Jira or invent ticket data. The exact Jira branch convention is conditional on
an actual repository/team rule. Preserve user-owned task summaries when it applies.

For changed behavior observe the intended failing test, implement minimal green,
then check the actual user path. If no adequate automated seam exists, retain an
executable reproduction and the reason; do not claim automated coverage.
Build runs required checks and self-inspects, then commits implementation before
formal review. Report `implementation complete; review pending`. Review returns
findings without editing. Use a fresh reviewer when available; disclose missing
independence and let the user decide whether to accept that limitation. Fixes
belong to build and produce follow-up commits, with affected rechecks/review.

Development is complete only after required review resolutions, execution
verification and commits. A missing required runtime check remains `verification
pending`, even if unit tests pass or a user accepts an independent-review gap.
No automatic flow pushes. Release distinguishes PR sharing, merge and deployment.

## Acceptance and comparative evaluation

| ID | Observable acceptance |
| --- | --- |
| S1 | Ten introductory skills in four stages; all skills remain installed/discoverable. |
| S2 | Vague feature starts clarify; static edit bypasses interview and documents. |
| S3 | Material questions show situations, alternatives, effects and recommendations; delegated defaults are explicit. |
| S4 | Manual switches pause; one-spec automatic transitions resume only that spec and stop before push. |
| S5 | Exact specialist opt-ins stay user/project/skill-scoped; decline does not erase checks. |
| S6 | Behavior work saves/reuses spec and plan; no Jira prerequisite without project rules. |
| S7 | Red/green or executable reproduction, implementation commit, separate review and follow-up fixes are distinguishable. |
| S8 | Missing runtime evidence blocks development-complete status; missing review independence is disclosed separately. |
| S9 | Final reports distinguish expected/actual design, departure reason/effect, evidence and current stage. |
| S10 | Compare candidate separately with 0.2.0 and no skills using real disposable projects and independent behavioral checks. |

Freeze scenario inputs, variant source snapshots and a common outcome rubric
before trials. Execute at least five matched development scenarios per arm;
report per-case results and limitations, not a population success rate or speedup
from heterogeneous single samples. Separate correctness from workflow compliance,
learning/decisions/redundant questions, novice/experienced conditions, elapsed
time and human-effort proxies. No real human comprehension or active time is
measured by an agent-only fixture. Preserve raw actions and failures; sanitize
artifacts for an independent reviewer and test rubric sensitivity in scratch.

Required repository checks: `python3 scripts/validate.py` and
`python3 -m unittest discover -s tests -v`. Preserve frozen source hashes,
operational verify/automate extraction checks and established latency guards.
Do not publish, bump a version, overwrite unrelated work, or claim universal
equivalence. No unresolved product decision blocks this accepted scope.
