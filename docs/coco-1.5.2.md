# COCO 1.5.2: planning evidence for new implementations

- Coco-plan adds up to three bullets with confirmed paths, symbols and verification evidence when a new capability spans multiple implementation files or modules. The usual task scope, acceptance and planned checks still apply.
- Coco-build uses the note to start discovery and checks its pointers against the current checkout. It runs the usual implementation checks and omits the planning note from formal review by default.
- Existing behavior changes and single-file additions use the ordinary plan. The 30 skill identifiers and the installer interface are unchanged.

Paired Codex runs reduced discovery and total tokens for two new implementations. The existing-change and review results varied by task. The repository's evaluation record is at `docs/evaluation/plan-build-handoff.md`.

## Installation and recovery

```sh
npx --yes @thisis-joe/coco-skills@1.5.2 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.2 install --runtime claude
```

Use the same explicit scope as the existing installation and start a new client session. To roll back, reinstall pinned 1.5.1 with the same runtime and destination. Preserve personal edits if installer preflight reports a conflict.
