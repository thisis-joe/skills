# COCO Skills 1.2.0 release candidate

## Consumer changes

- Add `coco-blog`, bringing the catalog from 29 to 30 skills. It selects local development notes, drafts evidence-backed public articles, prepares the repository-native publication handoff and verifies a requested publication.
- Preserve source notes, hand edits, settled author choices and separate content histories. Drafting and author acceptance do not authorize Git delivery or publication; commit/push authorization does not imply PR/MR creation.
- Discover the consumer's actual draft/publication schema. Hugo's `draft: false` is an example; projects using `published` or `status` retain their documented state transition.
- Existing skill identifiers, installer interfaces and frozen upstream source attribution are unchanged. This is a minor release because it adds a public skill without removing an existing one.

## Installation and rollback

The version is prepared locally and is not claimed as published. After registry publication, run the version-pinned installer with the intended runtime and project, for example:

```sh
npx --yes @thisis-joe/coco-skills@1.2.0 install --runtime codex --project .
npx --yes @thisis-joe/coco-skills@1.2.0 install --runtime claude --project .
```

Open a new agent session after installation. Updating npm alone does not install skills. To roll back, rerun the same command with `@1.1.0` and the same runtime/destination. The older catalog removes the managed `coco-blog` directory; personal changes must be preserved and reconciled if installer preflight stops. No source-note or published-article migration is part of this package update.

## Verification

The validator and 200 repository tests passed; the affected 14 npm distribution tests also passed after the archive allow-list update. Four native Codex scenarios exercised note selection, a `status: draft` manuscript, an approved `published: true` transition and the preserved Hugo release path. Both runtime installers passed temporary upgrade, reinstall, personal-file protection and exact rollback checks. See `docs/evaluation/coco-blog-1.2.0/` in the source repository for the frozen protocol, evidence and final independent review. Behavior samples establish only the exercised paths; they do not prove universal prompt adherence, comparative model quality, or a real consumer site's publisher.

Native behavior was exercised once per scenario in Codex; Claude installation was checked without a native Claude session. Local renderer and local-origin results do not establish a real public deployment. Child sandbox restrictions required same-origin isolated clones for publication preparation; original application changes remained intact. No registry publication or personal installation is performed by this verification.
