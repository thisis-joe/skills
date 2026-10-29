# COCO 1.4.0 release preparation

## Candidate and review

Feature branch: feat/askme-research-integration. Main source integration: c94cfde, merged locally in f2d7a97. Independent review of the feature found the compressed-summary zero-recovery disclosure gap; fa654d0 fixed it and the reviewer confirmed resolution. A Python 3.9 ASCII-locale probe reproduced a new test's implicit-decoding failure; 545bfaf fixed UTF-8 text IO, independently rechecked. Incremental release metadata and README merge resolution have no open independent findings.

Three separate fresh-context probes exercised a sufficient compressed summary, explicit quiz answer withholding, and research-alias recovery using one supplied handoff. These are sampled model responses, not universal compliance or performance proof. See askme-research-integration.md for scope and limits.

## Local executable verification

- After main integration: package validation and all 211 tests passed (65.394 seconds), `/private/tmp/coco-askme-main-integration-tests.log`.
- Final source 1.4.0: package validation, explicit ASCII-locale focused tests and normal `npm pack` with prepack passed. Prepack ran all 211 tests (65.446 seconds), `/private/tmp/coco-1.4.0-preparation/prepack.log`.
- The exact tarball contains 477 regular files, no Python caches, and every member matches the current source bytes. Release notes and all primary-source provenance are included.
- The packed CLI reports 1.4.0. A fresh offline npm cache installed and validated both Codex and Claude into separate temporary destinations (30 skills, 126 installed files each), preserving TIL, alias and owner. Actual user-global installations were not overwritten while predecessor publication remained pending.

Archive: `/private/tmp/coco-1.4.0-preparation/thisis-joe-coco-skills-1.4.0.tgz`.
Integrity: `sha512-GsW9blY4Xxa2a3G/8SpYOFiXUrC5fTS5OmCjMNcCcSujhQ7FeZ+BbPbMFU2m6Fc2C1Q8tA5p9VXq3zKMpA8HHw==`.

## Publication gate and recovery

At preparation, predecessor PR #33 is merged into main but npm 1.3.0 awaits user browser 2FA. GitHub publication/merge and npm 1.4.0 remain pending, not successful. Before proceeding, verify the predecessor completion notice, main containment and registry 1.3.0. Refresh target/work refs, keep all CI gates and pin the candidate head for merge. Publish this exact inspected tarball only when its source is merged and current.

After publication verify registry 1.4.0 and integrity, then download/install through a fresh registry cache for each runtime. Re-run owned global preflight/source comparisons only if installing locally. Recovery is a preflighted reinstall of pinned 1.3.0 at the same explicit destination with personal TIL preserved; never reuse a published npm version.
