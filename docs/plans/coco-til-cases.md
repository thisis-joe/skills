# Session troubleshooting case plan

Specification: [session troubleshooting cases](../specs/coco-til-cases.md).

1. Split concept and case selection before any storage changes. Reuse the existing root resolution, ignore rule and user-content protections. Add the case format, evidence and duplicate rules, and align discovery text and the team decision record.
2. Add a case checker and local fixtures for case-only and mixed workspaces, malformed or missing case evidence references, and missing, duplicate or misplaced index links. Run scenario checks for insufficient evidence and semantic duplicates separately from the structural checker.
3. Run package validation and the full test suite. Commit the verified work in the dedicated branch, then use the supported installer and validate readback at the established Codex destination.
