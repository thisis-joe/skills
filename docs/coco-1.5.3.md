# COCO 1.5.3: troubleshooting cases from a session

- Coco-til can save one representative troubleshooting case per session in `TIL/cases/<slug>.md` and link it under `문제 해결 사례` in `TIL/INDEX.md`. A case can be the only output.
- Cases record the symptoms and success criteria, the evidence behind each diagnostic decision, a procedure for recurrence, and the fix and revalidation. The procedure distinguishes actual actions from examples and read-only checks from actions that change state.
- Capture requires a recheck that meets the success criteria. A matching case changes only when the session supplies new or corrected evidence.
- Concept notes keep their existing format, checker and limit of three per topic. Cases have a separate template and checker. Both use the same TIL root in the primary checkout.

## Installation and recovery

```sh
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.3 install --runtime claude
```

Use the same scope as your existing installation and start a new client session. To roll back, reinstall pinned 1.5.2 at the same runtime and destination. Keep your local TIL files during either installation. Resolve any local skill edit reported by installer preflight before retrying.
