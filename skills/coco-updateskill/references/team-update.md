# Maintain skills for team conventions

## Authoritative source and scope

Find the authoritative repository from the current workspace, user-specified location, and project maintenance guidance. For COCO, compare registration in `coco.json`, `skills/coco-*/`, `skills/_coco-shared/`, and the actual installation manifest. Do not depend on one user's absolute path or search all personal directories. If the source is unconfirmed, establish its location rather than arbitrarily promoting installed files to a new source of truth.

First distinguish maintainers and source locations for installed system or external-plugin skills. Direct cache edits may disappear on update. If a team copy is needed, align its purpose, name, and location with the request before proceeding; retain upstream licenses and attribution. Do not turn an existing-skill update into arbitrary creation of a new skill, upstream upgrade, or automatic installation.

Reuse agreed team commands, review standards, and execution modes. Apply conditional modes where repository rules differ. For example, do not copy one Node repository's `pnpm` commands into a Python repository or every team skill's common commands. Respect explicit user/team scope and ask only about missing material behavior.

## Dedicated branch and worktree

This team rule applies whenever the update will change any maintained file: skill sources, references, UI metadata, registration, decision records, evaluation evidence, or tests. A proposal-only, review, or explanation request changes no files and creates neither a branch nor a worktree.

1. **Record the starting checkout.** Before creating anything, record its path, branch, HEAD, and dirty and untracked paths. It stays read-only for the whole update.
2. **Confirm the base.** Use the repository's documented integration branch, such as `main`, unless the user or the established task names another base. If the change depends on commits that exist only on the starting branch, or on uncommitted edits there, ask which base to use. Never copy, stash, or move uncommitted user changes into the worktree.
3. **Create a new branch.** Name it according to repository branch rules, for example `feat/<skill>-<change>`, and validate it with `git check-ref-format --branch`. Never reuse, reset, or rename a branch that belongs to other work. Git refuses a branch already checked out in another worktree; do not force it.
4. **Create a new linked worktree.** Prefer the runtime's supported worktree feature when one exists; otherwise run `git worktree add -b <branch> <path> <base>`. Choose a path outside tracked content, such as an ignored worktree directory the repository designates or a sibling directory, rather than a guessed personal absolute path. Never overwrite an existing path. Confirm the new path, branch, and base with `git worktree list --porcelain` before the first edit.
5. **Work only inside it.** Read the target source, edit, run checks, commit, and run the installer from the worktree path, for example `python3 <worktree>/scripts/install.py ...`, so the installed copy is the verified branch version. When installing, report that the installed copy comes from the unmerged dedicated branch.
6. **Confirm isolation before reporting.** Compare the starting checkout's branch, HEAD, and dirty and untracked paths with the recorded state. Report any difference instead of hiding or reverting it.
7. **Leave it in place.** Report the worktree path, branch, and base. Push, PR, merge, and worktree removal are separate scope; remove a worktree only on request through the [owned worktree cleanup](../../_coco-shared/advanced/context.md#conditional-owned-worktree-and-simulator-cleanup) procedure.

A linked worktree counts as dedicated only when its branch was created for this update from the confirmed base and holds no unrelated commits or changes, such as a host-created session worktree for this request or the worktree of an interrupted run of the same update. Otherwise create a new one. If the source is not a Git repository or the worktree cannot be created because of permissions, an existing path, or Git support, stop before editing, report the blocker, and ask how to proceed. Editing in the starting checkout is never a fallback.

## Compare before/after and inspect effects

Keep maintained COCO instruction documents and discovery descriptions in English. Localize actual replies to the user's language and preserve user-owned literals such as exact Jira Summaries.

Capture pre-change files/commits/hashes and relevant cases. Briefly state the intent as "current behavior → desired team behavior → preserved behavior → verification method." Do not read all unrelated skill sources or recreate an agreed development specification from the beginning.

Identify which file owns each current rule. If common contract, routing, decision records, and entrypoints conflict, establish one owner and reference it. Find callers and uses with `rg` or available reference search. Align descriptions, procedure, conditional references, and examples so they do not promise different behavior. Change only necessary fields in `agents/openai.yaml`; do not change existing policy/dependencies or automatic selection behavior without a request.

Do not execute the skill merely because you are editing it. For example, modifying `coco-push` does not authorize a remote push from a user's repository. Test behavior within authorized boundaries using temporary repositories, fake credentials, or local destinations. Reviewing only policies/stages does not establish actual service behavior.

When modifying `coco-updateskill` itself, retain the starting version and agreed scope; instructions changed during the work do not expand authority or completion conditions. Reread the final files to ensure the applied procedure, changes, and verification agree.

## Attribution and team decisions

- `sources/**/*.source` and `sources/manifest.json` are frozen source evidence. Do not overwrite source text or its original SHA-256 to change team wording/rules. Handle an upstream-version update as a separate attribution update only when requested.
- Retain original `essential_rules` in `sources/coverage.json` as facts about that source snapshot. Adoption/modification/exclusion reasons and `implemented_references` must reflect actual team changes. Align related guidance when source mappings change. Do not remove an original requirement while still claiming it is preserved.
- Record common-rule choices and reasons in the existing `skills/_coco-shared/decisions.md`. Use existing repository records/commits and evidence for individual changes. Do not create duplicate authoritative maintenance records.

## Verification and installation

Discover actual COCO check commands and run them from the dedicated worktree. Examples for the current package:

```text
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/install.py --runtime <confirmed-runtime> <confirmed-scope> --dry-run
python3 scripts/install.py --runtime <confirmed-runtime> <confirmed-scope>
python3 scripts/validate.py --installed <confirmed-installation-directory>
```

Use `codex` or `claude` for the confirmed runtime. The confirmed scope is the installation being updated: `--project <folder>` for a project install, `--dest <directory>` for a custom one, or `--global`. Pass it explicitly, because an agent shell is not a terminal and the installer falls back to the global folder without one, which would bring COCO back to every project for a user who moved to project installs. Follow the [runtime guide](../../_coco-shared/runtimes.md) when both runtimes are installed. Do not assume another repository has these commands. Also run available skill-format checks. Format validation does not prove sound judgment: from the procedure tier up, test actual cases for both changed and preserved paths; a wording-tier change needs only these package checks and a diff reread. If required tools or independent review are unavailable, distinguish confirmed scope from unverified scope. Do not weaken checks or rewrite historical evaluation reports to hide failure.

Before installation, compare the ownership manifest with current files and use the supported installer's preflight. Preserve and show differences for conflicts involving personal edits, extra files, same-name external skills, or symbolic links. Do not delete the ownership manifest or manipulate hashes to manufacture installation success. If a supported preservation/migration procedure cannot be established, leave installation blocked separately from source changes.

Reread relevant source/installed files, hashes, and references and confirm other skills and personal files survive. If installation fails after the source commit, do not recreate the existing commit. On resumption, locate the dedicated worktree with `git worktree list --porcelain`, inspect its actual commit/change/installation state and continue from the remaining installation step. Distinguish the verified version from actual installation state in the report.
