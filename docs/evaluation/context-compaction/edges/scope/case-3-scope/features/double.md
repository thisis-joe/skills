# Double

Public route: `python3 app.py --double N`.
Subfeatures/states: positive, negative, and zero integers. No authentication,
fixture, or persistent state is required; every command is an independent reset.

| Live recipe | Exact stdout |
| --- | --- |
| `python3 app.py --double 3` | `6` followed by a newline |
| `python3 app.py --double -4` | `-8` followed by a newline |
| `python3 app.py --double 0` | `0` followed by a newline |

Success also requires exit 0 and empty stderr. Drive these recipes with
`python3 verify_cli.py drive`; retained checks have feature `double` and states
`positive`, `negative`, and `zero`. Negative values are valid option operands.
The operation is required and mutually exclusive with `--multiply`; malformed
calls are covered in `argument-validation.md`.
