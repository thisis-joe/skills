# Integrate the development branch and push one work branch

## Targets and starting state

Discover remote names, refs, and paths from the actual repository and pass them safely as shell/process arguments. The `<...>` values below are placeholders for confirmed values; do not execute them literally.

- Check `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --porcelain=v1 -uall`, current HEAD, and staged content. With detached HEAD or an unborn branch, establish the work branch/initial commit before proceeding.
- Identify existing merge/rebase/cherry-pick/revert operations. Do not automatically abort or overwrite unrelated progress. Commit only confirmed, in-scope requested changes separately; do not stage all user changes or automatically stash/pop them. If safe scope is unresolved, report only the affected paths and necessary decision.
- The base ref is `refs/heads/dev` or `refs/heads/develop` at the confirmed remote. Do not assume the work branch's upstream or remote default HEAD is the development base. If both candidates exist, apply the explicit request, repository rules, and current PR base; ask only about remaining ambiguity. If neither exists, do not substitute `main` or create a remote development branch.
- Establish the push remote and target ref separately. Default to `refs/heads/<work-branch>` with the current branch's name. A `feature/x` branch tracking `origin/dev` must not be pushed to `dev` merely because of its upstream. A differently named target needs an explicit user request or confirmed repository rule. Validate the branch name with `git check-ref-format`.
- Do not expose tokens embedded in remote URLs. Inspect existing pushRemote, pushDefault, fork/PR links, and the actual push URL without changing global Git configuration. Multiple push URLs may change multiple repositories; do not push before establishing one write destination.

The name may change during final work-summary comparison. Record the initial remote work ref/OID and explicitly requested destination, then finalize the ref after [branch and ticket alignment](branch-and-ticket.md). Do not skip fetching unintegrated commits from the original work remote before renaming.

## Fetch current refs

After a failed remote query or fetch, do not treat old tracking refs as current. Query exact refs for actual branch existence and OIDs:

```text
git ls-remote --heads <base-remote> refs/heads/dev refs/heads/develop
git fetch <base-remote> refs/heads/<selected-development-branch>
git rev-parse FETCH_HEAD
```

Record the fetched development commit in a variable/trail before another fetch: the next fetch changes `FETCH_HEAD`. Query the target ref at the push remote with `ls-remote`; if present, fetch that exact ref and record its commit separately. Do not confirm only the name and then merge a stale `origin/dev`. Confirm each fetched object is a commit.

If the original remote work commit is not an ancestor of local HEAD, integrate that work branch first. Also integrate the development-base commit until it is an ancestor of HEAD. Do not discard others' remote work and force local history over it. Do not automatically apply `--allow-unrelated-histories` to unrelated histories.

## Merge and resolve conflicts

The default pull integrates each recorded commit with `git merge --no-commit --no-edit <fetched-commit>`. Since `--no-commit` permits fast-forward, distinguish an unfinished merge from a completed fast-forward using `MERGE_HEAD`. Honor a different repository integration policy without automatically choosing shared-history rewrites or a path requiring force-push.

On conflicts, obtain the complete list with `git status` and `git ls-files -u`. Read both versions, the common base, requirements, callers, and tests; preserve both intentions. Resolve delete/modify, rename, schema, lockfile, and binary conflicts according to their meaning. Use the repository's actual tools/policy for lockfiles without assuming new authority to install dependencies. Do not discard an entire side through broad `--ours`/`--theirs` use.

Resolve clear text conflicts and continue. If product contracts conflict, such as preserving versus changing a response format, present that choice and its alternatives. A conflict alone does not require renewed approval for every stage.

Stage only resolved paths. Confirm `git ls-files -u` is empty and inspect the diff and suspected markers. Do not blindly remove legitimate strings resembling markers. Run actual project lint/typecheck/test/build and needed behavior checks. Missing tools do not make required checks pass. Verify normal paths and regressions showing both remote and local changes survive together. Apply these checks to automatic merges without text conflicts too.

Complete an unfinished merge with an integration commit after checking. If check-related fixes create uncommitted changes, include only necessary changes and verify again. Apply the same process to additional integrations and confirm required checks for final HEAD. On failure, retain the original commits, current state, and recoverable integration points instead of erasing evidence with an automatic reset.

## Push and races

Before pushing, confirm [alignment between actual work, branch, and ticket](branch-and-ticket.md). If alignment was necessary, finish renaming, Jira updates, and readback before publication. Record the verified HEAD OID; recheck inclusion of the actual base commit, no unmerged index or unfinished Git operations, and completion of required work commits. Query the development-base and remote work refs again; if they advanced, integrate and verify the new commits and reassess the summary. After a rename, check both the original remote work ref and new destination ref. Stop after at most three refresh/integration rounds even if continuous advancement prevents a stable snapshot. Use a single explicit refspec with the verified OID as source rather than Git's default matching behavior. Do not publish an unverified new commit if HEAD changes meanwhile.

```text
git push <confirmed-single-push-destination> <verified-commit-OID>:refs/heads/<final-work-branch>
git ls-remote --heads <same-push-destination> refs/heads/<final-work-branch>
```

When filling the refspec from shell variables, brace them, `"${oid}:refs/heads/${branch}"`, and quote the branch as one argument ([shell rules](../../_coco-shared/runtimes.md#shell-commands)).

Push and fetch URLs may differ. Query/fetch refs at the write destination and use that same destination for push and readback. Do not apply the example directly to a remote with multiple push URLs. Specify one confirmed destination and read results there. `--force`, `--force-with-lease`, `--mirror`, `--all`, and protection-policy bypass are not this skill's default behavior.

After a non-fast-forward rejection caused by remote work advancing, refetch the development-base and push-target refs, integrate and verify required new commits, then retry. Limit total push attempts to three. Distinguish protection-policy, authentication, and check-hook failures from races; do not retry indefinitely or bypass checks.

A network error hiding the push response establishes neither failure nor success. Read the remote ref to determine publication before deciding the next action. After a successful push, an exactly matching OID confirms it. If the ref advanced to another commit, fetch it and check whether it contains the pushed commit. If it does, report that publication was confirmed and the remote subsequently advanced. Otherwise, or if verification is unavailable, report that state instead of flattening it into success or no conflicts.

Verification covers the fetched base commit and verified work commit. Do not claim atomic prevention of later development-branch changes by others. After confirmed publication, open a draft PR/MR only through the [pull/merge request procedure](pull-request.md). Remote branch deletion, protection-setting changes, edits to an existing PR/MR, PR merge, and deployment need a separate request.
