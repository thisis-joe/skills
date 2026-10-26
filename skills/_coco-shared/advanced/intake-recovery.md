# Intake parent gates and owned-ticket compensation

Read/apply the [automation core](automate.md) first; no new authority.

**Team adaptation — parent gates and owned-ticket compensation.** The parent
gates in setup and triage prohibit ordinary writes when the original parent is missing,
deleted or uncertain. Their sole exception is compensation for the exact ticket
newly created by this authorized attempt after a definite failed handoff. Keep
its project, source/correlation, creation-operation and revision receipt. Before
cancelling, read the current ticket and require matching identity, ownership and
unchanged content/status; use the configured compensation endpoint with a
conditional revision/ownership guard. No owned creation receipt, concurrent
change or unavailable guard means no cancellation.

An unknown reply outcome may already have landed: reconcile the exact original
thread, ticket and trusted marker before either compensation or repeat posting.
Unavailable or ambiguous readback holds both; it is not evidence of absence.
Confirmed source loss before any reply attempt permits only the compensation
above. An unknown cancellation outcome likewise needs ticket readback before
any retry. A refused, unavailable or unresolved cancellation leaves an explicitly
reported blocked/orphan ticket with its exact ID and actual state, never a
completed handoff. Do not broaden credentials, undo another writer's work, create
another ticket or post at another destination. Prove these boundaries before
activation, including lost responses, source loss and concurrent ticket change.
