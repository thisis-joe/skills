# Runtime verification

This short-lived integer CLI uses Python's standard library. No installation,
authentication, fixture, migration, build step, or server is required. Run the
following commands from this directory.

- **Launch:** `python3 app.py --help`. Exit 0 and a usage message listing
  `--double` and `--multiply` establish the usable public interface.
- **Doctor:** `python3 verify_cli.py doctor`. This launches the real CLI help,
  checks its public options against the driver, and reconciles
  `features/index.json`, feature documents, and executable recipes. Every check
  must pass before driving. Re-run doctor after an unexpected failure.
- **Drive:** `python3 verify_cli.py drive`. A fresh doctor runs first, then every
  indexed feature runs through `app.py` in fresh subprocesses. Coverage includes
  both help aliases; positive, negative, and zero arithmetic; required and
  mutually exclusive operations; integer validation; argument count errors; and
  an unknown option. Expected numbers are literal values independent of product
  implementation. Successful arithmetic requires exact stdout, empty stderr, and
  exit 0; parser errors require empty stdout, exit 2, and a matching diagnostic.
- **Regression:** `python3 -m unittest -v` runs the existing test suite. Keep its
  stdout, stderr, and return code with the runtime evidence; the suite alone
  covers only positive doubling.
- **Reset:** every invocation uses a new process and has no persistent app state.
- **Evidence:** the helper prints raw child commands, inputs, outputs, return
  codes, expectations, and its exact `evidence_path`. Records include app, helper,
  and feature-map SHA-256 snapshots. It creates `evidence/doctor.json` or
  `evidence/drive.json` only if absent; existing paths are preserved and subsequent
  runs use numbered files beginning with `evidence/doctor-001.json` and
  `evidence/drive-001.json`. Never delete or overwrite earlier proof.
- **Cleanup:** subprocesses finish before the helper returns. No ports, sessions,
  scratch fixture data, or background processes need cleanup. Confirm the printed
  evidence path exists and is readable after the run; keep it and all user files.
- **Failure behavior:** helper usage errors exit nonzero. Failed doctor or drive
  checks retain their observations and exit 1. A failed drive preflight skips
  dependent cases and records the blocker. Report a product regression without
  changing product, tests, or user notes.

Feature index: `features/index.json`. Read the indexed documents for public
routes, exact recipes, states, observations, and gotchas. Reconcile newly exposed
options or state changes with both the map and executable driver before claiming
complete coverage. These recipes represent the documented states, not every
possible integer or argument spelling.
