# Runtime verification

The current target is the short-lived Python CLI in `app.py`; source inspection finds three user-facing features: help, double, and triple. `argparse` requires one integer operation and rejects both operations together. The previous feature index omitted triple: this was documentation drift. Product and existing test sources are unchanged. Target SHA-256 values are retained in `evidence/snapshot.json`.

## Launch, doctor, and isolation

Run all commands from this case directory with Python 3. There are no dependencies, ports, authentication, data fixtures, or long-lived processes. Each `python3 app.py ...` command launches and terminates its own instance. Before driving, run `python3 app.py --help`: expect exit 0 and both `--double` and `--triple` in the usage. Repeat doctor after an unexpected failure before diagnosing the app.

## Feature index and live recipes

| Feature / state | Exact command | Required observation | Retained record |
| --- | --- | --- | --- |
| Help | `python3 app.py --help` | Exit 0; usage exposes double and triple | `evidence/01-doctor.json` |
| Double positive | `python3 app.py --double 3` | Exit 0; stdout `6` | `evidence/02-double_positive.json` |
| Double negative | `python3 app.py --double -4` | Exit 0; stdout `-8` | `evidence/03-double_negative.json` |
| Double zero | `python3 app.py --double 0` | Exit 0; stdout `0` | `evidence/04-double_zero.json` |
| Triple positive | `python3 app.py --triple 3` | Exit 0; stdout `9` | `evidence/05-triple_positive.json` |
| Triple negative | `python3 app.py --triple -4` | Exit 0; stdout `-12` | `evidence/06-triple_negative.json` |
| Triple zero | `python3 app.py --triple 0` | Exit 0; stdout `0` | `evidence/07-triple_zero.json` |
| Missing operation | `python3 app.py` | Exit 2; empty stdout; stderr says one operation is required | `evidence/08-required.json` |
| Both operations | `python3 app.py --double 3 --triple 3` | Exit 2; empty stdout; stderr reports conflict | `evidence/09-exclusive.json` |
| Double noninteger | `python3 app.py --double abc` | Exit 2; empty stdout; stderr reports invalid int | `evidence/10-double_type.json` |
| Triple noninteger | `python3 app.py --triple abc` | Exit 2; empty stdout; stderr reports invalid int | `evidence/11-triple_type.json` |
| Unknown argument | `python3 app.py --double 3 --unknown` | Exit 2; empty stdout; stderr reports unrecognized arguments | `evidence/12-unknown.json` |
| Existing checks | `python3 -m unittest -v` | Exit 0; one existing test passes | `evidence/13-existing_checks.json` |

All rows were driven live and passed. Numeric stdout includes a terminating newline. Each record includes the exact command, independent expected observation, raw stdout, raw stderr, exit code, and outcome; separate `.stdout` and `.stderr` files preserve streams. The existing unittest covers only positive double, so the live matrix is the evidence for the other mapped states. No UI, network, persistence, or external side effects are exposed by the inspected app.

## Cleanup and limits

Each process exited; no server or mutable fixture needs reset. Run checks with `PYTHONDONTWRITEBYTECODE=1` to avoid test import caches. Retain the evidence files after cleanup and check they exist. Source snapshots and file existence are checked in `evidence/14-retention.json`.

These observations cover every discovered feature with representative positive, negative, zero, and parser error states. They do not exhaust all integer magnitudes or argument spellings, prove future revisions, or cover another Python/runtime environment. Reinspect the source and refresh this map and live evidence when CLI flags, parser behavior, or numeric semantics change.
