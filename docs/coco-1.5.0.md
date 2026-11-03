# COCO 1.5.0: a contents line atop every skill

This release gives every coco skill entrypoint a table of contents and makes it a package rule. Skill names, the skill count (30) and the installer interface are unchanged.

- Each `skills/coco-*/SKILL.md` opens with a `**Contents:**` line directly below its title, linking every `##` section in order, so readers and agents see a skill's shape before its body.
- `coco-research`, previously a single paragraph, gains a `## Forwarding` section so its contents line has a target. Its forwarding behavior is unchanged.
- `scripts/validate.py` rejects a skill whose contents line is missing, links a renamed section, omits a section or lists them out of order. Fenced code is ignored. Anchors use GitHub's heading slug.
- The always-read size caps for coco-merge and coco-ship and the coco-askme entry cap each rise by 100 characters to absorb the line; the decision is recorded in [`decisions.md`](../skills/_coco-shared/decisions.md).
- The README is rewritten around installation, the four-stage flow and the full skill list; per-release history moves to the release notes.

## Compatibility

A team that adapted a skill with coco-updateskill must keep its contents line in step with its sections, or validation and installation stop with `Contents must link every ## section in order`. Running `validate --installed` from 1.5.0 against a bundle installed by 1.4.x fails until that bundle is reinstalled with 1.5.0.

## Installation after npm publication

```sh
npx --yes @thisis-joe/coco-skills@1.5.0 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.0 install --runtime claude
```

Choose the same scope as the existing installation and start a new client session. If this release fails, reinstall pinned 1.4.2 at the same explicit runtime and destination. Source version, GitHub merge and npm publication are separate states.
