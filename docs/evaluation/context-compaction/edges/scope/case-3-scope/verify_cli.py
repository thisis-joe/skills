"""Drive the public integer CLI and preserve each verification run."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

# Expected values come from the documented integer operations, not app internals.
CASES = {
    'help': [
        ('long-option', ['--help'], 0, None, ['usage:', '--double', '--multiply']),
        ('short-option', ['-h'], 0, None, ['usage:', '--double', '--multiply']),
    ],
    'double': [
        ('positive', ['--double', '3'], 0, '6\n', []),
        ('negative', ['--double', '-4'], 0, '-8\n', []),
        ('zero', ['--double', '0'], 0, '0\n', []),
    ],
    'multiply': [
        ('positive', ['--multiply', '3', '4'], 0, '12\n', []),
        ('negative-left', ['--multiply', '-3', '4'], 0, '-12\n', []),
        ('negative-right', ['--multiply', '3', '-4'], 0, '-12\n', []),
        ('both-negative', ['--multiply', '-3', '-4'], 0, '12\n', []),
        ('zero-left', ['--multiply', '0', '7'], 0, '0\n', []),
        ('zero-right', ['--multiply', '7', '0'], 0, '0\n', []),
    ],
    'argument-validation': [
        ('operation-required', [], 2, '', ['one of the arguments --double --multiply is required']),
        ('mutually-exclusive', ['--double', '3', '--multiply', '2', '4'], 2, '', ['not allowed with argument --double']),
        ('double-missing', ['--double'], 2, '', ['expected one argument']),
        ('double-noninteger', ['--double', 'abc'], 2, '', ['invalid int value']),
        ('multiply-missing', ['--multiply', '3'], 2, '', ['expected 2 arguments']),
        ('multiply-noninteger', ['--multiply', '3', 'abc'], 2, '', ['invalid int value']),
        ('multiply-extra', ['--multiply', '2', '3', '4'], 2, '', ['unrecognized arguments: 4']),
        ('unknown-option', ['--double', '3', '--unknown'], 2, '', ['unrecognized arguments: --unknown']),
    ],
}
PUBLIC_OPTIONS = {'--help', '--double', '--multiply'}


def invoke(arguments):
    command = [sys.executable, str(ROOT / 'app.py'), *arguments]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {'command': command, 'cwd': str(ROOT), 'arguments': arguments,
            'returncode': completed.returncode, 'stdout': completed.stdout,
            'stderr': completed.stderr}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retain(name, result):
    directory = ROOT / 'evidence'
    directory.mkdir(exist_ok=True)
    result['observed_at_utc'] = datetime.now(timezone.utc).isoformat()
    result['app_sha256'] = sha256(ROOT / 'app.py')
    result['helper_sha256'] = sha256(Path(__file__))
    result['feature_map_sha256'] = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in sorted((ROOT / 'features').iterdir()) if path.is_file()
    }
    # Exclusive creation preserves prior proof, including the original filenames.
    sequence = 0
    while True:
        filename = name + (f'-{sequence:03d}' if sequence else '') + '.json'
        path = directory / filename
        result['evidence_path'] = str(path.relative_to(ROOT))
        try:
            with path.open('x') as output:
                output.write(json.dumps(result, indent=2) + '\n')
            break
        except FileExistsError:
            sequence += 1
    print(json.dumps(result))


def doctor():
    observed = invoke(['--help'])
    options = set(re.findall(r'^\s+(?:-[a-z],\s+)?(--[a-z][a-z-]*)\b',
                             observed['stdout'], re.MULTILINE))
    index = json.loads((ROOT / 'features/index.json').read_text())
    mapped = index['features']
    feature_files = {path.stem for path in (ROOT / 'features').glob('*.md')}
    checks = {
        'help_usable': observed['returncode'] == 0 and 'usage:' in observed['stdout'] and observed['stderr'] == '',
        'public_options_mapped': options == PUBLIC_OPTIONS,
        'index_matches_driver': len(mapped) == len(set(mapped)) and set(mapped) == set(CASES),
        'index_matches_feature_files': set(mapped) == feature_files,
    }
    return {'passed': all(checks.values()), 'observation': observed,
            'observed_public_options': sorted(options),
            'expected_public_options': sorted(PUBLIC_OPTIONS),
            'mapped_features': mapped, 'feature_files': sorted(feature_files),
            'checks': checks}


def drive():
    preflight = doctor()
    checks = []
    if preflight['passed']:
        for feature in preflight['mapped_features']:
            for state, arguments, returncode, stdout, fragments in CASES[feature]:
                observed = invoke(arguments)
                observed.update({'feature': feature, 'state': state,
                                 'expected_returncode': returncode,
                                 'expected_stdout': stdout,
                                 'expected_fragments': fragments,
                                 'fragment_stream': 'stderr' if returncode else 'stdout'})
                stream = observed[observed['fragment_stream']]
                observed['passed'] = (
                    observed['returncode'] == returncode
                    and (stdout is None or observed['stdout'] == stdout)
                    and all(fragment in stream for fragment in fragments)
                    and (returncode != 0 or observed['stderr'] == '')
                )
                checks.append(observed)
    passed = preflight['passed'] and bool(checks) and all(check['passed'] for check in checks)
    return {'passed': passed, 'preflight': preflight, 'checks': checks,
            'mapped_features': preflight['mapped_features'],
            'blocked_reason': None if preflight['passed'] else 'Doctor failed; reconcile target and feature map before driving.'}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('doctor', 'drive'):
        raise SystemExit('usage: python3 verify_cli.py doctor|drive')
    name = sys.argv[1]
    result = doctor() if name == 'doctor' else drive()
    retain(name, result)
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
