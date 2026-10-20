---
name: coco-spec
description: "Use when agreed requirements need an authoritative specification, or a substantial feature needs explicit scope and acceptance criteria."
license: MIT
---

# coco-spec

Produce one usable contract for behavior and completion.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and on new scope, risk, state, or missing prerequisites, check for independently testable capabilities that need a capability map, revision of an existing agreement, missing project guidance or verification commands, vague quality targets that need measurable acceptance, and tracker publication or agent-ready handoff. If any applies or is unclear, read the [advanced modes](../_coco-shared/advanced/spec.md) before dependent work.

## Procedure and output

1. Read existing agreements, code, glossary/ADRs and the project specification system. Reuse its format and location; do not create a competing SPEC file.
2. Synthesize settled behavior. Ask only for missing material decisions. Reuse agreed test boundaries; identify what they can and cannot detect.
3. Write objective, users/observable behavior, scope, preserved behavior, constraints, acceptance, test strategy and unresolved decisions. Reference standing commands and conventions rather than repeating mutable policy in every feature spec.
4. If one request bundles independently testable capabilities, establish stable module IDs, one-way dependencies and boundary contracts before writing oversized module specs.
5. Separate durable behavioral decisions from implementation paths likely to change. Useful prototype state/type contracts can be retained with their origin; speculative details cannot become requirements by accident.
6. Record the spec reference/version for downstream work. Publication to a tracker follows the user's destination and authorization; local drafting does not imply posting permission.

Return: authoritative spec and explicit open issues. A request only to write a spec ends after that output; existing implementation authorization may continue to the next appropriate step.
