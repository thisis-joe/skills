# COCO 1.4.0: session exploration and evidence-backed answers

This release unifies technical investigation and optional quizzing under coco-askme. The coco-research name remains a forwarding alias.

- A bare call offers up to three concepts from the current session, each with relevance and free-text entry. It does not start a quiz or broad investigation.
- Compressed or handoff context is disclosed even when no recovery is needed. Missing context allows one bounded recovery batch of at most two identified session-linked sources (120 excerpt lines total), then a target question if still insufficient.
- A specific question receives a direct evidence-backed answer. Quiz requests retain one source-grounded question at a time, answer withholding and feedback.
- Evidence gathering follows material gaps or changed scope/version/revision; matching verified evidence is reused. Versioned primary sources, historical-intent uncertainty and requested findings artifacts remain supported.
- Personal note capture remains coco-til. The 1.3.0 primary-checkout, package-cache exclusion and cross-platform fixes are preserved.

## Migration

Existing coco-research invocations continue to work. Bare research now opens the same session-topic menu as askme. To preserve the former quiz-first interaction, explicitly request a quiz, for example `$coco-askme quiz me on this retry flow`. To investigate without a menu, include the actual question after either name.

Install through the existing CLI using an explicit runtime and scope. After installing, start a new client session or refresh its skills; file installation and actual client discovery are separate checks. No token, latency or learning improvement is guaranteed by instruction-size limits or the sampled conversational probes.

## Recovery

If the installed release fails, inspect existing ownership with the previous 1.3.0 package's dry-run, then reinstall that pinned version at the same explicit runtime and destination. Preserve personal TIL independently. npm publication is immutable; do not overwrite a published version or claim GitHub merge equals npm publication.

## Installation after npm publication

```sh
npx --yes @thisis-joe/coco-skills@1.4.0 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.4.0 install --runtime claude
```

The existing explicit `--project`, `--global`, `--dest` and `--dry-run` options remain supported. Choose the same scope as the existing installation; do not create an unintended global install. Source version, GitHub merge, npm registry publication and client discovery are separate states.
