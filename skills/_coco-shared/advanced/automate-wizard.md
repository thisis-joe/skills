Read/apply [core](automate.md) first; no new authority.

## Conditional human-operated setup wizard

Use for an explicitly requested repeatable/manual setup that requires a person's dashboard access,
credential entry or irreversible choice; do not turn agent-runnable steps into human busywork.
Inspect env examples, configuration, CI secret/variable references and the actual current setup first.
Build a dependency-ordered stage table: stage name, verified dashboard/command journey, produced value,
secret/public classification, destination and irreversible boundary. Reuse choices already settled.
Verify current dashboard URLs/labels from primary documentation or available UI; mark unknown steps
instead of inventing them. Each stage should fit one focused screen and show remaining progress.

Author a scratch or requested reusable script with consistent stage/progress/confirmation helpers.
Open a verified URL before requesting its value; capture secrets with hidden input and do not echo them.
Write `.env` values through an idempotent, correctly quoted key upsert that preserves unrelated keys
and file permissions. Avoid command interpolation, duplicate keys and logging of secret values.
Only write a remote secret/variable to a user-authorized destination that actually needs it; map names
to the real CI references. Confirm irreversible actions through the runtime's required user boundary.
Handle rerun/completed stages and partial failure without duplicating effects or losing captured state.

Run `bash -n` for a Bash wizard and ShellCheck if available. Trace every required value from source
through hidden/public capture to its intended destination, and test helpers on fake local data.
Safe readback reports presence or a masked checksum, never reveals a credential.
Do not execute an interactive script unattended to call it tested: it may open a browser and block.
Hand off its exact invocation, remaining manual steps and cleanup/retention instructions. Commit the
script only when the requested deliverable is a repeatable repository setup path; otherwise keep it
explicitly disposable. Prepared, statically checked and human-completed are separate states.

