# COCO 1.4.2: default assignee, reviewer and labels for new PRs/MRs

This release changes how coco-push, coco-merge and coco-ship fill a pull or merge request they create. The skill count (30) and the installer interface are unchanged.

- The opener, the authenticated forge account that created the request, becomes its assignee and is requested as reviewer. An explicit request or repository rule naming other people wins.
- Labels come only from the repository's existing labels: a repository mapping first, otherwise the labels that clearly match the change's main kind. Labels are never created; when none fits, none is added and the report says so.
- Metadata is written after creation in separate calls and read back, so a refused field never fails or repeats the creation. GitHub refuses the author as reviewer (its API returns HTTP 422 while `gh pr edit --add-reviewer` silently exits 0, so the readback decides); that is reported as unavailable without substituting another reviewer.
- Requests that were already open keep their metadata.

The rule lives in [`skills/_coco-shared/request-metadata.md`](../skills/_coco-shared/request-metadata.md) and replaces coco-push's earlier instruction not to request reviewers or set assignees.

## Installation after npm publication

```sh
npx --yes @thisis-joe/coco-skills@1.4.2 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.4.2 install --runtime claude
```

Choose the same scope as the existing installation and start a new client session. If this release fails, reinstall pinned 1.4.1 at the same explicit runtime and destination. Source version, GitHub merge and npm publication are separate states.
