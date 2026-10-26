# Recovery revision 2: strict integer outputs and paced admission

This new cohort inherits [the recovery protocol](../protocol.md), with only the
prospective instrument and admission changes recorded here. Both skill sources,
five paired profiles, two candidate preservation probes, authority, owner facts,
rubric and per-call/per-project caps stay unchanged. The stopped first recovery
attempt is sealed separately; its two question-only turns, two unavailable owner
classifiers and ten unstarted projects are neither resumed nor pooled.

The first range observer used Python equality, which accepts a boundary float
as equal to an integer. A mixed float/integer JSON response could therefore conceal
corruption: `9.223372036854776e18` denotes 192 cents more than `9223372036854775808`.
Revision 2 requires each returned `price_cents` to have exact Python type `int`
(excluding bool), as well as complete exact output equality. Before actors, all
five independent reference profiles must pass, the price-cap mutation and a new
mixed-float-output mutation must each fail, and restoration must pass. The mixed
mutation explicitly demonstrates that the former equality check would pass.

No observation in attempt 1 accepted a range output: both projects remained
unimplemented and unchanged, with empty output and a false result. No owner reply
or oracle feedback reached those actors. This is an instrument repair before any
usable comparison evidence, not a favorable replacement of a poor product result.

Both owner-phase failures were HTTP 429 in the same native engine used by actors;
earlier actor and control calls had succeeded. These facts do not establish a
classifier-specific fault. The provider receipts permit one further availability
check after 2026-10-26 10:21:17 UTC. Make exactly one native classification control
for the public range question with the unchanged 90-second cap, no retry. If it
fails, stop. Reuse the three passing attempt-1 classifier controls with exact-byte
provenance because their prompt, topics, routing and native engine did not change.

On a successful availability control, admit one project at a time. Keep at least
30 seconds between native call starts in this process; record actual pacing
separately from native elapsed time and the unchanged 420/90-second call budgets.
This is an explicit operational pacing rule applied equally to both arms. It
does not imply a speed benefit. Retain all wall-clock costs. Any further observed
429 stops this attempt; no replacement cohort, model, engine or manual owner
classifier is authorized by this protocol. An unavailable comparison keeps the
release gate pending.

Freeze this addendum, its runner/tests, the inherited recovery protocol and all
original reused dependencies before the single availability check and primary
dispatch. Preserve attempt 1's frozen originals and archive unchanged. No stopped
actor is resumed. Report twelve newly prepared projects, exact attempted/unstarted
counts, every emitted turn, and all historical operational attempts separately.
