---
name: coco-verify
description: "Use when checking real app/API/CLI behavior, testing change impact, proving a safety assumption, or creating/maintaining a verification or formal-proof harness. 실행 검증·영향 검증·증명."
license: MIT
---

# coco-verify

Return execution evidence for the actual claim and its limits.

Read the [common contract](../_coco-shared/contracts.md) before acting. Initially and when scope, risk, or state changes, check for standing-quality audits, runtime-helper creation/maintenance, formal verification creation/maintenance, requested workflow experiments, and pre-commit setup. If any trigger applies or applicability is unclear, read the [advanced core and cumulative mode selection](../_coco-shared/advanced/verify.md) and every matching module before dependent work. The [integration decisions](../_coco-shared/decisions.md) resolve original rule conflicts.

## Procedure and output

1. Name the acceptance or safety claim, exact target version/snapshot, setup and cheapest decisive observable signal. Distinguish runtime verification, blast-radius checks, benchmark and formal proof modes.
2. Exercise real shipped code and representative inputs. For UI inspect relevant states, DOM/visual output, console/network and accessibility; use the available authorized browser capability rather than requiring a named MCP.
3. For impact, trace consumers beyond symbol callers: schemas, wire formats, timing, teardown, flags and cross-language readers. Identify the one or two load-bearing safety facts and try to falsify them with real execution.
4. For harness creation/maintenance or formal methods, use the advanced lifecycle. State the model, assumptions, counterexamples and drift triggers. A proof of an abstraction is not execution of the deployed system.
5. Report passed, failed, unavailable or not-applicable per required check with commands/inputs/results and evidence pointers. Missing tools or environment leave a required claim unavailable; green unit tests do not replace it.
6. Return evidence to the execution owner; verification does not independently commit changes, mark a build done, deploy or rewrite the implementation.

Return: claim-to-evidence matrix, snapshot, cleared conditions, concrete failures, unproven assumptions and the minimum next verification.
