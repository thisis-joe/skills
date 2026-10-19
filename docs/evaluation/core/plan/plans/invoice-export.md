# Invoice export plan v1

Contract: ../spec.md; current structure comes from ../code-map.md. This is a planning-only artifact, single-owner sequential execution. Actual repository base/HEAD and command availability cannot be frozen because only the source map is supplied. Resolve those discoverable facts at pickup; commands in ../commands.md are required proposed checks, not execution receipts.

One mutable state source: ../tasks/invoice-export/<ID>.json. This plan carries IDs, structure and rationale, without a second status checklist.

Vertical behavior graph:
- CSV-1: user exports current visible invoices as safe CSV, through request to returned/downloadable artifact. No separate schema/API/UI phase tickets. Acceptance: exact header/order/booleans/safe text; preserved filters; empty results. Focused test_export plus scripts/exercise_export.py and full suite, with scoped review and work-unit commit.
- EMAIL-1 blocked by CSV-1 because it links a usable export: user submits validated recipient, work is queued and status is shown. Acceptance: valid address yields existing export link, invalid address rejected before enqueue, failed delivery visible; fixture runs scripts/exercise_email.py plus test_mail/full suite. Reuse existing link-access/security policies; discover those before implementation and escalate any missing material policy.
- AUDIT-1 blocked by CSV-1 because it observes completed export behavior: support sees current-tenant completion events, other tenants absent, failed export not falsely completed. Focused test_audit plus full suite and relevant user/API path; verify the tenant-negative case with a positive same-tenant control.

Shared symbol migration is a separate feature branch, feature/delivery-result, with scoped work-unit commits:
- MIG-EXPAND: make DeliveryResult the canonical internal type and retain ExportResult as a compatible alias for existing consumers. Prove identical behavior and imports under full suite.
- MIG-EXPORT / MIG-MAIL / MIG-AUDIT: each blocked only by MIG-EXPAND; migrate its caller package, tests, examples and applicable documentation references. Batches remain green, with their focused/full checks. Single writer executes sequentially; no delegation or jointly writable task file is proposed.
- MIG-CONTRACT: blocked by all three caller batches; remove obsolete alias, search active imports/string/schema/doc/example/backreferences for ExportResult, check cross-language/wire readers before concluding the name is internal, then full suite and public runtime recipes. Historical plan references are evidence, not stale active APIs. If the discovered symbol is externally serialized, stop this removal and resolve compatibility scope.
- INTEGRATE: blocked by CSV-1, EMAIL-1, AUDIT-1 and MIG-CONTRACT; verify complete CSV->email->status/audit journey on final combined revision, test same-tenant and other-tenant behavior, run full suite, scoped final review and record the integration commit/evidence.

The migration can start independently of the CSV behavior because the compatibility alias allows existing callers to work; features have no invented MIG prerequisite. The final integrate task is the genuine convergence checkpoint. DAG frontier initially CSV-1 and MIG-EXPAND. Choose CSV-1 first for immediate user value in sequential execution; this schedule is not a false dependency.

Branches: feature/invoice-export for the vertical capabilities, feature/delivery-result for the coordinated migration, and a named integration branch chosen from the actual common base at pickup. No branches are created by this draft. Each task closes only after acceptance, project-required checks, scoped review and a task-owned work-unit commit with ID in its state file. Do not include unrelated dirty work.

Risk/checkpoints: validate public CSV safety at CSV-1; validate recipient-before-effect and persisted delivery status at EMAIL-1; tenant isolation at AUDIT-1; compatibility/import identity during expansion and every caller batch; no old active consumers before contract. Rollback a caller batch to the compatible alias during migration; roll back the contract commit if a missed reader appears. Do not remove the alias until all readers are known.

No integration-only exception is necessary from the supplied map: both symbols can coexist and green batches are feasible. If actual discovery disproves this, label an integration-only branch and final gate explicitly; red intermediates cannot be normal done/shippable tasks. No deployment, ticket publication or code execution is authorized by this plan.

Expected scope: CSV surface/tests and existing list integration; mail endpoint/queue/status/tests; audit read surface/tests; core result declaration and its three caller packages/docs/examples. These are navigation estimates, not immutable file-count promises. Unavailable: actual code review, Git baseline, executable runtime fixture and test availability. Material new decisions discovered there block only dependent tasks.
