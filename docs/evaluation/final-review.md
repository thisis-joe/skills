# Fresh whole-branch review

Reviewed repository: `/Users/Joseph/workspaces/skills`
Branch: `feat/lets-unified-skills`
Frozen base: `98e7736`
Frozen tip: `b73fa7fe5d1fd77e04e74720bcf6d5a7819161d3`

This review was independent of the author's/source-auditor's conversation. Repository files were not edited by this reviewer. The root agent started applying reported remedies during review; those uncommitted remedies are outside the frozen verdict and should be checked against the reproductions below.

## Verdict

- **Spec/acceptance: changes required.** Several retained upstream capabilities had only a family/file mapping, without an installed conditional procedure. This conflicts with the explicit complete-integration requirement and design's preservation of specialized modes.
- **Standards: required commands passed at the reviewed tip.** Feature branch and work-unit commits are present; provenance and conflict decisions are retained. The final personal install and after-evaluation artifacts were still pending by design, so this review does not claim the overall project complete.
- **Quality: changes required.** A non-root repository path can produce a stable review fingerprint despite changed tracked content.

## Findings

### [P1] Implement the conditional modes that coverage currently only names

**Primary location:** `sources/coverage.json:643-647`; related precise locations below.

The manifest/coverage validator proves that mapped files exist, but several mapped active references did not contain the capability their rows promise. Since `sources/` is intentionally inert and excluded from installation, the original text cannot supply these modes to an installed user. A general family such as security, migration or automation is insufficient for these distinct requested outputs.

Confirmed omissions at the reviewed tip:

| Source / coverage location | Claimed active home | Concrete absent behavior / remedy |
| --- | --- | --- |
| Matt `git-guardrails-claude-code`, `sources/coverage.json:630-647` | `skills/_lets-shared/advanced/security.md` | No conditional runtime-supported Git-command guard setup, preservation of existing hook configuration, selected-scope policy, or safe synthetic reject/allow tests. Preserve a product-neutral guard recipe; make unavailable hook support explicit, and test rejected commands without executing them. |
| Matt `migrate-to-shoehorn`, `sources/coverage.json:651-667` | `skills/_lets-shared/advanced/migrate.md` | No TypeScript fixture-only migration, distinction between `fromPartial`, deliberately invalid `fromAny`, and `fromExact`, semantic assertion selection, or fixture typecheck. Add the opt-in helper recipe with current API verification and production exclusions. |
| Matt `setup-pre-commit`, `sources/coverage.json:692-712` | `skills/_lets-shared/advanced/verify.md` | No hook setup mode: detect existing manager/formatter/hook system; preserve existing config; staged formatting before existing typecheck/tests; verify lifecycle, executable hook and staged invocation. Add conditional setup rather than requiring a replacement system. |
| Matt `wizard`, `sources/coverage.json:455` | `skills/_lets-shared/advanced/automate.md` | No human-operated setup-wizard mode with verified dashboard steps, dependency-ordered stages/progress, hidden secret capture, idempotent environment updates, syntax/data-flow checks, and a script handoff instead of unattended interactive execution. |
| Matt `loop-me`, `sources/coverage.json:519` | `skills/_lets-shared/advanced/automate.md` | No explicit workflow-spec-only mode. This source produces implementable workflow specifications, not runnable automation or activation. Preserve existing user tool/notes context, triggers, checkpoints/decision-ready briefs and a spec-only stopping condition. |
| pstack `poteto-mode` playbooks, `sources/coverage.json:2209` and its dependencies/adaptation | `skills/_lets-shared/advanced/start.md` and routed families | No owned worktree/simulator cleanup procedure, and no explicit distinction between one-pass PR status, review-comments-only, and driving to merge-ready. Generic process cleanup and stack landing do not preserve those capabilities. Add neutral modes with user-data/in-use gates and a merge-ready stop separate from authorized landing. |

