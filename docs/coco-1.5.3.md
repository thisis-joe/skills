# COCO 1.5.3: troubleshooting cases and collaborative thumbnails

- Coco-til can save one representative troubleshooting case per session in `TIL/cases/<slug>.md` and link it under `문제 해결 사례` in `TIL/INDEX.md`. A case can be the only output.
- Cases record the symptoms and success criteria, the evidence behind each diagnostic decision, a procedure for recurrence, and the fix and revalidation. The procedure distinguishes actual actions from examples and read-only checks from actions that change state.
- Capture requires a recheck that meets the success criteria. A matching case changes only when the session supplies new or corrected evidence.
- Concept notes keep their existing format, checker and limit of three per topic. Cases have a separate template and checker. Both use the same TIL root in the primary checkout.

## Character-first blog thumbnails

- Coco-blog reads approved character names and references from the consumer project's image/brand guide and asks the author whether to use one, both where applicable, no character, or a recommendation before drawing.
- The author and assistant agree on a scene, review rendered candidates, and iterate on composition, expression, props and background while preserving character identity and settled choices.
- Character-free concepts remain available. Missing references are requested rather than invented; the selected candidate is checked in real desktop/mobile layouts before final acceptance.
- Final-image acceptance does not authorize upload or publication. Project-specific character names stay outside the reusable skill.

## Installation and recovery

```sh
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude
```

Use the same scope as your existing installation and start a new client session. To roll back, reinstall pinned 1.5.2 at the same runtime and destination. Keep your local TIL files during either installation. Resolve any local skill edit reported by installer preflight before retrying.
