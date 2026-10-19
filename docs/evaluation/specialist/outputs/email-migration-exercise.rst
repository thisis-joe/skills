Exercise: identify the unsafe backfill
=====================================

Audience: an engineer learning the dual-field transition in decision 0008.
Goal: explain one concrete race and distinguish code rollback from data recovery.
This is a single exercise, not a new course workspace.

Given facts
-----------
``contact_email`` retains exact input; ``email`` strips and lowercases it.
Every new write increments ``revision``. A backfill batch holds at most 500 rows.
Production restore is untested. Old and new consumers are both live.

Problem
-------
1. The backfill reads ``Alice@EXAMPLE.test`` at revision 4.
2. The application writes ``new@example.test`` to both fields at revision 5.
3. The backfill writes the canonical scanned value without checking revision.

Write the value each reader sees after step 3. Then state the conditional update
that would protect step 2, and identify what cannot be reconstructed after the
old value is dropped. Explain whether reverting application code restores it.

Answer key
----------
The old reader sees ``new@example.test``; the new reader sees
``alice@example.test``. Compare the scanned revision in the update; a changed
revision means skip or reload, without replacing the current new value.
Normalization loses spelling/whitespace, and code rollback cannot reconstruct
the original. An exact source backup/archive and a tested recovery procedure
are separate requirements. The permitted batch maximum remains 500.

Check comprehension by asking the learner to produce a different interleaving
that is safe under the revision guard. No learner response was observed here;
creating this exercise is not evidence that learning occurred.
