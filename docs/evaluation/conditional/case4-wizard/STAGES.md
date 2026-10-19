# Setup wizard stage/value trace
| Stage | Journey/source | Value and classification | Destination | Boundary and recovery |
|---|---|---|---|---|
| 1 | Open documented https://resend.com/api-keys; log in and use approved existing sending key. Logged-in labels not verified. | RESEND_API_KEY; secret, hidden capture | local .env only, literal parser in inputs/app_config.py | Person controls credential creation; no remote action here. Rerun keeps present key unless replacement confirmed. Failure before upsert keeps old file. |
| 2 | Agreed origin from supplied .env.example/brief | APP_ORIGIN; public, settled https://reports.example.invalid | local .env, preserve existing value | Atomic idempotent upsert; existing differing value retained, owner resolves change separately. |
| 3 | .github/workflows/send.yml env references | same secret/public names | presence-only local readback; manual future CI secret/variable handoff | Remote storage not authorized or executed; no email send. Partial local state stays resumable. |

Exact future human invocation: `bash /tmp/lets-conditional-validation/case4-wizard/setup-wizard.sh /path/to/owned/project/.env` in a real terminal. Do not source the env file; use the supplied data parser. This syntax is fixture-specific, not a promise of compatibility with every dotenv library. Existing malformed env syntax blocks rather than overwrites.

Prepared and Bash syntax checked; helper unit behavior checked on labelled fake values. ShellCheck unavailable. Interactive completion and authenticated dashboard behavior unverified. The wizard itself was never executed. Nothing was committed; this requested output is disposable. Retain the helper alongside the wizard until local setup is done. Keep the resulting .env private for its intended lifetime; human removes it at the end of that use. No remote secret copy is retained here.

[Resend's primary key documentation](https://resend.com/docs/dashboard/api-keys/introduction) links the verified URL and explains single-view values. Browser evidence was public docs/login only; it did not verify an authenticated account or create a key. Local fake artifacts contain conspicuous synthetic values, never real credentials.
