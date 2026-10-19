# Operation selection and invalid input

Route: python3 app.py [operation arguments]
States: omitted operation, both operations (either order), malformed integer,
missing multiply operand, unknown option. No auth or fixture prerequisites.
Drive: python3 verify_cli.py drive.
Recipes: no arguments returns a required-operation error; --double 3 --multiply
2 4 and --multiply 2 4 --double 3 return an exclusivity error; --double text
and --multiply 2 text return an integer error; --multiply 2 returns a missing
operand error; --double 3 --unknown returns an unknown-option error.
Success: exit 2, empty stdout, stderr naming the corresponding input error.
Gotcha: an expected rejection is a passed check, not a helper failure. Only
these concrete invalid inputs are covered; arbitrary parser inputs are not.
Reset: each request starts a new subprocess and retains its complete output.
