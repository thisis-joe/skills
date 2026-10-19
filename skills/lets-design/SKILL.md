---
name: lets-design
description: "Use when choosing module or API interfaces, changing architecture, deciding a test boundary, exploring prototypes, or comparing alternative implementations. 설계·인터페이스·프로토타입."
license: MIT
---

# let's-design

Select a small understandable interface that earns its implementation complexity.

Read the [common contract](../_lets-shared/contracts.md) before acting. Load [advanced modes](../_lets-shared/advanced/design.md) only when the task needs their additional procedure. The [integration decisions](../_lets-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Establish the behavior, consumers, invariants and preservation constraints from research or the agreed brief. Reuse an existing adequate interface.
2. Consider genuinely different designs when the choice is uncertain. Compare caller burden, maintainability/locality, testability, failure behavior and transition cost; avoid cosmetic alternatives.
3. Define contracts including ordering, errors, configuration and performance expectations, not merely type signatures. Put behavior behind the public interface and select an observable test surface.
4. For uncertain feasibility, run a bounded disposable prototype against primary sources. State the probe question and success measure; keep prototype artifacts isolated. Production adoption requires normal implementation and checks.
5. For shared APIs, apply compatibility and idempotency modes from the advanced reference. For structural redesign, identify callers to migrate and obsolete APIs to remove.

Return: selected interface, alternatives and trade-offs, test surface and implementation constraints. Material new product decisions remain explicit; design does not silently expand implementation scope.
