# Local TIL inventory and recommendations

Scope: `skills/coco-blog/SKILL.md` and `references/local-notes.md`. Synced without conflicts to `origin/main` at `3c78bb03e43f58885bc0afed7bb2016d09d676b4` on branch `feat/coco-blog-til-recommendations`.

## Acceptance and fresh-context review

Read-only instruction simulations checked the following cases:

- Four mixed-contributor notes: complete numbered table; confirmed own OAuth fix and API decision prioritized; shared diagnosis + fix bundle qualified by contributor.
- Large inventory with duplicate titles, an unreadable note and unknown identity: every eligible row retained, bounded excerpts, explicit uncertainty and response-limit continuation.
- Previously selected teammate note, draft only: selected material reused without reopening the menu, inventing ownership or authorizing Git/publication actions.

All three passed. Review found an entrypoint conflict between selected-file-only reading and inventory excerpts. The entrypoint now permits bounded metadata/excerpts before selection and full source bodies only after selection. A focused fresh-context recheck confirmed the resolution. These are instruction simulations, not guarantees of every model's behavior or a live run over private notes.

## Verification after main integration

- `python3 scripts/validate.py`: passed, 30 skills.
- `python3 -m unittest discover -s tests -v`: passed on an isolated Linux copy with Git 2.53.0, 212 tests, 15 npm tests skipped because Linux Node is unavailable.
- `python -m unittest discover -s tests -p test_npm_distribution.py -v`: passed on Windows with Node/npm, all 15 tests. Together these runs cover the full suite.
- Supported installer and installed validation: passed in a disposable destination before integration, 30 skills and 126 files. Active installed skills were not replaced.
- `git diff --check`: passed.

Earlier environment checks did not pass: Windows lacked symlink privileges and exposed an unchanged template-test error; Ubuntu with Git 2.34.1 lacked the worktree/merge-tree options required by existing tests. The final runs above used current main and supported existing environments. No tests or security settings were weakened.

The update adds no external-write authorization. Inventory, contribution ranking and bundle suggestions do not authorize commit, push, request creation or publication. Installation, package versioning and registry release are outside this PR.
