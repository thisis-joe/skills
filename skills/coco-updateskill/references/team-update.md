# Maintain skills for team conventions

## Authoritative source and scope

Find the authoritative repository from the current workspace, user-specified location, and project maintenance guidance. For COCO, compare registration in `coco.json`, `skills/coco-*/`, `skills/_coco-shared/`, and the actual installation manifest. Do not depend on one user's absolute path or search all personal directories. If the source is unconfirmed, establish its location rather than arbitrarily promoting installed files to a new source of truth.

First distinguish maintainers and source locations for installed system or external-plugin skills. Direct cache edits may disappear on update. If a team copy is needed, align its purpose, name, and location with the request before proceeding; retain upstream licenses and attribution. Do not turn an existing-skill update into arbitrary creation of a new skill, upstream upgrade, or automatic installation.

Reuse agreed team commands, review standards, and execution modes. Apply conditional modes where repository rules differ. For example, do not copy one Node repository's `pnpm` commands into a Python repository or every team skill's common commands. Respect explicit user/team scope and ask only about missing material behavior.

## Compare before/after and inspect effects

Keep maintained COCO instruction documents and discovery descriptions in English. Localize actual replies to the user's language and preserve user-owned literals such as exact Jira Summaries.

Capture pre-change files/commits/hashes and relevant cases. Briefly state the intent as "current behavior → desired team behavior → preserved behavior → verification method." Do not read all unrelated skill sources or recreate an agreed development specification from the beginning.

Identify which file owns each current rule. If common contract, routing, decision records, and entrypoints conflict, establish one owner and reference it. Find callers and uses with `rg` or available reference search. Align descriptions, procedure, conditional references, and examples so they do not promise different behavior. Change only necessary fields in `agents/openai.yaml`; do not change existing policy/dependencies or automatic selection behavior without a request.

Do not execute the skill merely because you are editing it. For example, modifying `coco-push` does not authorize a remote push from a user's repository. Test behavior within authorized boundaries using temporary repositories, fake credentials, or local destinations. Reviewing only policies/stages does not establish actual service behavior.

When modifying `coco-updateskill` itself, retain the starting version and agreed scope; instructions changed during the work do not expand authority or completion conditions. Reread the final files to ensure the applied procedure, changes, and verification agree.

## Attribution and team decisions

- `sources/**/*.source` and `sources/manifest.json` are frozen source evidence. Do not overwrite source text or its original SHA-256 to change team wording/rules. Handle an upstream-version update as a separate attribution update only when requested.
- Retain original `essential_rules` in `sources/coverage.json` as facts about that source snapshot. Adoption/modification/exclusion reasons and `implemented_references` must reflect actual team changes. Align related guidance when source mappings change. Do not remove an original requirement while still claiming it is preserved.
- Record common-rule choices and reasons in the existing `skills/_coco-shared/decisions.md`. Use existing repository records/commits and evidence for individual changes. Do not create duplicate authoritative maintenance records.

## Verification and installation

Discover actual COCO check commands. Examples for the current package:

```text
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/install.py --dry-run
python3 scripts/install.py
python3 scripts/validate.py --installed <confirmed-installation-directory>
```

Do not assume another repository has these commands. Also run available skill-format checks. Format validation does not prove sound judgment: test actual cases for both changed and preserved paths. If required tools or independent review are unavailable, distinguish confirmed scope from unverified scope. Do not weaken checks or rewrite historical evaluation reports to hide failure.

Before installation, compare the ownership manifest with current files and use the supported installer's preflight. Preserve and show differences for conflicts involving personal edits, extra files, same-name external skills, or symbolic links. Do not delete the ownership manifest or manipulate hashes to manufacture installation success. If a supported preservation/migration procedure cannot be established, leave installation blocked separately from source changes.

Reread relevant source/installed files, hashes, and references and confirm other skills and personal files survive. If installation fails after the source commit, do not recreate the existing commit. On resumption, inspect actual commit/change/installation state and continue from the remaining installation step. Distinguish the verified version from actual installation state in the report.