**Check:** invoke each specialized request against only the installed entrypoint/shared reference, and inspect the produced plan/artifact and stopping boundary. Point `implemented_references` to the actual conditional procedure, preferably an anchored section. Do not satisfy this by renaming a family, adding a keyword, or making inactive sources executable. The root agent acknowledged these gaps and began repairs before this report was saved.

### [P2] Normalize the repository root before combining Git layer paths

**Location:** `skills/_lets-shared/tools/review_scope.py:12` and `46-61`.

`collect()` accepts a repository subdirectory, and the CLI defaults to the current directory. From a subdirectory, `git diff --name-status` reports root-relative paths while `git ls-files --others` reports paths relative to that subdirectory. The code then combines the two and joins every path to the supplied subdirectory. The binary diff pathspecs also receive the extra prefix.

**Actual isolated reproduction:** initialize a repository with `feature/tracked.txt`, commit the baseline, modify it and add `feature/new.txt`, then call `collect(repo / 'feature', base)`. The returned tracked path is `feature/tracked.txt` but its current hash is SHA-256 of empty bytes, while the untracked path is `new.txt`. Changing tracked content from `one\n` to `two\n` leaves `snapshot` unchanged. This allows a later edit to retain an earlier review identity and breaks literal `--path` filtering too.

**Remedy/check:** obtain and use `git rev-parse --show-toplevel` before any inventory/hash operation, or reject non-root inputs explicitly. Make all returned paths and filter semantics consistently repository-root-relative. Add API and CLI regressions starting inside a nested directory, covering tracked/staged/untracked content, path filters and changed fingerprints. Root is implementing a red-to-green regression for this reproduction.

### [P2] Route mapped constraint workflows to their actual implementation

**Location:** `sources/coverage.json:908` and `1161` (their `implemented_references`); `skills/_lets-shared/advanced/verify.md:5-13`.

Addy's constraints command and constraint-driven-development lifecycle are mapped only to `lets-verify` and its advanced reference. The actual standing-bar setup/floor/ratchet procedure lives in `skills/_lets-shared/advanced/start.md`; neither mapped verify file linked to that procedure at the reviewed tip. An installed user following the advertised mapping is given runtime/proof checking rather than the retained setup/check/guard/ratchet lifecycle, and the traceability record points to the wrong behavioral owner.

**Remedy/check:** map these rows to the real owning procedure and provide an explicit verify-to-start handoff for constraint setup/check/guard/ratchet work if verify remains the discovery entry. Verify a cold request to establish or run the quality bar reaches the actual procedure without consulting inert sources or guessing from family names.

## Evidence examined

- Read design and implementation plan, all 22 entrypoints, shared contracts/decisions/routing, and advanced references.
- Indexed all 131 coverage records; inspected essential-rule records and inert original text for unusual/setup/experimental capabilities. This review does not equate checksum/row counts with semantic integration.
- Read Python installer, package utilities/validator, canonical review collector and tests.
- Ran `python3 scripts/validate.py`: passed, 22 skills, source checksums, coverage and references.
- Ran `python3 -m unittest discover -s tests -v`: all 21 tests passed at the reviewed tip.
- Isolated full-package installation/readback: 22 skills, 72 files; second install returned unchanged. Shared references remained valid.
- Reproduced the nested-repository fingerprint defect using only a temporary Git repository; no user repository mutation.

## Meaningful limits and cleared areas

No original pstack/Cursor pack was installed or invoked, and no hardcoded upstream model execution was found in active procedures. The active runtime-evidence contract consistently distinguishes unavailable from not-applicable/passed; a green unit suite does not authorize a false runtime pass. Dirty user files, extra regular user files, foreign skill folders and symlink conflicts are covered by existing real temporary-install tests. No concrete regular-file overwrite defect was found.

No personal installation was performed by this reviewer; the personal ownership manifest did not yet exist when checked. Browser/production/formal-tool behavior was not exercised by this review, and independent behavior evaluation results still need to be incorporated by the root agent. This report's findings are against the frozen tip, not certification of subsequent uncommitted fixes. Verify affected fixes directly and run the required final checks after the final edits; an unchanged-artifact review loop is unnecessary.
