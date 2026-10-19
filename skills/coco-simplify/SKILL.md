---
name: coco-simplify
description: "Use when reducing complexity, removing dead code, improving architecture or refactoring while preserving observable behavior. 단순화·리팩터링·죽은 코드 제거."
license: MIT
---

# coco-simplify

Remove concepts and indirection while preserving the behavior that consumers rely on.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/simplify.md) only when the task needs their additional procedure.

## Procedure and output

1. State preserved behavior and public contracts; establish current regression checks and actual callers before editing.
2. Identify the smallest structural change that removes complexity: inline a pass-through, delete unused branches, consolidate genuine duplication or deepen a module behind a smaller interface. Renaming or moving complexity alone is not a demonstrated simplification.
3. Compare alternatives by caller burden, locality, testability and number of concepts, not line count alone. Do not introduce an abstraction for hypothetical future reuse.
4. Keep structural refactoring separate from new feature behavior. Migrate callers before deleting legacy interfaces; verify config/runtime/cross-language references before declaring code dead.
5. Preserve meaningful contracts, comments and evidence. Type-system improvements should express real domain constraints and eliminate impossible states, not silence checking with casts/suppressions.
6. Run focused and required regression checks and compare relevant runtime behavior. Hand the scoped change through build/review; remove experiments that fail to buy simpler maintenance.

Return: what complexity disappeared, preserved contracts, migrated/removed call sites and regression evidence.
