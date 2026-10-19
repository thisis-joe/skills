# Multiply

Route: python3 app.py --multiply A B
States: positive operands, either negative operand, both negative, zero in either
position. No authentication, fixtures, installation or server needed.
Recipes: --multiply 3 4 returns 12; --multiply -3 4 and --multiply 3 -4
return -12; --multiply -3 -4 returns 12; --multiply 0 4 and --multiply 4 0
return 0.
Success: exit 0, exactly the integer plus newline on stdout, empty stderr.
Drive: python3 verify_cli.py drive. Each invocation is an independent process.
Gotcha: exactly two integers are required; --double cannot coexist with this
operation. Shared invalid states are mapped in operation-selection.md.
