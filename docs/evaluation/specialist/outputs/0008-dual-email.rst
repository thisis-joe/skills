0008: Add a canonical email field alongside the original
======================================================

Status
------
Proposed fixture decision; not a production migration approval.

Supersedes: none

Context
-------
Decision 0007 preserves exact ``contact_email`` spelling for audit use.
Old and new consumers remain live at the same time. The selected new ``email``
form strips surrounding whitespace and lowercases text. That normalization is
not reversible: multiple original strings produce the same canonical value.

Decision
--------
Add ``email`` without removing ``contact_email``. All relevant writes must
update both fields and increment ``revision`` before new-only reads switch.
Backfill only with ``0 <= batch_size <= 500``. Compare the scanned revision;
if it changed, skip or reload the current row rather than overwrite a new write.
Retain the original field through audit and migration retirement gates.

Alternatives
------------
An in-place rename/drop would break old consumers and remove the audit source.
An offline rewrite would require a separately accepted outage and recovery plan;
no such acceptance exists in the fixture facts.

Consequences
------------
Dual-write consistency and reconciliation add temporary maintenance work.
Keeping the old value preserves audit spelling and read rollback options.
Production backup and restore have not been tested, so destructive contraction
remains blocked. This decision does not promise zero downtime.

References
----------
* ``fixtures/decisions/0007-email-source.rst``
* ``fixtures/decision-facts.rst``
* ``outputs/migration-plan.md``
