# Atomic claim property: stale abstraction; real fixture bug

Claim: for one intent key, at most one worker returns a successful ownership claim. Harm: duplicate destructive/financial effects after two workers both act. Target is `fixtures/scenarios.py:split_claim`, current split-read/write fixture. The prior abstract model treated check-and-set as one indivisible transition. Its two worker orderings pass ordinary Python exploration, but that assumption no longer maps to the current target.

Concrete counterexample from actual fixture steps: A reads no owner; B reads no owner; A writes owner and returns success; B writes owner and returns success. Both winners remain recorded. This is a possible real code interleaving in the fixture and demonstrates a bug in that promise; it is not an impossible-model-step false alarm. No product fix is made in verification scope.

| Check | Observation / status |
|---|---|
| Prior abstract atomic model | Passes two bounded orderings in Python; stale assumption |
| Mapping to current code | Failed: read and write are separate yieldable steps |
| Counterexample replay | Passed reproduction: winners `[A, B]` |
| Updated formal model and tool proof | Unavailable: no formal verifier installed/authorized here |
| Claim on production system | Unavailable: no real product snapshot/driver |

Creation artifact requirements are retained as a draft: guarded state `owner`, property above, entrypoints and all writers, separate `read-owner`, conditional `write-owner`, and `return-success` transitions, two workers/one key as initial bounds; scheduling may occur between actual steps. Atomicity may only be assumed for a real documented transaction/CAS/lock. Current ordinary generator execution exposes the split. Real network/database isolation and other entrypoints remain uncovered.

Maintenance decision: classify possible broken promise/bug, keep previous sync unchanged. A real sync commit was not supplied; the prior file/model description is only a provisional baseline, not a verified historical code match. Do not stamp current code in-sync or weaken at-most-one to get green. When an available approved verifier is selected, record exact tool/version/command/bounds and execute cold-reader instructions. Generated-input or Python state exploration is not relabeled formal proof. Tool installation did not occur.

Sensitivity: the current split implementation itself serves as the realistic broken variant relative to the atomic abstraction. The local Python test reproduces failure and restores no product code because none is changed. A proper new formal pass still requires deliberately broken-current-behavior sensitivity and restored-pass receipts using the actual verifier. Those receipts are unavailable. Reproduction: `python3 /tmp/lets-specialist-validation/checks.py`; trace in `evidence/observations.json:verify-formal`. Report the bug to debug/build; formal verification remains blocked.
