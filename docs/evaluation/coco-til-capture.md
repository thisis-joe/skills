# Session TIL change verification

Base: `04507c149787c9792bfedd1cd8f1f65dd2c59a6a`; branch: `feat/coco-til-session-capture`.
Spec: [session TIL capture](../specs/coco-til.md). Tier: shared/procedure change, checked with isolated local repositories and installer destinations. Starting checkout: main, clean at the base above.

## Executed checks

- `python3 scripts/validate.py`: passed, 30 skills; original source checksums, current coverage owners and payload references valid.
- `python3 -m unittest discover -s tests -v`: passed, 205 tests in 59.729 seconds. After final documentation and test-label cleanup, focused TIL tests passed (22) and source-fidelity tests passed (13).
- Real repositories: primary and nested linked invocations choose the same primary TIL; an ignored note remains after removing the linked worktree. Non-Git resolution creates no files. A moved/missing primary raises instead of creating a linked TIL. Bare primary plus its linked checkout reject fallback. Symlinked TIL rejects writes outside the root. Separate Git metadata and a newline pathname resolve a non-linked primary correctly.
- Initial fixtures exposed two defects: broken linked metadata looked like a non-Git folder, and separate metadata could be mistaken for the primary folder. Marker detection and non-linked Git identity checks fixed them; the same cases now pass.
- Existing checker and example exactly equal their base versions after substituting the skill identifier. Existing translated-template, schema/budget, index, malformed-template and literal-Markdown cases pass.
- Installer fixture: install the base into a temporary custom destination, preserve an unrelated user file, install the candidate, confirm old coco-learn removal and new resolver presence, and validate installed hashes/references. Passed. Live Codex destination preflight also passed with no ownership conflict.

## Direct scenario review

These are author walkthroughs of the final instructions, not an independent model evaluation or proof of semantic selection quality.

1. Changed selection path: a session has four worthwhile authentication candidates, one React concept and several activity-log lines. Select the best three authentication concepts and one React concept; exclude log lines, without splitting authentication into artificial topics or asking for approval. A sparse topic with only one concept produces only that note.
2. Empty and repeat paths: a session with only routine commands stops before any storage mutation. Rephrasing a concept already in TIL with no new evidence skips it and leaves content/dates unchanged; new evidence updates the existing semantic match. Conflicting user content is preserved for resolution.
3. Preserved format path: each selected concept uses the existing five sections, budget and translated TEMPLATE labels. Capture starts new notes as learning, never inferred understood. Example and checker fixtures validate the preserved format; note importance and truth still require agent judgment.

Self-review covered changed registration, bare invocation routing, callers, blog discovery, resolver/code/tests, schema preservation and attribution overrides. No independent fresh-context agent review was performed. Source snapshots and essential_rules remain unchanged; excluded teaching modes are explicitly recorded rather than claimed preserved. Primary storage prevents linked-worktree deletion loss, not loss of the primary folder itself or lack of backup.

## P2 review follow-up

Review of `fe2ef1883b89dc09b6e7adb376a9f9ba2c176008` found that separate Git
metadata plus a linked worktree selected the metadata directory as the primary
working folder. The review correction is now exercised with real repositories:

- Red: both absolute and relative `core.worktree` configurations failed with
  `Primary checkout is not a working tree` before the fix.
- Green: resolve from the shared Git configuration when its directory is listed
  as the primary; relative paths resolve against that directory. Verify the
  candidate's top-level, common Git directory and primary Git directory identity.
- Both configurations now return the same primary TIL from primary and nested
  linked invocations. Notes remain after deleting the linked checkout.
- Missing targets, unrelated repositories, configured linked checkouts and absent
  primary-path configuration fail closed without creating a fallback TIL.
  If Git records no primary path, the resolver still does not guess or scan folders.
- `python3 -B scripts/validate.py`: passed. `python3 -B -m unittest discover -s tests -v`:
  207 tests passed in 63.692 seconds, including the preserved note-format cases.
- Installer fixture: copy the current ownership-managed installation into a
  temporary destination, update through the supported installer, validate the
  installed package and resolver equality, and retain an unrelated user file. Passed.
- Direct diff/self-review checked the P2 correction and primary-only identity guard.
  No independent fresh-context review was performed. Frozen upstream sources,
  note format and selection behavior are unchanged by this fix.

## 1.3.0 Git publication preparation

The user authorized remote push and main merge with source version 1.3.0 and
requested README maintenance. Integrated origin/main at `dd28983a1242ba546e5e0c7e9da6e1cbc38e4515`;
the only conflict was the shared decision record, resolved by retaining the
consumer publication-schema row and the session-TIL section. The blog's schema
fix remains alongside primary-checkout note discovery. No dev/develop refs were
present at the confirmed write remote; main is the explicitly requested target.

Version, README, migration notes and the package file allowlist now describe 1.3.0.
Registry installation examples remain pinned to the already published 1.2.0,
because Git push/merge does not authorize or prove npm publication. No tag or
registry publication is claimed. Rollback is a reviewed revert of the feature
on main or an explicit-destination reinstall of the previous package; TIL remains
personal and must be preserved separately.

After integration, `python3 -B scripts/validate.py` passed and
`python3 -B -m unittest discover -s tests -v` passed all 207 tests in 69.263 seconds.
Archive tests validate the packed CLI, both runtime installs, the new release
notes/resolver and absence of the old skill. No dependency changes were introduced.
Direct diff review checked both sides of the integration conflict, package
contents and the README publication boundary; independent review remains unavailable.
Forge check/merge/readback are pending at this preparation snapshot.

## CI packaging correction and npm scope

The first PR run at `8a78ca6` failed Linux Python 3.9 and current Python because
ordinary discovery imported the resolver before npm packaging and generated
`skills/coco-til/tools/__pycache__/resolve_workspace.*.pyc`. Earlier local `-B`
runs suppressed that side effect and did not establish the standing CI path.
An isolated contaminated-package regression failed before the fix, observing
both a cache-directory file and a legacy `.pyc` in the archive. Explicit package
file exclusions now remove both while retaining runtime source. All 15 npm
archive tests passed after the fix. Standing commands without `-B` passed package
validation and all 208 tests in 65.200 seconds. After that run, a fixture-only
portability change retained space-path coverage on all platforms and newline
coverage on POSIX, because Windows forbids that filename; all six resolver tests passed.

The user subsequently explicitly authorized npm publication, confirming that this
chat publishes 1.3.0 and the askme/research chat separately publishes 1.4.0.
The earlier Git-only publication boundary is superseded for 1.3.0. README registry
examples now target the authorized version; registry publication and fresh-cache
readback still require actual execution before being reported complete. A summary
of failures, fixes and shared-installation hazards was delivered to the named
askme/research chat at the user's explicit request.

## Windows Python 3.9 encoding correction

At head `67035f2`, Linux checks, all shell checks and Windows current Python
passed. Windows Python 3.9 exposed one new test reading UTF-8 coverage.json
with its default cp1252 encoding. An ASCII-default local run reproduced the
same implicit-decoding defect (`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C
python3 -m unittest discover -s tests -p test_source_fidelity.py -v`). Explicit
UTF-8 reading fixes the test without changing its assertions or source facts;
all 13 source-fidelity tests then passed in the same non-UTF-8-default run.
Keep file encodings explicit rather than making UTF-8 mode a CI prerequisite.
