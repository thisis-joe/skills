"""Validation and file ownership for the dependency-free LET'S bundle."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote


class PackageError(ValueError):
    pass


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise PackageError('Cannot read JSON: ' + str(path)) from exc


def safe_relative(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise PackageError('Invalid relative path: ' + str(value))
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or str(p) != value:
        raise PackageError('Unsafe path: ' + value)
    return p


def config(root):
    data = read_json(root / 'lets.json')
    names = data.get('skills', [])
    if (data.get('schema') != 1 or data.get('shared') != '_lets-shared' or
            not isinstance(names, list) or not names or len(names) != len(set(names))):
        raise PackageError('Invalid package configuration')
    for name in names:
        if not isinstance(name, str) or not re.fullmatch(r'lets-[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise PackageError('Invalid skill name/path: ' + str(name))
    return data


def payload(root, data):
    result = {}
    for folder in [data['shared']] + data['skills']:
        origin = root / 'skills' / folder
        if not origin.is_dir() or origin.is_symlink():
            raise PackageError('Missing or symlinked package directory: ' + str(origin))
        for path in sorted(origin.rglob('*')):
            if path.is_symlink():
                raise PackageError('Package symlinks are not supported: ' + str(path))
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                result[path.relative_to(root / 'skills').as_posix()] = path
    return result


def scalar(value):
    if value.startswith('"'):
        try:
            return json.loads(value)
        except ValueError as exc:
            raise PackageError('Invalid quoted YAML scalar') from exc
    return value


def validate_payload(base, data):
    errors = []
    for name in data['skills']:
        path = base / name / 'SKILL.md'
        if not path.is_file():
            errors.append('Missing SKILL.md: ' + name)
            continue
        text = path.read_text()
        parts = text.split('---\n', 2)
        try:
            if not text.startswith('---\n') or len(parts) != 3:
                raise PackageError('Missing frontmatter')
            fields = {}
            for line in parts[1].splitlines():
                key, sep, value = line.partition(': ')
                if not sep or key in fields:
                    raise PackageError('Unsupported or duplicate frontmatter field')
                fields[key] = scalar(value)
            if fields.get('name') != name:
                raise PackageError('Frontmatter name differs from directory')
            desc = fields.get('description')
            if not isinstance(desc, str) or not desc.startswith('Use when') or len(desc) > 1024:
                raise PackageError('Missing or invalid discovery description')
            if len(parts[2].strip()) < 40:
                raise PackageError('Skill body is empty')
            ui = base / name / 'agents/openai.yaml'
            if not ui.is_file():
                raise PackageError('Missing UI metadata')
            values = {}
            for line in ui.read_text().splitlines():
                if line.startswith('  ') and ': ' in line:
                    key, value = line.strip().split(': ', 1)
                    values[key] = scalar(value)
            expected = data.get('display_prefix', "let's-") + name[len('lets-'):]
            if values.get('display_name') != expected:
                raise PackageError('UI display name does not match the selected prefix')
            if '$' + name not in values.get('default_prompt', ''):
                raise PackageError('Default prompt does not name its invocation')
            if not 25 <= len(values.get('short_description', '')) <= 64:
                raise PackageError('UI short description must be 25–64 characters')
        except PackageError as exc:
            errors.append(name + ': ' + str(exc))
    allowed = {data['shared']} | set(data['skills'])
    for folder in allowed:
        directory = base / folder
        for path in directory.rglob('*'):
            if path.is_symlink():
                errors.append('Symlink inside payload: ' + str(path))
                continue
            if not path.is_file() or path.suffix != '.md':
                continue
            for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', path.read_text()):
                target = unquote(target.strip('<>').split('#', 1)[0])
                if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    relative = resolved.relative_to(base.resolve())
                    safe = relative.parts and relative.parts[0] in allowed
                except ValueError:
                    safe = False
                if not safe or not resolved.exists():
                    errors.append(str(path.relative_to(base)) + ': broken/escaping reference ' + target)
    if errors:
        raise PackageError('\n'.join(errors))


def validate_sources(root, data):
    manifest_path = root / 'sources/manifest.json'
    if not manifest_path.exists():
        if data.get('provenance_required'):
            raise PackageError('Missing required source provenance')
        return
    manifest = read_json(manifest_path)
    originals = {}
    for item in manifest.get('files', []):
        local = safe_relative(item['local'])
        p = root / local
        if p.is_symlink() or not p.is_file() or sha(p) != item['sha256']:
            raise PackageError('Source checksum mismatch: ' + item['local'])
        key = (item['author'], item['path'])
        if key in originals:
            raise PackageError('Duplicate source manifest item')
        originals[key] = item
    expected = {key for key in originals if key[1].endswith('/SKILL.md') or
                (key[1].startswith('.claude/commands/') and key[1].endswith('.md'))}
    rows = read_json(root / 'sources/coverage.json').get('entries', [])
    actual = set()
    for row in rows:
        key = (row['author'], row['path'])
        if key in actual or key not in expected:
            raise PackageError('Duplicate or unknown coverage item: ' + str(key))
        actual.add(key)
        if ('lets-' + row['family'] not in data['skills'] or
                row.get('disposition') not in {'merged', 'adapted', 'reference'} or
                not row.get('essential_rules') or not row.get('adaptation') or
                not row.get('implemented_references')):
            raise PackageError('Incomplete source disposition: ' + str(key))
        for ref in row['implemented_references']:
            p = root / safe_relative(ref.split('#', 1)[0])
            if not p.is_file():
                raise PackageError('Missing integrated procedure for ' + str(key) + ': ' + ref)
    if actual != expected:
        raise PackageError('Coverage missing upstream entries: ' + repr(sorted(expected - actual)))


def validate_package(root):
    data = config(root)
    payload(root, data)
    validate_payload(root / 'skills', data)
    validate_sources(root, data)
    return data


def install_manifest(destination):
    path = destination / '.lets-install.json'
    if not path.exists():
        return None
    data = read_json(path)
    if data.get('schema') != 1 or not isinstance(data.get('files'), dict):
        raise PackageError('Invalid installation ownership manifest')
    for rel, digest in data['files'].items():
        p = safe_relative(rel)
        if (p.parts[0] != '_lets-shared' and not re.fullmatch(r'lets-[a-z0-9]+(?:-[a-z0-9]+)*', p.parts[0])):
            raise PackageError('Invalid managed installation path: ' + rel)
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise PackageError('Invalid managed hash')
    return data


def validate_installed(destination):
    if destination.is_symlink():
        raise PackageError('Symlinked installation root is not supported')
    info = install_manifest(destination)
    if info is None:
        raise PackageError('No installation manifest')
    for rel, digest in info['files'].items():
        p = destination / rel
        if p.is_symlink() or not p.is_file() or sha(p) != digest:
            raise PackageError('Installed file changed or missing: ' + rel)
    validate_payload(destination, info['package'])
    return info
