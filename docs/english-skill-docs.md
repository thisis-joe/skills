# English skill sources, localized user interaction

The user requires maintained skill documents to be written in English to avoid
mixed-language instruction overhead. The active COCO tree now uses English for
all instruction Markdown, discovery descriptions, and UI metadata. The scope is
97 Markdown/YAML documents across the shared support files and 26 entrypoints.
Legal attribution and frozen upstream source evidence retain their original
content.

The original English sentence in every discovery description is unchanged;
only its redundant Korean summary was removed. Combined description lines fell
from 4,447 to 3,967 characters. This is a description-text measurement, not a
native model token or session-context measurement. English normalization is
separate from the [21.49% loading-guidance comparison](context-compaction.md),
whose snapshots were frozen before this work.

Team workflows for push, skill maintenance, explanation, and request drafting,
plus build's branch-preparation section, were translated obligation by obligation.
Names and UI selection policy stay intact. Branch links now target the English
heading. Exact Jira Summaries remain user-owned literals: preserve their actual
language, case, punctuation, and underscores, and obtain approval for necessary
Git-invalid-character transformations rather than silently slugifying.

English instruction sources still request localized user replies, choices, and
explanation labels. The fixed eight explanation items retain their meaning and
order. Request drafting still preserves prompt-only intent after a numbered
choice and executes only when the user authorizes execution. Existing waits,
settled-question skips, publication boundaries, installation preservation, and
partial-failure handling remain part of their original workflows.

The repository's `AGENTS.md`, maintenance reference, and decision history now
record the language rule. A regression test rejects Hangul in active Markdown
and YAML, including discovery metadata and references; legal license text is
outside that instruction-document check. A heading-link test catches stale
translated anchors. A bilingual review covers English meaning, which a character
detector alone cannot establish.

[Evaluation and installation records](evaluation/english-skill-docs/README.md)
retain the static comparison, observed pre-change language failure, 41 passing
tests, directed Korean interaction probes, and the supported managed update.
The installed 99 files match the source exactly, and all 50 unrelated files keep
their original content. This final installation includes the preceding compaction
work unit. Native client catalog refresh and all workflow branches were not
tested.
