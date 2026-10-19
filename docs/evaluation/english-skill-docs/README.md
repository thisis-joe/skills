# English normalization evidence

Baseline: compaction commit `78ab56a`. This is a separate work unit from the
frozen [compaction comparison](../context-compaction/README.md).

## Source checks

- [Before-change language check](before-language-check.json): 193 lines with Hangul in active instruction Markdown/YAML; the language assertion was expected to fail.
- [Structure comparison](structure.json): all 26 English primary descriptions and UI metadata preserved, 97 English instruction/metadata documents, source evidence and license unchanged. Description lines shrink by 480 characters; native token counts were not measured.
- [Required checks](root-checks.json): package validation and all 41 unit tests passed. New checks cover active language, injected metadata/reference failures, and local heading links.
- [Bilingual review](review.md): static comparison of the complete team workflows and branch rule, followed by a final applied-tree check.

The Hangul detector enforces the concrete mixed-language regression observed
here; human review establishes that the replacement instructions are English
and preserve the original meaning. It is not a general natural-language
classifier. License attribution is preserved outside the detector.

## Directed local interaction

[Requests, observations, and limits](behavior-results.json) and [raw responses](behavior/)
retain a fresh worker's application of the English procedures to Korean requests:

1. Explain `coco-verify` briefly: returned eight Korean explanation items without running verification.
2. Draft only a local `fixture-report` request: returned wording without creating the report.
3. Show three explicitly requested numbered alternatives, then select `1`: still returned only the complete invocation. The coordinator directly checked that `REPORT.json` did not exist.
4. Explicitly request execution of option 1: created the local report with original values `[2, 3, 7]`, sum `12`, and the requested focus. Original input and user notes remained unchanged.

This was directed, not blinded. The coordinator reminded the worker of the
continuing prompt-only intent with the numeric follow-up. The catalog was tiny
and supplied, and execution used a local fixture skill with an observable file
write. This supports localized interaction and the demonstrated boundary; it
does not prove every recommendation format, catalog branch, native invocation,
or remote workflow. The behavior snapshot predates only the final explicit
maintenance-policy paragraph and language-decision row.

## Managed installation

[Installation verification](installation.json) records the supported dry-run,
successful update to `/Users/Joseph/.codex/skills`, installed validation, and an
unchanged repeat. All 26 skills and 99 payload files match their source bytes.
The 50 unrelated files have identical before/after aggregate hashes. No ownership
manifest was bypassed, no unmanaged cache was edited, and no remote publication
was requested or performed. The result includes both compaction and translation.
