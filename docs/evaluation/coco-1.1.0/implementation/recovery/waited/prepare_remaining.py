"""Restore the eleven never-started cases offline; --run is an explicit later action."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
ARCHIVE_SHA256 = '8d82a766cbf012b78677634f1bac721ad8da5321ca934bcfb6cd2d23e1873e5e'
FIRST_ID = '84bc1e8e980b'
RUNNER = Path('docs/evaluation/coco-1.1.0/implementation/recovery/waited/budget900_run.py')


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinks are not permitted in restored evidence')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = dict(sha256=digest(path), mode=stat.S_IMODE(path.stat().st_mode))
    return result


def extract_checked(archive, manifest_path, target):
    expected = read(manifest_path)
    if digest(archive) != ARCHIVE_SHA256 or expected['sha256'] != ARCHIVE_SHA256:
        raise ValueError('Sealed source archive hash differs')
    with tarfile.open(archive, 'r:gz') as tar:
        members = tar.getmembers()
        if len(members) != len(expected['members']) or len({m.name for m in members}) != len(members):
            raise ValueError('Missing, extra or duplicate archive members')
        for member in members:
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts or path.parts[0] != 'run':
                raise ValueError('Unsafe archive entry: '+member.name)
            wanted = expected['members'].get(member.name)
            data = tar.extractfile(member).read()
            if wanted != dict(sha256=hashlib.sha256(data).hexdigest(), mode=stat.S_IMODE(member.mode)):
                raise ValueError('Archive byte/mode mismatch: '+member.name)
            dest = target.joinpath(*path.parts[1:])
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            dest.chmod(member.mode)


def prepare(output, archive, manifest_path):
    output.mkdir(parents=True, exist_ok=False)
    original = output/'source-original'
    extract_checked(archive, manifest_path, original)
    control = read(original/'control.json')
    hold = read(original/'user-requested-admission-hold.json')
    first, *pending = control['trials']
    if first['id'] != FIRST_ID or len(pending) != 11 or len(control['hashes']) != 22:
        raise ValueError('Unexpected source cohort')
    if not read(original/'records'/FIRST_ID/'result.json')['stable']:
        raise ValueError('Completed first case is not stable in source evidence')
    if [t['id'] for t in pending] != [t['id'] for t in hold['held']]:
        raise ValueError('Pending order differs from original human hold')
    runtime, runner = output/'runtime', output/'frozen-runner'
    runtime.mkdir()
    for relative, expected in control['hashes'].items():
        source = original/'frozen'/relative
        if digest(source) != expected:
            raise ValueError('Frozen dependency differs: '+relative)
        dest = runner/relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    for name in ['owner', 'snapshots']:
        shutil.copytree(original/name, runtime/name)
    for trial, held in zip(pending, hold['held']):
        source = original/'user-held-projects'/trial['id']
        if files(source) != held['file_manifest']:
            raise ValueError('Held project changed: '+trial['id'])
        for path in (original/'records'/trial['id']).rglob('turn-*.json'):
            if re.fullmatch(r'turn-[0-9]+\.json', path.name):
                raise ValueError('Pending case already has a native invocation')
        project, record = runtime/'projects'/trial['id'], runtime/'records'/trial['id']
        shutil.copytree(source, project)
        if files(project) != held['file_manifest']:
            raise ValueError('Restoration changed project bytes/modes')
        record.mkdir(parents=True)
        trial.update(project=str(project), record=str(record))
    control['trials'] = pending
    control['deferred_continuation'] = dict(source_archive_sha256=ARCHIVE_SHA256, completed_trial_excluded=FIRST_ID,
        original_stop_preserved=str(original/'STOP'), explanation='New root for never-started cases; no stopped actor is resumed.')
    save(runtime/'control.json', control)
    for name in ['classifier-controls.json', 'reused-controls.json', 'last-native-start.json']:
        shutil.copy2(original/name, runtime/name)
    if not read(runtime/'classifier-controls.json')['passed']:
        raise ValueError('Inherited classifier controls did not pass')
    spent = read(original/'user-stop-outcome.json')['cooldown_estimate_sum_seconds']
    save(runtime/'inherited-budget'/'turn-0.cooldown.json', dict(credited_cooldown_estimate_seconds=spent,
        source_archive_sha256=ARCHIVE_SHA256, explanation='Completed first case allowance retained once; original evidence is outside this runtime.'))
    receipt = dict(prepared_at=datetime.now(timezone.utc).isoformat(), source_archive_sha256=ARCHIVE_SHA256,
        native_calls_during_prepare=0, model=control['model'], reasoning_effort=control['reasoning_effort'],
        expected_cli=control['cli'], completed_trial_excluded=FIRST_ID, pending_order=[t['id'] for t in pending],
        runner_manifest=files(runner), runtime_before_run_manifest=files(runtime),
        future_authorization='Preparation is offline. --run requires a later explicit request to perform the remaining experiments.')
    save(output/'prepared-root.json', receipt)
    return receipt


def run_explicit(output):
    receipt = read(output/'prepared-root.json')
    runtime, runner = output/'runtime', output/'frozen-runner'
    if files(runner) != receipt['runner_manifest'] or files(runtime) != receipt['runtime_before_run_manifest']:
        raise ValueError('Prepared state changed or native work already began; do not replay it')
    version = subprocess.run(['codex', '--version'], check=True, capture_output=True, text=True).stdout.strip()
    if version != receipt['expected_cli']:
        raise ValueError('CLI version changed; declare a revised comparison protocol before running')
    save(output/'explicit-run-receipt.json', dict(started_at=datetime.now(timezone.utc).isoformat(), cli=version,
        requested_model=receipt['model'], reasoning_effort=receipt['reasoning_effort'],
        limitation='Matching CLI/model aliases do not establish unchanged server-side model weights across dates.'))
    return subprocess.call([sys.executable, str(runner/RUNNER), 'run', '--root', str(runtime)], cwd=runner)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New preparation directory, or that prepared directory with --run')
    parser.add_argument('--archive', type=Path, default=HERE/'evidence/budget900-first-native.tar.gz')
    parser.add_argument('--manifest', type=Path, default=HERE/'evidence/budget900-first-native-manifest.json')
    parser.add_argument('--run', action='store_true', help='Explicit future model execution; never enabled by preparation')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.run:
        sys.exit(run_explicit(output))
    receipt = prepare(output, args.archive.resolve(), args.manifest.resolve())
    print(json.dumps(dict(prepared=str(output), pending_cases=len(receipt['pending_order']), native_calls=0,
        next_action='Await a later user request; then invoke this helper with the same --output and --run.')))
