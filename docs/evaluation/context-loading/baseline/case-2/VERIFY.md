# Runtime verification

This repository ships a short-lived Python CLI. The source feature map includes
help, double, triple, required mode selection, mutually exclusive modes, integer
validation, required values, and unknown option errors. The prior map omitted
triple and CLI error states; this was documentation drift. Product files remain
unchanged.

Run these commands from the directory containing this document:

```sh
python3 app.py --help
python3 -m unittest -v
python3 verify_cli.py
```

Launch is each command itself. No dependency installation, migration, server,
authentication, network, session, fixture, or persistent state is required.
Doctor is `python3 app.py --help`: exit 0 must expose both arithmetic modes. If a
check unexpectedly fails, rerun doctor and inspect `app.py` and the raw evidence.
The existing unit suite covers only `--double 3`; it does not establish the map.

| Feature | Public drive | Independent success observation | State or gotcha |
| --- | --- | --- | --- |
| Help | `python3 app.py --help` and `python3 app.py -h` | Exit 0, usage plus both modes on stdout | No mode needed; stderr empty |
| Double | `python3 app.py --double 3`; repeat with `-4`, `0` | Exit 0 and exact stdout `6`, `-8`, `0` | Fresh process per input; stderr empty |
| Triple | `python3 app.py --triple 3`; repeat with `-4`, `0` | Exit 0 and exact stdout `9`, `-12`, `0` | Fresh process per input; stderr empty |
| Required mode | `python3 app.py` | Exit 2; required-mode error on stderr, empty stdout | No arithmetic result |
| Exclusive modes | `python3 app.py --double 3 --triple 3` | Exit 2; conflict error on stderr, empty stdout | Two modes cannot be combined |
| Integer validation | `python3 app.py --double x`; repeat with `--triple x` | Exit 2; invalid-int error on stderr, empty stdout | Both modes checked |
| Required value | `python3 app.py --double`; repeat with `--triple` | Exit 2; expected-argument error on stderr, empty stdout | Both modes checked |
| Unknown option | `python3 app.py --double 3 --unknown` | Exit 2; unrecognized-argument error on stderr, empty stdout | A valid mode prevents masking this branch |

`verify_cli.py` drives every row through subprocesses and fixed expectations,
checks exit status and output, and returns nonzero on any mismatch. It records
Python version, hashes of the actual product and test files, and per-command
observations in `evidence/cli/report.json`. Raw stdout, stderr, and exit status
are adjacent files. `evidence/baseline-commands.json` retains the initial doctor,
launch, and unchanged existing suite before documentation maintenance.

Cleanup: the helper waits for all owned CLI child processes; no process remains
running and no application state needs resetting. Retain `evidence/` for review.
The helper checks that every retained per-command evidence file exists before
returning success. Rerun the commands above as a cold reader; no absolute path or
personal session is needed.

Observed maintenance result: all 15 mapped recipes passed on the file snapshot
in `evidence/cli/report.json`; the existing suite passed (one test). No product
regression or unreachable feature was found in this bounded inspection. This is
source and live coverage of the discoverable CLI surfaces and sampled integer
inputs, not an exhaustive proof over all integers, argument spellings, operating
systems, or future revisions. No external prerequisite was required.
