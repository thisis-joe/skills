---
name: coco-start
description: "Use when choosing a development workflow, setting up repository commands and quality constraints, or deciding which specialist procedure is needed."
license: MIT
---

# coco-start

Choose an appropriate workflow and establish the project quality bar.

Read the [common contract](../_coco-shared/contracts.md) before acting. Load [advanced modes](../_coco-shared/advanced/start.md) only when the task needs their additional procedure.

## Procedure and output

1. Read repository instructions, current branch/status, existing spec/plan/task target, CI and documented commands. Discover the actual stack before choosing checks.
2. Select the smallest route that satisfies risk and acceptance using the [selection table](../_coco-shared/routing.md). A static edit can finish directly with its relevant check. Existing sufficient artifacts skip their creation step.
3. For setup, record commands, required closure checks, evidence locations and owners. Reuse existing constraints; identify missing enforcement rather than starting a second policy file.
4. If no standing quality bar exists, use the advanced setup mode: inspect existing measurements, ask only unresolved policy decisions, and attach checks to edit/task/CI stages. In unattended work, retain the existing bar and flag unset targets instead of inventing an interview or silently weakening checks.
5. Hand off only the next needed purpose. A specialist adds checks to the route; it does not start every other specialist.

Return: selected route and reason, authoritative artifacts, actual commands and remaining decisions. Setup output includes enforced versus measured-only thresholds and execution points.
