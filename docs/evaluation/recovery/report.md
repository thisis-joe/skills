# Fresh interrupted-state recovery applications

Both bounded applications reached their authorized outcomes. The implementation-resume case transitioned from context inspection to build-owned reconciliation and recorded T1 done against the existing commit. The separate context-only case prepared a packet and kept authoritative state byte-for-byte unchanged.

This is one fresh agent applying a frozen bundle to two bounded scopes, not a formal or general proof. No author/reviewer history, evaluator output/report/results, live repository instructions, global skills, external content or other agents were used. Writes were confined to `/tmp/lets-recovery-validation`; no product or Git bytes changed.

## Observed state and outcomes

| Observation | Authorized resume | Context-only |
| --- | --- | --- |
| Workflows | lets-context → lets-build | lets-context |
| T1 before | open, commit null | open, commit null |
| T1 after | done, existing commit recorded | open, commit null |
| Branch | feature/context | feature/context |
| HEAD | 03b7e6a2131b4eec2d177c6591a22084c554e3f6 | same |
| Base main | 6175af547fab7883e093e0dfdfcde1fd977a3c93 | same |
| Product commits ahead of main | 1 → 1 | 1 → 1 |
| New product commits | 0 | 0 |
| Dirty paths | empty → empty | empty → empty |
| Fresh suite | 1 test passed | 1 test passed |
| Fresh public CLI | input 6 → 12, exit 0 | input 6 → 12, exit 0 |
| Preexisting artifacts changed | task-state.json only | none |
| Original verification/review receipts | unchanged | unchanged |
| Repository and .git file bytes | unchanged | unchanged |

The authoritative file is each copy’s `task-state.json`, outside the copied Git repository. The recorded task T1 points to its existing work-unit commit and receipt/current-check evidence. No new status commit was manufactured. T2 remains pending and exactly retains its original record; its dependency on T1 is satisfied in the resumed case, but README explicitly says T2 is not requested now.

## Ownership and rule application

Frozen `lets-context` step 4 and advanced context task-pickup steps 4–6 assign inspection and the exact reconciliation packet to context, and completion-state writes to build. They explicitly permit an already authorized implementation-resume request to continue directly into build. The common recovery contract and `lets-build` step 5/advanced recovery steps require checking an already successful commit and reconciling status instead of repeating implementation or committing twice. The context-only scope therefore ends at the packet even though the same commit supports a proposed update.

Both packets were written while T1 was still open, with a guarded proposed replacement. Only the resume copy then entered the build phase, verified the precondition hash/HEAD/content identities, replaced T1 atomically, and read back the state in a separate command process. `evidence/context-phase-readback.json`, `resume/evidence/build-reconciliation.json` and each case’s `evidence/after-state-readback.json` expose this boundary.

## Receipt identity and actual checks

`receipt.json` SHA-256 is `a61985275358d01db3cc082b302b571fca7a5e7cfb29fb592cace9a36aee2125` in source and both copies. For `double.py`, `tests/test_double.py` and `README.md`, all three receipt hashes match working-file bytes and `git show HEAD:<path>` blob bytes. The product commit contains only the intended multiplication expression change. Fresh commands were `python3 -m unittest discover -s tests -v`, `python3 double.py 6`, and `git diff --check main...HEAD`; all returned exit 0. Runtime used Python 3.9.6 and Git 2.50.1.

The original review has no required findings and explicitly labels same-agent self-review. That degraded independence is retained in task state and packets. The prior review-scope token describes a pre-commit worktree diff; the current helper describes identical committed bytes. Their tokens differ as expected because HEAD/layer changed. Receipt applicability is established by exact content and commit inspection, rather than asserting the tokens are equal. No new independent-review claim was made.

## Hash/readback evidence

Resume task-state SHA-256: `5156b3f51d4ae746285645fa468076a2a304a79625e3929d5ba61ccbe48c3cd5` → `1e2189f4ee461e773668fc69e4a850e067bd9fc10e02ffe88757fec8303a1da1`. Context-only SHA-256 stays `5156b3f51d4ae746285645fa468076a2a304a79625e3929d5ba61ccbe48c3cd5`.

Source freeze covered 127 permitted frozen/fixture files before execution; the exact same hashes were confirmed afterward with no changes. See `evidence/source-sha256.before.json`, `evidence/source-sha256.after.json`, and `evidence/source-integrity.json`. Each case also has complete before/after copied artifact hashes; comparison shows only resume/task-state.json changed.

Raw command records in each case’s evidence directory preserve cwd, argv, exit code, stdout and stderr for Git branch/base/HEAD/status/log/count/diffs/untracked inventories, committed blobs, suite/runtime/version checks, the frozen review-scope helper and separate task-state readback. `receipt-identity.json` relates each inherited receipt/file to its hash.

## Limits and ambiguities

No contradictory workflow rule required stopping. The fixture input calls the checkbox an external tracker, while its README and the user scope designate a local task-state file. This run uses only the isolated designated local authority, with no external access. T2’s `blockers: ["T1"]` is retained as the supplied dependency reference; this bounded recovery does not invent a T2 schema/status transition.

The fixture supplies no unrelated dirty state. Empty before/after dirty inventories are observable; preservation of a nonempty unrelated edit was not exercised. Required review remains degraded self-review, so this run provides no independent-review guarantee. No implementation or generalized failure-path proof is claimed.

## Artifacts

- `results.json`: structured observed outcomes and limitations.
- `resume/packet.md`, `resume/proposed-state-patch.json`, `resume/task-state.json`: authorized recovery artifacts.
- `context-only/packet.md`, `context-only/proposed-state-patch.json`, `context-only/task-state.json`: read-only scope artifacts.
- `evidence/` and case `evidence/`: source freezes, actual command outputs, receipt identities, state write/readbacks and artifact hashes.

## Frozen rule files read

| Frozen skill file | SHA-256 |
| --- | --- |
| lets-context/SKILL.md | 2e5ccc5063b11aeb66231ab1d0562b88895938a99410a03a8ab45edadefea6b3 |
| lets-build/SKILL.md | 49e7d6ff2751fabaa46ec656579141b642e7a43889159fc30ddaf54967bffb15 |
| _lets-shared/contracts.md | 62272ac57e59eada632f236092f6a6d24eeb1360a0ad4d9210623d9203b18395 |
| _lets-shared/routing.md | 64e8b1e5d9644adb977b280564679a1c2f042767ce9bfe5c9e74ddaa91a13307 |
| _lets-shared/advanced/context.md | f62e7c3e07269e7c14f56b12ec0cb5c01be608b8e019628de2bb9a434b4e88b6 |
| _lets-shared/advanced/build.md | c34a1810ec6f87db16d897aacbb3b1594359bb4ab1307b55023f837272b6efe7 |
| _lets-shared/decisions.md | 48011a0ee107443c2839e5aa31ddd103c4f75763655e7d24fcd844b85c33ec0f |
| _lets-shared/tools/review_scope.py | 906784fa44e365a0324034b8f0e7c3ad74b270a0651eaa45e3e7a9b2757a5703 |
