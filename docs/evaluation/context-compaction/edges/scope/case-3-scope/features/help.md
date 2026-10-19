# Help

Public routes: `python3 app.py --help` and `python3 app.py -h`.
Subfeatures/states: the long and short help aliases. No operation, fixture,
authentication, or server is required. Each call runs in a new process.

Both commands must exit 0, leave stderr empty, and print a usage message naming
`--double` and `--multiply`. `python3 verify_cli.py drive` records feature `help`
with states `long-option` and `short-option`. Doctor also checks that the options
listed by actual help match the supported driver options. Help is a usable route
even though arithmetic operations are otherwise required.
