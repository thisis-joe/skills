# COCO 1.5.4: collaborative blog thumbnails

**Contents:** [Character-first blog thumbnails](#character-first-blog-thumbnails) · [Installation and recovery](#installation-and-recovery)

## Character-first blog thumbnails

- Coco-blog reads approved character names and references from the consumer project's image/brand guide and asks the author whether to use one, both where applicable, no character, or a recommendation before drawing.
- The author and assistant agree on a scene, review rendered candidates, and iterate on composition, expression, props and background while preserving character identity and settled choices.
- Character-free concepts remain available. Missing references are requested rather than invented; the selected candidate is checked in real desktop/mobile layouts before final acceptance.
- Final-image acceptance does not authorize upload or publication. Project-specific character names stay outside the reusable skill.

## Installation and recovery

Run these commands once 1.5.4 is available on npm. Before then, use the [source installer](../README.md#시작하기).

```sh
npx --yes @thisis-joe/coco-skills@1.5.4 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.4 install --runtime claude
```

Use the same scope as your existing installation and start a new client session. To roll back, reinstall pinned 1.5.3 at the same runtime and destination. Resolve any local skill edit reported by installer preflight before retrying.
