"""Verify the current integer CLI through real, isolated subprocess calls."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def invoke(arguments):
    command = [sys.executable, str(ROOT / 'app.py'), *arguments]
    completed = subprocess.run(command,
                               cwd=ROOT, capture_output=True, text=True)
    return {'command': command, 'cwd': str(ROOT), 'arguments': arguments,
            'returncode': completed.returncode,
            'stdout': completed.stdout, 'stderr': completed.stderr}


def retain(name, result):
    directory = ROOT / 'evidence'
    directory.mkdir(exist_ok=True)
    result['app_sha256'] = hashlib.sha256((ROOT / 'app.py').read_bytes()).hexdigest()
    result['helper_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['python'] = sys.version
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    destination = directory / (name + '-' + stamp + '.json')
    result['evidence_path'] = str(destination.relative_to(ROOT))
    with destination.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('doctor', 'drive'):
        raise SystemExit('usage: python3 verify_cli.py doctor|drive')
    if sys.argv[1] == 'doctor':
        observed = invoke(['--help'])
        passed = (observed['returncode'] == 0 and observed['stderr'] == ''
                  and all(marker in observed['stdout']
                          for marker in ('usage:', '--double', '--multiply')))
        retain('doctor', {'passed': passed, 'observation': observed})
    else:
        checks = []
        valid = [
            ('double', ['--double', '3'], '6\n'),
            ('double', ['--double', '-4'], '-8\n'),
            ('double', ['--double', '0'], '0\n'),
            ('multiply', ['--multiply', '3', '4'], '12\n'),
            ('multiply', ['--multiply', '-3', '4'], '-12\n'),
            ('multiply', ['--multiply', '3', '-4'], '-12\n'),
            ('multiply', ['--multiply', '-3', '-4'], '12\n'),
            ('multiply', ['--multiply', '0', '4'], '0\n'),
            ('multiply', ['--multiply', '4', '0'], '0\n'),
        ]
        for feature, arguments, expected in valid:
            observed = invoke(arguments)
            observed['feature'] = feature
            observed['expected_stdout'] = expected
            observed['passed'] = (observed['returncode'] == 0
                                  and observed['stdout'] == expected
                                  and observed['stderr'] == '')
            checks.append(observed)
        invalid = [
            ([], 'one of the arguments --double --multiply is required'),
            (['--double', '3', '--multiply', '2', '4'], 'not allowed with argument'),
            (['--multiply', '2', '4', '--double', '3'], 'not allowed with argument'),
            (['--double', 'text'], 'invalid int value'),
            (['--multiply', '2', 'text'], 'invalid int value'),
            (['--multiply', '2'], 'expected 2 arguments'),
            (['--double', '3', '--unknown'], 'unrecognized arguments'),
        ]
        for arguments, error in invalid:
            observed = invoke(arguments)
            observed['feature'] = 'operation-selection'
            observed['expected_exit'] = 2
            observed['expected_stderr_fragment'] = error
            observed['passed'] = (observed['returncode'] == 2
                                  and observed['stdout'] == ''
                                  and error in observed['stderr'])
            checks.append(observed)
        passed = all(check['passed'] for check in checks)
        retain('drive', {'passed': passed, 'checks': checks})
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
