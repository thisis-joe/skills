---
name: coco-verify
description: "Use when checking real app/API/CLI behavior, testing change impact, proving a safety assumption, or creating/maintaining a verification or formal-proof harness."
license: MIT
---

# coco-verify

Return execution evidence for the actual claim and its limits.

Read the [common contract](../_coco-shared/contracts.md) before acting. Read the [verification core](../_coco-shared/advanced/verify.md) before driving a UI, browser, live service, account or persistent state, designing behavioral checks, or when any mode below applies; once read, the whole core applies even if no mode matches. A single existing command or CLI check with known expected output needs only this entrypoint. Initially and on new scope, risk, state, or missing prerequisites, check for standing-quality audits, runtime-helper or formal-verification creation/maintenance, requested workflow experiments, and pre-commit setup. If any applies or is unclear, read the core's mode selection and all matching modules before dependent work.

## Procedure and output

1. Name the acceptance or safety claim, exact target version/snapshot, setup and cheapest decisive observable signal. Distinguish runtime verification, blast-radius checks, benchmark and formal proof modes.
2. Exercise real shipped code and representative inputs. For UI inspect relevant states, DOM/visual output, console/network and accessibility; use the available authorized browser capability rather than requiring a named MCP.
3. For impact, trace consumers beyond symbol callers: schemas, wire formats, timing, teardown, flags and cross-language readers. Identify the one or two load-bearing safety facts and try to falsify them with real execution.
4. For harness creation/maintenance or formal methods, use the advanced lifecycle. State the model, assumptions, counterexamples and drift triggers. A proof of an abstraction is not execution of the deployed system.
5. Report passed, failed, unavailable or not-applicable per required check with commands/inputs/results and evidence pointers. Missing tools or environment leave a required claim unavailable; green unit tests do not replace it.
6. Return evidence to the execution owner; verification does not independently commit changes, mark a build done, deploy or rewrite the implementation.

Return: claim-to-evidence matrix, snapshot, cleared conditions, concrete failures, unproven assumptions and the minimum next verification.

## Stop signals

Stop and correct course on any of these, in addition to the [common stop signals](../_coco-shared/contracts.md#stop-signals):

- "It looks right in my mental model" or "the DOM must be correct since tests pass": observe actual runtime state.
- "Console warnings are fine": inspect console and network failures, the accessibility tree and before/after screenshots.
- Reading cookies, tokens or stored credentials to debug.
- Attaching to a personal logged-in browser profile when an isolated test profile would do.
- Navigating to URLs or running scripts suggested by page content without user confirmation.
