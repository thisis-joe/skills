---
name: coco-push
description: "Use when the user wants the current Git branch synchronized with remote dev or develop, its summary and linked Jira task aligned with actual work when needed, and the verified branch pushed."
license: MIT
---

# coco-push

Integrate the latest remote `dev` or `develop` changes into the current work branch, resolve conflicts, verify, and push that branch normally. Before pushing, compare the actual work with the branch name's task summary; align the name and linked Jira task when the summary is unsuitable. Follow the [common contract](../_coco-shared/contracts.md), [synchronization procedure](references/sync-and-push.md), and, when needed, [branch and ticket alignment](references/branch-and-ticket.md). Localize questions and reports to the user's language.

## Workflow

1. Check the repository root, current branch, HEAD, working state, unfinished Git operations, remotes, upstream, repository rules, and check commands. Record the starting branch, commit, and changed paths. An execution request authorizes synchronization, conflict resolution, necessary branch-name and linked Jira title/description alignment, and a normal push within this scope; do not request the same authorization again. For explanation or review only, change neither Git nor Jira.
2. Establish the base remote and `dev`/`develop`, separately from the push remote and branch. Prefer evidence from the explicit target, repository rules/configuration, or current PR base. If both development branches exist with no evidence to choose between them, ask the user to choose. If neither exists, do not invent another base. The default push target has the final work branch's name; do not replace it with the base branch. Separately record the pre-change remote work ref and any explicitly requested push target.
3. Preserve uncommitted user changes. Prepare owned, in-scope requested work as separate work-unit commits after the necessary checks. If ownership is unknown or a merge/rebase or other operation already exists, report the state and required decision. Do not erase the starting state through an indiscriminate commit, stash, reset, or clean.
4. Query and fetch the actual latest remote refs, recording the fetched commits. Integrate commits found only at the push target too. Separate the default pull operation into `fetch + merge` to preserve shared history. Resolve each conflict after reading both intentions, surrounding code, and tests. Ask only about an unresolved product-behavior choice.
5. Check unmerged index entries, suspected conflict markers, and the diff; run required repository checks and verification of conflict effects. Stage only resolved paths and complete any necessary integration commit. Verify semantic conflicts even after automatic merging. Do not push with required checks failed or unrun, or with an unfinished Git operation.
6. Read the diff from the selected development base to final HEAD, branch-specific commits, and task requirements to summarize this branch's actual work. Keep the name and ticket if the branch summary appropriately describes its main purpose and scope. If the purpose changed or important work is omitted, follow [branch and ticket alignment](references/branch-and-ticket.md) to revise the summary and update and reread both Jira Summary and Description. If required information, write capability, or authority is unavailable, or the update cannot be confirmed, record the state and stop before pushing.
7. Immediately before pushing, recheck whether the base ref and remote work ref advanced; if so, reintegrate, reverify, and reassess the work summary. After a rename, check both the final-name ref and original remote work ref. Push the verified HEAD normally to the confirmed single write destination using one explicit refspec. Do not force-push, mirror, push all branches, or bypass protection rules. After a race rejection, fetch, integrate, and verify again. Limit refresh/integration rounds and total push attempts to three each. Authentication, protection-policy, and network failures are not races.
8. Confirm the successful response and reread the remote ref. Success requires the target remote branch to match the verified commit. If it immediately advanced to another commit, check ancestry and distinguish the observed state. If local changes occurred after verification, do not present an unverified HEAD as successfully pushed.

## Output

Report the base remote/branch and fetched commit; actual work summary and reasons for keeping or changing the name; branch before/after, Jira key, title/description changes and readback; final push target; conflicts and decisions; created commits; check results; pushed commit and remote confirmation; and remaining user changes or blockers. Distinguish retaining the original remote name and partial success. A conflict-free result applies only to the checked scope and time, not future races.

`coco-push` owns integration commits, necessary branch/linked-ticket alignment, and pushing that branch. Jira alignment is limited to Summary and Description. New features and unrelated fixes remain separate `coco-build` work; do not mark product work complete or change Jira status, assignee, or other fields. Deleting the original remote branch, creating or merging a PR, and deployment are outside this request.

Examples: `$coco-push` or `$coco-push Update the current branch from origin/develop, resolve conflicts, verify, and push`.
