# Runtime verification

This short-lived CLI has no dependencies or long-running server.
Launch: python3 app.py --help
Doctor: python3 verify_cli.py doctor
Drive: python3 verify_cli.py drive
Reset: each invocation is a fresh process; keep retained evidence.
Evidence: each run prints and retains its actual subprocess commands, inputs,
outputs, return codes, app/helper SHA-256, Python version and evidence path.
Fresh files are evidence/doctor-<UTC timestamp>.json and
evidence/drive-<UTC timestamp>.json; old proof is never overwritten.
Both helper modes exit 0 when all their checks pass, 1 on a failed check.
Invalid helper usage exits nonzero. A healthy doctor proves the public help
surface advertises both operations; the drive proves only its concrete cases.
Cleanup: there are no owned background processes; preserve proof and user files.

Feature index: features/index.json. Mapped: double, multiply, operation-selection.
Drive covers positive/negative/zero double; operand signs and either zero for
multiply; required operation, mutual exclusion in both orders, bad integer,
missing multiply operand and unknown-option rejection. Feature documents list
the independent expected results. All actions use the public CLI.

Regression: python3 -m unittest -v (the existing suite covers double-positive
only; helper evidence supplies the other mapped runtime checks).
Cold-reader sequence: run launch, doctor, drive, regression; inspect the printed
proof paths and confirm those files remain accessible after cleanup.
No background process or disposable application state is created. Preserve all
evidence; there is no teardown command to run.

Resume note: HANDOFF.json and TASK_STATE.json refer to the earlier double-only
snapshot. Their status and previous proof do not verify current uncommitted
--multiply behavior. They are preserved unchanged, as are app.py, test_app.py
and USER_NOTES.md. Current evidence and gaps are returned in RESULT.json;
verification maintenance does not mark the product task complete or commit it.
