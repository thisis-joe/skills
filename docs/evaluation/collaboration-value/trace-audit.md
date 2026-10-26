# Completed primary trace audit

This audit reads all 20 v2 primary results and their retained actor/owner records.
It describes observed behavior and attribution limits; it does not replace the
functional oracle or independent blind judgments. The originals were not arms,
so neither this comparison nor the earlier null result judges their effectiveness.
See [upstream intent](upstream-intent.md) for pinned originals and adaptations.

## Coverage and method

Frozen inputs are candidate `622975e349e6276b225aa9ef02ee69d664dd2927`, driver
`4c7ede8dc78535019a2472c9ff3969b0efedaa78`, and native CLI
`0.163.0-alpha.11.2`, recorded in [control.json](/private/tmp/coco-collaboration-value-v2/control.json).
The table identifies every audited trial; C/B mean COCO/bare.

| Seed | Lifecycle C | Lifecycle B | Review C | Review B |
| --- | --- | --- | --- | --- |
| 0 | `e126f1774c0b` | `18e3c6759fae` | `d55f9b3d3f54` | `a9a53be98a8a` |
| 1 | `909f1629c2ae` | `30583ca77dc8` | `e9287625a91b` | `df301b5ecfad` |
| 2 | `f226fa0a5d81` | `400c6ab73961` | `76f5fe45dc3f` | `720a9cfb72f9` |
| 3 | `15169f7554d2` | `13616f4d9925` | `4aadd71cd013` | `15e4e6ece481` |
| 4 | `841aba34ded2` | `62589328086d` | `68f6adea10b2` | `09f08c634b2e` |

Evidence coordinates below are relative to the raw run root
`/private/tmp/coco-collaboration-value-v2`; the same `records/<id>/...` coordinates
survive relocation/archiving under the [evidence convention](evidence/README.md).
The audit inspected result/stage outcomes, owner questions/replies/delivery flags,
actor prompts/messages/commands, raw JSONL tool events, and stable-project Git
histories/diffs. It did not execute native actors or upstream instructions.
C2's quarantined project was not inspected for a final-state claim.

All 69 actor turns were scanned: 1,365 JSONL events, 442 completed commands,
27 completed file-change events and 48 changed-path entries. All 59 owner
classification records were schema-valid; semantic validity is a separate question.

## Isolation and fairness observations

No recorded actor command, tool result or changed path shows global skill-body,
inert `sources/`, control/record/owner-project/snapshot, foreign-project or
parent-directory access. All changed paths resolve inside their own project.
No unexpected recorded tool type appeared. All ten COCO trials read local
`.guide` bodies; all ten bare trials only discovered its absence. COCO had 45
definite guide-body read commands and four local `review_scope.py` executions;
these counts describe activation, not costs caused by individual rules.

All nine stable COCO `guide_after` maps equal the frozen 117-file manifest.
C2 is unknown. Recorded final equality does not prove continuous non-mutation.
All ten reviews preserve the prepared source/HEAD. Startup catalog metadata
remains a known isolation limit: no recorded body access does not establish that
metadata or the base model's prior engineering knowledge was absent.

## Material decisions and confirmed policy rework

A conservative episode means changing already-implemented product behavior to
resolve an undisclosed owner-owned policy, grouping related edits made in one
response/repair into one episode. It excludes operational retries, expected RED
checks, requested scope change, and documentation-only commits. These are observed
episodes, not isolated causal effects of a skill or complete counts of all work.

All ten first initial outcomes fail only `chosen_identity_and_file_collision`,
then pass after the owner supplies trim/case identity. None first elicited identity.
The brief said detailed import rules were unsettled; it did not explicitly list
identity/case/whitespace. Thus these are material decision-discovery failures,
not omission of an explicit four-question checklist.

Each cell below identifies the product repair commit and exact command receipt.
`t3.c4` means command 4 in `records/<id>/turn-3.json` for that table's trial ID.

| Seed | COCO identity repair | Bare identity repair |
| --- | --- | --- |
| 0 | `31276a1`, t3.c6 | `5727e9e`, t3.c4 |
| 1 | `24db372`, t3.c6 | `dbd4441`, t3.c4 |
| 2 | `bcf98ad`, t4.c7 | `f4aa0a8`, t3.c4 |
| 3 | `fc439a3`, t3.c5 | `127f31a`, t3.c4 |
| 4 | `2e04be2`, t3.c6 | `fe04cbf`, t3.c4 |

There is one additional confirmed bare episode. B4 implements reject-on-duplicate
and reject-on-stored-collision in turn1 command4, commits `7f8c312` in command7,
then asks whether those policies should remain. The first owner answer requires
first-row/stored-row preservation. [Turn2 event7](/private/tmp/coco-collaboration-value-v2/records/62589328086d/turn-2.events.jsonl:7)
records the source/test/document changes; command3 commits `6eec43f`. Its product
diff replaces duplicate rejection with skipping and stored rejection with
`ON CONFLICT ... DO NOTHING`. The atomic invalid-row default already matched;
it is not another episode. The subsequent identity repair is separate.

Across all first-turn commands/file-change events, B4 alone writes product code
before the first owner policy answer. Confirmed counts are therefore COCO 5,
bare 6: a limited observed rework advantage in seed4, despite equal identity
repair counts. Do not substitute correction-message counts for episodes or call
this zero rework improvement. Later C2 work remains incomplete/unknown.

