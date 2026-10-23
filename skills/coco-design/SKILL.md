---
name: coco-design
description: "Use when choosing module or API interfaces, changing architecture, deciding a test boundary, exploring prototypes, or comparing alternative implementations."
license: MIT
---

# coco-design

Select a small understandable interface that earns its implementation complexity.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for a shared or public API contract, retry-sensitive or idempotent effects, type-discipline choices, deepening shallow modules or an architecture opportunity survey, comparing structurally different alternatives, a disposable prototype, and the opt-in TypeScript package-boundary recipe. If any applies, read the [advanced modes](../_coco-shared/advanced/design.md) before dependent work.

## Procedure and output

1. Establish the behavior, consumers, invariants and preservation constraints from research or the agreed brief. Reuse an existing adequate interface.
2. Consider genuinely different designs when the choice is uncertain. Compare caller burden, maintainability/locality, testability, failure behavior and transition cost; avoid cosmetic alternatives.
3. Define contracts including ordering, errors, configuration and performance expectations, not merely type signatures. Put behavior behind the public interface and select an observable test surface.
4. For uncertain feasibility, run a bounded disposable prototype against primary sources. State the probe question and success measure; keep prototype artifacts isolated. Production adoption requires normal implementation and checks.
5. For shared APIs, apply compatibility and idempotency modes from the advanced reference. For structural redesign, identify callers to migrate and obsolete APIs to remove.

Return: selected interface, alternatives and trade-offs, test surface and implementation constraints. Material new product decisions remain explicit; design does not silently expand implementation scope.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "Nobody uses that undocumented behavior": observable behavior is a contract someone depends on.
- "We'll add pagination, versioning or docs when needed": design list growth, error shape and extension now.
- "Accepting an idempotency key is enough" or "the queue is exactly-once": store the key with its result and design for at-least-once delivery.
- A check-then-insert key guard, a key regenerated per attempt, or a reused key with a different body silently returning the first response.
- Response shapes or error formats that vary by endpoint or condition, or validation scattered through internal code instead of at boundaries.
