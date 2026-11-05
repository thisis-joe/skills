# COCO 1.5.1: complete TIL inventories for blog recommendations

This release updates coco-blog to recommend author-owned topics from a complete local TIL inventory. Skill identifiers, the skill count (30) and the installer interface are unchanged.

- Show every eligible note in a numbered table, including duplicate titles and uncertain authorship; report unreadable notes and continue large inventories without silently omitting rows.
- Prioritize confirmed author contributions and suggest related note bundles with contribution context.
- Read bounded metadata and excerpts before selection, then full source bodies after selection. Continue an existing selection without reopening the menu.
- Keep inventory and recommendations separate from authorization to commit, push or publish.
- Isolate the worktree installer regression test from terminal input and the real global install. This is a test correction, not an installer interface change.

The release includes the mandatory skill contents lines and validation rules introduced in [1.5.0](coco-1.5.0.md). Existing instruction-simulation evidence is recorded in the repository at `docs/evaluation/blog-til-recommendations.md`; it does not guarantee every model's behavior.

## Installation and recovery

```sh
npx --yes @thisis-joe/coco-skills@1.5.1 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.1 install --runtime claude
```

Choose the same scope as the existing installation and start a new client session. If this release fails, reinstall pinned 1.5.0 at the same explicit runtime and destination. Preserve personal edits if installation reports a conflict. Source preparation, GitHub publication and npm publication are separate states.
