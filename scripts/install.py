"""Install COCO for Codex or Claude Code while preserving user-owned files."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from package_utils import (PackageError, install_manifest, payload, sha,
                           validate_package, validate_installed)

# Project-scoped skill folders each runtime reads from the folder it starts in up to the repository root.
PROJECT_SKILLS = {'claude': Path('.claude/skills'), 'codex': Path('.agents/skills')}
RUNTIME_NAMES = {'claude': 'Claude Code', 'codex': 'Codex'}


def default_destination(runtime):
    variable = 'CLAUDE_CONFIG_DIR' if runtime == 'claude' else 'CODEX_HOME'
    directory = '.claude' if runtime == 'claude' else '.codex'
    config_dir = os.environ.get(variable)
    return (Path(config_dir).expanduser() if config_dir else Path.home() / directory) / 'skills'


def project_destination(runtime, folder):
    project = Path(folder).expanduser().resolve()
    if not project.is_dir():
        raise PackageError('Project folder not found: ' + str(folder))
    if project == Path.home().resolve():
        raise PackageError('The home folder is not a project; use --global to install for every project')
    dest = project / PROJECT_SKILLS[runtime]
    if dest == default_destination(runtime).expanduser().resolve():
        raise PackageError('Project folder resolves to the global skills folder; use --global instead')
    return project, dest


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


def acquire_lock(dest):
    lock = dest / '.coco-install.lock'
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise PackageError('Another installation owns .coco-install.lock; inspect that process before retrying') from exc
    os.close(fd)
    return lock


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
    lock = acquire_lock(dest)
    try:
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


def uninstall(dest, dry_run=False):
    """Remove only the files this installer recorded, and only while they are unmodified."""
    if dest.is_symlink():
        raise PackageError('Refusing a symlinked destination')
    if not dest.exists() or install_manifest(dest) is None:
        return {'status': 'absent', 'action': 'uninstall', 'destination': str(dest)}
    old, folders = preflight(dest, {})
    result = {'action': 'uninstall', 'files': len(old['files']), 'destination': str(dest)}
    if dry_run:
        return {'status': 'dry-run', **result}
    lock = acquire_lock(dest)
    try:
        preflight(dest, {})
        with tempfile.TemporaryDirectory(prefix='.coco-remove-', dir=str(dest.parent)) as td:
            trash = Path(td)
            moved = []
            try:
                for folder in sorted(folders):
                    if (dest / folder).exists():
                        os.replace(str(dest / folder), str(trash / folder))
                        moved.append(folder)
                os.replace(str(dest / '.coco-install.json'), str(trash / 'manifest.json'))
            except BaseException:
                for folder in reversed(moved):
                    os.replace(str(trash / folder), str(dest / folder))
                raise
    finally:
        lock.unlink()
    return {'status': 'removed', **result}


def git_exclude_pattern(path):
    return '/' + re.sub(r'([\\*?\[])', r'\\\1', path)


def exclude_from_git(project, dest, folders, dry_run=False):
    """Hide installed COCO files from the project's Git status without touching tracked files."""
    def git(*args):
        try:
            result = subprocess.run(['git', '-C', str(project), *args],
                                    capture_output=True, text=True, encoding='utf-8')
        except OSError:
            return None
        return result.stdout.strip() if result.returncode == 0 else None

    top = git('rev-parse', '--show-toplevel')
    exclude = git('rev-parse', '--git-path', 'info/exclude')
    if not top or not exclude:
        return None
    exclude = Path(exclude) if Path(exclude).is_absolute() else project / exclude
    base = dest.relative_to(Path(top).resolve()).as_posix()
    wanted = [git_exclude_pattern(base + '/' + name + '/') for name in sorted(folders)]
    wanted.append(git_exclude_pattern(base + '/') + '.coco-install.*')
    text = exclude.read_text(encoding='utf-8') if exclude.is_file() else ''
    current = text.splitlines()
    missing = [line for line in wanted if line not in current]
    if missing and not dry_run:
        exclude.parent.mkdir(parents=True, exist_ok=True)
        prefix = '' if not text or text.endswith('\n') else '\n'
        exclude.write_text(text + prefix + '# coco-skills install\n' + '\n'.join(missing) + '\n',
                           encoding='utf-8')
    return {'file': str(exclude), 'added': len(missing)}


def ask(prompt):
    sys.stderr.write(prompt)
    sys.stderr.flush()
    line = sys.stdin.readline()
    if not line:
        raise PackageError('Cancelled: no answer was given')
    return line.strip()


def confirm(question):
    return ask(question + ' [Y/n] ').lower() in ('', 'y', 'yes')


