# Bounded balance property

Status: **bug**. The unchanged initial model passed, but it assumed a rejection
branch that the current `wallet.spend` does not implement. The maintained model
now represents the current unconditional subtraction. Its check fails, and all
six counterexamples replay against real code. Product code was not changed.

Property: balance stays nonnegative after spend. This property is unchanged.
Coverage: `wallet.py`, public `spend(balance, amount)`, one sequential call,
initial balances 0..2 inclusive and amounts 0..3 inclusive (12 combinations).
Inputs are ordinary Python integers in these bounds. The atomic model step maps
to the function's single `return balance - amount` expression. There is no
overspending-rejection assumption in the current model. No other wallet path or
writer exists in the supplied file; callers, concurrency, persistent storage,
other numeric types, wider bounds and operation sequences remain unproven.

Target wallet SHA-256: `c2a7fe2a389d179f1060189feffe4ce1675ad51bb4c3ad601daaf5e2968ffdc2`.
Last sync commit: unavailable; the previous verification-file baseline is
provisional, not a historically confirmed code match. No passing sync was
advanced by this failed maintenance check. The hash above identifies the code
inspected and replayed during this maintenance, not a green proof revision.

## Run and interpret

Run from the case directory using Python standard library only:

```sh
python3 proof/check.py
python3 proof/replay.py
```

`check.py` exhaustively enumerates the unchanged 12 model inputs, prints its
bounds and all counterexamples, and exits 1 on any negative result. The emitted
counterexamples are retained in `proof/counterexamples.json`. `replay.py` calls
the actual `wallet.spend` for every retained counterexample and a positive
observer case `spend(2, 1) == 1`. It exits 1 when all property violations are
confirmed, 2 for a model/replay/observer mismatch, and never labels a reproduced
bug a passing property. Neither command modifies the wallet or sends anything.

Concrete first trace: start balance 0, spend amount 1, receive -1. All six
traces are one possible real code step; none requires an impossible model
transition. Thus the original pass was stale model evidence, and the current
violation is a product bug rather than an abstract-only counterexample.

## Retained evidence

- `evidence/baseline-command.json` and `baseline.stdout.txt` / `baseline.exit.txt`:
  initial unchanged command exited 0 and printed a bounded pass.
- `evidence/check.before.py`, `README.before.md`, `baseline-snapshot.json`:
  exact original model, description and file hashes.
- `evidence/drift-inspection.stdout.txt`: current code and old model, showing
  the nonexistent overspending guard in the old model.
- `evidence/updated-model.stdout.txt` / `updated-model.exit.txt`: 12 combinations,
  six violations, exit 1; adjacent stderr retained.
- `evidence/counterexample-replay.stdout.txt` / `counterexample-replay.exit.txt`:
  all six real negative results plus positive observer, exit 1; stderr retained.

## Maintenance and limits

Inspect every change to spend, new paths/writers and affected callers, atomicity,
numeric semantics or input bounds. Update the transition from actual code before
rerunning; retain the nonnegative property unless a separately evidenced
intentional contract change authorizes it. Do not silently reduce bounds. Replay
all new counterexamples and distinguish impossible model steps from real bugs.
Keep prior sync while blocked/failing; only establish a passing sync after the
exact revision is checked. If a future fix makes the model pass, demonstrate
sensitivity on a realistic broken scratch variant, restore it, and rerun before
claiming success. No new pass occurred here, so that passing-proof sensitivity
step is not applicable in this run.

This is exhaustive enumeration of a stated one-step bounded model, with concrete
real-code counterexample replays. It is not an unbounded proof or a language
verifier result, and the initial green abstraction did not establish deployed
behavior. The minimum next step is a separately authorized product fix followed
by the same bounds/property, real-code replay, and required project checks.
