# Multiply

Public route: `python3 app.py --multiply A B`.
Subfeatures/states: positive operands, either negative operand, both negative
operands, and either zero operand. No authentication or fixture is required.
Each command starts a fresh process with no state to reset.

| Live recipe | Exact stdout |
| --- | --- |
| `python3 app.py --multiply 3 4` | `12` followed by a newline |
| `python3 app.py --multiply -3 4` | `-12` followed by a newline |
| `python3 app.py --multiply 3 -4` | `-12` followed by a newline |
| `python3 app.py --multiply -3 -4` | `12` followed by a newline |
| `python3 app.py --multiply 0 7` | `0` followed by a newline |
| `python3 app.py --multiply 7 0` | `0` followed by a newline |

Success also requires exit 0 and empty stderr. `python3 verify_cli.py drive`
retains these as feature `multiply`. Exactly two integer operands are required,
including when one begins with a minus sign. Malformed calls and the mutually
exclusive `--double` option are covered in `argument-validation.md`.
