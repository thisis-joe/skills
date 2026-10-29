#!/usr/bin/env python3
"""Resolve durable TIL storage without creating or modifying any files."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


class ResolutionError(ValueError):
    pass


def git(folder, *args):
    try:
        return subprocess.run(['git', '-C', str(folder), *args],
                              capture_output=True, text=True, encoding='utf-8',
                              env={**os.environ, 'LC_ALL': 'C'})
    except OSError as exc:
        raise ResolutionError(f'Git unavailable: {exc}') from exc


def require_git(folder, *args):
    result = git(folder, *args)
    if result.returncode:
        raise ResolutionError(result.stderr.strip() or 'Git metadata unavailable')
    return result.stdout.removesuffix('\n')


def common_dir(folder):
    value = require_git(folder, 'rev-parse', '--git-common-dir')
    return (folder / value).resolve()


def resolve_workspace(start):
    start = Path(start).expanduser().resolve()
    if not start.is_dir():
        raise ResolutionError(f'Working directory missing: {start}')
    probe = git(start, 'rev-parse', '--is-inside-work-tree')
    if probe.returncode:
        # Other failures (permissions, corrupt metadata, unsafe ownership) must
        # never turn a repository into the outside-Git fallback.
        if 'not a git repository' not in probe.stderr.lower():
            raise ResolutionError(probe.stderr.strip() or 'Git metadata unavailable')
        if any((folder / '.git').exists() or (folder / '.git').is_symlink()
               for folder in (start, *start.parents)):
            raise ResolutionError('Repository marker exists but Git metadata is unavailable; refusing fallback')
        primary, repository = start, False
    else:
        if probe.stdout.strip() != 'true':
            raise ResolutionError('No non-bare primary checkout; refusing fallback')
        # -z preserves spaces/newlines and avoids Git pathname quoting. The
        # first record is Git's primary tree, never selected by branch name.
        listing = require_git(start, 'worktree', 'list', '--porcelain', '-z')
        first = listing.split('\0\0', 1)[0].split('\0')
        if not first or not first[0].startswith('worktree ') or 'bare' in first:
            raise ResolutionError('No non-bare primary checkout; refusing fallback')
        if Path(require_git(start, 'rev-parse', '--absolute-git-dir')).resolve() == common_dir(start):
            # --separate-git-dir can list the metadata folder as the first
            # worktree; a non-linked checkout identifies itself unambiguously.
            primary = Path(require_git(start, 'rev-parse', '--show-toplevel')).resolve()
        else:
            primary = Path(first[0][len('worktree '):]).resolve()
        if not primary.is_dir():
            raise ResolutionError(f'Primary checkout missing: {primary}')
        if require_git(primary, 'rev-parse', '--is-inside-work-tree') != 'true':
            raise ResolutionError('Primary checkout is not a working tree')
        top = Path(require_git(primary, 'rev-parse', '--show-toplevel')).resolve()
        if top != primary or common_dir(primary) != common_dir(start):
            raise ResolutionError('Primary checkout identity mismatch; refusing fallback')
        repository = True
    til = primary / 'TIL'
    if til.is_symlink() or (til.exists() and not til.is_dir()):
        raise ResolutionError(f'TIL must be a real directory: {til}')
    return {'primary': str(primary), 'til': str(til), 'repository': repository}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        print(json.dumps(resolve_workspace(args.path), ensure_ascii=False))
    except ResolutionError as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    main()
