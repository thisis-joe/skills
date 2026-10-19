# LET'S Implementation Plan

**Goal:** Deliver and install a coherent, source-traceable merge of all three skill trees under LET'S.
**Spec:** [design.md](design.md)
**Execution:** User explicitly requested autonomous completion; execute without another design approval. Use independent agents for source audit and behavioral validation, not permission expansion.
**Stack:** Markdown, JSON, Python 3 standard library; no runtime dependencies.

## Tasks

- [x] 1. Pin all upstream sources, retain inert originals and licenses, inventory every skill/command, and record rule conflicts. Source audits must cover all inventory rows.
- [x] 2. Establish common input/output, routing, evidence, review-scope, commit/resume, and authorization contracts. Record baseline behavior before authoring integrated skills.
- [x] 3. Create each LET'S entrypoint and its needed conditional reference; validate each before moving on. Fold duplicate procedures into one owner; preserve specialized capabilities through explicit modes.
- [x] 4. Test then implement read-only Git review-scope collection: committed, staged, unstaged, deleted and untracked; literal task paths; unavailable refs; no mutation.
- [x] 5. Test then implement package validation and installation: source checksums and coverage, references after copying, foreign file conflicts, idempotence, symlinks, and dry-run.
- [x] 6. Evaluate representative integrated workflows in fresh contexts: lightweight, clarified feature, failure, dirty work, interrupted commit, unavailable browser, migration, formal verification, specialized reference retrieval. Record limitations honestly. See [evaluation](evaluation/README.md); moved-target limits are retained, with a frozen recovery rerun.
- [x] 7. Produce Korean usage/selection documentation; install the suite into the user's Codex skill directory, preserving pre-existing skills and verifying installed bytes. [Installation readback](evaluation/installation.json): 22 skills/72 files, unchanged second install, 50 unrelated entries preserved.
- [x] 8. Run full validation and tests; obtain fresh whole-branch review, fix material findings, commit by work unit, and audit every requirement against current files and installed state. [Review resolutions](evaluation/review-resolution.md), [completion audit](evaluation/completion-audit.md); 23 tests and 22 format checks passed.

## Interfaces

- `sources/manifest.json`: author/repository/commit plus every retained path, local path and SHA-256.
- `sources/coverage.json`: one row per upstream SKILL.md/command: author, original path, integrated family, disposition, essential rules, adaptation reason and implemented references.
- `skills/_lets-shared/contracts.md`: work input, review scope, evidence and completion invariants shared by all entrypoints.
- `python3 scripts/review_scope.py --repo REPO --base REF [--path PATH ...]`: JSON metadata including untracked paths; never stage, reset, clean or commit.
- `python3 scripts/validate.py [--root ROOT]`: nonzero on invalid package, provenance gaps or unresolved installed references.
- `python3 scripts/install.py [--dest DIR] [--dry-run]`: default `~/.codex/skills`; identical installation is idempotent, conflicting user files fail before writes.

## Review focus

False success from a green unit suite while required runtime evidence is absent; untracked files omitted from reviews; user edits overwritten during installation; a source skill represented only by a vague name without its useful capability; relative references broken after installation; state updates lost after commits; accidental pstack/tool/model execution from retained source data.
