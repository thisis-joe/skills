---
name: coco-migrate
description: "Use when replacing or removing an API/system, changing schemas or wire formats, performing a wide mechanical refactor, or deprecating behavior."
license: MIT
---

# coco-migrate

Change consumers and persisted state in a verifiable compatibility sequence.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/migrate.md) only when the task needs their additional procedure.

## Procedure and output

1. Inventory actual consumers, stored/wire formats, mixed-version deployment behavior and undocumented observable dependencies. Trace safety assumptions beyond the diff.
2. Choose expand–migrate–contract: add the new form while old consumers still work, backfill/transition in bounded batches, verify adoption, then remove the old form in a separately scoped step.
3. State compatibility window, per-batch evidence, resumability/idempotency, data reconciliation and rollback/forward-recovery constraints. Reverting application code does not automatically restore data.
4. Prefer independently green batches. When unavoidable interdependent intermediate work requires an integration-only branch, label it explicitly, prevent normal done/ship claims and require integrated verification before release.
5. Remove callers before legacy APIs; check runtime/config/other-language consumers before declaring dead code. Retain a measured removal condition rather than a date alone.
6. Produce local migration artifacts and dry-run evidence within scope. Destructive production execution and announcements follow explicit existing authorization at action time.

Return: consumer map, phased tasks, checks and recovery plan, proven/unproven compatibility conditions and removal gate.
