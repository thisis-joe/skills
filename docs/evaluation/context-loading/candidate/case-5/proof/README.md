# Bounded balance property

Property: the balance returned by one `wallet.spend(balance, amount)` stays
nonnegative for every initial balance 0..2 and amount 0..3, inclusive. The property
and original bounds are preserved. There are 12 input pairs; no test is skipped.
A negative returned balance is a real wallet safety failure.

## Code mapping and assumptions

Covered code: all of `wallet.py`, currently one public function, `spend`, with one
unconditional `return balance - amount`. The model represents that exact indivisible
single-call arithmetic step. It assumes Python integer inputs in the stated finite
domains and a sequential, stateless call. It does not assume overspending is rejected.
There is no concurrency, persistence, external effect, callback or other balance
writer in this snapshot. Calls outside the bounds, repeated calls/sequences,
non-integer inputs, callers, concurrency and deployment are not covered.

The earlier model silently rejected overspending (`amount > balance`) while the
actual function subtracts it. Its green run was a stale abstraction, not a prior
successful product verification. The corrected model is compared to real code for
every bounded pair. Both the model and real result are checked for nonnegativity.

## Run and interpret

From the case directory, with Python 3 and no external dependencies:

```sh
python3 proof/check.py
python3 -B -c 'from wallet import spend; import json; result=spend(0,1); print(json.dumps({"balance":0,"amount":1,"actual":result}), flush=True); assert result >= 0, "nonnegative balance violated"'
```

Exit 0 means every modeled/real pair matches and the bounded property holds.
Exit 1 means the property has a counterexample. Exit 2 means code/model correspondence
drift. Other exceptions indicate the check is unavailable/broken and require diagnosis.
The current expected outcome is exit 1: balance 0, spend amount 1, returned balance -1.
The direct real-code replay also exits 1. Six of the 12 bounded pairs violate the
unchanged property; every modeled result matches the real function.

## Evidence, sync and future maintenance

`../evidence/original-snapshot.json` retains original product/model/document contents
and hashes; `../evidence/baseline-check.json` retains the unchanged initial green run.
`../evidence/maintained-check.json` retains the corrected exhaustive run and tool
version. `../evidence/counterexample-replay.json` retains a direct real-code replay.
`../evidence/closure.json` records the checked product hash and unchanged-product
check. Raw stdout, stderr, argv, working directory and exit codes are preserved.

Last sync commit: unavailable; the original verification files are a provisional
baseline without Git history or a previously confirmed model/code match. This
maintenance checks the current wallet hash recorded in the retained outputs; it
does not invent a historical sync commit or a passing safety revision.

Result: model updated, actual product bug reproduced. No wallet fix is authorized.
A newly passing property would require an isolated realistic broken-variant sensitivity
check followed by restoration and rerun. There is no new pass here: the corrected
check detects the actual unsafe implementation. Keep the red result and counterexample.

On any change to wallet behavior, balance writers, call atomicity, bounds, input
assumptions, Python semantics or verification files, run the existing check unchanged
before editing, inspect the code diff, re-establish mapping, preserve the property,
then rerun and replay counterexamples through the real function. Reduce bounds or
change the property only with explicit evidence of an intended contract change.
The finite enumeration and matching real executions do not establish an unbounded
formal proof or validate the whole application.
