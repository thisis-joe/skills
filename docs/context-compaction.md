# Compact loading guidance without weakening operational rules

The first extraction preserved the original operational text but introduced
9,001 characters of selection tables and module-entry guards. In its five-task
application, those additions consumed most of the text avoided by splitting the
two large procedures: observed document output fell by only 1.6%.

This follow-up uses `206773fbf03cf1046299408a49e3a6999cb2a19c` as its
baseline. It changes loading instructions and ownership of decision history;
it keeps the original 23 verification/automation operational sections intact.

## Keep safety conditions; shorten their expression

Both selectors still evaluate every applicable row, load cumulative prerequisites
before dependent work, and reassess new scope, risk, state, or missing
prerequisites. They retain broad fallback when uncertain, all-mode fallback when
unclassifiable, and a stop on unavailable required guidance. Core and common
rules apply even when no specialist row matches. Reading does not expand scope
or authority. Mode selection remains the agent's responsibility.

Maintenance still loads the creation contract before its maintenance procedure.
Intake triage still loads setup; intake fixes load setup, triage, and fix.
Specification-only work reads relevant execution constraints without activating
the operation. Each directly opened module still requires its core first.

The fixed acceptance budget was chosen before editing: at most 4,500 characters
for the two selectors and all fifteen guards, versus the frozen 9,001-character
baseline. The result is 4,490 characters. Measurement counts whitespace and
Unicode characters without discounts; deleting a required guard cannot pass the
structural gate. This measures added guidance, not complete task context.

## Put operational rules in operational owners

`decisions.md` remains attributed conflict history. Its eighteen baseline
decisions and final policy paragraph were audited against common and specialist
rules before making history conditional. Two policies lacked sufficiently clear
operational ownership: model/agent-tree restrictions and experimental opt-in
with disposable probes and production gates. They now appear in the mandatory
common contract. All baseline policies have an operational owner.

Normal work reads the common contract and selected procedure. Unresolved rule
conflicts or their rationale trigger reading the decision history. Removing an
unconditional history pointer does not remove that history or authorize an
agent to ignore a conflict. The exact permitted preamble-reference change is
explicit in the reconstruction test; all other frozen preamble content and
operational sections remain checked.

## Evidence and interpretation

See [the evaluation record](evaluation/context-compaction/README.md) for frozen
snapshots, actual local application, safety edge cases, source ownership,
required checks, and installation verification. Structural conservation and
limited observed behavior support this change; neither proves equivalence for
every model, runtime, project, or future request.

The English-language normalization requested afterward is a separate work unit.
Its edits and measurements must not be folded into this frozen comparison.
