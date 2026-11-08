# COCO 1.5.6: keep planning evidence within its intended handoff

**Contents:** [Planning and formal review](#planning-and-formal-review) · [Installation and recovery](#installation-and-recovery)

## Planning and formal review

- Coco-plan carries confirmed discoveries only in a short implementation note for a new capability spanning multiple implementation files or modules. Existing changes and single-file implementations retain expected scope, acceptance criteria and planned checks. Prior check details stay out of the whole plan for those tasks.
- Coco-build checks eligible pointers against the current checkout and uses scoped discovery when they no longer apply. It assembles the default formal review handoff from requirements, actual change scope, the current snapshot and its verification. Required checks that are pending or unavailable remain visible. Planning-only checks and findings stay out, wherever they appeared in the plan.

## Installation and recovery

```sh
npx --yes @thisis-joe/coco-skills@1.5.6 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.6 install --runtime claude
```

Use the same scope as your existing installation and start a new client session. To roll back, reinstall pinned 1.5.5 at the same runtime and destination. Resolve any local skill edit reported by installer preflight before retrying.
