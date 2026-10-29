# COCO Skills 1.3.0

## Changes

The thirty-skill catalog replaces `coco-learn` with `coco-til`. Bare invocation captures the current session directly: select at most three reusable, evidenced concepts per meaningful topic, write one note per concept, and update semantic matches rather than generating duplicates. Sparse sessions need no filler; an empty session creates nothing. Repeated capture without new information preserves note content and dates.

TIL storage in Git repositories belongs to the primary checkout, independent of branch names and the invoking linked worktree. The resolver verifies common/primary Git identity and, for separate metadata listed as a working folder, reads recorded `core.worktree`, including relative paths. Missing, unrelated or linked targets fail closed. Outside Git, cwd/TIL remains supported. Blog discovery uses the same primary-note location.

## Migration

- Replace `/coco-learn` or `$coco-learn` calls with `/coco-til` or `$coco-til` after updating the relevant runtime. The supported ownership-aware installer removes the managed old identifier and preserves unrelated files. Personal installation conflicts remain protected.
- The note schema, translated template sections, budgets, checker and existing notes remain unchanged. Legacy linked-worktree notes are compared and copied into the primary TIL without deleting originals or overwriting divergent user content.
- Standalone explanation, review and mission-led teaching modes are removed from this entrypoint. Use ordinary chat for explanations, `coco-askme` for interactive questions and `coco-research` for broader investigation.
- New notes start as learning. Capturing a concept is not evidence of understanding. Primary storage prevents linked-worktree removal loss but does not back up ignored notes or protect against deletion of the primary checkout itself.

## Installation and publication boundary

The user authorized version `1.3.0` for both Git integration and npm publication. README registry examples target this version. Remote branch publication, main merging and npm publication are distinct results; release completion requires registry metadata/integrity readback and fresh-cache installation of the verified archive. The following source commands remain an alternative to npm.

From this source checkout:

```sh
python3 scripts/install.py --runtime codex --project /path/to/project
python3 scripts/install.py --runtime claude --project /path/to/project
```

Use existing explicit global/custom destinations when updating such installations. Update both runtimes separately and start a new session. The earlier package version can be reinstalled at the same explicit destination to roll back; preserve TIL independently because neither installer commits or removes personal notes.

## Evidence

[Implementation and P2 regression evidence](evaluation/coco-til-capture.md) records real repository resolution, note-format preservation and installer tests. After integrating main at `dd28983`, package validation and all 207 unit tests passed (69.263 seconds). The archive tests exercise the packed CLI and both runtime installers, and assert that the 1.3.0 release notes and new resolver are included while the old skill is absent. Tests validate resolver behavior and layout, while concept selection remains agent judgment. Direct review is not an independent model evaluation. Original source snapshots and essential rules remain preserved, with team overrides explicitly recorded.

CI archive correction: package file exclusions keep Python caches out even when present. An isolated contaminated-package regression and all 208 standing tests passed without bytecode suppression. Space-path resolution remains cross-platform; newline filenames are additionally tested on POSIX.
