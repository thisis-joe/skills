# COCO 1.5.5: verify planning evidence before implementation

**Contents:** [Planning and build handoff](#planning-and-build-handoff) · [Installation and recovery](#installation-and-recovery)

## Planning and build handoff

- Coco-plan passes a brief implementation note for a new capability spanning multiple implementation files or modules. Tests alone do not expand the implementation scope. The note records the known source revision when a pointer or check result depends on it.
- Coco-build checks the referenced paths, symbols and revision against the current checkout. Missing, stale, conflicting or irrelevant pointers trigger scoped discovery for the affected part. Build runs its usual implementation checks.
- Existing changes follow the ordinary plan. Formal review receives requirements, actual change scope and current verification evidence.

## Installation and recovery

Install 1.5.5 from npm with the command for your runtime. To install from a checkout, see the [source installer](../README.md#시작하기).

```sh
npx --yes @thisis-joe/coco-skills@1.5.5 install --runtime codex
npx --yes @thisis-joe/coco-skills@1.5.5 install --runtime claude
```

Use the same scope as your existing installation and start a new client session. To roll back, reinstall pinned 1.5.4 at the same runtime and destination. Resolve any local skill edit reported by installer preflight before retrying.
