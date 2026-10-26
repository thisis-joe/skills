# Four-stage development and skill transitions

Apply the [common contract](contracts.md). This is the owner of selection,
handoff and preference policy, not an additional skill or a grant to publish.

## Introductory path

| Stage | Introductory skills | Expected result |
| --- | --- | --- |
| Requirements | `coco-clarify`, `coco-spec`, `coco-plan` | Agreed behavior, saved specification and dependency-ready plan |
| Implementation | `coco-build`, `coco-debug` | Tested implementation commits; formal review pending |
| Review and verification | `coco-review`, `coco-verify` | Findings resolved, actual behavior verified, follow-up commits |
| Release | `coco-push`, `coco-merge`, `coco-ship` | Separately requested PR sharing, merge or deployment |

Install all skills. Start guidance with these ten and offer purpose-specific
specialists, discovery and learning tools as further choices. Preserve explicit
full-catalog requests and expert direct invocation. Never hide an applicable
specialist to keep a short list. Do not make users learn upstream/internal modes.

For a vague new feature without a named skill, announce requirements and clarify,
then start concrete questions without a preliminary permission/menu turn. A
clear static edit runs directly with its relevant checks. A behavior change
requires saved spec and plan before code, even for a single task: reuse adequate
files; follow project conventions, otherwise `docs/specs/<feature>.md` and
`docs/plans/<feature>.md`. A small contract needs behavior/scope/acceptance; its
plan can be one task with a check. Explanations and clear static edits are exempt.

## Manual and automatic basic transitions

Manual is the default. Before switching skills, including returning from review
to build, state the current stage, next exact skill, purpose, expected result
and why it is needed in plain language. Offer **run this next skill once** and
**automatically continue basic steps for this spec** in that same question;
do not add a second automatic-mode interview or nag separately after a refusal.
An explicit next-skill request already chooses that execution. Reuse existing
authorization, selections and valid evidence rather than asking again for them.
An explicit request for implementation, review, verification and fixes for the
same spec already selects those named stages; preserve that scope on resume
without a new opt-in interview. Continuous task scheduling alone does not select
unrequested stages.
Reading a supporting reference or doing a selected skill's own tests is not a
new skill switch. A plan/run command never silently selects automatic mode.

Bind automatic basic transitions to one spec identity and its agreed scope.
Record the mode, current stage/skill, spec reference, approvals, open decisions,
commits and evidence in the authoritative work record, not a second tracker.
On resume read that record and reconcile actual commits; do not reset consent
because the chat changed or apply it to another spec because the project matches.
Automatic progress announces stage changes, still asks new material questions,
and stops after reviewed/verified implementation and follow-up commits, **before
push**. A release request is a separate purpose; do not treat the mode as push,
PR, merge or deployment authorization.

## Specialist consent and personal preferences

Introduce an additional specialist before execution and pause even in automatic
basic flow. Explain what it checks, why this task needs it, its likely cost and
what remains unverified without it. Offer use once, decline, and when useful
automatic use of this exact specialist for this user and project. A previously
explicit user/project/skill opt-in can satisfy this gate; a basic-flow opt-in
cannot. Selecting security never selects performance or migration as well.

Use an established personal preference store when the project has one. Otherwise,
after an explicit opt-in, use `.coco/preferences/<user-key>.json`: derive a stable
file-safe key from the runtime's known user identity (or a user-confirmed key),
not from an invented identity. Save schema version, user identity, canonical
project-root identity and exact automatically allowed skill identifiers. In Git
add `/.coco/preferences/` to this checkout's local `info/exclude` before writing;
keep the file user-private where permissions support it and never stage it.
On lookup require both user and canonical project root to match; a copied file
is not consent for another project. A missing/invalid/mismatched record means
manual selection. Remove only the named skill on revocation. Without a known
identity or available private excluded store, retain the choice in the scoped
record and report cross-chat persistence unavailable. Never put personal defaults
in shared AGENTS.md/CLAUDE.md, a global profile, or another user's settings.
Follow project instructions first; show or revoke a preference when requested.

Declining a specialist omits that separate examination, not required behavior,
boundary controls or ordinary tests. Report omitted coverage. If mandatory
verification is unavailable, keep development pending instead of inferring pass.
Explicitly requesting a specialist already selects it; do not require a second
introductory approval. A mere recommendation or keyword match does not select it.

## Questions, delegation and reports

Before writing a behavioral test or implementation for a slice, use its actual
input/output examples to find unsettled choices that change the public result.
Recover answers from the request, accepted decisions and existing contracts first.
Matching identity, handling a collision and choosing emitted representation are
separate choices when they affect this task; settling one does not settle the
others. Ask only the unresolved material choice. If its owner has no answer,
leave dependent behavior pending and continue independent permitted work. This
is not a fixed questionnaire or renewed approval for settled work; reversible
implementation details remain the agent's choice.

Investigate facts yourself. A decision question names a concrete situation,
understandable alternatives, resulting behavior/cost, and a recommended answer
with its reason. Follow dependency-ready rounds in an explicit grill. When the
current behavior and failure cases are usable, preview further useful questions
with recommended values and effects; offer deeper questioning or adoption of
those displayed defaults and the next skill. The user's delegation accepts the
displayed recommendations; unknown material choices still require a question.

When an accepted design changes, retain the original expectation and the
superseding choice with its reason in the existing spec/decision record. Link
that history from the task state; do not overwrite the only evidence of the
original assumption or copy it into a second tracker.

For reversible in-scope implementation choices, proceed. The completion report
distinguishes original design expectation, actual choice, reason for departure
and effect, then evidence and state. Always include this comparison in the final
user-facing development report, even when unchanged: `Expected: ...; actual: ...;
departure and reason/effect: none / ...`. A work-record link alone does not satisfy
it. Compare against the original expectation and any superseding decision, not
only the latest spec text; say no material departure when appropriate.
Report implementation complete/review pending after build's checks, self-inspection
and commit. Formal review is separate and preferably fresh-context; disclose
unavailable independence for the user's decision, never label self-review independent.
Build owns accepted fixes and follow-up commits; rerun/review only affected scope.
Development complete requires acceptance, required reviews/resolutions, actual
execution checks and commits. Missing required runtime evidence is verification
pending even if the user accepted a review-independence limitation. Keep PR,
merge and deployment outcomes distinct from development complete.
