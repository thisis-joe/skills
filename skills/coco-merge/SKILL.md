---
name: coco-merge
description: "Use when the user wants an already pushed branch's PR or MR merged directly into its target branch once the forge's checks pass, without coco-ship's release-readiness review."
license: MIT
---

# coco-merge

Land one pushed PR/MR in its own base, such as `develop`, then read back the result. Only a request this skill opens uses the confirmed base repository's default branch. The bar is the forge's checks, approvals and mergeability on the pushed commit; readiness, independent review, rollout and deployment stay with ship. Read the [common contract](../_coco-shared/contracts.md) and [forge procedure](references/forge-merge.md) together. Localize questions and reports to the user's language.

## Boundary

| Need | Skill |
|---|---|
| Land a pushed PR/MR in its target branch now, with the forge's gate as the bar | `coco-merge` |
| Sync with dev/develop, resolve conflicts, push, open a draft PR/MR | `coco-push` |
| Decide readiness, prepare a reviewed PR, land a dependent stack, release, tag or deploy | `coco-ship` |

Lighter than ship means fewer gates, not fewer protections. Never bypass branch protection or required checks (`--admin`, disabling rules), approve your own request, force-push or rebase the branch, resolve conflicts, push work commits, change Jira fields or state, delete branches unasked, tag, or deploy.

## Workflow

1. **Locate.** Read root, branch, HEAD, push destination and repository rules; identify the forge and existing authentication. A bare invocation executes on the current branch; explanation/review changes nothing. Select the named PR/MR, otherwise the open one from this branch and source repository. Confirm its actual base repository and branch from forge metadata; never guess a fork's upstream. Without a request, confirm the intended base repository and its default branch against `git ls-remote --symref <target-remote> HEAD`. Execution authorizes this one request's creation, draft readiness, one required merge-based branch update, check waiting, merge and readback; do not ask again.
2. **Preflight.** Run [the preflight](tools/merge_preflight.py) with the confirmed source/base remotes and branches and `--expect-head <forge-head>`; omit expected head only before a request exists. Pass `--target-remote` for a fork; its default is source for same-repository requests. Exit 0 is clear, 1 lists blockers, 2 could not run; never read 2 as clear. It fetches objects without moving refs. Record source/base repositories and branches, head and target tip. Follow the [result table](references/forge-merge.md#preflight-results): unpushed/conflicting work returns to push; carried dev/develop work, unseen commits and ambiguous integration base stop. Local edits stay excluded.
3. **Request.** Open a missing request as non-draft into the confirmed default branch using its template. Mark a draft ready. Merge an existing request into its base, including `develop`, without asking. Retarget only on an explicit target request after clear preflight there; otherwise merge nowhere. Recheck the observed request identity/head before retargeting, then confirm the applied target matches preflight. Report closed/merged requests without reopening. Before readiness, branch update or merge, reread and compare source/base repository and branch plus head to the preflight receipt; a change restarts discovery/preflight within the authorized target scope.
4. **Gate.** Read mergeability, checks, approvals and unresolved review threads with their comment bodies from the forge in one shell call ([commands](references/forge-merge.md#gate)). Wait for pending checks with the forge's watch, bounded by the runtime; still pending at the limit is reported, not merged. A failed or cancelled check blocks: report its name and link and hand the fix to `coco-debug` or `coco-build`, unless the user explicitly waives that named non-required check. Missing approvals, unresolved required threads and other protection rules block; report what is missing. When the forge requires the branch to be up to date and reports no conflicts, update it once with the forge's merge-based update, never a rebase, then rerun the preflight with the new head and wait for its checks.
5. **Merge.** Use repository method, else the only allowed method, else recent target history, else a merge commit preserving work units. Immediately revalidate the receipt, then pin the checked head. Head pinning cannot atomically pin the base: report that remaining API race. Keep the source branch unless requested otherwise or deleted by repository policy. A rejected changed state restarts preflight; stop after three merge attempts.
6. **Read back.** In one shell call, read the PR/MR's merged state and resulting commit once, fetch the target branch and confirm it contains that commit; re-read only while the state is still changing. A merge queue entry or armed auto-merge is `queued`, not merged: report what it waits for, and keep watching only when the user asked. Leave the user's checkout, local branches and uncommitted files as they were; offer to fast-forward the local target branch.

## Output

Lead with `merged`, `queued` or `blocked` and the PR/MR URL. Give the merge commit and target readback, queue prerequisite, or each blocker's evidence, consequence and resolving skill. Mention creation/readiness, waived checks, a non-default merge method and source deletion when applicable.

Merge owns request creation/readiness, the forge's merge update, landing and readback. Product fixes belong to `coco-build`, integration/pushes to `coco-push`, release decisions to `coco-ship`.

Examples: `$coco-merge` in Codex or `/coco-merge` in Claude Code. Append `Merge the current branch's PR into its target branch once its checks pass` to provide an explicit request.
