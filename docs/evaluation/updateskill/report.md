# Bounded coco-updateskill application

One direct application to three self-authored temporary cases. This is not a benchmark, broad certification, or an independent behavioral evaluation. No author chat or other evaluation reports were read. All writes stayed under this temporary root. No real user question, agent spawn, remote push, deployment, service write, global install or maintained repository edit occurred.

## Instruction sources and fixture

Applied the maintained `skills/coco-updateskill/SKILL.md`, `references/team-update.md` and `_coco-shared/contracts.md` read from `/Users/Joseph/workspaces/skills`. Their starting/final hashes, plus the allowed installer/checker source hashes, are captured in `instruction-source-hashes.before.json` and `.after.json`; all are equal. Checker/installer copies in every fixture are byte-identical to those starting files.

Each fixture is a two-entrypoint maintained COCO package with registration/UI metadata, shared contract and existing decisions, a synthetic inert original plus manifest checksum and coverage facts, actual AGENTS.md/CI commands, three preservation/package unit tests, an owned local installation, an unrelated note and an unrelated personal skill. Git uses /dev/null global/system configuration and only fixture-local identity/hooks settings; HOME and CODEX_HOME are untouched.

## Results

| Case | Actual outcome | Work-unit commit | Installation |
| --- | --- | --- | --- |
| CASE-A | source-and-install-complete | 920d6eaaf89c | installed |
| CASE-B | proposal-only-complete | none | unchanged-no-install-attempt |
| CASE-C | source-complete-install-blocked | 59e4e770b374 | blocked-user-modified-managed-file |

A replaced universal pytest with discovered project checks, retaining conditional scope for other projects. The shared caller-impact rule lives once in the shared contract and is linked by both entrypoints and references. Exactly eight scoped maintenance files changed. Existing D001 explains why upstream behavior was adapted; D002 explicitly identifies the new team convention. Source bytes, source manifest checksum, original essential_rules, names/discovery/UI policy/dependencies remain intact. The supported dry-run and install succeeded. The installed validator passed for two skills/eight files; every managed installed file hash matches its source. Both unrelated user files were preserved.

B produced `case-b/proposal.md` with replacement rule text, explicit affected paths, provenance treatment and eventual check/install impact. Maintained-source and installed-file hashes, branch and HEAD remain exactly unchanged. No work-unit commit or installation was attempted for the proposal. Baseline installation in its log belongs to fixture setup, before this request.

C made the same validated scoped source change on a feature branch and committed it. The supported installer dry-run exited 2: `Preserving user-modified or extra file: coco-build/SKILL.md`. Installation remains blocked. No subsequent install, force operation or ownership-manifest rewrite was attempted. Every installed byte, including the personal managed-file edit and unrelated files, remains identical to its pre-update state. `case-c/preserved-installed-user-change.diff` preserves the exact user change. No supported conflict-resolution decision was available within the bounded request, so source completion and installation completion remain distinct.

## Actual checks and evidence

Each baseline and each applicable source result ran `python3 scripts/validate.py` (two skills, source checksums/coverage/references) and `python3 -m unittest discover -s tests -v` (three tests, all pass). A/C also passed `git diff --check` before an atomic commit. A used supported `install.py --root <fixture> --dest <fixture-install> --dry-run`, then the actual install and `validate.py --installed <fixture-install>`. C used the same supported preflight and preserved its expected rejection. Full argv/cwd/exit/output records are in each `commands.jsonl`; full source/installed SHA-256 maps are in each `before.json`/`after.json`. `results.json` supplies structured summaries and evidence paths.

Inspected final diffs and actual A installed contract, B proposal and unchanged hashes, and C user conflict diff and preflight output. Direct inspection confirms both caller links, single rule ownership, provenance distinction, clean worktrees and scoped commits. The fixture tests check package validity and preserved source/UI facts; they do not prove behavior across arbitrary projects or future requests. No independent reviewer or external-service behavior was claimed because the application constraint prohibited agents and the scope was local.

## Setup failure retained

Initial fixture setup failed because scripts/ had not been created before copying the allowed checker files. Fixed setup.py and recreated only the incomplete temporary case-a directory. This happened before baseline/application evidence; it is retained in `setup-repair.txt` and results.json and is not counted as a skill outcome. No checker was weakened or bypassed.
