# Session TIL implementation plan

Specification: [session TIL capture](../specs/coco-til.md).

1. Rename entrypoint and registration; replace teaching modes with session selection/capture and stable primary-checkout storage. Align callers and adoption records without changing frozen source facts.
2. Add a read-only primary-checkout resolver; retain the note checker/schema. Exercise real repository destinations and preserved note behavior, and record scenario review.
3. Run required package/unit checks, self-inspect, commit the work unit, and use the supported installer at the established Codex destination. Preserve conflicts, report source/install/publication separately; leave the dedicated branch and worktree available.

Source implementation and verification completed; see [verification evidence](../evaluation/coco-til-capture.md). Installation readback follows the source commit.

## P2 follow-up

1. Add real-repository regressions for separate metadata with a linked worktree,
   including absolute/relative primary paths and invalid configured targets; observe failure.
2. Resolve the primary from common metadata and verify its primary/common identity.
3. Run package and all unit checks, self-review, commit separately, install at the
   established Codex destination and validate readback. Preserve the existing note format.

P2 source correction, red/green regressions, 207-test suite, package validation and
installer fixture passed; see the verification record's P2 follow-up. Installation
readback is performed after the follow-up commit.
