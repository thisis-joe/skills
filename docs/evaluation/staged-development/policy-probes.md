# Directed policy probes

These are actual disposable-project executions in fresh agent contexts, separate
from the blinded comparative trials. They are synthetic consent fixtures, not
observations of human comprehension. No publication or specialist examination ran.
The portable archive retains resulting fixture files and modes, and this document
records the fresh policy agents' reported observations. It does not contain their
complete action/output transcripts. Archive inspection alone cannot authenticate
those agents' conversational freshness or reconstruct every decision; the native
comparative and final-report trials retain full action records separately.

## Manual transitions during continuous task scheduling

Project: `/private/tmp/coco-staged-manual-probe`. Local candidate skill snapshot
`fbe87ea`; authoritative `work-state.json` selected manual skill transitions and
continuous task scheduling. The explicit request selected `coco-spec` for an
agreed ASCII access-code normalizer contract.

Observed: saved `docs/specs/access-code-normalization.md`, updated the authoritative
record, preserved `skill_mode: manual` and `automatic_basic_transitions: false`,
and stopped before `coco-plan` or implementation. The final response introduced
the next skill with once/automatic-for-this-spec alternatives. Continuous task
scheduling did not silently change skill consent. The seed implementation stayed
unchanged. This rechecks the advanced spec/plan conflict found in initial review.

## Personal specialist preference persistence

The primary comparison froze before the fallback persistence recipe was made
concrete. This final-source delta is exercised here, not retroactively attributed
to the earlier snapshot. Both local workflows had SHA-256
`f9069f6d39ccaeeb2206c1ea26b3500f94e5193f42a96916525e0e5473007de0`.

A fresh agent received an explicit synthetic opt-in for known runtime identity
`fixture-owner-a`, only `coco-security`, only project
`/private/tmp/coco-staged-preferences-a`. It created the actual record:

```json
{
  "schema_version": 1,
  "user_identity": "fixture-owner-a",
  "project_root": "/private/tmp/coco-staged-preferences-a",
  "automatically_allowed_skills": ["coco-security"]
}
```

Readback confirmed `.coco/preferences/fixture-owner-a.json`, directories `0700`,
file `0600`, owner matching the running user, and `/.coco/preferences/` in this
checkout's `.git/info/exclude`. `git check-ignore -v` identified that local rule;
`git ls-files` showed no tracked preference. No code changed and no commit ran.

For sensitivity, the author copied that record unchanged to project B without
repairing its stored project root, exclusion or permissions. A separate agent
inspected both actual projects read-only:

| Runtime identity / project / requested specialist | Consent result |
| --- | --- |
| `fixture-owner-b` / A / security | manual; no matching user record |
| `fixture-owner-a` / B / security | manual; stored root is A, not canonical B |
| `fixture-owner-a` / A / performance | manual; exact skill absent |
| `fixture-owner-a` / A / security | stored consent matches |

B's copied file was `0644`, unexcluded and untracked; it was not treated as valid
consent or repaired. These probes evaluate provided identities and records; they
do not authenticate a real human identity or prove historical opt-in provenance.
Revocation and unavailable-identity fallbacks remain specified and source-reviewed,
not claimed as separately exercised runtime cases.
