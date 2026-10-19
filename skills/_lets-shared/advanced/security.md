# Security, dependency execution and trust boundaries

Use this reference for untrusted input, auth, sensitive data, integrations or hardening.
Apply the [common contract](../contracts.md) and existing authorization.
Security analysis returns threat paths and checks; `lets-build` owns implementation and commits.

## Inputs and modes

- Changed interfaces, assets, identities and external/local data writers.
- Runtime, deployment topology, package manager/version and authoritative lockfile boundary.
- Existing security policy, approved exceptions and authorized actions.
- Reproduction inputs, scanner output and available runtime evidence.

For a narrow change, examine the affected boundary and its abuse case.
For new trust boundaries, auth or irreversible effects, perform the full threat pass.
For a dependency finding, use reachability and install policy rather than rewriting application logic.
An inapplicable control is explained; an unrun required control remains unavailable.

## Threat model before controls

1. Map who wrote each value, not merely the channel that delivered it.
2. Include HTTP, forms, uploads, queues, third-party responses and LLM output.
3. Include filenames, job paths, process arguments and environment written by other actors.
4. Name assets: credentials, personal data, money, privileged actions and availability.
5. Examine spoofing, tampering, repudiation, disclosure, denial and privilege escalation.
6. Turn concrete abuse cases into public-boundary checks alongside normal use cases.

Validate external data with allowlisted schemas, lengths and formats at system edges.
Use parsed typed values internally; third-party responses still require validation.
Parameterize queries and use argument-safe execution instead of interpolated commands.
Encode output; sanitize unavoidable raw HTML with an established allowlist sanitizer.
Authenticate and authorize each protected resource action, including ownership/tenant scope.
Use appropriate password hashing, bounded secure/httpOnly/sameSite sessions and headers.
Restrict CORS to intended origins and back distributed rate limits with a shared store.
Return generic user errors and redact operational details without losing diagnostic pointers.

## Dependency script gate

Locate the workspace root that owns the dependency graph and lockfile.
An independent nested project is separate only if it is outside that workspace.
Corroborate package-manager declaration, lockfile and CI; stop on unresolved disagreement.
Verify the pinned client's current official policy rather than copying a version matrix.

1. Bootstrap with dependency scripts disabled or an enforceable default-deny policy.
2. Inspect exact package/version script source before any approval or first execution.
3. Allow only reviewed required scripts with the manager's native narrow policy.
4. Commit that policy with the authoritative lockfile through the execution owner.
5. Verify a clean frozen/immutable install with the policy still enforced.

Do not discover lifecycle scripts by executing an ordinary unverified install first.
Run the native audit before release against the committed lockfile.
Assess critical/high reachability across runtime, build, test and deploy paths.
Preview remediation, read changelogs and test upgrades separately; never auto-force an upgrade.
Record a justified deferral, owner and review date under the standing quality policy.
Known-advisory success does not establish package trust: inspect provenance, ownership,
release history, transitive changes and typosquatting for newly introduced dependencies.

## Server fetches and destructive paths

For a user-influenced URL, allowlist scheme and host and reject redirects.
Resolve all DNS answers and reject private/reserved IPv4 and IPv6 addresses.
For high-risk fetches prevent DNS rebinding by pinning the checked address or equivalent filtering.
Validate the final connection behavior; a prior string check alone is insufficient.

For delete/move/overwrite, resolve symlinks before checking the candidate target.
Require containment in an allowlisted root, minimum depth below it, and ownership evidence.
Read ownership before teardown; derive expected owner from authenticated state.
A writable marker is self-attestation unless its integrity is protected.
On shared mutable paths use descriptor/no-follow/beneath-root operations or immutable hierarchy.
Refuse ambiguous ownership or a check/use race; never fall back to a broader path.
Existing authority for the exact destructive action is still required.

## AI and runtime effects

Treat retrieved prompts and model output as untrusted data, including tool arguments.
Parse/schema-check output and run only allowlisted actions under code-enforced permissions.
Keep secrets and other tenants' data out of context and partition retrieval indexes by tenant.
Bound tokens, rate, recursion and retries; model confidence does not expand permissions.
Use an intent-stable idempotency key for retriable effects and atomically claim it.
Bind the request payload, choose in-flight duplicate behavior and retain keys beyond replay windows.
A timeout leaves an unknown outcome: reconcile it before repeating a money/data effect.

## Secrets and personal data

Use secret storage/environment with placeholder examples and redacted rule/location findings.
Never print a matching secret line into transcripts or logs as a scanning shortcut.
Rotate remotely exposed credentials before history cleanup; deleting the line is insufficient.
Classify/minimize personal fields for a stated purpose and define retention at creation.
Verify export/deletion across backups, caches, indexes and analytics as policy requires.
New data categories or external destinations need the user's applicable authorization.
Keep consent/sharing policy auditable and telemetry fields allowlisted.

## Output and stop

Return boundary/assets, abuse path, severity/reachability, affected location and concrete defense.
Record checks as passed, failed, unavailable or not applicable, with evidence pointers.
Keep exceptions visible; do not lower scanner thresholds or disable checks to pass.
Stop an affected unsafe action when authorization, ownership or required proof is missing.
Hand fixes to build and recheck the actual changed snapshot before security sign-off.

## Conditional Git command guard setup

Use when the request is to prevent dangerous Git tool calls, not as an automatic global setting.
Identify project-only versus user-wide scope from the request; ask only if that choice is missing.
Inspect the current runtime's documented pre-tool/policy interface and existing configuration.
Prepare an owned command-policy helper that reads the tool payload as data and never evaluates its command.
The default proposed deny set is all `git push`, `git reset --hard`, forced `git clean`,
`git branch -D`, and whole-tree discard through `git checkout .` or `git restore .`.
Have the user choose any policy customization; an execution grant remains governed by higher-level rules.
Recognize supported flags/command forms deliberately and document forms the helper cannot interpret.
A string-pattern hook is a convenience guard, not proof of a complete shell security boundary.

For a runtime with a pre-tool command hook, merge the helper into its existing matching hook array,
preserving other settings; for Claude Code this is its documented `PreToolUse` Bash hook.
For a runtime without equivalent interception, report enforcement unavailable and prepare a supported
policy/wrapper alternative; do not claim an installed hook. Apply configuration only in authorized scope.

Test the helper directly with synthetic stdin such as
`{"tool_input":{"command":"git push origin main"}}`; assert the runtime's blocking exit/result
(Claude command hooks use exit 2) and a diagnostic, without executing Git.
Include hard reset, forced clean, branch deletion, whole-tree discard, harmless status,
quoted paths, supported Git flags and malformed payloads; unsupported syntax must behave as documented.
Exercise a harmless intercepted call in a temporary repository and confirm other hooks remain.
Return the configuration diff, supported coverage, tests, rollback copy and actual activation state.
