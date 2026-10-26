# Upstream intent and integration audit

COCO's previous null functional result cannot establish that Matt Pocock's,
Addy Osmani's, or Lauren Tan's original skill trees lack value. Those trees were
not experimental arms. The previous comparison ran staged COCO, published COCO
0.2.0 and no loaded skill bodies on six deliberately clear tasks. Its own report
found no demonstrated functional advantage and said the briefs contained no
unsettled product decisions. See the [conditions](../staged-development/protocol.md#conditions-and-isolation)
and [comparison](../staged-development/report.md#candidate-versus-published-020),
report lines 89-120. This audit also does not establish that any original tree
works better: stated goals and plausible mechanisms are not measured effects.

This is a source audit of frozen COCO `622975e`, read on 2026-10-23. Upstream
`.source` files were read only as inert evidence; no upstream workflow or helper
was executed. The [source inventory](../../../sources/README.md) and
[manifest](../../../sources/manifest.json) identify the original commits and
checksums. Active COCO rules, not these snapshots, govern COCO execution.

## What each original tree intends

| Tree | Stated objective | Concrete mechanisms relevant to this evaluation |
| --- | --- | --- |
| Matt Pocock | Small, adaptable, composable engineering skills that preserve developer control. Address misalignment, verbose project language, weak feedback and poor module design. | Dependency-aware grilling; glossary and ADR maintenance; tests through agreed public seams; observed red-before-green vertical slices; separate Standards and Spec reviewers. |
| Addy Osmani and collaborators | Make agents consistently follow production engineering workflows, quality gates and evidence requirements across the lifecycle. | Pre-build intent extraction; specs and small tasks; behavioral TDD; explicit counterarguments to step-skipping rationalizations; focused context and restartable boundaries; five-axis review and an executed test-sensitivity experiment. |
| Lauren Tan / pstack | Write less, higher-quality code and make parallel execution trustworthy by going deep on design and verification. | Task-specific playbooks; named data shapes before logic; delegated implementation separated from lead judgment; complementary models; direct checks of real artifacts; explicit session pickup and scoped history reconstruction. |

These descriptions trace to the inert [Matt README](../../../sources/matt/README.md.source),
lines 15-19, 109-207 and 211-239; [Addy README](../../../sources/addy/README.md.source),
lines 3-5, 226-286 and 343-378; and [pstack README](../../../sources/pstack/pstack/README.md.source),
lines 5-11, 41-45 and 96-110. Original pinned versions:
[Matt](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/README.md),
[Addy](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/README.md),
[pstack](https://github.com/cursor/plugins/blob/d457567332aa6989e753ea289f30ea2bfbc80bc0/pstack/README.md).
These are author-stated purposes, not independent effectiveness findings.

## Observed preservation and adaptation

### Ambiguity and decision ownership

Matt's [grilling source](../../../sources/matt/skills/productivity/grilling/SKILL.md.source),
lines 8-30, asks the entire dependency-ready frontier, attaches recommendations,
resolves accessible facts without burdening the user, and finishes only when the
frontier is empty and the user confirms shared understanding.
[COCO grill mode](../../../skills/_coco-shared/advanced/clarify.md#grill-mode),
lines 72-95, preserves these mechanics but also allows explicit adoption of
shown remaining defaults. The latter is a team adaptation recorded in
[staged decisions](../../../skills/_coco-shared/decisions.md#accepted-staged-development-decisions-2026-10-23),
line 64. It does not authorize silently adopting unshown material choices.

Addy's [interview source](../../../sources/addy/skills/interview-me/SKILL.md.source),
lines 40-77 and 113-146, instead requires a confidence estimate, one question
with a guess at a time, explicit confirmation and an immediate terminal turn.
[COCO focused mode](../../../skills/_coco-shared/advanced/clarify.md#focused-interview),
lines 39-54, makes the number optional, permits brief independent-question
grouping, accepts an unambiguous affirmative and reuses existing authorization.
The [integration decision](../../../skills/_coco-shared/decisions.md), line 38,
keeps focused interviewing distinct from explicit full-frontier grilling.
This resolves conflicting interaction contracts; it does not preserve both
original contracts unchanged. [Pinned Matt primitive](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling/SKILL.md),
[pinned Addy interview](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/interview-me/SKILL.md).

### Implementation and review timing

Matt's [TDD source](../../../sources/matt/skills/engineering/tdd/SKILL.md.source),
lines 14-38, specifies public seams, independent expected values and one
red-before-green slice at a time. It explicitly defers refactoring to review.
COCO preserves the behavioral loop but permits small local cleanup after green,
rechecking it and separating structural refactoring. The Matt/Addy loop conflict
is explicit in the [decision record](../../../skills/_coco-shared/decisions.md),
line 7, and [coverage adaptation](../../../sources/coverage.json), lines 1723-1747.
See [COCO implementation](../../../skills/coco-build/SKILL.md#procedure-and-output),
lines 34-39. This is a compromise, not evidence that the combined loop is superior.

Matt's [implement source](../../../sources/matt/skills/engineering/implement/SKILL.md.source),
lines 11-17, reviews before committing. Staged COCO commits tested,
self-inspected implementation first, reports review pending, and fixes formal
findings in follow-up commits. This timing change is an accepted team choice in
[decisions](../../../skills/_coco-shared/decisions.md#accepted-staged-development-decisions-2026-10-23),
line 67. It preserves a separate formal review stage but changes the original
commit boundary. [Pinned Matt TDD](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md).

COCO's saved spec-and-plan requirement for every behavior change is also a team
choice, documented at [decision line 65](../../../skills/_coco-shared/decisions.md#accepted-staged-development-decisions-2026-10-23).
The [pstack README](../../../sources/pstack/pstack/README.md.source), lines 265-267,
says planning is optional rather than a default. Mandatory documents cannot be
attributed to that author's intended default merely because pstack contributes
other build rules.

### Independent review and model diversity

Matt's [review source](../../../sources/matt/skills/engineering/code-review/SKILL.md.source),
lines 6-11 and 58-89, mandates parallel Standards and Spec subagents to avoid
context contamination, and keeps their reports separate. COCO preserves
separate spec, standards and quality verdicts, but verdict separation alone does
not reproduce independent reviewers. Its [review entrypoint](../../../skills/coco-review/SKILL.md),
lines 9 and 15-20, prefers fresh review and discloses unavailable independence.
The previous comparative evaluation explicitly accepted same-agent formal
review; its later independent artifact judge was a different check. See
[reported limitation](../staged-development/report.md#limits-and-closure-receipt),
lines 181-187. [Pinned Matt review](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md).

pstack's [interrogate source](../../../sources/pstack/pstack/skills/interrogate/SKILL.md.source),
lines 9 and 25-38, explicitly attributes its adversarial signal to model diversity,
rather than assigned personas, and launches one reviewer per configured model.
Its [feature playbook](../../../sources/pstack/pstack/skills/poteto-mode/playbooks/feature.md.source),
line 12, mandates delegated code writing for review separation, with a stated
exception for subagents that cannot spawn. COCO makes concurrency conditional
on authorization and useful decomposition, and its
[bounded adversarial mode](../../../skills/_coco-shared/advanced/review.md#bounded-adversarial-mode),
lines 79-95, does not mandate multiple models. This is a substantial portability
adaptation, recorded in [coverage](../../../sources/coverage.json), lines
2173-2196 and 2452. A fresh instance of the same model tests a different mechanism
from cross-model diversity. [Pinned interrogate](https://github.com/cursor/plugins/blob/d457567332aa6989e753ea289f30ea2bfbc80bc0/pstack/skills/interrogate/SKILL.md),
[pinned feature playbook](https://github.com/cursor/plugins/blob/d457567332aa6989e753ea289f30ea2bfbc80bc0/pstack/skills/poteto-mode/playbooks/feature.md).

Addy's [review source](../../../sources/addy/skills/code-review-and-quality/SKILL.md.source),
lines 152-164, requires an executed inverted-condition experiment to check test
sensitivity. COCO's [review procedure](../../../skills/_coco-shared/advanced/review.md#independent-axes),
lines 41-43, requests an isolated scratch mutation when sensitivity is uncertain.
Both question green tests, but the trigger and execution boundary differ.
The readonly review cases in this evaluation cannot directly measure the
original's executed mutation step. [Pinned Addy review](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md).

### Handoff and resumption

Matt's [handoff source](../../../sources/matt/skills/productivity/handoff/SKILL.md.source),
lines 8-16, references durable artifacts instead of duplicating them. Addy's
[context source](../../../sources/addy/skills/context-engineering/SKILL.md.source),
lines 123-137, persists accepted scope, task state, changed files, verification
and unresolved approvals at restartable task boundaries. pstack's
[pickup source](../../../sources/pstack/pstack/skills/poteto-mode/playbooks/session-pickup.md.source),
lines 3-9, reconstructs the real resume point without redoing completed work and
checks inherited claims against the original goal on the real artifact.

[COCO pickup](../../../skills/_coco-shared/advanced/context.md#task-pickup),
lines 30-44, and [handoff](../../../skills/_coco-shared/advanced/context.md#portable-handoff-and-phase-boundaries),
lines 65-73, substantially preserve those mechanisms. They additionally assign
authoritative task-state reconciliation to build and require reuse to match
unchanged code, environment and checks. A written handoff can support recovery;
it is not proof that the next agent recovered correctly.
[Pinned Addy context](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/context-engineering/SKILL.md),
[pinned pstack pickup](https://github.com/cursor/plugins/blob/d457567332aa6989e753ea289f30ea2bfbc80bc0/pstack/skills/poteto-mode/playbooks/session-pickup.md).

## Why coverage does not establish the causal mechanism

[Coverage](../../../sources/coverage.json) records attribution, essential source
rules and adaptation destinations. It can establish that a maintainer accounted
for a technique. It cannot establish that the agent loaded it, followed its
trigger, preserved its ordering or independence, or improved an outcome because
of it. Shared language about review is not equivalent to parallel isolated
review; optional same-model challenge is not diverse-model challenge; a saved
plan is not recovered intent; a green test is not demonstrated sensitivity.

The repository records actual earlier integration omissions: generic conditional
loading hid source modes, and all 24 Addy rationalization tables were initially
dropped before compressed stop signals were restored. See
[decisions](../../../skills/_coco-shared/decisions.md), lines 35-36. Those are
recorded source-fidelity defects and repairs, not proof of a remaining regression
or of the repaired rules' empirical value.

Further interference remains hypothetical: a common orchestrator may add cost
to Matt's small composable tools; competing interview and TDD rules may weaken
triggers; removing mandatory delegation or model diversity may remove an
intended source mechanism; added spec/plan and stage transitions may cost more
than they prevent on clear work. The reverse is also possible: consistent
ownership and shared boundaries may prevent omissions. The audit supplies
reasons to test these alternatives, not a verdict between them. The
[staged decision record](../../../skills/_coco-shared/decisions.md#accepted-staged-development-decisions-2026-10-23),
lines 54-55, correctly attributes the resulting combination to the team.

## Mapping to the collaboration-value cases

The [collaboration-value specification](../../specs/collaboration-value.md)
defines a COCO-versus-no-skills screen. Its planned cases exercise mechanisms
that the earlier clear-task comparison left largely untested:

| Case | Source mechanism made observable | Independent outcome, not procedural credit |
| --- | --- | --- |
| Ambiguous inventory import | Intent extraction, ready-frontier questions, concrete scenarios and preservation of owner decisions. SKU identity, duplicate handling, malformed-row atomicity and zero-price summary entries vary across five owner profiles. | Actual CLI/database behavior matches the owner's choices; product facts elicited, owner corrections and redundant questions are classified separately. |
| Supplier and batch requirement change | Named data shape, public behavioral tests, minimal coherent slices, preserved contracts and direct verification. | Composite identity, legacy-data handling, batch idempotence and conflicting-payload rejection work through public calls without losing data or breaking the old invocation. |
| Lost conversation after an import commit | Durable decisions, real Git/task-state reconstruction, evidence reuse and first-incomplete-task pickup. | A fresh process recovers summary choices from surviving artifacts, preserves the changed import behavior and avoids duplicate implementation or needless repetition of valid checks. |
| Identical billing/refund review patches | Spec and quality lenses, intent anchoring, reachable-path reasoning and evidence-based rejection of distractors. | Detect warmed-cache tenant-authorization bypass, payload-blind idempotence and mutation on rejected over-refund; report false positives, actionable evidence and unsupported approval. |

See the [lifecycle design](../../specs/collaboration-value.md#lifecycle-project),
lines 38-80, and [review design](../../specs/collaboration-value.md#independent-review-project),
lines 84-96. The lifecycle projects are longitudinal samples, not three
independent observations per project. Synthetic-owner interventions are proxies;
human active time, comprehension and satisfaction remain unmeasured.

Even a positive result would establish only a bounded incremental benefit of
this frozen COCO combination under these conditions. A null result would
nominate costly procedures for isolated ablation, not identify the responsible
rule or invalidate the original trees. The screen uses the same native default
model and prohibits nested agents, so it does not test Matt's parallel-axis
execution or pstack's diverse-model review as originally specified. A future
direct comparison would need each original tree as a separate arm, with its
required capabilities available or explicit adaptation limits. The
[ablation criteria](../../specs/collaboration-value.md#procedure-reduction-plan-criteria)
correctly require a later single-rule experiment before attributing a cost or
benefit to that rule.

## Audit verification and limits

All source-behavior claims above were checked by reading pinned inert files and
active COCO rules; upstream effectiveness was not executed or measured. Relative
file targets, cited source line ranges and pinned manifest URLs were checked.
The evaluation specification describes planned execution; its outcomes belong
in the separate retained-results report. This document changes no active rule
and supplies no authorization to run an upstream workflow.
