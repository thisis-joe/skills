"""Collect review metadata without staging, committing, or changing files."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys


def collect(repo, base, paths=()):
    repo = Path(repo).resolve()

    def git(*args):
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
        if result.returncode:
            raise ValueError('git command failed: ' + os.fsdecode(result.stderr).strip())
        return result.stdout

    # Git diff uses root-relative names while ls-files uses the supplied cwd.
    # Anchor both layers and file hashing to the same actual repository root.
    repo = Path(os.fsdecode(git('rev-parse', '--show-toplevel')).strip()).resolve()

    scopes = []
    for path in paths:
        parsed = PurePosixPath(path)
        if not path or parsed.is_absolute() or '..' in parsed.parts:
            raise ValueError('path must be relative to the repository and cannot escape it')
        scopes.append(str(parsed).rstrip('/'))
    try:
        resolved = git('rev-parse', '--verify', '--end-of-options', base + '^{commit}').decode().strip()
    except ValueError as exc:
        raise ValueError('invalid base reference: ' + base) from exc
    head = git('rev-parse', 'HEAD').decode().strip()
    comparison = git('merge-base', resolved, head).decode().strip()
    files = {}

    def selected(path):
        return not scopes or any(s == '.' or path == s or path.startswith(s + '/') for s in scopes)

    def add(path, layer, status):
        if selected(path):
            row = files.setdefault(path, {'path': path, 'layers': [], 'statuses': {}})
            row['layers'].append(layer)
            row['statuses'][layer] = status

    diff_options = ['--no-ext-diff', '--no-textconv', '--no-renames']
    layers = [('committed', [comparison, head]), ('staged', ['--cached']), ('worktree', [])]
    for layer, args in layers:
        fields = git('diff', *diff_options, '--name-status', '-z', *args, '--').split(b'\0')
        for i in range(0, len(fields) - 1, 2):
            add(os.fsdecode(fields[i + 1]), layer, fields[i].decode('ascii'))
    for path in git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0'):
        if path:
            add(os.fsdecode(path), 'untracked', '?')

    ordered = [files[p] for p in sorted(files)]
    digest = hashlib.sha256()
    digest.update(json.dumps({'base': comparison, 'head': head, 'files': ordered}, sort_keys=True).encode())
    if ordered:
        literal_paths = [':(literal)' + row['path'] for row in ordered]
        for _, args in layers:
            digest.update(git('diff', *diff_options, '--binary', *args, '--', *literal_paths))
        for row in ordered:
            p = repo / row['path']
            # Inspect links themselves, never read their targets outside the repository.
            if p.is_symlink():
                body = os.fsencode(os.readlink(p))
            elif p.is_file():
                body = p.read_bytes()
            else:
                body = b''
            row['current_sha256'] = hashlib.sha256(body).hexdigest()
            digest.update(os.fsencode(row['path']) + b'\0' + body + b'\0')
    return {'schema': 1, 'repository': str(repo), 'requested_base': base,
            'base_commit': resolved, 'comparison_commit': comparison, 'head': head,
            'task_paths': scopes, 'has_changes': bool(ordered), 'files': ordered,
            'snapshot': digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--base', required=True, help='commit/ref; comparison uses its merge-base with HEAD')
    parser.add_argument('--path', action='append', default=[], help='literal task file or directory; repeatable')
    args = parser.parse_args()
    try:
        result = collect(args.repo, args.base, args.path)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
