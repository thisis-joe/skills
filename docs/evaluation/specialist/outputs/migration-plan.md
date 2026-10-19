# Stored email rename: expand, migrate, contract

Fixture contracts: old `contact_email` preserves exact spelling; new `email` is `strip().lower()`. This operation includes lossy normalization and cannot be treated as a harmless rename. Consumers remain independently deployed.

| Consumer / data | Current dependency | Transition acceptance |
|---|---|---|
| Old worker | Reads and writes `contact_email` | Old writer must be upgraded to dual-write before any new-only read |
| New API | Reads `email` | Must tolerate nullable expanded rows or wait until reconciliation |
| Audit exporter | Needs exact old spelling | Preserve original column/archive; canonical value cannot reconstruct it |
| Retry/replay worker | Replays old serialized events | Adapter translates old payload and dual-writes; retain through replay window |
| Configuration/other languages | Unknown | Inventory and owner acknowledgment pending; search is not complete proof |

Load-bearing facts: every active writer maintains the chosen old/new relation, and backfill cannot overwrite a newer application write. The local naive backfill read an old address, raced a dual-write, then restored stale new data. The revision-guarded preview instead returned `retry-current-row` and preserved the new write. This validates the fixture race, not a production database transaction.

1. **Expand, M1:** add nullable `email`, retain `contact_email`. Exercise both readers, errors and old serialized input; test meaningful DDL reversal locally. Independently green batch.
2. **Writers, M2:** migrate all write paths to one transactional owner writing raw old value, canonical new value and monotonic revision. Do not switch reads until old-only writers are gone or intercepted by an authorized adapter. Mixed-version compatibility window remains open.
3. **Backfill, M3:** 0–500 rows per batch, cursor by stable ID. Compare scanned revision in the update; on conflict skip/reload current row, never overwrite. Persist cursor/count/error evidence and reconcile source/new values, nulls and representative transformed records. Rerun is idempotent. Pause on project-approved lock/lag/error budgets; numeric production budgets are not supplied.
4. **Switch reads, M4:** require reconciled rows and tested fallback/error semantics; deploy cohort and retain dual-write. Bake through a full actual retry/replay and mixed-version window, whose duration must come from configured systems.
5. **Stop old writes, M5:** only after all known old readers/writers and replay consumers have migrated, with measured zero active old use across that window.
6. **Contract, M6:** separate destructive deployment. Remove old field only after audit retention requirements, all caller migration, measured zero use, explicit destructive/data-impact authority, tested recovery and integrated regression evidence.

Recovery before M6: revert read routing while dual-writes keep old data current. Backfill normalization is not reversible; a code revert cannot restore original spelling once dropped. Retain the old column plus an integrity-checked exact source snapshot. A production backup/restore or forward-repair rehearsal must record recovery owner, restore point, duration, validation, new-write preservation and loss window before destructive cutover. No backup/recovery capability was demonstrated here, so M6 is blocked. No production backfill, drop, announcement or deployment occurred.

Acceptance evidence: `checks.py` migration case and `evidence/observations.json:migrate`. Plan batches require their own build-owned commits on a feature branch if implemented; no such implementation is claimed.
