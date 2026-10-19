# Runtime verification

Run every command below from this case directory. The primary interface is a
short-lived Python CLI. No build, server, account, migrations, packages, seeded
data, port, or network is needed. Python 3 is the only runtime prerequisite.

## Launch and doctor

`python3 app.py --help` must exit 0 and list `--double`, `--triple`, and `-h/--help`.
Each drive command launches a fresh process and its exit is its teardown. Doctor
passed before the first drive; repeat it after an unexpected failure. This checks
that the correct local interface is available, not the arithmetic by itself.

## Indexed feature map and drive recipes

| Feature | Entry point and state | Concrete command | Success observation |
| --- | --- | --- | --- |
| Double, positive | Fresh process, integer argument | `python3 app.py --double 3` | Exit 0; stdout `6` plus newline; empty stderr |
| Double, negative | Negative integer passed as the next argument | `python3 app.py --double -4` | Exit 0; stdout `-8` plus newline; empty stderr |
| Double, zero | Integer zero | `python3 app.py --double 0` | Exit 0; stdout `0` plus newline; empty stderr |
| Triple, positive | Fresh process, integer argument | `python3 app.py --triple 3` | Exit 0; stdout `9` plus newline; empty stderr |
| Triple, negative | Negative integer passed as the next argument | `python3 app.py --triple -4` | Exit 0; stdout `-12` plus newline; empty stderr |
| Triple, zero | Integer zero | `python3 app.py --triple 0` | Exit 0; stdout `0` plus newline; empty stderr |
| Help and short help | No arithmetic mode needed | `python3 app.py --help` and `python3 app.py -h` | Exit 0; usage and both arithmetic flags on stdout |
| Required mode | No argument supplied | `python3 app.py` | Exit 2; empty stdout; stderr says one of the arguments is required |
| Exclusive modes | Both arithmetic modes supplied | `python3 app.py --double 3 --triple 3` | Exit 2; empty stdout; stderr says not allowed with argument |
| Integer validation | Noninteger supplied | `python3 app.py --double nope` and `python3 app.py --triple nope` | Exit 2; empty stdout; stderr says invalid int value |
| Missing value | Mode without its integer | `python3 app.py --double` and `python3 app.py --triple` | Exit 2; empty stdout; stderr says expected one argument |
| Unknown flag | Unsupported option | `python3 app.py --unknown` | Exit 2; empty stdout; usage/error on stderr |

`argparse` also supports the `--double=3` and `--triple=3` spelling; verify those
entry points produce `6` and `9` with exit 0. Negative values and zero must remain
covered: a positive-only run misses important load-bearing states.

## Existing checks

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v` must exit 0. The current suite
contains only one positive-double subprocess test, so it does not cover triple,
negative/zero values, help, or validation. The live feature-map drives supply
those observations; do not claim the unit suite alone proves the whole CLI.

## Evidence and cleanup

`evidence/commands.json` indexes actual argv, stdout, stderr, exits, independently
specified expected values/errors, and pass/fail outcomes. Each command also has
its raw observation in `evidence/<name>.json`. `evidence/snapshot-before.json`
and `evidence/snapshot-after.json` identify source/document snapshots by SHA-256.
`evidence/coverage.json` records source/live reconciliation. `RESULT.json` is the
case report. Retain this evidence after cleanup and check its paths still exist.

No persistent CLI state or owned long-running processes exist. Drives set
`PYTHONDONTWRITEBYTECODE=1` to avoid scratch bytecode. Keep retained proof. No app
or unit-test changes are permitted in this maintenance task.

## Maintenance result and limits

The old index documented only double. Source inspection found triple, help, and
argument-validation states, so this document expands the map and recipes. This
is verified documentation drift, not an observed product regression. Re-drive
the recipes after this correction. This document covers the listed examples and
public states, not every integer or every possible parser spelling. The CLI has
no UI, authentication, network, or persisted effects to verify. Reconcile this
map after parser flags, mode selection, arithmetic, or error behavior changes.
