# Runtime verification

Target: the local Python CLI in `app.py`; exact product-file SHA-256 values are in
`evidence/snapshot.json`. This recipe requires Python 3, the case directory as the
working directory, and no packages, credentials, fixtures, ports or external services.

## Launch and doctor

This CLI starts a fresh process for each action and exits immediately. There is no
build, migration, persistent data, or background server. Run:

```sh
python3 -m unittest -v
python3 app.py --help
```

The existing single unit test checks positive doubling only. The help command must
exit 0, list `--double` and `--triple`, and show them as mutually exclusive required
choices. Retain stdout, stderr, exit code and the source snapshot before driving.
If an unexpected result occurs, rerun help and compare the snapshot before retrying.
Baseline results are in `evidence/baseline-checks.json` and `evidence/doctor.json`.

## Feature index and drive recipes

Source inspection of all of `app.py`, `test_app.py` and `README.md` identifies these
user-facing features. Every row below is exercised as a fresh process. There are no
alternate UI, HTTP or library entrypoints in this application.

| Feature / state | Exact command | Expected observation | Evidence |
| --- | --- | --- | --- |
| Help | `python3 app.py --help` | Exit 0; both operation flags shown | `evidence/help.json` |
| Double positive | `python3 app.py --double 3` | Exit 0, stdout `6` | `evidence/double-positive.json` |
| Double negative | `python3 app.py --double -4` | Exit 0, stdout `-8` | `evidence/double-negative.json` |
| Double zero | `python3 app.py --double 0` | Exit 0, stdout `0` | `evidence/double-zero.json` |
| Triple positive | `python3 app.py --triple 3` | Exit 0, stdout `9` | `evidence/triple-positive.json` |
| Triple negative | `python3 app.py --triple -4` | Exit 0, stdout `-12` | `evidence/triple-negative.json` |
| Triple zero | `python3 app.py --triple 0` | Exit 0, stdout `0` | `evidence/triple-zero.json` |
| Required operation | `python3 app.py` | Exit 2, stderr says one operation is required | `evidence/missing-operation.json` |
| Exclusive operations | `python3 app.py --double 3 --triple 3` | Exit 2, stderr says argument not allowed | `evidence/conflicting-operations.json` |
| Integer input | `python3 app.py --triple nope` | Exit 2, stderr says invalid int value | `evidence/invalid-integer.json` |
| Required value | `python3 app.py --double` | Exit 2, stderr says expected one argument | `evidence/missing-value.json` |
| Unknown option | `python3 app.py --double 3 --unknown` | Exit 2, stderr says unrecognized arguments | `evidence/unknown-option.json` |

Negative numbers are values, not flags. Zero is significant: it must select the
requested operation. Errors must not emit a computed value on stdout. Each success
must match the literal expected value, not an expectation computed by product code.

## Evidence and cleanup

`evidence/*.json` retains exact argv, cwd, exit code, raw stdout/stderr, independent
expectations and verdicts. `RESULT.json` summarizes the complete source/live coverage
and any gaps. Preserve evidence after the run. Each process exits normally; no
long-lived process or user data requires cleanup. Exclude Python bytecode generation
when running via an owned harness or remove only owned cache residue.

The previous feature map omitted triple; this is documentation drift. Both operation
paths and shared help/error behavior are now mapped. These finite local examples do
not prove all integer inputs, every argparse spelling, or other Python/platform
versions. No product code changes are authorized by this recipe.
