# Argument validation

Public route: malformed calls to `python3 app.py`. Subfeatures are operation
selection, operand type/count, and unknown options. No fixture, authentication,
or setup is required. Every call has an independent fresh process.

| Live recipe | Required stderr fragment |
| --- | --- |
| `python3 app.py` | `one of the arguments --double --multiply is required` |
| `python3 app.py --double 3 --multiply 2 4` | `not allowed with argument --double` |
| `python3 app.py --double` | `expected one argument` |
| `python3 app.py --double abc` | `invalid int value` |
| `python3 app.py --multiply 3` | `expected 2 arguments` |
| `python3 app.py --multiply 3 abc` | `invalid int value` |
| `python3 app.py --multiply 2 3 4` | `unrecognized arguments: 4` |
| `python3 app.py --double 3 --unknown` | `unrecognized arguments: --unknown` |

All recipes require exit 2 and empty stdout. These are expected rejections, not
helper failures. `python3 verify_cli.py drive` retains them as feature
`argument-validation`. Diagnostics also include usage and executable names; match
the stable fragment rather than the entire platform-dependent message. Valid
negative and zero operands are covered in `double.md` and `multiply.md`.
