# Tenant delete and pending dependency review

Target: `fixtures/scenarios.py:delete_route`; supporting ownership manifest and dependency fixtures. This is a synthetic local review, not an assessment of an unseen production repository.

**Block the destructive path.** The route checks `tenant-a/jobs/<job>/data.txt`, then unlinks the derived path. A requester-controlled directory can resolve into tenant B. The local negative case returned 204 and removed B's file; the positive own-file case also removed its file, proving the observer sees effects. A literal B-prefixed path was rejected, which does not establish ownership of an A-shaped target.

| Asset / boundary | Abuse path | Control handed to build | Decisive check / result |
|---|---|---|---|
| Tenant B data / authenticated A to filesystem | A-shaped path crosses symlink into B | Resolve target; require approved-root containment, minimum depth, trusted authenticated owner binding; use no-follow/beneath-root descriptor operations or immutable hierarchy for check/use race | Cross-tenant symlink delete **failed security requirement**; local effect observed |
| Tenant A data / legitimate owner | Owner's authorized own job | Preserve approved legitimate deletion and diagnostic receipt | Positive control passed in fixture |
| Ownership / requester-writable marker | Actor writes their own ownership claim | Read trusted registry before teardown; writable marker alone is insufficient | Registry not implemented in target; ownership proof unavailable |
| Build host credentials / dependency lifecycle | Pending `postinstall` writes a file | Keep scripts disabled/default-deny; inspect pinned source and provenance before narrowly approving required script | `pending-package.json` and `install.js` inspected as text; nothing installed or executed |

Potential severity: high cross-tenant integrity impact in this target. Reachability is demonstrated only in the local mutable hierarchy; production mount/identity topology is unknown. No claim of safe production containment or race resistance follows.

Dependency graph ownership, authoritative lockfile and CI are missing from this narrow fixture. `pnpm@9.15.0` is a fixture declaration, not a verified current policy. The current official pinned-client default-deny mechanism, clean frozen install and native audit remain unavailable under this read-only/local evaluation. Do not run an ordinary install to discover scripts. Review provenance, ownership, release/transitive changes and required build effect; preserve a policy with the authoritative lockfile through build. No upgrade, credential change or service installation is authorized.

Reproduction: `python3 /tmp/lets-specialist-validation/checks.py`; observations in `evidence/observations.json`, key `security`. Product fixes and post-fix abuse tests are a build handoff; this review changes no route.
