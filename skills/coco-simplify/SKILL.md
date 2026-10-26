---
name: coco-simplify
description: "Use when reducing complexity, removing dead code, improving architecture or refactoring while preserving observable behavior."
license: MIT
---

# coco-simplify

Remove concepts and indirection while preserving the behavior that consumers rely on.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a structural responsibility change, deleting a legacy internal API after migrating its callers, external consumers that need the migration sequence, code whose purpose or history is unclear, and a broad mechanical change that needs a codemod. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/simplify.md) before dependent work.

## Procedure and output

1. State preserved behavior and public contracts; establish current regression checks and actual callers before editing.
2. Identify the smallest structural change that removes complexity: inline a pass-through, delete unused branches, consolidate genuine duplication or deepen a module behind a smaller interface. Renaming or moving complexity alone is not a demonstrated simplification.
3. Compare alternatives by caller burden, locality, testability and number of concepts, not line count alone. Do not introduce an abstraction for hypothetical future reuse.
4. Keep structural refactoring separate from new feature behavior. Migrate callers before deleting legacy interfaces; verify config/runtime/cross-language references before declaring code dead.
5. Preserve meaningful contracts, comments and evidence. Type-system improvements should express real domain constraints and eliminate impossible states, not silence checking with casts/suppressions.
6. Run focused and required regression checks and compare relevant runtime behavior. Hand the scoped change through build/review; remove experiments that fail to buy simpler maintenance.

Return: what complexity disappeared, preserved contracts, migrated/removed call sites and regression evidence.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "Fewer lines is simpler": simplicity is comprehension speed, not line count.
- "This abstraction might be useful later": remove speculative abstraction; re-add it when needed.
- "The original author must have had a reason": check history first, then decide; accumulated complexity often has none.
- Weakening public-behavior checks to hide a regression, or removing error handling to look cleaner. A check coupled only to removed private structure may be retired or replaced only with independent public-contract evidence, unchanged behavior checks and a recorded reason; follow the [test boundary](../_coco-shared/advanced/simplify.md#execute-in-verifiable-steps) before doing so.
- Simplifying code you do not understand, or batching many simplifications into one hard-to-review commit.
