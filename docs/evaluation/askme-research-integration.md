# Askme research integration verification

## Scope and provenance

Starting checkout: main at 04507c149787c9792bfedd1cd8f1f65dd2c59a6a, clean. The user explicitly selected the already installed TIL work as the integration base: ba462cb (including the later separate-metadata primary-checkout fix). Work is isolated on feat/askme-research-integration. Source snapshots, source manifest and original essential_rules are unchanged. Existing research coverage rows now identify askme as owner; the shared evidence procedure stays reusable. The new orientation/recovery/alias rules are team-authored.

## Executable local checks

- Isolated installation fixture: install the real bundle into a temporary skills directory containing an unrelated user skill; validate the installed manifest, follow the alias link to the owner and its conditional research/quiz references, compare all TIL files, then run idempotent installation. This exercises actual installer behavior, not an invented conversational engine.
- Opening-cost guard: askme entry must fit within its prior 6052-byte entry size; alias must fit within 700 bytes. Confirm the opening declares no discovery when context suffices, one recovery batch/two identified sources/120 excerpt lines when it does not, and no quiz-reference preload. These are instruction-size and structural checks, not measured token or latency claims.
- Research preservation: existing source-fidelity mutation tests remain enabled and now inspect the real askme owner. All four original research coverage rows retain essential_rules and live shared-evidence references; no upstream source is reattributed to team-created menu behavior.

Commands: `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`, and the supported installer's explicit global dry-run, installation and installed validation.

## Author walkthrough of conversation paths

These are direct instruction reviews, not fresh-model execution results.

| Case | Concrete input | Required path and inspected boundary |
|---|---|---|
| Changed opening | Bare askme after a retry/cache discussion | At most three session concepts; free text; no research/question-pattern loading or content-discovery call |
| Compaction recovery | Summary says a retry decision is missing and names a task section plus one symbol | One batch reading only those two known sources, at most 120 lines; disclose recoverable coverage; ask for a target if still insufficient; no history sweep |
| Preserved investigation and quiz | Explicit research asks why a guard exists; later user requests a quiz | Alias forwards original question directly; load historical evidence without compulsory quiz; explicit quiz asks one sourced question, withholds answer and waits; an incorrect reply alone does not trigger a new investigation |

Direct review found and fixed duplicated quiz-loading instructions and a stale source-index statement that denied research ownership. Package tests initially exposed the old family/stop-signal owner assumptions; they were moved to askme rather than weakened. Opening-size guards caught excess entry text and a six-character shared hot-path overflow; conditional quiz details were split out and duplicate prose removed without raising thresholds.

## Verified results

Package validation passed (30 skills). The complete suite passed: 210 tests in 62.687 seconds; log: `/private/tmp/coco-askme-integration-verified-tests.log`. Opening entry size is 5821 bytes (prior bound 6052); alias is 551 bytes. Explicit global installer dry-run passed against the existing owned install. The local installation fixture passed, including unrelated-file preservation, TIL equality and idempotence. The starting main checkout remains clean at its original HEAD.

## Evidence limits

No independent fresh-context conversational run was performed in this turn. Model compliance with topic relevance, recovery limits, tool choice and answer timing remains unverified at runtime; the walkthrough is author review only. Actual token cost and latency were not measured. Automatic compaction may omit capsule content despite guidance; recovery can only inspect available session-linked pointers and must disclose gaps. The installed bundle comes from the unmerged dedicated branch, not main. No remote publication is part of this task.

## Post-implementation independent review and correction

An independent reviewer inspected ba462cb..79ef23c and independently passed package validation and all 210 tests. It found one P2 instruction gap: evidence-boundary disclosure applied only after recovery, omitting a sufficient compressed-summary menu with zero recovery. The owner now requires disclosure for compressed or handoff context whether recovery ran or not; a structural regression check covers that condition.

Separate fresh-context behavioral probes actually applied the skill to synthetic inputs (not private session transcripts). A compressed retry/cache summary with no source pointers produced three relevant options, free-text entry and an explicit remaining-summary boundary without content discovery. An explicit quiz on a supplied pure-Python retry function produced exactly one source-located question and withheld its answer. Both probes passed before the correction; the correction closes the documented guarantee rather than claiming a reproduced model failure. These probes establish those specific responses, not all models, future conversations or token savings.

A third fresh-context probe exercised the research alias after the disclosure correction: from an incomplete summary it read only the supplied handoff (one source, at most 60 lines requested), stopped when sufficient concepts were recovered, disclosed the summary/handoff boundary and offered three relevant topics plus free text. It did not read the implementation or unrelated fixture file, browse the web, scan Git history or preload research/quiz references.

The predecessor release reported a Windows default-encoding failure, prompting a matching check of this change's new tests. `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 -m unittest discover -s tests -p test_askme_integration.py -v` reproduced UnicodeDecodeError in the coverage JSON read on Python 3.9. All new text reads/writes now specify UTF-8; the same command passes after correction. This is a reproduced test portability defect, separate from the conversational instruction finding.