def ask_projects(runtime, global_dest):
    """Ask where to install; return the chosen project folders, or [] for a global install."""
    sys.stderr.write(f'Where should COCO skills for {RUNTIME_NAMES[runtime]} be installed?\n'
                     f'  1) Project folders only: <project>/{PROJECT_SKILLS[runtime].as_posix()}\n'
                     f'  2) Every project (global): {global_dest}\n')
    choice = ask('Choose [1]: ')
    while choice not in ('', '1', '2'):
        choice = ask('Choose 1 or 2: ')
    if choice == '2':
        return []
    # Offer the current folder unless it is the home folder, which is never a project.
    cwd = Path.cwd()
    default = '' if cwd.resolve() == Path.home().resolve() else str(cwd)
    projects = []
    while True:
        if projects:
            folder = ask('Another project folder (blank to finish): ')
            if not folder:
                return projects
        else:
            folder = ask(f'Project folder [{default}]: ' if default else 'Project folder: ') or default
            if not folder:
                continue
        try:
            project_destination(runtime, folder)
        except PackageError as exc:
            sys.stderr.write(str(exc) + '\n')
            continue
        projects.append(folder)


def plan_global_removal(args, targets, global_dest, interactive):
    """Decide before any write whether a global install that would shadow project installs goes."""
    scoped = targets[0][0] is not None or args.dest is not None
    if args.remove_global and not scoped:
        raise PackageError('--remove-global needs --project or --dest')
    if not scoped or global_dest.is_symlink() or not global_dest.is_dir() or \
            install_manifest(global_dest) is None:
        return False
    if any(dest.resolve() == global_dest.resolve() for _, dest in targets):
        if args.remove_global:
            raise PackageError('--remove-global would remove the destination itself')
        return False
    remove = args.remove_global or interactive and confirm(
        f'A global COCO install remains at {global_dest}.\nIt shows coco skills in every project, '
        f'and {RUNTIME_NAMES[args.runtime]} may run it instead of the project copy.\n'
        'Remove it after the project install?')
    if not remove:
        sys.stderr.write(f'Warning: the global COCO install at {global_dest} still applies to '
                         'every project; remove it with --remove-global.\n')
        return False
    try:
        preflight(global_dest, {})
    except PackageError as exc:
        raise PackageError(f'Cannot remove the global install at {global_dest}: {exc}') from exc
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--runtime', choices=('codex', 'claude'), default='codex',
                        help='Runtime for the default destination (default: codex)')
    target = parser.add_mutually_exclusive_group()
    target.add_argument('--project', action='append', metavar='FOLDER',
                        help='Install only for this project, in FOLDER/.claude/skills (Claude Code) '
                             'or FOLDER/.agents/skills (Codex); repeat for more projects')
    target.add_argument('--global', dest='global_install', action='store_true',
                        help='Install for every project: $CODEX_HOME/skills (~/.codex/skills) or '
                             '$CLAUDE_CONFIG_DIR/skills (~/.claude/skills)')
    target.add_argument('--dest', type=Path,
                        help='Override destination, e.g. /project/.claude/skills; '
                             'otherwise the global folder of the runtime')
    parser.add_argument('--remove-global', action='store_true',
                        help='After --project or --dest installs succeed, remove the global install')
    parser.add_argument('--uninstall', action='store_true',
                        help='Remove the COCO install from the selected destination instead')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    interactive = sys.stdin.isatty()
    try:
        global_dest = default_destination(args.runtime)
        projects = args.project
        if (projects is None and args.dest is None and not args.global_install and
                not args.uninstall and interactive):
            projects = ask_projects(args.runtime, global_dest) or None
        targets = ([project_destination(args.runtime, p) for p in projects] if projects else
                   [(None, args.dest.expanduser())] if args.dest is not None else
                   [(None, global_dest)])
        if args.uninstall:
            if args.remove_global:
                raise PackageError('--remove-global applies to installs; use --uninstall --global')
            results = [uninstall(dest, args.dry_run) for _, dest in targets]
        else:
            remove_global = plan_global_removal(args, targets, global_dest, interactive)
            data = validate_package(args.root)
            folders = {data['shared'], *data['skills']}
            results = []
            for project, dest in targets:
                result = install(args.root, dest, args.dry_run)
                if project is not None:
                    result['project'] = str(project)
                    result['git_exclude'] = exclude_from_git(project, dest, folders, args.dry_run)
                results.append(result)
            if remove_global:
                results.append(uninstall(global_dest, args.dry_run))
        output = results[0] if len(results) == 1 else results
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except KeyboardInterrupt:
        parser.exit(130, 'Cancelled\n')
    except (PackageError, KeyError, TypeError, OSError, ValueError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