Supplier namespaces, migration, batch replay and the new stored-row update rule
are explicitly requested CHANGE. Their implementation and changed test
expectations are legitimate scope work. All nine executed resume outcomes pass
on their first recorded functional observation; C2 never reaches resume.

Eight resumed cases first elicit zero-price policy on resume. B1 instead chooses
a compatible include-zero default without eliciting it. Passing output establishes
compatibility, not owner control or recovery of a previously supplied choice.
B2 directly re-asks grouping/empty-output facts supplied in CHANGE because they
were not preserved in its surviving record ([turn4 prompt](/private/tmp/coco-collaboration-value-v2/records/400c6ab73961/turn-4.prompt.txt),
[turn5 final](/private/tmp/coco-collaboration-value-v2/records/400c6ab73961/turn-5.json)).
That is a durability limitation; its COCO mate has no resume outcome, so it cannot
establish matched recovery superiority. Conditional zero-only-group questions
in C1/B3 are not automatically forgotten settled facts because a broad topic
label repeats.

## Adherence and useful work

C0 loads clarification and workflow rules (turn1 commands4-5), then implements
after the collision/invalid answer without a further-choice preview (turn2).
The [clarify entrypoint](../../../skills/coco-clarify/SKILL.md), line19, and
[workflow](../../../skills/_coco-shared/workflow.md), lines82-88, require preview
and leave undisplayed material choices with the owner. This is an observed
discovery/adherence gap, not evidence that an unperformed preview is ineffective.
The focused interview mode alone does not waive that universal preview rule.

C0's repair commentary and plan explain the raw-key cause, but its final report
says actual behavior matches clarified requirements with "no material departure."
It does not explain the original unapproved assumption's departure there, as
[workflow](../../../skills/_coco-shared/workflow.md), lines90-95, requires.
This is a reporting limitation, not an added functional penalty.

Both review arms reproduce the same three seeded root defect types in every
fixture: cached authorization bypass, payload-blind replay, and rejected-refund
mutation. Oversized-integer overflow is a valid additional D3 symptom, not a
fourth independent root. No final review claims either seeded benign distractor.
Public CLI/temp-database controls provide meaningful evidence; see the
[overflow control](evidence/overflow-control.json). Five numeric fixtures repeat
three roots, not fifteen distinct bugs.

COCO review bodies and public checks were executed without an observed root-
detection gain. Model-diverse challenge and independent parallel reviewers were
not exercised under this profile; they cannot be called causally ineffective.
Likewise, many implementation failures are expected RED checks rather than
introduced defects. Practical package value includes adherence, but "not followed,"
"not triggered" and "executed without a measured gain" remain different findings.

## Cost attribution and instrumentation

Every lifecycle contains a recorded Git permission/locking failure followed by
retry. Some compound shell commands return zero despite an earlier Git failure;
for example B1 turn1 command3 and turn5 command7. Inspect output as well as exit
status. These are operational retries, not skill ceremony. Bare actors also rerun
unchanged baseline/CLI checks and sometimes create documentation checkpoints.
State must be checked before calling any repetition redundant.

C2's exact question "After your trial, what is the next checkpoint?" is
misclassified `procedure[]` instead of scheduled checkpoint feedback. The driver
therefore injects technical authorization. [Turn3](/private/tmp/coco-collaboration-value-v2/records/f226fa0a5d81/turn-3.json)
takes 9.770 actor seconds with no commands/tool items; its four raw events contain
only thread/turn start, the acknowledgement and turn completion. The extra owner
classification takes 7.733 seconds. Keep raw totals primary. A labeled sensitivity
can remove exactly those observed costs, not turn2, identity repair or the later
timeout, and cannot reconstruct possible cognitive effects of the extra context.
This exchange is instrumentation burden, not actor ceremony.

C2 turn5 reaches the shared 420s budget (420.326 seconds recorded). Its owned CLI
leader exits after SIGINT, but descendant quiescence is unverified and usage lacks
a `turn.completed` event. The result truthfully marks final observation unstable,
closure unknown and change execution failed. No fresh actor, immutable snapshot
or completed-summary inference follows. It is an unfinished attempt, not proof
that its partial code is functionally wrong. Primary recovery elsewhere is
planned-checkpoint/new-thread recovery, not demonstrated abrupt-crash recovery.

## Bounded reduction hypotheses

The traces support candidates for subsequent controlled reductions, not per-rule
causal cost estimates:

- Compact repeated routing/state/report prose and verification-record commits.
  C0 makes separate evidence commits while C3 integrates records into four work
  units; that variation is not a mandated fixed commit quota.
- Test narrower relevant reading and evidence reuse against repeated resume
  checks. COCO [context](../../../skills/_coco-shared/advanced/context.md), lines32-36,
  already permits reuse for unchanged relevant state; Addy's inert
  [restart contract](../../../sources/addy/skills/context-engineering/SKILL.md.source),
  lines123-137, conditions reruns on missing/moved/dependent evidence.
- Repair material-choice discovery/preview activation before judging the
  clarification mechanism. Retain meaningful RED checks and public boundary probes.

The mandatory spec-plus-plan and commit-before-formal-review policies are user-
chosen COCO integration decisions ([decisions](../../../skills/_coco-shared/decisions.md),
lines65-67). Compact their implementation without silently deleting those choices
or attributing their costs to all three original authors. Original pstack model
independence, Matt's full ready-frontier grill, and Addy's mandatory mutation
experiment differ materially from this profile; merged-content coverage alone
establishes neither mechanism fidelity nor incremental effectiveness.
