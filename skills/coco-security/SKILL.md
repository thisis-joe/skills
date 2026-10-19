---
name: coco-security
description: "Use when designing or changing authentication, authorization, payments, sensitive data, uploads, external input or security controls."
license: MIT
---

# coco-security

Identify trust-boundary attacks and verify the required defenses.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/security.md) only when the task needs their additional procedure.

## Procedure and output

1. Identify assets, actors, trust boundaries, privileged operations and data flows. Tie each relevant abuse case to a control and an observable check.
2. Verify server-side object/function authorization, input validation, safe query/output encoding, session/secret handling and least-privilege access. Do not treat client validation or CORS as authorization.
3. Use specialized modes for SSRF, derived filesystem targets, dependency scripts/lockfiles, privacy and AI/tool boundaries. A syntactically valid path or model-produced argument is not ownership evidence.
4. Test negative and cross-tenant cases as well as the happy path. Use test data and redacted outputs; never leak a found secret through a report or fixture.
5. Keep existing approved security choices; propose material changes at the relevant authorization boundary. Hardening is not permission to rotate credentials, broaden access or install services without scope.
6. Hand scoped implementation and regression criteria to build, and evidence to review/ship. Document residual risk and any unavailable assessment rather than issuing an unsupported safety claim.

Return: threat/control/test matrix, concrete findings or defenses, verified abuse cases and residual risk.
