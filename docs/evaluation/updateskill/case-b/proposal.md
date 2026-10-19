# Concrete proposal only

Replace the `Checks` paragraph in `skills/_coco-shared/contracts.md` with:

```text
Discover the current project's required checks from its repository instructions and CI. For this maintained COCO package, those facts require `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. Run them before completion and record each command, inspected snapshot, exit result and evidence pointer. In another project, use that project's discovered checks; these COCO commands are conditional on this package.
```

Add a single shared `Shared procedure impact` section:

```text
Before committing a shared procedure change, inspect both registered entrypoints and their linked references. Record which callers change and which behavior is preserved. This team rule is owned here; entrypoints refer to it rather than defining separate copies. An inspected diff and passing focused checks do not imply remote publication or unrelated product work is complete.
```

Update both `coco-build` and `coco-review` entrypoint links and `references/team-checks.md` to refer to those shared sections; remove each repeated legacy pytest example. Change README's package example to the repository's two actual commands. Revise D001 to explain the current project facts, and add D002 as a new team convention with no invented upstream attribution. Change coverage disposition to `adapted`, revise its adaptation explanation, and list both caller implementations. Preserve `essential_rules`, original snapshot, source manifest, names/frontmatter/UI/policy/dependencies, and unrelated user files.

Source impact: two entrypoints, two linked references, shared contract, existing decisions, README and coverage. An eventual implementation would run the package validator and unittest suite, commit the validated work unit on a feature branch, then dry-run and apply the supported installer to the already-known local destination. The present request authorizes no source edit, commit or installation. The installed bundle and source remain exactly as inspected.
