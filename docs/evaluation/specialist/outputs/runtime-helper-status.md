# Runtime helper: draft, blocked before UI drive

Target: `scratch-expense-ui-v2`; feature map `runtime-helper/features.json` contains one primary journey, `expense.create`, at `/expenses/new`. Startup requires `runtime-helper/fixture-state.json`, which is absent. A browser driver is also unavailable. The source map names entering 12.50, Save expense, visible Saved and independent persisted-ledger readback; it does not substitute internal code calls for user navigation.

The cold-reader sequence below was executed by the local harness. Launch exits 2 with the exact absent prerequisite and starts no process. Doctor confirms no usable instance or driver. Drive and capture exit 2 without pretending to interact or inventing a screenshot. Cleanup has no owned process/scratch records to remove, retains proof, and the final evidence check confirms all five receipts still exist. Source coverage is 1 mapped feature, live coverage 0/1.

```sh
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py launch
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py doctor
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py drive
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py capture
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py cleanup
python3 /tmp/lets-specialist-validation/runtime-helper/helper.py check-evidence
```

These are a runnable scaffold's failure paths, not a launched baseline. No exact real production launch/auth/fixture commands were supplied, so none are invented. The absent concrete fixture is an unreachable prerequisite; the UI journey itself is not verified-unreachable by live interaction. Classify separately: baseline setup gap, browser driver gap, no evidence of product regression, no proven helper drive correction.

Creation is not ready: baseline build/start and mapped journey have not succeeded. Maintenance cannot return clean without every mapped feature driven live. Keep the helper a draft and retain the single feature instead of removing it to manufacture coverage. Next required work is an authorized usable fixture/baseline and driver, actual launch/doctor, real route actions and persistence, independent reset, re-drive, cleanup and retained receipts. No product files or user sessions were changed. Evidence: `evidence/runtime-helper/*.json` and `evidence/observations.json:verify-runtime-helper`.
