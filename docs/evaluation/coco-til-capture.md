# Session TIL change verification

Base: `04507c149787c9792bfedd1cd8f1f65dd2c59a6a`; branch: `feat/coco-til-session-capture`.
Spec: [session TIL capture](../specs/coco-til.md). Tier: shared/procedure change, checked with isolated local repositories and installer destinations. Starting checkout: main, clean at the base above.

## Executed checks

- `python3 scripts/validate.py`: passed, 30 skills; original source checksums, current coverage owners and payload references valid.
- `python3 -m unittest discover -s tests -v`: passed, 205 tests in 59.729 seconds. After final documentation and test-label cleanup, focused TIL tests passed (22) and source-fidelity tests passed (13).
- Real repositories: primary and nested linked invocations choose the same primary TIL; an ignored note remains after removing the linked worktree. Non-Git resolution creates no files. A moved/missing primary raises instead of creating a linked TIL. Bare primary plus its linked checkout reject fallback. Symlinked TIL rejects writes outside the root. Separate Git metadata and a newline pathname resolve a non-linked primary correctly.
- Initial fixtures exposed two defects: broken linked metadata looked like a non-Git folder, and separate metadata could be mistaken for the primary folder. Marker detection and non-linked Git identity checks fixed them; the same cases now pass.
- Existing checker and example exactly equal their base versions after substituting the skill identifier. Existing translated-template, schema/budget, index, malformed-template and literal-Markdown cases pass.
- Installer fixture: install the base into a temporary custom destination, preserve an unrelated user file, install the candidate, confirm old coco-learn removal and new resolver presence, and validate installed hashes/references. Passed. Live Codex destination preflight also passed with no ownership conflict.

## Direct scenario review

These are author walkthroughs of the final instructions, not an independent model evaluation or proof of semantic selection quality.

1. Changed selection path: a session has four worthwhile authentication candidates, one React concept and several activity-log lines. Select the best three authentication concepts and one React concept; exclude log lines, without splitting authentication into artificial topics or asking for approval. A sparse topic with only one concept produces only that note.
2. Empty and repeat paths: a session with only routine commands stops before any storage mutation. Rephrasing a concept already in TIL with no new evidence skips it and leaves content/dates unchanged; new evidence updates the existing semantic match. Conflicting user content is preserved for resolution.
3. Preserved format path: each selected concept uses the existing five sections, budget and translated TEMPLATE labels. Capture starts new notes as learning, never inferred understood. Example and checker fixtures validate the preserved format; note importance and truth still require agent judgment.

Self-review covered changed registration, bare invocation routing, callers, blog discovery, resolver/code/tests, schema preservation and attribution overrides. No independent fresh-context agent review was performed. Source snapshots and essential_rules remain unchanged; excluded teaching modes are explicitly recorded rather than claimed preserved. Primary storage prevents linked-worktree deletion loss, not loss of the primary folder itself or lack of backup.
