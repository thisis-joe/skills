Read/apply [core](verify.md) first; no new authority.

## Maintain formal verification

1. Collect each check's property, coverage, assumptions, bounds, command, and last sync commit; run it unchanged first.
2. Read all covered-code changes since sync, including moved/split functions and new writers to guarded state.
3. Classify no effect, stale description, evidenced intentional promise change, or possible broken promise.
4. Update from code before rerunning. Change a property only with evidence of an intended contract change; disclose reduced bounds.
5. Replay a failing counterexample against real code. An impossible step is model drift; possible steps identify a product bug.
6. For a new pass, deliberately break the guarded current behavior in scratch and confirm sensitivity, then restore.
7. Update coverage and sync only after checking that revision; a blocked check keeps its previous sync.

If sync history is absent, disclose the last verification-file change as a provisional baseline, not a previously confirmed code match.
Report in-sync, updated, bug, or blocked per check, including a stale pass that becomes a real bug after correction.
Keep verification maintenance separate from any product fix and state new code not yet covered.

