---
name: coco-spec
description: "Use when agreed requirements need an authoritative specification, or a substantial feature needs explicit scope and acceptance criteria."
license: MIT
---

# coco-spec

Produce one usable contract for behavior and completion. All behavior changes need this saved contract and a saved plan before code, including small tasks; reuse project files and keep small contracts brief. Apply the [transition contract](../_coco-shared/workflow.md) before another skill.

Read the [common contract](../_coco-shared/contracts.md) before acting; when the request already shows that the file below applies, read both in one call. Initially and on new scope, risk, state, or missing prerequisites, check for independently testable capabilities that need a capability map, revision of an existing agreement, missing project guidance or verification commands, vague quality targets that need measurable acceptance, and tracker publication or agent-ready handoff. If any applies, read the [advanced modes](../_coco-shared/advanced/spec.md) before dependent work.

## Procedure and output

1. Read existing agreements, code, glossary/ADRs and the project specification system. Reuse its format and location; do not create a competing SPEC file.
2. Synthesize settled behavior. Ask only for missing material decisions. Reuse agreed test boundaries; identify what they can and cannot detect.
3. Write objective, users/observable behavior, scope, preserved behavior, constraints, acceptance, test strategy and unresolved decisions. Reference standing commands and conventions rather than repeating mutable policy in every feature spec.
4. If one request bundles independently testable capabilities, establish stable module IDs, one-way dependencies and boundary contracts before writing oversized module specs.
5. Separate durable behavioral decisions from implementation paths likely to change. Useful prototype state/type contracts can be retained with their origin; speculative details cannot become requirements by accident.
6. Record the spec reference/version for downstream work. Publication to a tracker follows the user's destination and authorization; local drafting does not imply posting permission.

Return: authoritative spec and explicit open issues. A spec-only request ends here; otherwise apply the shared transition contract before the next skill. Continuous implementation authorization alone does not select automatic transitions.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "This is simple, I don't need a spec": it still needs acceptance criteria; a two-line spec is fine.
- "I'll write the spec after I code it": that is documentation; the value is clarity before code.
- "I'll decompose during planning": capability boundaries and dependency direction come before an oversized spec.
- Implementing behavior no spec or task mentions, or making architectural decisions without recording them.
