---
name: coco-merge
description: "Use when the user wants an already pushed branch's PR or MR merged directly into its target branch once the forge's checks pass, without coco-ship's release-readiness review."
license: MIT
---

# coco-merge

Land the pushed work branch's pull request or merge request in its target branch, then read the merged result back. The target is the request's own base, such as `develop`; only a request this skill opens targets the repository's default branch. This is the light path after `coco-push`: no readiness verdict, independent review, rollout plan or deployment. The bar is the forge's own gate (passing checks, required approvals, mergeability) applied to exactly the commit the user pushed. Follow the [common contract](../_coco-shared/contracts.md) and the [forge procedure](references/forge-merge.md). Read the files this request needs together in one call. Localize questions and reports to the user's language.

## Boundary

| Need | Skill |
|---|---|
| Land a pushed PR/MR in its target branch now, with the forge's gate as the bar | `coco-merge` |
| Sync with dev/develop, resolve conflicts, push, open a draft PR/MR | `coco-push` |
| Decide readiness, prepare a reviewed PR, land a dependent stack, release, tag or deploy | `coco-ship` |

Lighter than ship means fewer gates, not fewer protections. Never bypass branch protection or required checks (`--admin`, disabling rules), approve your own request, force-push or rebase the branch, resolve conflicts, push work commits, change Jira fields or state, delete branches unasked, tag, or deploy.

## Workflow

1. **Locate.** Read the repository root, current branch, HEAD, push remote and repository rules. A bare invocation is an execution request for the current branch. Identify the forge and its already authenticated CLI. Select the PR/MR named in the request, otherwise the open one whose source is the current branch in the push repository. Its base branch is the merge target. With no open request, the target is the default branch, read from the forge and confirmed with `git ls-remote --symref <remote> HEAD`. An execution request authorizes, for this one PR/MR: opening it when none exists, marking a draft ready, one merge-based branch update the forge requires, waiting for checks, the merge and its readback. Do not ask again for these. An explanation or review request changes nothing.
2. **Preflight.** Run [the preflight](tools/merge_preflight.py) from this skill's directory: `python3 <skill-dir>/tools/merge_preflight.py --repo <repo> --remote <remote> --branch <branch> --target <target-branch>`, adding `--expect-head <forge-head>` once the PR/MR is known. Exit 0 is clear, 1 lists blockers, 2 means it could not run; never read 2 as clear. It fetches objects only and moves no ref. Handle each code as the [preflight table](references/forge-merge.md#preflight-results) says: unpushed or conflicting work returns to `coco-push`; dev/develop commits that would ride along into another target, commits nobody here pushed, and an ambiguous integration base stop for the user. Uncommitted local changes are reported as excluded, never committed or stashed.
3. **Request.** With no open PR/MR, open one (not a draft) from the branch into the default branch, filling the repository template when one exists. A draft, such as the one `coco-push` opens, is marked ready. A PR/MR whose base is not the default branch, such as `develop`, is merged into that base without asking. Never retarget it unless the request explicitly names another target branch; then retarget only when the preflight against that branch is clear, otherwise report its blockers without merging anywhere. A closed or merged request is reported, not reopened. The forge's head must equal the preflight `head`.
4. **Gate.** Read mergeability, checks, approvals and unresolved review threads with their comment bodies from the forge in one shell call ([commands](references/forge-merge.md#gate)). Wait for pending checks with the forge's watch, bounded by the runtime; still pending at the limit is reported, not merged. A failed or cancelled check blocks: report its name and link and hand the fix to `coco-debug` or `coco-build`, unless the user explicitly waives that named non-required check. Missing approvals, unresolved required threads and other protection rules block; report what is missing. When the forge requires the branch to be up to date and reports no conflicts, update it once with the forge's merge-based update, never a rebase, then rerun the preflight with the new head and wait for its checks.
5. **Merge.** Take the method from repository rules, else the only one the forge allows, else what recent target-branch history shows, else a merge commit, which keeps work-unit commits. Pin the merge to the checked head. Keep the source branch unless the user asked or the repository deletes merged branches itself. If the forge rejects a moved head or changed state, re-read it and restart from step 2; stop after three merge attempts.
6. **Read back.** In one shell call, read the PR/MR's merged state and resulting commit once, fetch the target branch and confirm it contains that commit; re-read only while the state is still changing. A merge queue entry or armed auto-merge is `queued`, not merged: report what it waits for, and keep watching only when the user asked. Leave the user's checkout, local branches and uncommitted files as they were; offer to fast-forward the local target branch.

## Output

Lead with the final state, `merged`, `queued` or `blocked`, and the PR/MR URL. For `merged`, give the merge commit and target-branch readback; for `queued`, what it waits for; for `blocked`, each blocker's evidence, one plain sentence on its consequence and the skill that resolves it. Mention a request this skill opened or marked ready, a waived check, a merge method other than the repository default, and a source branch that was deleted.

`coco-merge` owns, on an execution request, opening a missing PR/MR to the default branch, marking it ready, the forge's merge-based update, the merge and its readback. Product fixes stay with `coco-build`, integration and pushes with `coco-push`, and release decisions with `coco-ship`.

Examples: `$coco-merge` in Codex or `/coco-merge` in Claude Code. Append `Merge the current branch's PR into its target branch once its checks pass` to provide an explicit request.
