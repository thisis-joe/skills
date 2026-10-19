# Double

Route: python3 app.py --double N
States: positive, negative, zero. No authentication or fixture needed.
Recipe: --double 3 returns 6; --double -4 returns -8; --double 0 returns 0.
Success: exit 0, exactly the integer plus newline on stdout, empty stderr.
Drive: python3 verify_cli.py drive. Each invocation is a fresh process.
Gotcha: --double requires one integer and cannot coexist with --multiply.
Invalid shared states are mapped in operation-selection.md.
