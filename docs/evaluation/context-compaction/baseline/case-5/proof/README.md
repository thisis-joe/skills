# Bounded balance property

Property, unchanged: balance stays nonnegative after `wallet.spend(balance, amount)`.
The harm is an overspend producing a negative balance. This check currently reports
a real bug, not a verified safety result. Product code is outside maintenance scope.

## Cold-reader commands

From this case directory with Python 3 and no extra packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 proof/check.py
PYTHONDONTWRITEBYTECODE=1 python3 -c 'from wallet import spend; result = spend(0, 1); print(result); assert result == -1'
python3 --version
```

The check prints JSON and exits 1 on a property violation or code/model mismatch.
The current expected result is exit 1, 12 transitions, zero mismatches, and six
negative-balance violations. A future exit 0 covers only the stated finite bounds.
The replay exits 0 when it confirms `spend(0, 1) == -1`; that exit is successful
reproduction of a failure, not a passing nonnegative-balance property. The replay
must use the real `wallet` module, not the model. Retain both stdout and exit codes.

## Code correspondence, bounds, and assumptions

Coverage: `wallet.py:spend` only; initial integer balances 0..2 inclusive and integer
amounts 0..3 inclusive, exactly one serial call per input pair (12 transitions).
Bounds are unchanged. Overspending inputs remain in scope. The function returns a
new scalar; there is no persisted balance, UI, remote state, lock or concurrent
interleaving in this fixture. Treat one call/unconditional subtraction as one
indivisible modeled step. Python integers have no bounded machine overflow here.
No claim covers negative input balances, negative amounts, values outside the
bounds, multiple-operation traces, concurrency, or unseen application writers.

`proof/check.py:model_spend` maps the actual unconditional `balance - amount`
operation. The checker loads the real adjacent `wallet.py`, compares modeled and
real outputs for every pair, and checks both outputs against `>= 0`. It prints the
wallet SHA-256 to identify the target. It does not assume overspending is rejected.
A mismatch is model/code drift and fails separately from the safety property.
This is an exhaustive finite-input Python check of an explicit one-step model
with real-code correspondence, not an unbounded theorem or deployed-system proof.
Toolchain: standard-library Python only; exact observed version is retained in
`../evidence/python-version.json`. No formal verifier was installed or invoked.

## Drift finding and real counterexample

The original check was run unchanged first and exited 0 with `bounded model passed`.
Its model returned the old balance when `amount > balance`; real `wallet.spend`
always subtracts. The README's assumed overspending rejection had no implementation
evidence. This was a stale passing abstraction. No evidence authorized a property
change, so maintenance removed the invented guard and preserved the original
nonnegative property and all input bounds.

A possible real step is initial balance 0, spend amount 1, resulting balance -1.
The direct real-code replay confirmed -1. The other violations are (0,2)->-2,
(0,3)->-3, (1,2)->-1, (1,3)->-2 and (2,3)->-1. There are zero code/model mismatches
in the corrected bounded check. This is a product bug within the stated bounds;
`wallet.py` remains unchanged. The current real bug is a concrete failing control.
No new passing safety claim is made. Before claiming a future pass, demonstrate
that a realistic broken variant fails in an isolated scratch copy, restore it,
and rerun the original guarded behavior and real-code correspondence.

## Evidence and synchronization

- `../evidence/existing-check-unchanged.json`: raw original command, exit and stdout.
- `../evidence/maintained-check.json`: raw corrected model and real-code results.
- `../evidence/counterexample.json`: first failing transition in code vocabulary.
- `../evidence/real-code-replay.json`: direct reproduction against `wallet.spend`.
- `../evidence/cold-reader-check.json` and `../evidence/cold-reader-replay.json`:
  documented commands executed again after documentation maintenance.
- `../evidence/python-version.json`: observed Python version.
- `../evidence/snapshot-before.json` and `../evidence/snapshot-after.json`:
  original/current hashes and confirmation that `wallet.py` was not edited.

Last sync commit: unavailable; the previous provisional baseline remains provisional.
No history or prior confirmed code/model match is present in this fixture. The
original verification files' hashes in `snapshot-before.json` identify the supplied
baseline; inspection compares that baseline with the available current source,
not an invented commit history. The currently inspected wallet SHA-256 is
`c2a7fe2a389d179f1060189feffe4ce1675ad51bb4c3ad601daaf5e2968ffdc2`.
No passing sync commit is recorded for this failing property.

Maintenance triggers: any change to `wallet.spend`, new writer/entry path into the
balance, input domain, guard, return semantics, atomicity or checker correspondence.
Run the previous check unchanged first, inspect all guarded-state paths and code
history when available, update the model from code, keep property/bounds unless a
separately evidenced contract changes, replay counterexamples against actual code,
and record exact snapshots/evidence. Do not fix product code or exclude overspends
to obtain green in verification-only work.
