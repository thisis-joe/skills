---
name: coco-security
description: "Use when designing or changing authentication, authorization, payments, sensitive data, uploads, external input or security controls."
license: MIT
---

# coco-security

Identify trust-boundary attacks and verify the required defenses.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for a new trust boundary, authentication or irreversible effect (full threat pass), dependency install scripts or lockfile policy, server fetches of user-influenced URLs, delete, move or overwrite targets derived from data, model output, tool arguments or retriable money/data effects, secrets or personal-data handling, and a requested Git command guard. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/security.md) before dependent work.

## Procedure and output

1. Identify assets, actors, trust boundaries, privileged operations and data flows. Tie each relevant abuse case to a control and an observable check.
2. Verify server-side object/function authorization, input validation, safe query/output encoding, session/secret handling and least-privilege access. Do not treat client validation or CORS as authorization.
3. Use specialized modes for SSRF, derived filesystem targets, dependency scripts/lockfiles, privacy and AI/tool boundaries. A syntactically valid path or model-produced argument is not ownership evidence.
4. Test negative and cross-tenant cases as well as the happy path. Use test data and redacted outputs; never leak a found secret through a report or fixture.
5. Keep existing approved security choices; propose material changes at the relevant authorization boundary. Hardening is not permission to rotate credentials, broaden access or install services without scope.
6. Hand scoped implementation and regression criteria to build, and evidence to review/ship. Document residual risk and any unavailable assessment rather than issuing an unsupported safety claim.

Return: threat/control/test matrix, concrete findings or defenses, verified abuse cases and residual risk.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "It's internal" or "no one would try this": internal tools get compromised and scanners find obscure paths.
- "The framework handles it" or "the audit passed": frameworks need correct use; audits miss new malicious packages and unreviewed install scripts.
- "It's just model output": treat it as untrusted input before queries, DOM, shell or eval.
- "Collect it now, we might need it": data without purpose, retention and deletion path is breach scope.
- User input reaching queries, shell or HTML; endpoints without authorization; wildcard CORS; per-instance rate limits; or a destructive target guarded only by a path-shape check.
