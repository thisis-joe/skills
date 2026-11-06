# Character-first blog thumbnail collaboration

Scope: `coco-blog` editorial cover-image procedure and its two entry references. No publication, image upload, or installation is performed by these checks.

## Fresh-context cases

A read-only reviewer independently read the changed skill and references with no conversation history.

1. Project guide supplies two approved characters; author selects one and requests revisions. Expected: reuse selection, inspect approved references, preserve appearance, agree on scene, render and revise the selected candidate, preview before final acceptance. Reviewer confirmed the sequence.
2. Author declines characters but still wants a thumbnail. Expected: ordinary technical-concept route without adding a mascot or abandoning the cover. Reviewer confirmed.
3. Author accepts the final image but has not authorized upload. Expected: local export/verification only; upload and publication remain separately authorized. Reviewer confirmed.

Reviewer found one ambiguity: local-notes referred to previewing an accepted image while editorial required preview before final acceptance. Corrected it to previewing the selected candidate before final acceptance; direct reread confirms agreement.

Project names and asset locations remain outside the reusable skill. Missing references/tooling remain explicit gaps. Existing raw-note privacy, draft state, worktree separation and human request ownership are preserved.

## Package checks

- `python3 scripts/validate.py`: passed (30 skills, source checksums, coverage and references).
- After synchronizing `main` at `04779a7` (package 1.5.3), the complete final suite passed: **217 tests**, 55.768 seconds in the same network-disabled Linux environment. Blog source files remained identical through the synchronization.
- Initial full suite on a disposable copy in `node:20-bookworm`, network disabled: **212 tests passed**, 62.325 seconds, Git 2.39.5 / Python 3.11.2 / Node 20.20.2. Included npm archive/install tests; no tests were modified or skipped.
- Earlier Windows run: 212 tests, 3 errors and 1 skip. Two errors required symbolic-link privileges; the third followed a UTF-8 decoding failure. The same suite passed on Linux without changing tests. The first sandbox attempt additionally lacked temporary Git write permission.
- Supported installer successfully staged the verified package in a separate local destination. Installed `coco-blog` was compared against staging and the final synchronized source: all 7 files matched. The 4 changed files were applied with a backup; hashes of 169 other installed files remained unchanged. This installs the unmerged feature branch locally, not a released package update.

## Consumer integration

The consumer blog README links its character guide. Approved public reference URLs respond with HTTP 200. The guide keeps project character names and asset locations outside the reusable package and leaves request merging to the human. The final fresh-context reread confirmed guide discovery, all three cases, missing-reference handling and preserved note-selection/privacy paths with no actionable findings.
