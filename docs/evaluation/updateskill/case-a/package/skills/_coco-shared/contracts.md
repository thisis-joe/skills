# Fixture common contract

## Checks

Discover the current project's required checks from its repository instructions and CI. For this maintained COCO package, those facts require `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. Run them before completion and record each command, inspected snapshot, exit result and evidence pointer. In another project, use that project's discovered checks; these COCO commands are conditional on this package.

## Shared procedure impact

Before committing a shared procedure change, inspect both registered entrypoints and their linked references. Record which callers change and which behavior is preserved. This team rule is owned here; entrypoints refer to it rather than defining separate copies. An inspected diff and passing focused checks do not imply remote publication or unrelated product work is complete.

## Ownership

Use a feature branch and atomic work-unit commits. Preserve user edits. Upstream files are inert evidence.
