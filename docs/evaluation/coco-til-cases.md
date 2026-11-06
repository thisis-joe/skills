# Troubleshooting case verification

Base: `9f5fbd760b0b10039d2e27379154aa2926094cfa`. Branch: `feat/coco-til-troubleshooting-cases`. Specification: [session troubleshooting cases](../specs/coco-til-cases.md).

## Scenario review

- Case only. A Jenkins job waited ten minutes before its first stage in build 71. The queue log and executor view showed occupied executors. Restoring the reserved executor was followed by a twenty-second wait in build 72, below the one-minute success criterion. The load was unrecorded, so recovery was observed without establishing a controlled comparison. With no separately selected concept, the write path needs the case file, case template and index alone. The local checker fixture passes for this layout and leaves the case and index intact.
- Insufficient evidence. With the build 72 recheck removed, the executor restoration is an action with no observed result against the success criterion. Case selection stops before storage setup for cases. A separate eligible concept still follows the concept path. With no eligible concept, the session stops before storage changes.
- No-new-evidence repeat. A differently worded title and the same build 71 and 72 observations match the existing case. The read-only match precedes initialization and the only selected case is skipped, preserving the file, timestamp and index entry. If a later recheck adds material evidence, update that same file. A changed build number by itself does not establish a different case.

The selection and matching scenarios are direct reviews of the instructions. Independent fresh-context execution was unavailable. The checker fixtures exercise on-disk structure, source pointer fields, ordered sections and missing, duplicate, misplaced or literal index links. The mixed-workspace fixture runs both checkers, and the existing regression suite covers the preserved concept format and storage rules.

## Package and installation checks

- Package validation and the full 217-test suite passed. Existing concept tests still cover translated headings, the 60-line budget, index behavior, and primary checkout resolution.
- The global installation already contained a managed TIL read-source feature and separate plan/build revisions. A temporary installation candidate preserved those revisions and reconciled the shared decision record and TIL entrypoint. Its inventory excludes the case template. Case, concept and read-source checks passed in that candidate.
- A scratch installation preserved an unrelated local file. Its case checker accepted a case-only Git workspace, and its shared inventory listed the case without listing its template. Repeated installer preflight returned unchanged after running both tools without bytecode caches in the managed directory.
