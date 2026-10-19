"""Install COCO for Codex or Claude Code while preserving user-owned files."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
from package_utils import (PackageError, install_manifest, payload, sha,
                           validate_package, validate_installed)


def default_destination(runtime):
    if runtime == 'claude':
        config_dir = os.environ.get('CLAUDE_CONFIG_DIR')
        return (Path(config_dir).expanduser() if config_dir else Path.home() / '.claude') / 'skills'
    return Path.home() / '.codex/skills'


def preflight(dest, desired):
    if dest.is_symlink():
        raise PackageError('Refusing a symlinked destination')
    old = install_manifest(dest) if dest.exists() else None
    known = old['files'] if old else {}
    folders = {p.split('/')[0] for p in desired} | {p.split('/')[0] for p in known}
    for folder in folders:
        location = dest / folder
        if location.is_symlink():
            raise PackageError('Refusing a symlinked installed folder: ' + folder)
        if location.exists() and not any(p.startswith(folder + '/') for p in known):
            raise PackageError('Foreign skill directory already exists: ' + folder)
        if location.exists():
            for p in location.rglob('*'):
                if p.is_symlink():
                    raise PackageError('Installed symlink conflict: ' + str(p))
                if p.is_file():
                    rel = p.relative_to(dest).as_posix()
                    if rel not in known or sha(p) != known[rel]:
                        raise PackageError('Preserving user-modified or extra file: ' + rel)
    for rel, digest in known.items():
        p = dest / rel
        if not p.is_file() or sha(p) != digest:
            raise PackageError('Managed file changed or missing: ' + rel)
    return old, folders


def install(root, dest, dry_run=False):
    data = validate_package(root)
    files = payload(root, data)
    desired = {rel: sha(p) for rel, p in files.items()}
    old, folders = preflight(dest, desired)
    info = {'schema': 1, 'package': data, 'files': desired}
    if old == info:
        validate_installed(dest)
        return {'status': 'unchanged', 'skills': len(data['skills']), 'files': len(files), 'destination': str(dest)}
    if dry_run:
        return {'status': 'dry-run', 'skills': len(data['skills']), 'files': len(files), 'destination': str(dest)}
    dest.mkdir(parents=True, exist_ok=True)
    lock = dest / '.coco-install.lock'
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise PackageError('Another installation owns .coco-install.lock; inspect that process before retrying') from exc
    try:
        os.close(fd)
        preflight(dest, desired)
        with tempfile.TemporaryDirectory(prefix='.coco-stage-', dir=str(dest.parent)) as td:
            stage = Path(td)
            incoming = stage / 'incoming'
            backup = stage / 'backup'
            incoming.mkdir()
            backup.mkdir()
            for rel, source in files.items():
                target = incoming / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            moved, activated = [], []
            try:
                for folder in sorted(folders):
                    current = dest / folder
                    if current.exists():
                        os.replace(str(current), str(backup / folder))
                        moved.append(folder)
                    if (incoming / folder).exists():
                        os.replace(str(incoming / folder), str(current))
                        activated.append(folder)
                staged_manifest = stage / 'manifest.json'
                staged_manifest.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n')
                os.replace(str(staged_manifest), str(dest / '.coco-install.json'))
            except BaseException:
                for folder in reversed(activated):
                    os.replace(str(dest / folder), str(incoming / folder))
                for folder in reversed(moved):
                    os.replace(str(backup / folder), str(dest / folder))
                raise
    finally:
        lock.unlink()
    validate_installed(dest)
    return {'status': 'installed', 'skills': len(data['skills']), 'files': len(files), 'destination': str(dest)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--runtime', choices=('codex', 'claude'), default='codex',
                        help='Runtime for the default destination (default: codex)')
    parser.add_argument('--dest', type=Path,
                        help='Override destination, e.g. /project/.claude/skills; '
                             'otherwise ~/.codex/skills or $CLAUDE_CONFIG_DIR/skills '
                             '(~/.claude/skills when unset)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        dest = args.dest.expanduser() if args.dest is not None else default_destination(args.runtime)
        print(json.dumps(install(args.root, dest, args.dry_run), ensure_ascii=False, indent=2))
    except (PackageError, KeyError, TypeError, OSError, ValueError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
