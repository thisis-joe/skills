Read/apply [core](automate.md) first; no new authority.

## CI and deployment preparation

Discover the existing stack, lockfiles, wrappers, merge requirements, and CI provider; preserve required checks.
Order cheap applicable static checks before focused tests, broader integration tests, and build/runtime gates.
Exercise local changes with the same commands used in CI and include service-readiness and isolated test-data setup.
Use test-scoped credentials in the secret facility, separate from production credentials and committed configuration.
When CI fails, read the failing child logs and classify code defect, stale base, environment, or supported flake before retrying.
One bounded fresh run can test an infrastructure hypothesis; the same failure again needs diagnosis, not repeated reruns.
Do not disable a gate, weaken thresholds, or skip tests to turn the pipeline green.
Optimize measured slow CI with sound caches, independent jobs, safe path filters, sharding, and test setup before buying more capacity.
For authorized deployment workflows define staging verification, rollout signals, rollback artifact/action, and flag retirement.
Green CI is an input to readiness, not evidence that production changed or a merge completed.

