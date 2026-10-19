# Bounded balance property

Status: **bug**. The unchanged baseline check passed, but it modeled overspend rejection that is absent from current `wallet.py`. After aligning the model to the real function, the same nonnegative-balance property fails. Product code has not been changed.

## Claim, target, mapping, and bounds

Property: balance stays nonnegative after `spend(balance, amount)`.

Coverage remains exactly one sequential call, starting balances 0..2 inclusive and amounts 0..3 inclusive (12 pairs). `wallet.py` contains only `spend`, which unconditionally returns `balance - amount`; `model_spend` now has that same transition. The check compares the modeled and real result for every pair and independently checks nonnegativity. No code guard or contractual evidence supports the old assumption that overspending is rejected; removing that unsupported assumption does not weaken the property or input bounds.

Assumptions: integer inputs in these bounds, pure sequential execution of the inspected function, no concurrency, no persistent state, and one indivisible return-expression transition. Negative input values, multiple-step histories, exceptions from other types, concurrency, deployed services, and balances/amounts beyond the stated bounds are not covered. This is finite model enumeration with actual Python execution, not an unbounded theorem or verification of a deployed system.

Current covered-code SHA-256: `c2a7fe2a389d179f1060189feffe4ce1675ad51bb4c3ad601daaf5e2968ffdc2` (`wallet.py`). Tool: Python 3.9.6; no third-party solver or package is required. Version evidence is `../evidence/04-tool-version.json` relative to this file.

Last sync commit: unavailable; the original verification-file snapshot is a provisional baseline, not a previously confirmed code/model match. No commit history is provided for establishing covered-code changes since sync. Original file hashes and unchanged baseline outputs are retained under `../evidence/snapshot-before.json`, `../evidence/original-check.py.txt`, and `../evidence/01-baseline.json`. Current correspondence was checked for the recorded wallet snapshot and all 12 pairs; zero model/code mismatches were observed. The property remains failed.

## Cold-reader commands and interpretation

From the case directory:

```sh
python3 proof/check.py
```

Expected current exit: **1**. JSON stdout reports 12 checked pairs, no correspondence mismatches, and six counterexamples with both modeled and real outputs. Exit 0 would mean the property and correspondence held for these pairs only; nonzero must be inspected as a counterexample, model drift, or runtime failure. `../evidence/02-current-bounded-check.json` preserves the executed command and raw streams.

Replay the minimal counterexample through the real function:

```sh
python3 -c 'from wallet import spend; balance, amount = 0, 1; actual = spend(balance, amount); print(f"spend(balance={balance}, amount={amount}) -> {actual}", flush=True); assert actual >= 0, f"nonnegative balance violated: {actual}"'
```

Observed: `spend(balance=0, amount=1) -> -1`, assertion failure and exit 1. This is a possible real code transition, so the corrected counterexample is a product bug, not an impossible model step. The other failing pairs are (0,2), (0,3), (1,2), (1,3), and (2,3); the main check calls real code on every one. Raw replay evidence: `../evidence/03-real-counterexample.json`.

The baseline command was run unchanged before reading the model/current code: it exited 0 with `bounded model passed: balances 0..2, amounts 0..3`. That stale pass does not establish safety. No new passing proof is claimed; sensitivity testing of a new pass is therefore not applicable. The current check directly detects six actual unsafe results.

## Maintenance and boundaries

When `wallet.py`, its callers/input contract, writers, atomicity, or ownership of balance state changes, rerun the existing check unchanged first; inspect all relevant source and history, then reconcile model/code correspondence before changing the model. A new guard, fee, split function, deposit path, concurrent mutation, or persisted balance introduces a drift review. Extend coverage explicitly rather than silently dropping states. Do not change nonnegativity or reduce bounds merely to pass. Retain real-code counterexample replay and exact code hashes. If a later legitimate product fix passes, test sensitivity using an isolated broken variant, restore it, and confirm the real fixed check again. Missing runtime/tool/history evidence must be named.

This maintenance changed only proof files. No wallet fix is authorized here. The minimum next step is an implementation-owner decision on overspend behavior, a scoped product fix if required, and equal-input rerun/replay plus required project checks. There is no current safety proof to approve.
